import customtkinter as ctk
from image_widgets import *
from PIL import Image, ImageTk, ImageEnhance
from Settings import *
from menu import Menu
import os

class pixelize(ctk.CTk):
    def __init__(self):

        # setup
        super().__init__()
        ctk.set_appearance_mode('system')
        self.geometry('900x600')
        self.minsize(900, 600)
        self.title('Pixel Art Converter - PAC')
        self.init_parameters()

        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform= 'a')
        self.columnconfigure(1, weight=6, uniform= 'a')

        self.image_width = 0
        self.image_height = 0
        self.canvas_width = 0
        self.canvas_height = 0

        #widgets
        self.image_import = ImageImport(self, self.import_image)

        # run
        self.mainloop()

    def init_parameters(self):
        ### might try to pack these in a dictionary now that there are too many of them...

        self.pixel_size = ctk.DoubleVar(value = PIXEL_SIZE_DEFAULT)
        self.color_palette = ctk.DoubleVar(value = COLOR_PALETTE_DEFAULT)
        self.brightness = ctk.DoubleVar(value = BRIGHTNESS_DEFAULT)
        self.sharpness = ctk.DoubleVar(value = SHARPNESS_DEFAULT)
        self.vibrance = ctk.DoubleVar(value = VIBRANCE_DEFAULT)


        self.pixel_size.trace('w', self.manipulate_image)
        self.color_palette.trace('w', self.manipulate_image)
        self.brightness.trace('w', self.manipulate_image)
        self.sharpness.trace('w', self.manipulate_image)
        self.vibrance.trace('w', self.manipulate_image)



    def manipulate_image (self, *args):
        self.image = self. original

        # resize the image to the desired pixel size
        self.image = self.resize_image_pixelsize(self.image, self.pixel_size.get())
        # Changes the amount of present colors in the image
        self.image = self.quantize_colors(self.image, self.color_palette.get())
        # manipulates the bright of each pixel individually
        self.image = self.adjust_brightness(self.image, self.brightness.get())
        # adjusts the level of sharpness of the edges
        #self.image = self.enhance_sharpness(self.image, self.sharpness.get())
        # changes the color vibrancy
        self.image = self.adjust_vibrance(self.image, self.vibrance.get())
        self.parameter_values = f'{round(self.pixel_size.get())}' \
                                f' - {round(self.color_palette.get())}' \
                                f' - {round(self.brightness.get())}' \
                                f' - {round(self.vibrance.get())}'

        self.place_image()

    def import_image(self, path):
        self.original = Image.open(path)
        self.image = self.original
        self.image_title = os.path.splitext(os.path.basename(path))[0]  # extract the image title without the extention
        print(self.image_title)
        self.image_ratio = self.image.size[0] / self.image.size[1]
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.image_import.grid_forget()
        self.image_output = ImageOutput(self, self.resize_image)
        self.close_button = CloseOutput(self, self.close_app)

        self.menu = Menu(self, self.pixel_size,
                         self.color_palette,
                         self.brightness,
                         self.sharpness,
                         self.vibrance,
                         self.export_image)

    def close_app(self):
        # removes the image from the frame
        self.image_output.grid_forget()
        self.image_import.place_forget()
        self.menu.grid_forget()
        # recreates the import button
        self.image_import = ImageImport(self, self.import_image)

    def resize_image(self, event):
        # current canvas ratio
        canvas_ratio = event.width / event.height
        # update canvas attributes
        self.canvas_width = event.width
        self.canvas_height = event.height

        # resize
        if canvas_ratio > self.image_ratio:  # canvas is wider than the image
            self.image_height = int(event.height)
            self.image_width = int(self.image_height / self.image_ratio)
        else:  # canvas is taller than the image
            self.image_width = int(event.width)
            self.image_height = int(self.image_width / self.image_ratio)
        self.place_image()

    def place_image(self):
        # place
        self.image_output.delete('all')
        resized_image = self.image.resize((self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.image_output.create_image(self.canvas_width / 2, self.canvas_height / 2, image=self.image_tk)

    def export_image(self, name, file, path):
        export_string = f'{path}/{name} - {self.parameter_values}.{file}'
        print(export_string)
        self.image = self.image.resize((self.original.width, self.original.height))
        self.image.save(export_string)

    def resize_image_pixelsize(self, image, pixel_size):
        # Resize the image to the desired pixel size
        self.image = self.image.convert("RGB")
        self.new_width = self.image.size[1] // round(pixel_size)
        self.new_height = self.image.size[0] // round(pixel_size)
        self.resized_img_pixelsize = image.resize((self.new_width, self.new_height), Image.NEAREST)
        return self.resized_img_pixelsize

    def quantize_colors(self, image, color_palette):
        # Reduce the color palette
        self.image = self.image.convert("RGB")
        self.quantized_image = self.image.quantize(colors=round(color_palette))
        return self.quantized_image

    def adjust_brightness(self, image, brightness_factor):
        # Adjust the brightness of the image
        self.image = self.image.convert("RGB")
        brightness_float = brightness_factor / 100
        enhancer = ImageEnhance.Brightness(self.image)
        self.adjusted_image = enhancer.enhance(brightness_float)
        return self.adjusted_image

    def enhance_sharpness(self, image, sharpness_factor): # seems to interfere with the adjust_vibrance
        # Enhance the sharpness of the image                commented out for the time being
        self.image = self.image.convert("RGB")
        sharpness_float = sharpness_factor / 100
        enhancer = ImageEnhance.Sharpness(self.image)
        self.enhanced_image = enhancer.enhance(sharpness_factor)
        return self.enhanced_image

    def adjust_vibrance(self, image, vibrance_factor):
        # Adjust the vibrance of the image
        self.image = self.image.convert("RGB")
        vibrance_float = vibrance_factor / 100
        enhancer = ImageEnhance.Color(self.image)
        self.vibrant_image = enhancer.enhance(vibrance_float)
        return self.vibrant_image


   # the function below tends to give better output images compared to the current methods
   # above, but it's also much slower, might try to base the calculations on NumPy for a
   # faster execution in the future ...


   # def convert_to_pixel_art(self, image, pixel_size, color_palette):
   #     # Resize the image to the desired pixel size
   #     convert_resized_image = self.resize_image_pixelsize(image, pixel_size)
   #
   #     # Reduce the color palette
   #     quantized_image = self.quantize_colors(convert_resized_image, color_palette)
   #
   #     # Adjust pixel values
   #     pixel_art_image = quantized_image.convert("RGB")
   #
   #     # Create the final pixel art image
   #     width, height = convert_resized_image.size
   #     self.final_image = Image.new("RGB", (width * pixel_size, height * pixel_size))
   #
   #     for y in range(height):
   #         for x in range(width):
   #             pixel_color = pixel_art_image.getpixel((x, y))
   #             for j in range(pixel_size):
   #                 for i in range(pixel_size):
   #                     self.final_image.putpixel((x * pixel_size + i, y * pixel_size + j), pixel_color)
   #
   #     return self.final_image


pixelize()
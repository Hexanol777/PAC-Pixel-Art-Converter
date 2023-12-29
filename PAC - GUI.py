import sys
sys.path.append("utils")
import customtkinter as ctk
from utils.image_widgets import *
from PIL import Image, ImageTk, ImageEnhance
from utils.Settings import *
from utils.menu import Menu
import os



class pixelize(ctk.CTk):
    def __init__(self):

        # setup
        super().__init__()
        ctk.set_appearance_mode('system')
        self.geometry('1100x750')
        self.minsize(900, 600)

        try:
            self.iconbitmap('lantern.ico')
        except Exception as e:
            print(e + "\nicon could not be loaded, using default icon...")

        self.title('PAC - Pixel Art Converter')
        self.init_parameters()

        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform= 'a')
        self.columnconfigure(1, weight=6, uniform= 'a')

        self.image_width = 0
        self.image_height = 0
        self.canvas_width = 0
        self.canvas_height = 0

        # widgets
        self.image_import = ImageImport(self, self.import_image)

        # run
        self.mainloop()

    def init_parameters(self):
        ### might try to pack these in a dictionary now that there are too many of them...

        self.pixel_size = ctk.DoubleVar(value = PIXEL_SIZE_DEFAULT)
        self.color_palette = ctk.DoubleVar(value = COLOR_PALETTE_DEFAULT)
        self.brightness = ctk.DoubleVar(value = BRIGHTNESS_DEFAULT)
        self.vibrance = ctk.DoubleVar(value = VIBRANCE_DEFAULT)
        self.sharpness = ctk.DoubleVar(value = SHARPNESS_DEFAULT)


        self.pixel_size.trace('w', self.manipulate_image)
        self.color_palette.trace('w', self.manipulate_image)
        self.brightness.trace('w', self.manipulate_image)
        self.sharpness.trace('w', self.manipulate_image)
        self.vibrance.trace('w', self.manipulate_image)



    def manipulate_image(self, *args):
        self.image = self.original

        # resize the image to the desired pixel size
        self.image = self.resize_image_pixelsize(self.image, self.pixel_size.get())
        # Changes the amount of present colors in the image
        self.image = self.quantize_colors(self.image, self.color_palette.get())
        # manipulates the bright of each pixel individually
        self.image = self.adjust_brightness(self.image, self.brightness.get())
        # changes the color vibrancy
        self.image = self.adjust_vibrance(self.image, self.vibrance.get())
        # adjusts the level of sharpness of the edges
        self.image = self.enhance_sharpness(self.image, self.sharpness.get())

        self.parameter_values = f'{round(self.pixel_size.get())}' \
                                f' - {round(self.color_palette.get())}' \
                                f' - {round(self.brightness.get())}' \
                                f' - {round(self.vibrance.get())}' 

        self.place_image()


    def import_image(self, path):
        self.original = Image.open(path)
        self.image = self.original
        self.image_title = os.path.splitext(os.path.basename(path))[0]  # extract the image title without the extention
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
                         self.export_image
                         )

    def close_app(self):
        # removes the image from the frame
        self.image_output.grid_forget()
        self.image_import.place_forget()
        self.menu.grid_forget()
        # recreates the import button
        self.image_import = ImageImport(self, self.import_image)

    def resize_image(self, event):
        # Update canvas attributes
        self.canvas_width = event.width
        self.canvas_height = event.height

        # Calculate new dimensions while maintaining aspect ratio
        canvas_ratio = self.canvas_width / self.canvas_height
        if canvas_ratio > self.image_ratio:  # Canvas is wider than the image
            self.image_height = int(round(self.canvas_height))
            self.image_width = int(round(self.image_height * self.image_ratio))
        else:  # Canvas is taller than the image
            self.image_width = int(round(self.canvas_width))
            self.image_height = int(round(self.image_width / self.image_ratio))
        self.place_image()

    def place_image(self):
        # Delete existing items in the canvas
        self.image_output.delete('all')

        # Calculate new dimensions while maintaining aspect ratio
        canvas_ratio = self.canvas_width / self.canvas_height
        if canvas_ratio > self.image_ratio:  # Canvas is wider than the image
            self.image_height = int(round(self.canvas_height))
            self.image_width = int(round(self.image_height * self.image_ratio))
        else:  # Canvas is taller than the image
            self.image_width = int(round(self.canvas_width))
            self.image_height = int(round(self.image_width / self.image_ratio))

        # Calculate position to center the image
        x = (self.canvas_width - self.image_width) / 2
        y = (self.canvas_height - self.image_height) / 2

        # Resize and place the image
        resized_image = self.image.resize((self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.image_output.create_image(x + self.image_width / 2, 
                                       y + self.image_height / 2, 
                                       image=self.image_tk)

    def export_image(self, name, file, path):
        export_string = f'{path}/{name} - {self.parameter_values}.{file}'

        self.image = self.image.resize((self.original.width, 
                                        self.original.height))
        self.image.save(export_string)

    def resize_image_pixelsize(self, image, pixel_size):
        # Resize the image to the desired pixel size
        self.image = self.image.convert("RGB")
        
        self.new_width = self.image.size[1] // round(pixel_size)
        self.new_height = self.image.size[0] // round(pixel_size)

        self.resized_img_pixelsize = image.resize((self.new_width, 
                                                   self.new_height), Image.NEAREST)
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

    def enhance_sharpness(self, image, sharpness_factor): 
        # Enhance the sharpness of the image
        self.image = self.image.convert("RGB")
        sharpness_factor = sharpness_factor / 10
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

pixelize()
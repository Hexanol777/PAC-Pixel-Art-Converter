import customtkinter as ctk
from Settings import *
from tkinter import filedialog
from auto_value import *
from video_funcs import process_video



class Panel(ctk.CTkFrame):
    def __init__(self, parent): # main panel
        super().__init__(master = parent, fg_color = DARK_GREY, border_width = 0.75, border_color = BORDER, corner_radius=10)
        self.pack(fill = 'x', pady = 4, ipady = 8)

class ImagePanel(ctk.CTkFrame): # where the image lies 
    def __init__(self, parent):
        super().__init__(master = parent, fg_color = DARK_GREY)
        self.pack(fill = 'x', pady = 4, ipady = 8)

class SliderPanel(Panel): # logic for the panel used in Sliders
    def __init__(self, parent, text, data_var, min_value, max_value):
        super().__init__(parent = parent)
        self.data_var = data_var
        # layout
        self.rowconfigure((0,1), weight = 1)
        self.columnconfigure((0,1), weight = 1)

        ctk.CTkLabel(self, text = text).grid(column = 0, row = 0
                                             , sticky = 'W'
                                             , padx = 10)
        
        self.num_label = ctk.CTkLabel(self, text = data_var.get())
        self.num_label.grid(column = 1, row = 0
                            , sticky = 'E'
                            , padx = 10)

        ctk.CTkSlider(self,
                      fg_color = SLIDER_BG,
                      variable=data_var,
                      from_ = min_value,
                      to = max_value,
                      command = self.update_text).grid(row = 1, column = 0
                                                       , columnspan = 2
                                                       , sticky = 'ew'
                                                       , padx = 5
                                                       , pady = 5)

    def update_text(self, value):
        self.num_label.configure(text = f'{round(value, 0)}')

    def update_text_and_value(self, value):
        self.update_text(value)
        self.data_var.set(value)

class FileNamePanel(Panel):
    def __init__(self, parent, name_string, file_string):
        super().__init__(parent = parent)

        # data
        self.name_string = name_string
        self.name_string.trace('w', self.update_name_text)

        self.file_string = file_string

        # extra arguments
        ctk.CTkEntry(self, textvariable= self.name_string).pack(fill = 'x', padx = 20, pady = 5)
        checkbox_frame = ctk.CTkFrame(self, fg_color= 'transparent')

        jpg_check = ctk.CTkCheckBox(checkbox_frame, text = 'jpg', variable = self.file_string,
                                    command = lambda: self.click('jpg'),
                                    onvalue = 'jpg', offvalue = 'png')
        png_check = ctk.CTkCheckBox(checkbox_frame, text = 'png', variable = self.file_string,
                                    command = lambda: self.click('png'),
                                    onvalue = 'png', offvalue = 'jpg')
        jpg_check.pack(side = 'left', fill = 'x', expand = True)
        png_check.pack(side='right', fill='x', expand=True)

        checkbox_frame.pack(expand = True, fill = 'x', padx = 20)

        # preview text
        self.output = ctk.CTkLabel(self, text = '')
        self.output.pack()

    def click(self, value):
        self.file_string.set(value)
        self.update_name_text()

    def update_name_text(self, *args):
        if self.name_string.get():
            text = self.name_string.get() +'.' + self.file_string.get()
            self.output.configure(text = text)

class FilePathPanel(Panel):
    def __init__(self, parent, path_string):
        super().__init__(parent = parent)
        self.path_string = path_string

        ctk.CTkButton(self, text= 'Open Explorer', command = self.open_file_dialog).pack(pady = 5)
        ctk.CTkEntry(self, textvariable= self.path_string).pack(expand = True, fill = 'both', padx = 5, pady = 5)

    def open_file_dialog(self):
        self.path_string.set(filedialog.askdirectory())

class SaveButton(ctk.CTkButton):
    def __init__(self, parent, export_image, name_string, file_string, path_string):
        super().__init__(master = parent, text= 'Save', command=self.save)
        self.pack(side = 'bottom', pady = 10)
        self.export_image = export_image
        self.name_string = name_string
        self.file_string = file_string
        self.path_string = path_string


    def save(self):
        self.export_image(
            self.name_string.get(),
            self.file_string.get(),
            self.path_string.get()
            )

        
class SuggestedValues(ctk.CTkFrame):
    def __init__(self, parent, text, suggested_value):
        super().__init__(master=parent, fg_color=DARK_GREY)
        self.suggested_value = suggested_value

        ctk.CTkLabel(self, text=text).grid(column=0, row=0, sticky='W', padx=10)

        self.num_label = ctk.CTkLabel(self, text=self.suggested_value)
        self.num_label.grid(column=1, row=0, sticky='E', padx=10)
        # Add weight to the second column to push the label to the right
        self.grid_columnconfigure(1, weight=1)
        self.pack(expand=True, fill='both')

class AnalysisPanel(Panel):
    def __init__(self, parent, image, pixel_size, color_palette, brightness, sharpness, vibrance):
        super().__init__(parent=parent)
        self.pack(fill='x', side='bottom', pady=5, ipady=8)
        self.image = image

        ctk.CTkLabel(self, text="Suggested Values").pack(padx=5)

        self.analyze_image()

        SuggestedValues(self, 'Pixel Size', self.closest_pixel_size)
        SuggestedValues(self, 'Color Pallete', self.closest_palette)
        SuggestedValues(self, 'Brightness', self.closest_brightness)
        SuggestedValues(self, 'Edge Sharpness', self.closest_sharpness)
        SuggestedValues(self, 'Color Vibrance', self.closest_vibrance)

    def analyze_image(self):
        self.closest_pixel_size, self.closest_sharpness = find_closest_pixelsize(self.image.width, self.image.height)
        self.closest_brightness, self.closest_vibrance, self.closest_palette = find_closest_color_palette(self.image)
        
class SetSuggested(ctk.CTkButton):

    def __init__(self, parent, image, pixel_size, color_palette, brightness, sharpness, vibrance):
        super().__init__(master = parent, text= 'Set Values', command=self.set_values, border_width=0.75, border_color=BORDER)

        self.image = image
        self.pixel_slider = pixel_size
        self.color_pallete_slider = color_palette
        self.brightness_slider = brightness
        self.sharpness_slider = sharpness
        self.vibrance_slider = vibrance

        self.pack(side = 'bottom', pady = 5)

    def set_values(self):
        self.pixel_value, self.sharpness_value = find_closest_pixelsize(self.image.width, self.image.height)
        self.brightness_value, self.vibrance_value, self.color_pallete_value = find_closest_color_palette(self.image)
        
        self.pixel_slider.update_text_and_value(self.pixel_value)
        self.color_pallete_slider.update_text_and_value(self.color_pallete_value)
        self.brightness_slider.update_text_and_value(self.brightness_value)
        self.sharpness_slider.update_text_and_value(self.sharpness_value)
        self.vibrance_slider.update_text_and_value(self.vibrance_value)

class VideoValueEntry(Panel): # Value Entries for video

    def __init__(self, parent, text, data_var, min_value, max_value):
        super().__init__(parent = parent)
        self.data_var = data_var
        # layout
        self.rowconfigure((0,1), weight = 1)
        self.columnconfigure((0,1), weight = 1)
        ctk.CTkLabel(self, text = text).grid(column = 0, row = 0
                                             , sticky = 'W'
                                             , padx = 10)

        self.num_label = ctk.CTkLabel(self, text = data_var.get())
        self.num_label.grid(column = 1, row = 0
                            , sticky = 'E'
                            , padx = 10)
        ctk.CTkSlider(self,
                      fg_color = SLIDER_BG,
                      variable=data_var,
                      from_ = min_value,
                      to = max_value,
                      command = self.update_text).grid(row = 1, column = 0
                                                       , columnspan = 2
                                                       , sticky = 'ew'
                                                       , padx = 5
                                                       , pady = 5)

    def update_text(self, value):
        self.num_label.configure(text = f'{round(value, 0)}')
        
class ApplyValuesButton(ctk.CTkButton):
        def __init__(self, parent, video, pixel_size, color_palette, brightness, sharpness, vibrance):
            super().__init__(master = parent, text= 'Create Video', command=self.apply_values, border_width=0.75, border_color=BORDER)

            self.video = video
            self.pixel_value = pixel_size
            self.color_pallete_value = color_palette
            self.brightness_value = brightness
            self.sharpness_value = sharpness
            self.vibrance_value = vibrance

            self.pack(side = 'bottom', pady = 5)

        def apply_values(self):
            self.video = process_video(self.video, self.pixel_value.get(), 
                                       self.color_pallete_value.get(), self.brightness_value.get(), 
                                       self.sharpness_value.get(), self.vibrance_value.get())

        def update_values(self, *args):
                    print("Updated values:", self.pixel_value, self.color_pallete_value, self.brightness_value, self.sharpness_value)


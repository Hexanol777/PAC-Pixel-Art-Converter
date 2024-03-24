import customtkinter as ctk
from Panels import *
import PIL

class Menu(ctk.CTkTabview): # main menu
    def __init__(self, parent, pixel_size, color_palette, brightness, sharpness, vibrance, export_image, image):
        super().__init__(master = parent)
        self.grid(row = 0, column = 0, sticky = 'nsew', pady = 10 , padx = 10)

        # tabs, new tabs get added here
        self.add('Parameters')
        self.add('Save Options')

        # widget
        Parameters(self.tab('Parameters'), pixel_size, color_palette, brightness, sharpness, vibrance, image)
        SaveOptions(self.tab('Save Options'), export_image)



class Parameters(ctk.CTkFrame): # parameters tab
    def __init__(self, parent, pixel_size, color_palette, brightness, sharpness, vibrance, image):
        super().__init__(master = parent, fg_color= 'transparent')
        self.pack(expand = True, fill = 'both')
        if isinstance(image, (PIL.JpegImagePlugin.JpegImageFile, PIL.PngImagePlugin.PngImageFile)): # checks for img or vid
            pixel_panel = SliderPanel(self, 'Pixel Size', pixel_size, 1, 20)
            palette = SliderPanel(self, 'Color Palette', color_palette, 5, 100)
            brightness_panel = SliderPanel(self, 'Brightness', brightness, 0, 200)
            sharpness_panel = SliderPanel(self, 'Edge Sharpness', sharpness, 0, 20)
            vibrance_panel = SliderPanel(self, 'Color Vibrance', vibrance, 0, 300)
            SetSuggested(self, image, pixel_panel, palette, brightness_panel, sharpness_panel, vibrance_panel)    
            AnalysisPanel(self, image, pixel_size, color_palette, brightness, sharpness, vibrance)

        else:
            VideoValueEntry(self, 'Pixel Size', pixel_size)
            VideoValueEntry(self, 'Color Palette', color_palette)
            VideoValueEntry(self, 'Brightness', brightness)
            VideoValueEntry(self, 'Edge Sharpness', sharpness)
            VideoValueEntry(self, 'Color Vibrance', vibrance)
            ApplyValuesButton(self, image, pixel_size, color_palette, brightness, sharpness, vibrance)

class SaveOptions(ctk.CTkFrame): # save options tab
    def __init__(self, parent, export_image):
        super().__init__(master = parent, fg_color= 'transparent')
        self.pack(expand = True, fill = 'both')

        # data
        self.name_string = ctk.StringVar()
        self.file_string = ctk.StringVar(value= 'jpg')
        self.path_string = ctk.StringVar()

        # widget
        FileNamePanel(self, self.name_string, self.file_string)
        FilePathPanel(self, self.path_string)
        SaveButton(self, export_image, self.name_string, self.file_string, self.path_string)

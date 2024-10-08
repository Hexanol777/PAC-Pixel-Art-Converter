import customtkinter as ctk
from Settings import *
from tkinter import filedialog
from auto_value import *
from video_funcs import process_video
import threading

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

class ImageFileNamePanel(Panel):
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

class FileNamePanel(Panel): # file name panel for videos
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
        self.output.pack(pady=1)

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
        ctk.CTkEntry(self, textvariable= self.path_string, text_color='white').pack(expand = True, fill = 'both', padx = 5, pady = 5)

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
        
        ctk.CTkLabel(self, text=text).pack(side='left', padx=5)
        
        self.num_label = ctk.CTkLabel(self, text=suggested_value)
        self.num_label.pack(side='right', padx=5)
        # Add weight to the second column to push the label to the right
        self.pack(expand=True, padx=5, fill='x')  

class AnalysisPanel(Panel):
    def __init__(self, parent, image):
        super().__init__(parent=parent)
        self.pack(side='bottom', pady=10, padx=5, fill='x')
        self.image = image

        ctk.CTkLabel(self, text="Suggested Values").pack(pady=2)

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

class ProgressBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, border_color=BORDER, border_width=1, corner_radius=10)

        self.loading_progress = ctk.CTkProgressBar(master=self, width=200)
        self.loading_progress.configure(mode="indeterminate")
        self.loading_progress.pack(padx=10, pady=10)

        self.pack(side='bottom', pady=10, padx=5, fill='x')

    def start(self):
        # Show and start the progress bar
        self.loading_progress.start()

    def stop(self):
        # Stop and hide the progress bar
        self.loading_progress.stop()


class ApplyValuesButton(ctk.CTkButton):
    def __init__(self, parent, video, pixel_size, color_palette, brightness, sharpness, vibrance, load_video, progress_bar):
        super().__init__(master=parent, text='Create Video', command=self.apply_values, border_width=0.75, border_color=BORDER)

        self.video = video
        self.pixel_value = pixel_size
        self.color_palette_value = color_palette
        self.brightness_value = brightness
        self.sharpness_value = sharpness
        self.vibrance_value = vibrance
        self.load_video = load_video
        self.progress_bar = progress_bar

        self.pack(side='bottom', pady=5)

    def apply_values(self):
        # Start the progress bar
        self.progress_bar.start()

        # Create a separate thread to process the video
        thread = threading.Thread(target=self.process_video_in_thread)
        thread.start()

    def process_video_in_thread(self):
        # Run the video processing
        self.video = process_video(
            self.video,
            self.pixel_value.get(),
            self.color_palette_value.get(),
            self.brightness_value.get(),
            self.sharpness_value.get(),
            self.vibrance_value.get()
        )

        # Stop the progress bar after processing is complete
        self.progress_bar.stop()

        # Load the processed video
        self.load_video(self.video)

class Notifications(ctk.CTkFrame):
    def __init__(self, parent, message):
        super().__init__(parent, bg_color='transparent', fg_color=DARK_GREY, width=125, height=85, border_color=BORDER, border_width=1, corner_radius=10)
        self.pack_propagate(0)

        right_offset = 15
        
        self.cur_x = self.winfo_width()
        self.x = self.cur_x - (0 + right_offset)

        self.message_label = ctk.CTkLabel(self, text=message)
        self.message_label.pack(expand=True, fill="both", padx=10, pady=5)

        # Call break_message_into_parts method to split the message
        message_parts = self.break_message_into_parts(message)
        self.message_label.configure(text='\n'.join(message_parts))
        self.place(relx=0.99, rely=0.02, anchor='ne')

        self.after(5000, self.show_animation)

    def show_animation(self):
        if self.cur_x > self.x:
            self.cur_x -= 1
            self.place(x=self.cur_x)
            self.after(1, self.show_animation)
        else:
            self.hide_animation()


    def hide_animation(self):
        if self.cur_x < self.master.winfo_width():
            self.cur_x += 1
            self.place(x=self.cur_x)
            self.after(1, self.hide_animation)

    def break_message_into_parts(self, message=None):
        if message is None:
            message = self.message_label.cget("text")

        text_parts = []
        current_part = ''
        max_width = 125  # Width of the frame hard coded for now

        # Create a temporary label to calculate the width
        temp_label = ctk.CTkLabel(self, text="", font=self.message_label.cget("font"))
        for word in message.split():
            temp_label.configure(text=current_part + word)
            temp_label.update_idletasks()  # Update the widget
            if temp_label.winfo_reqwidth() > max_width:
                text_parts.append(current_part.strip())
                current_part = ''
            current_part += word + ' '
        text_parts.append(current_part.strip())

        # Destroy the temporary label
        temp_label.destroy()
        return text_parts 
import customtkinter as ctk
from tkinter import filedialog , Canvas
from Settings import *


class ImageImport(ctk.CTkFrame):
    def __init__(self, parent, import_func):
        super().__init__(master=parent)
        self.grid(column = 0, columnspan = 2,
                  row = 0 , sticky = 'nsew')
        self.import_func = import_func

        ctk.CTkButton(self, text='Import', command=self.open_dialog, 
                      corner_radius=10, border_width=0.75, 
                      border_color=BORDER).pack(expand=True)

    def open_dialog(self):
        path = filedialog.askopenfile().name
        self.import_func(path)


class ImageOutput(Canvas):
    def __init__(self, parent, resize_image):
        super().__init__(master=parent, 
                         background= BACKGROUND_COLOR, 
                         bd=0, highlightthickness=0, 
                         relief='ridge')
        
        self.grid(column=1,row=0
                  , sticky='nsew'
                  , padx = 10
                  , pady = 10)
        
        self.bind('<Configure>', resize_image)


class CloseOutput(ctk.CTkButton):
    def __init__(self, parent, close_func):
        super().__init__(master=parent, text='x' ,
                         text_color=WHITE,
                         command=close_func,
                         fg_color='transparent',
                         hover_color=CLOSE_RED,
                         corner_radius= 10,
                         width=40, height=40,
                         border_width= 0.75,
                         border_color=CLOSE_BORDER)
        self.place(relx = 0.99, rely = 0.01, anchor = 'ne')

import customtkinter as ctk
from tkinter import filedialog , Canvas
from Settings import *
from tkVideoPlayer import TkinterVideo


class ImageImport(ctk.CTkFrame): # That import button on the first layout
    def __init__(self, parent, import_func):
        super().__init__(master=parent)
        self.grid(column = 0, columnspan = 2,
                  row = 0 , sticky = 'nsew')
        self.import_func = import_func

        ctk.CTkButton(self, text='Import', command=self.open_dialog, 
                      corner_radius=10, border_width=0.75, 
                      border_color=BORDER).pack(expand=True)

    def open_dialog(self):
        try:
            path = filedialog.askopenfile(filetypes=[('Image', ['*.jpg', '*.jpeg', '*.png']), ('Video', ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.gif'])]).name
            self.import_func(path)
        except:
            pass

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

class VideoOutput(ctk.CTkFrame):

    def __init__(self, parent, video_file):
        super().__init__(master = parent, fg_color = BACKGROUND_COLOR)
        self.video_file = video_file
        self.grid(column=1,row=0
                  , sticky='nsew'
                  , padx = 10
                  , pady = 10)

        self.video_player = TkinterVideo(master=parent, scaled=True, keep_aspect=True, consistant_frame_rate=True, bg=BACKGROUND_COLOR)
        self.video_player.set_resampling_method(1)
        self.video_player.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        self.video_player.bind("<<Configure>>", self.place_video)
        self.video_player.bind("<<Loaded>>", self.place_video)
        self.video_player.bind("<<Duration>>", self.update_duration)
        self.video_player.bind("<<SecondChanged>>", self.update_scale)
        self.video_player.bind("<<Ended>>", self.video_ended)
        self.video_player.load(self.video_file)
        
        self.progress_slider = ctk.CTkSlider(master=parent, from_=-1, to=1, number_of_steps=1, command=self.seek)
        self.progress_slider.set(-1)
        self.progress_slider.grid(row=2, column=1, sticky='nsew', padx=10, pady=10)
        self.play_pause_btn = ctk.CTkButton(master=parent, text="Pause ⏸", command=self.play_pause,
                                                corner_radius=10, border_width=0.75, 
                                                border_color=BORDER)
        self.play_pause_btn.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)
        self.video_player.play()
        
    def place_video(self, event):
        self.update_duration(event)
        self.video_player.seek(1) 

    def update_duration(self, event):
        try:
            duration = int(self.video_player.video_info()["duration"])
            self.progress_slider.configure(from_=-1, to=duration, number_of_steps=duration)

        except Exception as e:
            print(e)
            

    def update_scale(self, event):
        try:
            self.progress_slider.set(int(self.video_player.current_duration()))
        except:
            pass

    def video_ended(self, event):
        self.play_pause_btn.configure(text="Play ▶")
        self.progress_slider.set(-1)
    
    def seek(self, value):
        if self.video_file:
            try:
                self.video_player.seek(int(value))
                self.video_player.play()
                self.video_player.after(50, self.video_player.pause)
                self.play_pause_btn.configure(text="Play ▶")
            except:
                pass

    def play_pause(self):
        if self.video_file:
            if self.video_player.is_paused():
                self.video_player.play()
                self.play_pause_btn.configure(text="Pause ⏸")

            else:
                self.video_player.pause()
                self.play_pause_btn.configure(text="Play ▶")


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

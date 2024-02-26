# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 10:34:44 2024

@author: Usuario
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from widgets.video_player.video_player import VideoPlayer

"""
La clase MainScreen representa la pantalla principal de la interfaz de usuario 
del Software de Análisis Biomecánico. Esta pantalla proporciona una interfaz 
para que el usuario pueda interactuar con las diversas funcionalidades del 
software, como cargar un video para su análisis.
"""
class MainScreen:
    
    def __init__(self, master):
        self.master = master
        
        self.configuration_main_screen()
        self.create_widgets()
    
    def configuration_main_screen(self):
        self.master.title("TIF")
        self.master.geometry("1500x900")
        self.master.resizable(False,False)
    
    
    def create_widgets(self):
        self.create_video_player()
        
        # Boton para cargar un video
        self.load_button = ttk.Button(self.master,text="Cargar Video", 
                                      width=20, command=self.load_video)
        self.load_button.place(x=10, y=10)
    
    
    def load_video(self):
        video_path = filedialog.askopenfilename()
        
        self.video_player.load_video(video_path)
    
    
    def create_video_player(self):
        self.video_frame = ttk.Frame(self.master, width=800, height=500)
        self.video_frame.pack_propagate(False)
        self.video_frame.pack()
        self.video_player = VideoPlayer(self.video_frame)
        
    
    def run(self):
        self.master.mainloop()


# ----------------- MAIN -----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MainScreen(root)
    app.run()
    
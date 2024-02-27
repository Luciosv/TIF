# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 10:34:44 2024

@author: Usuario
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from widgets.video_player.video_player import VideoPlayer
from tests.test_manager import TestManager

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
        
        self.test_manager = TestManager(master)
    
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
        
        # Boton para procesar el video
        self.process_button = ttk.Button(self.master,text="Procesar Video", 
                                      width=20, command=self.process_video)
        self.process_button.place(x=10, y=70)
        #self.create_progressbar()
    
    
    def load_video(self):
        video_path = filedialog.askopenfilename()
        
        self.video_player.load_video(video_path)
    
    
    def process_video(self):
        # me fijo si hay un video que procesar
        video = self.video_player.get_video()
        video_path = self.video_player.get_video_path()
        if video is not None and video_path is not None:
            # creo la barra de progreso
            progressbar = self.create_progressbar()
            # envio el video a procesar y guardo el video procesado
            result_video = self.test_manager.apply_test(video, video_path, progressbar)
            # elimino el progressbar
            #progressbar.destroy()
    
    def create_video_player(self):
        self.video_frame = ttk.Frame(self.master, width=800, height=500)
        self.video_frame.pack_propagate(False)
        self.video_frame.pack()
        self.video_player = VideoPlayer(self.video_frame)
    
    
    def create_progressbar(self):
        progressbar = ttk.Progressbar(self.master, length=800)
        progressbar.pack()
        return progressbar
    
    def run(self):
        self.master.mainloop()


# ----------------- MAIN -----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MainScreen(root)
    app.run()
    
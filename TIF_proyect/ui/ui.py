# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 10:34:44 2024

@author: Usuario
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import threading

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
        self.master.state('zoomed')
        
        width = self.master.winfo_screenwidth()
        height = self.master.winfo_screenheight()
        self.master.geometry(f"{width}x{height}")
        
        #self.master.resizable(False, False)
    
    
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
        
        
    
    
    def load_video(self):
        video_path = filedialog.askopenfilename()
        
        self.video_player.load_video(video_path)
    
    
    def process_video(self):
        # me fijo si hay un video que procesar
        video = self.video_player.get_video()
        video_path = self.video_player.get_video_path()
        if video is not None and video_path is not None:
            # creo la barra de progreso
            self.progessbar = self.create_progressbar()

            self.master.after(1)
            
            # desactivo el boton de procesamiento
            self.process_button.config(state=tk.DISABLED)
            
            # creo un hilo para procesar el video
            thread = threading.Thread(target=self.process_video_thread, args=(video, video_path))
            thread.start()
            
             
    def process_video_thread(self, video, video_path):
        # envio el video a procesar y guardo el video procesado
        result_video_path = self.test_manager.apply_test(video, video_path)
        
        # le doy el video al reproductor de video
        self.video_player.load_video(result_video_path)
        
        # elimino el progressbar y activo el boton nuevamente
        self.progessbar.destroy()
        self.process_button.config(state=tk.NORMAL)

    
    def create_video_player(self):
        self.video_frame = ttk.Frame(self.master, width=800, height=500)
        self.video_frame.pack_propagate(False)
        self.video_frame.pack()
        self.video_player = VideoPlayer(self.video_frame)
    
    
    def create_progressbar(self):
        progressbar = ttk.Progressbar(self.master, length=800, mode="indeterminate")
        progressbar.pack()
        progressbar.start(10)
        return progressbar
    
    def run(self):
        self.master.mainloop()


# ----------------- MAIN -----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MainScreen(root)
    app.run()
    
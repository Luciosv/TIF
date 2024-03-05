# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 10:34:44 2024

@author: Usuario
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
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
        self.master.attributes('-transparentcolor', 'white')
        
        self.configuration_main_screen()
        self.create_widgets()
        
        self.test_manager = TestManager(master)
        
    
    def configuration_main_screen(self):
        self.master.title("TIF")
        self.master.state('zoomed')
        
        width = self.master.winfo_screenwidth()
        height = self.master.winfo_screenheight()
        self.master.geometry(f"{width}x{height}")
        
        # pongo el fondo de pantalla
        bg = tk.PhotoImage(file="assets_diseño_1/background.png")
        
        background_label = ttk.Label(self.master, image = bg)
        background_label.image = bg
        background_label.place(x=0,y=0,relwidth=1,relheight=1)
    
    
    def create_widgets(self):
        self.create_video_player()
        
        # Boton para cargar un video
        self.image_button_load = tk.PhotoImage(file="assets_diseño_1/button cargar boton.png")
        self.load_button = tk.Button(self.master, image=self.image_button_load,
                                      width="218",height="81", command=self.load_video,
                                      bd=0, highlightthickness=0, bg="white")
        self.load_button.place(x=15, y=18)
        
        # Boton para procesar el video
        self.image_button_process = tk.PhotoImage(file="assets_diseño_1/button procesar video.png")
        self.process_button = tk.Button(self.master,image=self.image_button_process, 
                                      width="218",height="81", command=self.process_video,
                                      bd=0, highlightthickness=0, bg="white")
        self.process_button.place(x=15, y=135)
        
        
    
    
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
        width = int(self.master.winfo_screenwidth() * 0.45)
        height = int(self.master.winfo_screenheight() * 0.45)
        self.video_frame = ttk.Frame(self.master, width=width, height=height + 50)
        self.video_frame.pack_propagate(False)
        self.video_frame.pack(pady=10)
        self.video_player = VideoPlayer(self.video_frame, width, height)
    
    
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
    
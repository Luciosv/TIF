# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 11:04:19 2024

@author: Usuario
"""

import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image
from PIL import ImageTk
import imutils


class VideoPlayer:
    
    def __init__(self, master):
        self.master = master
        self.background = cv2.imread("D:/repositorio/TIF_repo/TIF/TIF_proyect/ui/widgets/video_player/assets/black_background_1920x1080.png")
        self.screen = tk.Label(self.master)
        self.screen.pack()
        self.master.after(10, self.show_black_screen)
        
        self.video_path = None
        self.video = None
        self.video_cap = None
        self.progress_bar = None
        
        self.playing = False
                
        self.create_widgets()
    
    
    def get_video(self):
        return self.video
    
    
    def get_video_path(self):
        return self.video_path
    
    
    def set_video(self, video):
        self.video = video
        self.preview()
        
    
    def create_widgets(self):
        self.play_button = tk.Button(self.master, text="Play", command=self.play_pause)
        self.play_button.pack(side=tk.LEFT)

        self.stop_button = tk.Button(self.master, text="Stop", command=self.stop)
        self.stop_button.pack(side=tk.LEFT)


    def create_progressbar(self, from_, to):
        # primero me fijo si hay que eliminar alguna
        if self.progress_bar is not None:
            self.progress_bar.destroy()
        
        self.progress_bar = tk.Scale(self.master, from_=from_, to=to, orient=tk.HORIZONTAL)
        self.progress_bar.pack(fill=tk.X)
    
    
    def set_image_in_screen(self, image):
        image = imutils.resize(image, width=800)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        im = Image.fromarray(image)
        img = ImageTk.PhotoImage(image=im)
        
        self.screen.configure(image=img)
        self.screen.image = img
    
    
    def show_black_screen(self):
        self.set_image_in_screen(self.background)
    
    
    def load_video(self, video_path):
        if len(video_path) > 0:
            self.video_path = video_path
            self.video = cv2.VideoCapture(self.video_path)
            self.video_cap = cv2.VideoCapture(self.video_path)
            
            self.preview()
    

    def preview(self):
        # hago que el primer frame sea la preview
        
        
        
        #ret, frame = self.video.read()
        ret, frame = self.video_cap.read()
        
        if ret:
            self.set_image_in_screen(frame)
            
            # creo el progressbar con el tiempo final
            end = self.video_cap.get(cv2.CAP_PROP_FRAME_COUNT)
            self.create_progressbar(0, end)


    def playing_video(self):
        if self.playing:
            
            # si el usuario cambio el frame
            if self.video_cap.get(cv2.CAP_PROP_POS_FRAMES) != self.progress_bar.get():
                self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, self.progress_bar.get())
            
            ret = self.change_frame()
            
            # cambio el valor del progressbar
            self.progress_bar.set(self.video_cap.get(cv2.CAP_PROP_POS_FRAMES))
            
            fps = 1 / self.video_cap.get(cv2.CAP_PROP_FPS)
            fpms = int(fps * 1000)
            
            self.master.after(fpms,self.playing_video)
            
            # se termina el video
            if not ret:
                self.stop()
                
    
            
    def change_frame(self):
        
        #ret, frame = self.video.read()
        ret, frame = self.video_cap.read()
        
        if ret:
            self.set_image_in_screen(frame)
        
        return ret


    def play_pause(self):
        if self.video is not None:
            # PLAY
            if not self.playing:
                self.playing = True
                self.playing_video()
            
                # cambio el boton
                self.play_button.config(text="Pause")
            
            # PAUSA
            else:
                self.playing = False
                # cambio el boton
                self.play_button.config(text="Play")


    def stop(self):
        if self.video is not None:
            self.playing = False
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            # cambio el boton
            self.play_button.config(text="Play")
            # cambio el valor del progressbar
            self.progress_bar.set(0)
            
            self.change_frame()

# ----------------- MAIN -----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayer(root)
    app.load_video("TUG.mp4")
    root.mainloop()
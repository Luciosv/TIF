# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 13:45:16 2024

@author: Usuario
"""

from .test_base import TestBase
import mediapipe as mp
import cv2
import numpy as np
from math import acos, degrees
import matplotlib 
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
class TUG(TestBase):
    def __init__(self, pantalla):
        super().__init__("TUG")
        
        self.pantalla = pantalla
        # VARIBALES NECESARIAS PARA SABER SI EL VIDEO ES PROCESABLE
        self.skipped_frame_count = 0
        self.accumulated_error = 0
        self.previous_skipped_frame = 0
        self.MAX_ACCUMULATE_ERROR = 10
        # VARIABLES 
        self.vector_hip_posX = []
        self.vector_hip_posY = []
        self.vector_tiempos = []
        self.delta_tiempo = 0
        self.frame_count = 0
        
    
    def apply_test(self, video, video_path):
        # Implementación específica del test TUG
        
        # proceso el video
        video_result = self.process_video(video, video_path)
        
        # retorno el video procesado
        return video_result
    
    def get_types_results(self):
        # Implementación para determinar qué tipos de resultados se pueden obtener
        return True, True  # Por ejemplo, texto y gráfico
    
    def get_text_result(self):
        # Implementación para obtener el texto de los resultados
        pass
    
    """
    PROCESA EL VIDEO CON MEDIAPIPE
    REPRESENTA EL WHILE QUE PROCESA CADA FRAME
    """
    def process_video(self, video, video_path):
        mp_pose = mp.solutions.pose
        
        frame_count = 0
        cap = cv2.VideoCapture(video_path)
        fps_original = cap.get(cv2.CAP_PROP_FPS)
        self.delta_tiempo = 1/fps_original
        self.frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_result, result_video_path = self.create_video(video, video_path)
        
        with mp_pose.Pose(
                static_image_mode=False) as pose:
            
            # leo el primer frame
            
            #ret, frame = video.read()
            ret, frame = cap.read()
            
            
            while ret :
                # PROCESO EL FRAME
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = pose.process(frame_rgb)
                
                # COMPRUEBO EL RESULTADO
                if not self.is_good_result(result, frame_count):
                    # logica para descartar el video
                    pass
                
                # OBTENGO LOS LANDMARKS
                width  = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
                landmarks_x, landmarks_y = self.get_landmarks(result, width, height)
                
                # CALCULO LOS ANGULOS
                self.calculate_angles(landmarks_x, landmarks_y)

                #CALCULO POSICION DE CADERA
                self.calculate_hip_pos(landmarks_x, landmarks_y, width, height)
                
                
                # GENERO EL FRAME OUTPUT
                output_frame = self.generate_output_frame(frame, landmarks_x, landmarks_y)
                
                # GUARDO EL FRAME OUTPUT
                video_result.write(output_frame)
                
                #AGREGO ELEMENTO AL VECTOR DE TIEMPOS
                self.vector_tiempos = np.append(self.vector_tiempos, frame_count/fps_original)
                # PASO AL SIGUIENTE FRAME
                ret, frame = video.read()
                frame_count += 1
        
        # devuelvo el video procesado
        video_result.release()
        
        #MUESTRO VIDEO
        self.show_graphic()
        
        return result_video_path
        

    def create_video(self, video, video_path):
        video_file_result = video_path + "_resultado.mp4"
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') #*'mpv4"
        FPS_result = video.get(cv2.CAP_PROP_FPS)
        
        # resolucion
        width  = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))   # float "width"
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float "height"
        
        resolution = (width, height)   #ej. (640, 480)
        
        video_result = cv2.VideoWriter(video_file_result, fourcc, FPS_result, resolution) # (name.mp4, fourcc, FPS, resolution)
        return video_result, video_file_result
        
    def get_landmarks(self, result, width, height):
        landmarks_x = []
        landmarks_y = []
        
        if result.pose_landmarks is not None:
            # escribo los landsmarks que interesan para el proyecto
            # pierna derecha --> 24 , 26 , 28
            # pierna izquierda --> 23 , 25 , 27
            index = [ 24 , 26 , 28 , 23 , 25 , 27 ]
            
            # tomo los landmarks
            for i in index:
                x = int( result.pose_landmarks.landmark[i].x * width )
                y = int( result.pose_landmarks.landmark[i].y * height )
                
                landmarks_x.append(x)
                landmarks_y.append(y)
        
        return landmarks_x , landmarks_y
    
    
    def calculate_angles(self, landmarks_x, landmarks_y):
        vector_angles_der = []
        vector_angles_izq = []
        
        # Calculo de ángulo pierna derecha:
        p1 = np.array([landmarks_x[0], landmarks_y[0]])
        p2 = np.array([landmarks_x[1], landmarks_y[1]])
        p3 = np.array([landmarks_x[2], landmarks_y[2]])

        l1 = np.linalg.norm(p2 - p3)
        l2 = np.linalg.norm(p1 - p3)
        l3 = np.linalg.norm(p1 - p2)

        angle = degrees(acos((l1**2 + l3**2 - l2**2) / (2 * l1 * l3)))
        vector_angles_der = np.append(vector_angles_der, angle)
        
        #Calculo de ángulo pierna izquierda
        p1 = np.array([landmarks_x[3], landmarks_y[3]])
        p2 = np.array([landmarks_x[4], landmarks_y[4]])
        p3 = np.array([landmarks_x[5], landmarks_y[5]])

        l1 = np.linalg.norm(p2 - p3)
        l2 = np.linalg.norm(p1 - p3)
        l3 = np.linalg.norm(p1 - p2)

        angle = degrees(acos((l1**2 + l3**2 - l2**2) / (2 * l1 * l3)))
        vector_angles_izq = np.append(vector_angles_izq, angle)

    def calculate_hip_pos(self, landmarks_x, landmarks_y, width, height):
        
        hipPromY = 100 - (((landmarks_y[0]+landmarks_y[5])/2)/height)*100 #100- menos va si es der-izq
        self.vector_hip_posY = np.append(self.vector_hip_posY, hipPromY)
        
        hipPromX = 100 - (((landmarks_x[0]+landmarks_x[5])/2)/width)*100 #100- menos va si es der-izq
        self.vector_hip_posX = np.append(self.vector_hip_posX, hipPromX)
        
    def calculate_subida(self):
        saltos=self.step_detection_window(self.vector_hip_posY,5)
        inicio_subida=0
        fin_subida=0
        for i in saltos:
            inicio_subida= i[0] *self.delta_tiempo
            fin_subida= i[1]*self.delta_tiempo
        return inicio_subida , fin_subida
    
    def calculate_bajada(self):
        vector_hip_posY_reversed = self.vector_hip_posY[::-1]
        saltos=self.step_detection_window(vector_hip_posY_reversed,5)
        inicio_caida=0
        fin_caida=0
        for i in saltos:        
            inicio_caida= (self.frame_count - i[0]) *self.delta_tiempo
            fin_caida= (self.frame_count - i[1]) *self.delta_tiempo
        return inicio_caida , fin_caida
            
    
    def generate_output_frame(self, frame, landmarks_x, landmarks_y):
        # GENERO LAS LINEAS
        aux_image = np.zeros(frame.shape, np.uint8)
        #Rigth leg
        cv2.line(aux_image, (landmarks_x[0], landmarks_y[0]), (landmarks_x[1], landmarks_y[1]), (3, 202, 251), 20)
        cv2.line(aux_image, (landmarks_x[1], landmarks_y[1]), (landmarks_x[2], landmarks_y[2]), (3, 202, 251), 20)
        #Left leg
        cv2.line(aux_image, (landmarks_x[3], landmarks_y[3]), (landmarks_x[4], landmarks_y[4]), (3, 202, 251), 20)
        cv2.line(aux_image, (landmarks_x[4], landmarks_y[4]), (landmarks_x[5], landmarks_y[5]), (3, 202, 251), 20)
        
        # AGREGO LAS LINEAS
        output = cv2.addWeighted(frame, 1, aux_image, 0.8, 0)
        
        # AGREGO LOS CIRCULOS
        for x,y in zip(landmarks_x, landmarks_y):
            cv2.circle(output, (x, y), 6, (5,5,170), 4)
        
        return output
        
    
    
    def is_good_result(self, result, frame_count):
        
        if result.pose_landmarks is None:
            self.skipped_frame_count += 1
            
            # LOGICA PARA EL FRAME ANTERIOR
            if self.previous_skipped_frame == frame_count - 1:
                self.accumulated_error += 1
            else:
                self.accumulated_error = 0
            
            self.previous_skipped_frame = frame_count
            
            # LOGICA PARA DESCARTAR EL VIDEO
        
        return self.accumulated_error == self.MAX_ACCUMULATE_ERROR
    
    def get_graphic_result(self):
        figure = Figure(figsize=(6.65, 2.5), dpi=100)
        
        matplotlib.use('TkAgg')
        ax1 = figure.add_subplot()
        #rect : tuple (left, bottom, right, top), default: (0, 0, 1, 1)
        figure.tight_layout(rect=(0.01,0.03,1.005,0.95))
        
        inicio_subida, fin_subida = self.calculate_subida()
        inicio_caida, fin_caida = self.calculate_bajada()
        
        ax1.plot(self.vector_tiempos, self.vector_hip_posX)
        ax1.plot(self.vector_tiempos, self.vector_hip_posY)
        ax1.axvline(x = inicio_subida, color = 'g', linestyle=':') #+{:5.0f}'.format(inicio_subida)
        ax1.axvline(x = fin_subida, color = 'b', linestyle=':')
        ax1.axvline(x = inicio_caida, color = 'g', linestyle=':')
        ax1.axvline(x = fin_caida, color = 'b', linestyle=':')   
        
        ax1.axvspan(self.vector_tiempos[0], inicio_subida, facecolor='b', alpha=0.1)
        ax1.axvspan(inicio_subida, fin_subida, facecolor='r', alpha=0.1)
        ax1.axvspan(fin_subida ,inicio_caida, facecolor='g', alpha=0.1)
        ax1.axvspan(inicio_caida, fin_caida, facecolor='r', alpha=0.1)
        ax1.axvspan(fin_caida, self.vector_tiempos[self.frame_count-1], facecolor='b', alpha=0.1)
        
        
        ax1.grid()
        ax1.set_xlabel("Tiempo [s]")
        ax1.set_ylabel("Porcentaje del frame [%]")
        ax1.set_title("Posición de la cadera en el video")
        #ax1.legend(['Desplazamiento horizontal de cadera en video','Altura de cadera en video'])
        ax1.legend(['Distancia horizontal', 'Altura cadera']) #Inicio subida', 'Fin subida'
        return figure
    
    def show_graphic(self):
        figure = self.get_graphic_result()
        graph_frame = tk.Frame(self.pantalla, width=507, height=285, bg="#02111B")
        graph_frame.place(x=350,y=447)
        
        figure_canvas = FigureCanvasTkAgg(figure, graph_frame)
        navBar_canvas = NavigationToolbar2Tk(figure_canvas, graph_frame)
        navBar_canvas.pack(anchor="sw", fill='none',pady=1,padx=1)#,side='bottom',anchor="sw"
        figure_canvas.get_tk_widget().pack(side='bottom',anchor="sw", fill='none',padx=1)
        figure_canvas.draw()
        
    def step_detection_window(self,data, window_size):
        high = False
        steps = []
        margin = 1.05

        for i in range(window_size, len(data)):
            window = data[i-window_size:i]
            window_avg = np.mean(window)
        
            if data[i] > (window_avg*margin) and not high:
                high = True
                start = i - window_size
            elif data[i] < (window_avg*margin) and high:
                high = False
                steps.append((start, i))
                start = i - window_size
        return steps

if __name__ == "__main__":
    tug = TUG()
    video_path = ""
    video = cv2.VideoCapture(video_path)
    
    tug.process_video(video, video_path)

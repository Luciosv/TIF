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

class TUG(TestBase):
    def __init__(self):
        super().__init__("TUG")
        
        # VARIBALES NECESARIAS PARA SABER SI EL VIDEO ES PROCESABLE
        self.skipped_frame_count = 0
        self.accumulated_error = 0
        self.previous_skipped_frame = 0
        self.MAX_ACCUMULATE_ERROR = 10
        
    
    def apply_test(self, video, video_path):
        # Implementación específica del test TUG
        
        # proceso el video
        video_result = self.process_video(video, video_path)
        
        # retorno el video procesado
        return video_result
    
    def get_types_results(self):
        # Implementación para determinar qué tipos de resultados se pueden obtener
        return True, True  # Por ejemplo, texto y gráfico
    
    def get_graphic_result(self):
        # Implementación para obtener los datos del gráfico
        pass
    
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
        
        video_result, result_video_path = self.create_video(video, video_path)
        
        with mp_pose.Pose(
                static_image_mode=False) as pose:
            
            # leo el primer frame
            
            #ret, frame = video.read()
            ret, frame = cv2.VideoCapture(video_path).read()
            
            
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
                
                #CALCULO POSICION DE CADERA
                self.calculate_hip_pos(landmarks_x, landmarks_y, width, height)
                
                # GENERO EL FRAME OUTPUT
                output_frame = self.generate_output_frame(frame, landmarks_x, landmarks_y)
                
                # GUARDO EL FRAME OUTPUT
                video_result.write(output_frame)
                
                # PASO AL SIGUIENTE FRAME
                ret, frame = video.read()
                frame_count += 1
        
        # devuelvo el video procesado
        video_result.release()
        
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
        vector_hip_posX = []
        vector_hip_posY = []
        
        hipPromY = 100 - (((landmarks_y[0]+landmarks_y[5])/2)/height)*100 #100- menos va si es der-izq
        vector_hip_posY = np.append(vector_hip_posY, hipPromY)
        
        hipPromX = 100 - (((landmarks_x[0]+landmarks_x[5])/2)/width)*100 #100- menos va si es der-izq
        vector_hip_posX = np.append(vector_hip_posX, hipPromX)
    
    
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
                
                
        

if __name__ == "__main__":
    tug = TUG()
    video_path = ""
    video = cv2.VideoCapture(video_path)
    
    tug.process_video(video, video_path)

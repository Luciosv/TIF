# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 13:45:16 2024

@author: Usuario
"""

from test_types.test_base import TestBase
import mediapipe as mp
import cv2

class TUG(TestBase):
    def __init__(self):
        super().__init__("Time Up and Go - TUG")
    
    def apply_test(self, video, video_path):
        # Implementación específica del test TUG
        pass
    
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
    DEVUELVE EL VIDEO PROCESADO Y EL RESULTADO DE MEDIAPIPE PARA REALIZAR
    LOS CALCULOS NECESARIOS
    """
    def process_video(self, video, video_path):
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose
        
        video_result = self.create_video(video, video_path)
        
        with mp_pose.Pose(
                static_image_mode=False) as pose:
            
            # leo el primer frame
            ret, frame = video.read()
            
            while ret :
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = pose.process(frame_rgb)
        

    def create_video(self, video, video_path):
        video_file_result = video_path + "_resultado.mp4"
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') #*'mpv4"
        FPS_result = video.get(cv2.CAP_PROP_FPS)
        
        # resolucion
        width_original  = video.get(cv2.CAP_PROP_FRAME_WIDTH)   # float "width"
        height_original = video.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float "height"
        
        scale_percent = 700 * 100 / height_original # Porcentaje de escalado para el video a guardar (será el mismo para el video original a mostrar)
        width_result = int(width_original * scale_percent / 100)
        height_result = int(height_original * scale_percent / 100)
        resolution_result = (width_result, height_result)   #ej. (640, 480)
        
        video_result = cv2.VideoWriter(video_file_result, fourcc, FPS_result, resolution_result) # (name.mp4, fourcc, FPS, resolution)
        return video_result
        

if __name__ == "__main__":
    pass
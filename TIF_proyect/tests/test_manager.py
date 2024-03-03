# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 13:41:17 2024

@author: Usuario
"""

# -------- IMPORT DE LOS TEST --------
from .test_types.tug import TUG

from .results_display import ResultsDisplay


class TestManager:
    
    def __init__(self, master):
        self.results_display = ResultsDisplay(master)
        
        # -------- CREACION DE LOS TEST --------
        self.create_tests()
        
        # Por defecto, el current test es el primer test del diccionario
        self.current_test = list(self.tests.keys())[0]
    
    
    def set_test_type(self, test_type):
        if test_type in self.tests:
            self.current_test = test_type
    
    
    def get_test_type(self):
        return self.tests.keys()
    
    
    def get_current_test(self):
        return self.current_test
    
    
    def apply_test(self, video, video_path):
        result_video_path = None
        
        if self.current_test in self.tests:
            result_video_path = self.tests[ self.current_test ].apply_test(video, video_path)
        
        return result_video_path
            
    
    
    def create_tests(self):
        # defino todos los test
        tug = TUG()
        
        # los agrego con el formato NOMBRE - TEST
        self.tests = { tug.name : tug }


if __name__ == "__main__":
    test_manager = TestManager([])
    
    print(test_manager.get_current_test())
    
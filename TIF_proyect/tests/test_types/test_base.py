# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 13:42:13 2024

@author: Usuario
"""

from abc import ABC, abstractmethod

class TestBase(ABC):
    
    def __init__(self, name):
        self._name = name
        
    @property
    def name(self):
        return self._name
    
    
    @abstractmethod
    def apply_test(self, video, video_path):
        pass


    @abstractmethod
    def get_types_results(self):
        pass


    @abstractmethod
    def get_graphic_result(self):
        pass


    @abstractmethod
    def get_text_result(self):
        pass
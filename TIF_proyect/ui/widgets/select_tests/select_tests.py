# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 19:05:04 2024

@author: Usuario
"""

import tkinter as tk

class SelectTests():
    def __init__(self, master, options, x=0, y=0, width="218", height="81"):
        self.master = master
        self.options = options
        self.selected_option = tk.StringVar()
        
        self.create_button(x, y, width, height)
    
    
    def create_button(self, x, y, width, heighti):
        # creo la imagen para el boton
        self.image_button = tk.PhotoImage(file="D:/repositorio/TIF_repo/TIF/TIF_proyect/ui/widgets/select_tests/assets/button seleccion.png")
        
        # agarro la primer opcion de options para que sea por defecto la opcion elegida
        self.selected_option.set(self.options[0])
        
        self.button = tk.Button(self.master, textvariable=self.selected_option, command=self.show_menu,
                                image=self.image_button, width=width, height=heighti, foreground="#DB5461",
                                compound="center", bg="#02111B", font=("Arial", 18),
                                bd=0, highlightthickness=0)
        
        self.button.place(x=x, y=y)
    
    
    def show_menu(self):
        menu = tk.Menu(self.master, tearoff=0)
        menu.config(font=("Arial", 15), bg="#02111B", fg="#DB5461")
        
        for option in self.options:
            menu.add_radiobutton(label=option, variable=self.selected_option, compound="left")
        
        # muestro el menu en la posicion del boton
        menu.post(self.button.winfo_rootx(), self.button.winfo_rooty() + self.button.winfo_height())
    
    
    def get(self):
        return self.selected_option.get()


# ----------------- MAIN -----------------
if __name__ == "__main__":
    master = tk.Tk()
    options = ["opcion 1", "opcion 2", "opcion 3"]
    
    select_test = SelectTests(master, options)
    
    master.mainloop()
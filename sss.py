import threading
from socket import *
from customtkinter import *

class MainWindow(CTK):
    def __init__(self):
        self.geometry("401x300")
        self.label = None
        
        self.menu_frame = CTkFrame(self, width=30, height=300)
        self.menu_frame.pack_propagate(False)
        self.menu_frame.place(x=0, y=0)
        self.is_show_menu = False
        self.speed_animate_menu = -5
        self.btn = CTKBotton(self, text="►", command=self.toggle_show_menu, width=30)
        
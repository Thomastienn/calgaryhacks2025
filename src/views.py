# Handle UI components and layout here
import time

import customtkinter as ctk
import src.utils as utils

class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hackathon")
        self.geometry("600x600")
        
        # Instantiate all views in here
        StartView(self)
        
        self.mainloop()
    
class StartView:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True)
        

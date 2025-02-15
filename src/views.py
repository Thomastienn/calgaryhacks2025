# Handle UI components and layout here
import time

import customtkinter as ctk
from tkcalendar import Calendar
from src.Finance.FinanceTracker import FinanceTracker
from src.Finance.Thing import Thing
from customtkinter import CTkFrame
from datetime import datetime

import src.utils as utils

class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hackathon")
        self.geometry("1200x600")
        
        # Instantiate all views in here
        TabsView(self)
        
        self.mainloop()
    
class StartView:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True)
        

class TabsView:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(self.parent, fg_color="black", height=100)
        self.frame.pack_propagate(False)
        self.frame.pack(side="bottom", fill="x")
        self.create_buttons()
        
    def create_buttons(self):
        self.finance_button = ctk.CTkButton(self.frame, text="Finance", command=self.finance_button_click)
        self.finance_button.pack(side="left", padx=50)
        self.tasks_button = ctk.CTkButton(self.frame, text="Tasks", command=self.tasks_button_click)
        self.tasks_button.pack(side="left", padx=50)
        
    def finance_button_click(self):
        FinanceView(self.parent)
    
    def tasks_button_click(self):
        TasksView(self.parent)

class FinanceView:
    def __init__(self, parent):
        self.tracker = FinanceTracker()
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack_propagate(False)
        self.frame.pack(fill="both", expand=True)
        self.finance_table = ctk.CTkFrame(self.frame, width=700)
        self.finance_table.pack_propagate(False)
        self.finance_table.pack(side="left", padx=10, pady=10, fill="y")
        self.add_finance_frame = ctk.CTkFrame(self.finance_table, height=50, fg_color="green")
        self.add_finance_frame.pack_propagate(False)
        self.add_finance_frame.pack(fill="x")
        self.selected_option = ctk.StringVar()
        self.categories_dropdown = ctk.CTkOptionMenu(self.add_finance_frame, variable=self.selected_option, values=Thing.OPTIONS_STR)
        self.categories_dropdown.set("Select a Category")
        self.categories_dropdown.pack(side="left", padx=5)
        self.add_finance_entry = ctk.CTkEntry(self.add_finance_frame)
        self.add_finance_entry.pack(side="left")
        self.add_finance_cost_frame = ctk.CTkFrame(self.add_finance_frame, fg_color="transparent")
        self.add_finance_cost_frame.pack(side="left", padx=5)
        self.add_finance_cost_entry_dollar = ctk.CTkLabel(self.add_finance_cost_frame, text="$")
        self.add_finance_cost_entry_dollar.pack(side="left")
        self.add_finance_cost_entry = ctk.CTkEntry(self.add_finance_cost_frame)
        self.add_finance_cost_entry.pack(padx=5)
        self.date_entry = ctk.CTkEntry(self.add_finance_frame)
        self.date_entry.pack(side="left")
        self.date_entry.insert(0, str(datetime.now().date()))
        self.add_button = ctk.CTkButton(self.add_finance_frame, text="+", command=self.add_button_press)
        self.add_button.pack(side="left", padx=10)
        self.finance_scroll_frame = ctk.CTkScrollableFrame(self.finance_table, fg_color="black")
        self.finance_scroll_frame.pack(fill="both", expand=True)
        
        self.date_frames = {}

    def add_button_press(self):
        category = self.categories_dropdown.get()
        name = self.add_finance_entry.get()
        cost = self.add_finance_cost_entry.get()
        
        # Check if valid
        year, month, day = map(int, self.date_entry.get().split("-"))
        if True:
            if self.tracker.dateEmpty(year, month, day):
                self.date_frames[self.date_entry.get()] = ctk.CTkFrame(self.finance_scroll_frame)
                self.date_frames[self.date_entry.get()].pack(side="top", fill="x", pady=5)
                current_date_label = ctk.CTkLabel(self.date_frames[self.date_entry.get()], text=f"{year}-{month}-{day}")
                current_date_label.pack(side="top")

            finance_frame = ctk.CTkFrame(self.date_frames[self.date_entry.get()], height=35)
            finance_frame.pack(fill="x", side="top", padx=5, pady=5)
            category_text = ctk.CTkLabel(finance_frame, text=category)
            category_text.pack(side="left", padx=50)
            name_text = ctk.CTkLabel(finance_frame, text=name)
            name_text.pack(side="left", expand=True)
            name_text = ctk.CTkLabel(finance_frame, text="$" + cost)
            name_text.pack(side="left", expand=True)
            
                
            self.tracker.put(name, cost, category, self.date_entry.get())
            
        
class TasksView:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack_propagate(False)
        self.frame.pack(fill="both", expand=True)



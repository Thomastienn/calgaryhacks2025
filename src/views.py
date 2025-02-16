# Handle UI components and layout here
import time

import customtkinter as ctk
from src.Finance.FinanceTracker import FinanceTracker
from src.Finance.Thing import Thing
from src.models import PieChartApp
from datetime import datetime
from PIL import Image

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
        self.frame = ctk.CTkFrame(parent, fg_color="#3C3D40")
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
        
        self.pie_chart_frame = ctk.CTkFrame(self.frame, fg_color="#3C3D40")
        self.pie_chart_frame.pack(side="left", expand=True)
        self.pie_chart_title = ctk.CTkLabel(self.pie_chart_frame, text="Overview of the Month", font=("Arial", 30, "bold"))
        self.pie_chart_title.pack(side="top")
        self.pie_chart = PieChartApp(self.pie_chart_frame)
        self.income_month = ctk.CTkLabel(self.pie_chart_frame, text="$0")
        self.spent_month = ctk.CTkLabel(self.pie_chart_frame, text="$0")
        
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
            
            self.tracker.put(name, float(cost), category, self.date_entry.get())
            self.pie_chart.update_chart(self.tracker)
            
        
class TasksView:
    def __init__(self, root):
        self.get_images()
        self.buttons = []
        self.root = root
        self.root.config(bg="#333333")
        ctk.set_appearance_mode("Dark")

        self.task_entry = ctk.CTkEntry(
            root, width=300, placeholder_text="Enter the task", font=("Arial", 14)
        )
        self.task_entry.pack(pady=20)

        self.add_button = ctk.CTkButton(
            self.root, text="Add Task", width=200, height=40, font=("Arial", 14),
            command=self.add_task
        )
        self.add_button.pack(pady=10)

        # Frame to hold all task items
        self.tasks_frame = ctk.CTkFrame(self.root, height=200)
        self.tasks_frame.pack(pady=10, fill="both", expand=True)

        self.clear_button = ctk.CTkButton(
            self.root, text="Clear All", width=200, height=40, font=("Arial", 14),
            command=self.clear_all_tasks
        )
        self.clear_button.pack(pady=5)
        
    def get_images(self):
        # Opens the images
        try:
            # Using .copy() keeps the image saved in memory so I don't have to keep opening the images to access them
            with Image.open(
                    "src/img/trash.png").copy() as trash_image, Image.open(
                "src/img/trashRed.png").copy() as trash_red_image:
                self.scaled_trash_image = ctk.CTkImage(trash_image, size=(70, 70))
                self.scaled_trash_red_image = ctk.CTkImage(trash_red_image, size=(70, 70))
        except FileNotFoundError as e:
            print(f"Cannot access all image dependencies: {e}")
            raise SystemExit

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            # Create a container frame for the task
            task_frame = ctk.CTkFrame(self.tasks_frame, fg_color="transparent")
            task_frame.pack(fill="x", pady=2, padx=10)

            # Task checkbox on the left with a callback to toggle text color
            task_checkbox = ctk.CTkCheckBox(
                task_frame, text=task, font=("Arial", 14),
                command=lambda: self.toggle_task(task_checkbox)
            )
            task_checkbox.pack(side="left", padx=(10, 0))

            # Remove button on the right
            remove_button = ctk.CTkButton(
                task_frame, text="", fg_color="transparent", width=70, height=70, image=self.scaled_trash_image,
                command=lambda: self.remove_task_item(task_frame)
            )
            index = len(self.buttons)
            self.buttons.append(remove_button)
            remove_button.bind("<Enter>", lambda: self.on_hover(index))
            remove_button.pack(side="right", padx=(0, 10))

            self.task_entry.delete(0, ctk.END)
    
    def on_hover(self, index):
        self.buttons[index].config(image=self.scaled_trash_red_image)

    def toggle_task(self, checkbox):
        # Change text color based on whether the checkbox is checked
        if checkbox.get():
            checkbox.configure(text_color="grey")
        else:
            checkbox.configure(text_color="white")

    def remove_task_item(self, task_frame):
        task_frame.destroy()

    def clear_all_tasks(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
# Handle UI components and layout here
import math
import os.path
import pickle
import time
import webbrowser

import customtkinter as ctk
from customtkinter import CTkFrame
from unicodedata import category

from src.Finance.FinanceTracker import FinanceTracker
from src.Finance.Thing import Thing
from src.FrontPage.QuoteReceiver import QuoteReceiver
from src.models import PieChartApp
from src.Rent.RentFinder import RentFinder
from datetime import datetime, date, timedelta
from PIL import Image

import src.utils as utils

class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title_text = "Hackathon"
        self.title(self.title_text)
        self.geometry("1200x600")
        
        # Instantiate all views in here
        MainMenu(self, self.title_text)
        #TabsView(self)
        
        self.mainloop()
    
class StartView:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True)
        
class MainMenu:
    def __init__(self, root, title, quote_position=0.3):
        self.root = root
        self.frame = ctk.CTkFrame(root)
        self.frame.pack(fill="both", expand=True)

        # Store parameters
        self.title_text = title
        self.quote_generator = QuoteReceiver()
        new_quote = self.quote_generator.getQuote()
        self.quote = new_quote.desc
        self.author = new_quote.author
        self.quote_position = quote_position  # Controls distance from top

        # Create the title at the top
        self.create_main_title()

        # Create the quote section
        self.create_quote_section()

        # Create the enter button
        self.create_enter_button()

    def create_main_title(self):
        """Creates the title at the top center."""
        title_label = ctk.CTkLabel(
            self.frame,
            text=self.title_text,
            font=("Arial", 40, "bold"),
            text_color="white"
        )
        title_label.place(relx=0.5, rely=0.05, anchor="center")  # Centered at the top

    def create_quote_section(self):
        """Creates the centered quote section with author."""
        quote_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        quote_frame.place(relx=0.5, rely=self.quote_position+0.08, anchor="center")  # ✅ Position is now adjustable

        # Quote text (Make it stand out)
        quote_label = ctk.CTkLabel(
            quote_frame,
            text=f'“{self.quote}”',
            font=("Arial", 30, "bold"),  # Large and bold for emphasis
            text_color="white",
            wraplength=750,
            justify="center"
        )
        quote_label.pack(pady=10)

        # Author text (Smaller, below the quote)
        author_label = ctk.CTkLabel(
            quote_frame,
            text=f"- {self.author}",
            font=("Arial", 18, "italic"),
            text_color="lightgray"
        )
        author_label.pack()

    def create_enter_button(self):
        """Creates the enter button centered at the bottom."""
        enter_button = ctk.CTkButton(
            self.frame,
            text="Enter",
            font=("Arial", 20, "bold"),
            fg_color="#4CAF50",  # Green color
            hover_color="#66BB6A",
            width=200,
            height=50,
            corner_radius=10,
            command=self.enter_pressed  # Placeholder function
        )
        enter_button.pack(side="bottom", pady=40)

    def enter_pressed(self):
        TabsView(self.root)
        FinanceView(self.root)
        self.frame.destroy()

class TabsView:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(self.parent, fg_color="black", height=100)
        self.frame.pack_propagate(False)
        self.frame.pack(side="bottom", fill="x")
        self.create_buttons()
        
    def create_buttons(self):
        self.finance_button = ctk.CTkButton(self.frame, text="Finance", command=self.finance_button_click)
        self.finance_button.pack(side="left", expand=True)
        self.tasks_button = ctk.CTkButton(self.frame, text="Tasks", command=self.tasks_button_click)
        self.tasks_button.pack(side="left", expand=True)
        self.house_button = ctk.CTkButton(self.frame, text="Renting", command=self.house_button_click)
        self.house_button.pack(side="left", expand=True)
        self.jobs_button = ctk.CTkButton(self.frame, text="Jobs", command=self.jobs_button_click)
        self.jobs_button.pack(side="left", expand=True)
        
    def switch_view(self, new_view):
        for widget in self.parent.winfo_children():
            if widget != self.frame:
                widget.destroy()
        
        new_view(self.parent)
            
        
    def finance_button_click(self):
        self.switch_view(FinanceView)
    
    def tasks_button_click(self):
        self.switch_view(TasksView)
        
    def house_button_click(self):
        self.switch_view(RentingView)
    
    def jobs_button_click(self):
        pass

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
        for year in self.tracker.finance_list.getYear():
            for month in self.tracker.finance_list.getMonth(year):
                for day in self.tracker.finance_list.getDay(year,month):
                    date = f"{year}-{month}-{day}"
                    for stuff in self.tracker.finance_list.getItem(year,month,day):
                        if date not in self.date_frames:
                            self.date_frames[date] = ctk.CTkFrame(self.finance_scroll_frame)
                            self.date_frames[date].pack(side="top", fill="x", pady=5)
                            current_date_label = ctk.CTkLabel(self.date_frames[date],
                                                              text=f"{year}-{month}-{day}")
                            current_date_label.pack(side="top")
                        finance_frame = ctk.CTkFrame(self.date_frames[date], height=35)
                        finance_frame.pack(fill="x", side="top", padx=5, pady=5)
                        category_text = ctk.CTkLabel(finance_frame, text=stuff.type)
                        category_text.pack(side="left", padx=50)
                        name_text = ctk.CTkLabel(finance_frame, text=stuff.name)
                        name_text.pack(side="left", expand=True)
                        amount_text = ctk.CTkLabel(finance_frame, text="$" + str(stuff.amount))
                        amount_text.pack(side="left", expand=True)
        try:
            self.pie_chart.update_chart(self.tracker)
        except:
            pass

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
            amount_text = ctk.CTkLabel(finance_frame, text="$" + cost)
            amount_text.pack(side="left", expand=True)
            
            self.tracker.put(name, float(cost), category, self.date_entry.get())
            self.pie_chart.update_chart(self.tracker)
            
        
class TasksView:
    def __init__(self, root):
        self.get_images()
        self.buttons = []
        self.frame = ctk.CTkFrame(root)
        self.frame.pack(expand=True, fill="both")
        self.todo_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.todo_frame.pack(side="left", expand=True, fill="both", padx=10)
        self.frame_dict = {}
        self.calendar_frame = ModernCalendar(self, self.frame)
        

        self.task_entry = ctk.CTkEntry(
            self.todo_frame, width=300, placeholder_text="Enter the task", font=("Arial", 14)
        )
        self.task_entry.pack(pady=20)

        self.add_button = ctk.CTkButton(
            self.todo_frame, text="Add Task", width=200, height=40, font=("Arial", 14),
            command=self.add_task
        )
        self.add_button.pack(pady=10)

        # Frame to hold all task items
        self.tasks_frame = ctk.CTkFrame(self.todo_frame, height=200, fg_color="#3C3D40")
        self.tasks_frame.pack(pady=10, fill="both", expand=True)

        self.clear_button = ctk.CTkButton(
            self.todo_frame, text="Clear All", width=200, height=40, font=("Arial", 14),
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
    
    def switch_view(self, selected_date):
        self.tasks_frame.pack_forget()
        self.clear_button.pack_forget()
        if selected_date in self.frame_dict:
            self.tasks_frame = self.frame_dict[selected_date]
        else:
            self.tasks_frame = ctk.CTkFrame(self.todo_frame, height=200, fg_color="#3C3D40")
        self.tasks_frame.pack(pady=10, fill="both", expand=True)
        self.clear_button.pack(pady=5)
        

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
            
            self.frame_dict[self.calendar_frame.get_selected_date()] = self.tasks_frame
            self.calendar_frame.dot_update()
    
    def on_hover(self, index):
        self.buttons[index].configure(image=self.scaled_trash_red_image)

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

class RentingView:
    def __init__(self,parent): 
        self.get_images()
        self.frame = CTkFrame(parent)
        self.frame.pack(fill="both", expand=True)
        self.scrolling_frame = ctk.CTkScrollableFrame(self.frame)
        self.scrolling_frame.pack(fill="both", expand=True)
        self.loading()
        parent.update_idletasks()
        self.rent_title = ctk.CTkLabel(self.scrolling_frame, text="Houses for rent near you", font=("Arial", 30, "bold"))
        self.rent_title.pack(side="top", expand=True, fill="x")
        self.house_rows = []

        self.renter = RentFinder()
        house_list = self.renter.getHouses()
        count = 1
        self.current_house_row = ctk.CTkFrame(self.scrolling_frame)
        for house in house_list:
            if count > 3:
                self.current_house_row.pack(padx=10, pady=10, expand=True, fill="x")
                self.current_house_row = ctk.CTkFrame(self.scrolling_frame)
                count = 1
            self.create_house(house.title, house.cost, house.address, house.link)
            count += 1
        
        self.loading_frame.destroy()
    
    def get_images(self):
        try:
            # Using .copy() keeps the image saved in memory so I don't have to keep opening the images to access them
            with Image.open(
                    "src/img/house.png").copy() as house_image:
                self.scaled_house_image = ctk.CTkImage(house_image, size=(200, 200))
        except FileNotFoundError as e:
            print(f"Cannot access all image dependencies: {e}")
            raise SystemExit
    
    def callback(self, url):
        webbrowser.open(url)
    
    def loading(self):
        self.loading_frame = ctk.CTkFrame(self.frame, width=self.frame.winfo_width()//2, height=self.frame.winfo_height()//2)
        self.loading_frame.place(relx=0, rely=0)
        self.loading_frame.pack_propagate(False)
        loading_frame_text = ctk.CTkLabel(self.loading_frame, text="Retrieving House Data...", font=("Arial", 100, "bold"))
        loading_frame_text.pack(expand=True, fill="both")
        
    def create_house(self, title, cost, address, link):
        house_frame = ctk.CTkFrame(self.current_house_row, width=400, height=400, fg_color="black")
        house_frame.pack_propagate(False)
        house_cost = ctk.CTkLabel(house_frame, text=f"${cost}/month")
        if cost is None:
            house_cost.configure(text="Inquire for price")
        house_cost.pack(side="top", expand=True)
        house_img = ctk.CTkLabel(house_frame, text="", image=self.scaled_house_image, fg_color="transparent")
        house_img.pack(side="top", expand=True)
        house_title = ctk.CTkLabel(house_frame, text=f"{title}")
        house_title.pack(side="top", expand=True)
        house_address = ctk.CTkLabel(house_frame, text=f"{address}")
        house_address.pack(side="top", expand=True)
        house_link = ctk.CTkLabel(house_frame, text="View more information", text_color="blue", underline=0, cursor="hand2")
        house_link.bind("<Button-1>", lambda e: self.callback(link))
        house_link.pack(side="top", expand=True)
        house_frame.pack(side="left", expand=True, padx=10)
        
class ModernCalendar:
    def __init__(self, task_class, parent, event_callback=None, year=None, month=None):
        self.event_callback = event_callback
        self.parent = parent
        self.task_class = task_class
        self.frame = ctk.CTkFrame(parent, fg_color="#3C3D40")
        self.frame.pack(side="right", fill="both", padx=20, pady=10)
        self.buttons_with_tasks = []

        # Default to current date if none provided
        today = date.today()
        self.year = year if year is not None else today.year
        self.month = month if month is not None else today.month
        self.selected_date = None

        self.create_widgets()
        self.draw_calendar()

    def create_widgets(self):
        self.create_header()
        self.create_day_labels()
        self.buttons_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.buttons_frame.pack(pady=(5, 10))

    def create_header(self):
        self.header_frame = ctk.CTkFrame(self.frame, fg_color="#2c3e50")
        self.header_frame.pack(fill="x", pady=10)

        self.prev_button = ctk.CTkButton(
            self.header_frame, text="◀", width=30, fg_color="#34495e",
            command=self.prev_month, font=("Segoe UI", 14, "bold")
        )
        self.prev_button.pack(side="left", padx=10, pady=5)

        self.month_label = ctk.CTkLabel(
            self.header_frame, text="", font=("Segoe UI", 16, "bold"),
            fg_color="transparent", text_color="white"
        )
        self.month_label.pack(side="left", expand=True)

        self.next_button = ctk.CTkButton(
            self.header_frame, text="▶", width=30, fg_color="#34495e",
            command=self.next_month, font=("Segoe UI", 14, "bold")
        )
        self.next_button.pack(side="right", padx=10, pady=5)

    def create_day_labels(self):
        self.days_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.days_frame.pack()
        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

        for day in days:
            lbl = ctk.CTkLabel(
                self.days_frame, text=day, font=("Segoe UI", 11, "bold"),
                fg_color="transparent", text_color="#2c3e50"
            )
            lbl.pack(side="left", expand=True, padx=5, pady=2)

    def draw_calendar(self, date_selected=None):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        self.month_label.configure(text=f"{self.get_month_name(self.month)} {self.year}")

        first_day = date(self.year, self.month, 1)
        first_day_weekday = (first_day.weekday() + 1) % 7
        num_days = self.days_in_month(self.year, self.month)

        # Determine previous and next month info for leading/trailing days
        prev_year, prev_month = (self.year, self.month - 1) if self.month > 1 else (self.year - 1, 12)
        next_year, next_month = (self.year, self.month + 1) if self.month < 12 else (self.year + 1, 1)
        num_days_prev = self.days_in_month(prev_year, prev_month)

        # Create a list of (date, is_current_month)
        day_cells = []
        for i in range(first_day_weekday):
            day_cells.append((date(prev_year, prev_month, num_days_prev - first_day_weekday + 1 + i), False))
        for d in range(1, num_days + 1):
            day_cells.append((date(self.year, self.month, d), True))
        next_day = 1
        while len(day_cells) < 42:
            day_cells.append((date(next_year, next_month, next_day), False))
            next_day += 1

        # Create calendar grid
        for index, (cell_date, in_current) in enumerate(day_cells):
            r, c = divmod(index, 7)
            
            btn_fg = "#2c3e50" if in_current  else "#bdc3c7"
            btn_bg = "#d3d3d3" if self.selected_date == cell_date else "#ffffff"
            print(cell_date, self.buttons_with_tasks)
            if cell_date in self.buttons_with_tasks:
                btn_bg="#5C6D70"
            btn = ctk.CTkButton(
                self.buttons_frame, text=str(cell_date.day),
                font=("Segoe UI", 12, "bold"),
                fg_color=btn_bg, text_color=btn_fg, width=40, height=40,
                command=lambda d=cell_date: self.on_day_click(d),
                hover_color="#5C6770"
            )
            btn.grid(row=r, column=c, padx=5, pady=5)

    def on_day_click(self, cell_date):
        self.selected_date = cell_date
        self.task_class.switch_view(self.selected_date)
        self.draw_calendar()
        if self.event_callback:
            self.event_callback(cell_date.strftime("%Y-%m-%d"))

    def prev_month(self):
        self.month -= 1
        if self.month < 1:
            self.month = 12
            self.year -= 1
        self.draw_calendar()

    def next_month(self):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
        self.draw_calendar()

    def days_in_month(self, year, month):
        return (date(year, month % 12 + 1, 1) - timedelta(days=1)).day

    def get_month_name(self, month):
        return ["January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"][month - 1]

    def get_selected_date(self):
        return self.selected_date
    
    def dot_update(self):
        self.buttons_with_tasks.append(self.get_selected_date())
        self.draw_calendar()
        
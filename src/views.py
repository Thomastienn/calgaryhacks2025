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
from src.Job.JobFinder import JobFinder
from src.Meals.Recipes import Recipes
from src.models import PieChartApp
from src.Rent.RentFinder import RentFinder
from datetime import datetime, date, timedelta
from PIL import Image
from src.Constants import Constants

import src.utils as utils

class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title_text = "HandiGo"
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
        self.root.configure(fg_color=Constants.DARK_GREY)
        self.frame = ctk.CTkFrame(root, fg_color=Constants.DARK_GREY)
        self.frame.pack(fill="x", expand=True)

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
        header_frame = ctk.CTkFrame(self.frame, fg_color=Constants.DARK_GREY)
        header_frame.pack(pady=80)
        title_label = ctk.CTkLabel(
            header_frame,
            text=self.title_text,
            font=(Constants.FONT, 40, "bold"),
            text_color="white",
            fg_color=Constants.DARK_GREY
        )
        subtitle_label = ctk.CTkLabel(header_frame, text="Your all-in-one app supporting transition to independence", font=(Constants.FONT, 20, "bold"))
        title_label.pack(expand=True)
        subtitle_label.pack(pady=10)

    def create_quote_section(self):
        quote_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        quote_frame.pack(pady=10)

        quote_label = ctk.CTkLabel(
            quote_frame,
            text=f'“{self.quote}”',
            font=(Constants.FONT, 30, "bold"),
            text_color="white",
            wraplength=750,
            justify="center"
        )
        quote_label.pack()

        author_label = ctk.CTkLabel(
            quote_frame,
            text=f"- {self.author}",
            font=("Segoe UI", 18, "italic"),
            text_color="lightgray"
        )
        author_label.pack(expand=True)

    def create_enter_button(self):
        enter_button = ctk.CTkButton(
            self.frame,
            text="Enter",
            font=("Segoe UI", 20, "bold"),
            fg_color=Constants.MILK,  #millk color
            hover_color="#C19A6B",
            text_color = Constants.DARK_GREY,
            width=200,
            height=50,
            corner_radius=10,
            command=self.enter_pressed  # Placeholder function
        )
        enter_button.pack(side="top", pady=80)

    def enter_pressed(self):
        TabsView(self.root)
        FinanceView(self.root)
        self.frame.destroy()

class TabsView:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(self.parent, fg_color="#40382E", height=100)
        self.frame.pack_propagate(False)
        self.frame.pack(side="bottom", fill="x")
        self.create_buttons()
        
    def create_buttons(self):
        self.finance_button = ctk.CTkButton(self.frame, text="Finance", command=self.finance_button_click, fg_color=Constants.MILK, font=(Constants.FONT, 25, "bold"), text_color=Constants.DARK_GREY, hover_color="#CBAC8A")
        self.finance_button.pack(side="left", expand=True)
        self.tasks_button = ctk.CTkButton(self.frame, text="Tasks", command=self.tasks_button_click,fg_color=Constants.MILK, font=(Constants.FONT, 25, "bold"), text_color=Constants.DARK_GREY, hover_color="#CBAC8A")
        self.tasks_button.pack(side="left", expand=True)
        self.house_button = ctk.CTkButton(self.frame, text="Renting", command=self.house_button_click,fg_color=Constants.MILK, font=(Constants.FONT, 25, "bold"), text_color=Constants.DARK_GREY, hover_color="#CBAC8A")
        self.house_button.pack(side="left", expand=True)
        self.jobs_button = ctk.CTkButton(self.frame, text="Jobs", command=self.jobs_button_click,fg_color=Constants.MILK, font=(Constants.FONT, 25, "bold"), text_color=Constants.DARK_GREY, hover_color="#CBAC8A")
        self.jobs_button.pack(side="left", expand=True)
        self.recipies_button = ctk.CTkButton(self.frame, text="Recipies", command=self.recipies_button_click,fg_color=Constants.MILK, font=(Constants.FONT, 25, "bold"), text_color=Constants.DARK_GREY, hover_color="#CBAC8A")
        self.recipies_button.pack(side="left",expand=True)
        
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
        self.switch_view(JobsView)
    
    def recipies_button_click(self):
        self.switch_view(CookingRecipesView)

class FinanceView:
    def __init__(self, parent):
        self.tracker = FinanceTracker()
        self.frame = ctk.CTkFrame(parent, fg_color=Constants.DARK_GREY)
        self.frame.pack_propagate(False)
        self.frame.pack(fill="both", expand=True)
        self.finance_table = ctk.CTkFrame(self.frame, width=700, fg_color=Constants.DARK_GREY)
        self.finance_table.pack_propagate(False)
        self.finance_table.pack(side="left", padx=10, pady=10, fill="y")
        self.add_finance_frame = ctk.CTkFrame(self.finance_table, height=50, fg_color=Constants.DARK_GREY, corner_radius=0)
        self.add_finance_frame.pack_propagate(False)
        self.add_finance_frame.pack(fill="x")
        self.selected_option = ctk.StringVar()
        self.categories_dropdown = ctk.CTkOptionMenu(self.add_finance_frame, variable=self.selected_option, values=Thing.OPTIONS_STR, fg_color=Constants.LIGHT_GREY, dropdown_text_color=Constants.MILK, button_color=Constants.LIGHT_GREY,button_hover_color=Constants.DARK_GREY, font=(Constants.FONT, 15, "bold"))
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
        self.add_button = ctk.CTkButton(self.add_finance_frame, text="+", command=self.add_button_press, fg_color=Constants.LIGHT_GREY, font=(Constants.FONT, 15, "bold"))
        self.add_button.pack(side="left", padx=10)
        self.finance_scroll_frame = ctk.CTkScrollableFrame(self.finance_table, fg_color=Constants.LIGHT_GREY)
        self.finance_scroll_frame.pack(fill="both", expand=True)
        
        self.pie_chart_frame = ctk.CTkFrame(self.frame, fg_color=Constants.ALTERNATE_GREY)
        self.pie_chart_frame.pack(side="left", fill="both", expand=True)
        year, month, _ = map(int, self.date_entry.get().split("-"))
        income = self.tracker.incomeThisMonth(year,month)
        expense = self.tracker.expenseSpecificMonth(year,month)
        self.pie_chart_title = ctk.CTkLabel(self.pie_chart_frame, text="Overview of the Month", font=("Segoe UI", 30, "bold"))
        self.income_month = ctk.CTkLabel(self.pie_chart_frame, text=f"Income for the month: ${income}", font=(Constants.FONT, 16, "bold"))
        self.spent_month = ctk.CTkLabel(self.pie_chart_frame, text=f"Expenses for the month: ${expense}", font=(Constants.FONT, 16, "bold"))
        self.pie_chart_title.pack(side="top")
        self.income_month.pack()
        self.spent_month.pack()
        self.pie_chart = PieChartApp(self.pie_chart_frame)
        self.pie_chart_frame.pack()
        
        self.date_frames = {}
        for year in self.tracker.finance_list.getYear():
            for month in self.tracker.finance_list.getMonth(year):
                for day in self.tracker.finance_list.getDay(year,month):
                    month_str = str(month).zfill(2)
                    day_str = str(day).zfill(2)
                    date = f"{year}-{month_str}-{day_str}"
                    for stuff in self.tracker.finance_list.getItem(year,month,day):
                        if date not in self.date_frames:
                            self.date_frames[date] = ctk.CTkFrame(self.finance_scroll_frame, fg_color=Constants.MILK)
                            self.date_frames[date].pack(side="top", fill="x", pady=5)
                            current_date_label = ctk.CTkLabel(self.date_frames[date],
                                                              text=f"{year}-{month}-{day}",
                                                              text_color=Constants.DARK_GREY,
                                                              font=(Constants.FONT, 20, "bold"))
                            current_date_label.pack(side="top")
                        finance_frame = ctk.CTkFrame(self.date_frames[date], height=35, fg_color="#6D5F50")
                        finance_frame.pack(fill="x", side="top", padx=5, pady=5)
                        category_text = ctk.CTkLabel(finance_frame, text=Thing.OPTIONS_STR[stuff.type],font=(Constants.FONT, 15, "bold"))
                        category_text.pack(side="left", padx=50)
                        name_text = ctk.CTkLabel(finance_frame, text=stuff.name,font=(Constants.FONT, 15, "bold"))
                        name_text.pack(side="left", expand=True)
                        amount_text = ctk.CTkLabel(finance_frame, text="$" + str(stuff.amount),font=(Constants.FONT, 15, "bold"))
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
            if self.date_entry.get() not in self.date_frames:
                print(self.date_entry.get(), self.date_frames)
                self.date_frames[self.date_entry.get()] = ctk.CTkFrame(self.finance_scroll_frame, fg_color=Constants.MILK)
                self.date_frames[self.date_entry.get()].pack(side="top", fill="x", pady=5)
                current_date_label = ctk.CTkLabel(self.date_frames[self.date_entry.get()],
                                                    text=f"{year}-{month}-{day}",
                                                    text_color=Constants.DARK_GREY,
                                                    font=(Constants.FONT, 20, "bold"))
                current_date_label.pack(side="top")
            finance_frame = ctk.CTkFrame(self.date_frames[self.date_entry.get()], height=35, fg_color="#6D5F50")
            finance_frame.pack(fill="x", side="top", padx=5, pady=5)
            category_text = ctk.CTkLabel(finance_frame, text=category,font=(Constants.FONT, 15, "bold"))
            category_text.pack(side="left", padx=50)
            name_text = ctk.CTkLabel(finance_frame, text=name,font=(Constants.FONT, 15, "bold"))
            name_text.pack(side="left", expand=True)
            amount_text = ctk.CTkLabel(finance_frame, text="$" + cost,font=(Constants.FONT, 15, "bold"))
            amount_text.pack(side="left", expand=True)
            
            self.tracker.put(name, float(cost), category, self.date_entry.get())
            income = self.tracker.incomeThisMonth(year, month)
            expense = self.tracker.expenseSpecificMonth(year, month)
            self.income_month.configure(text=f"Income for the month: ${income}")
            self.spent_month.configure(text=f"Expenses for the month: ${expense}")
            self.pie_chart.update_chart(self.tracker)
            
        
class TasksView:
    def __init__(self, root):
        self.get_images()
        self.buttons = []
        self.frame = ctk.CTkFrame(root, fg_color=Constants.DARK_GREY)
        self.frame.pack(expand=True, fill="both")
        self.todo_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.todo_frame.pack(side="left", expand=True, fill="both", padx=10)
        self.frame_dict = {}
        self.calendar_frame = ModernCalendar(self, self.frame)

        self.header_frame = ctk.CTkFrame(self.todo_frame,fg_color=Constants.DARK_GREY)
        self.header_frame.pack(side="top", fill="x", pady=10)
        self.task_entry = ctk.CTkEntry(
            self.header_frame, height=40, width=300, placeholder_text="Select a day", font=(Constants.FONT, 16, "bold"),
        )
        self.task_entry.pack(side="left",padx=10)

        self.add_button = ctk.CTkButton(
            self.header_frame, text="Add Task", width=200, height=40, font=(Constants.FONT, 16, "bold"), state="disabled", fg_color=Constants.MILK,
            text_color=Constants.DARK_BROWN,
            command=self.add_task
        )
        self.add_button.pack(side="left",padx=10)

        # Frame to hold all task items
        self.tasks_frame = ctk.CTkFrame(self.todo_frame, height=200, fg_color="#3C3D40")
        self.tasks_frame.pack(pady=10, fill="both", expand=True)
        
        self.frame_date = ctk.CTkLabel(self.tasks_frame, text="Pick a day",font=(Constants.FONT, 18, "bold"))
        self.frame_date.pack()

        self.clear_button = ctk.CTkButton(
            self.header_frame, text="Clear All", width=200, height=40, font=(Constants.FONT, 16, "bold"),
            fg_color=Constants.MILK,
            text_color=Constants.DARK_BROWN,
            command=self.clear_all_tasks
        )
        self.clear_button.pack(side="left", padx=10)
        
    def get_images(self):
        # Opens the images
        try:
            # Using .copy() keeps the image saved in memory so I don't have to keep opening the images to access them
            with Image.open(
                    "src/img/trash.png").copy() as trash_image:
                self.scaled_trash_image = ctk.CTkImage(trash_image, size=(50, 50))
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
            self.frame_date = ctk.CTkLabel(self.tasks_frame, text=f"Tasks for {selected_date}", font=(Constants.FONT, 18, "bold"), text_color=Constants.MILK)
            self.frame_date.pack(side="top")

        self.tasks_frame.pack(side="bottom", pady=10, fill="both", expand=True)
        self.clear_button.pack(pady=5)
        

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            # Create a container frame for the task
            task_frame = ctk.CTkFrame(self.tasks_frame, fg_color="transparent")
            task_frame.pack(fill="x", pady=2, padx=10)

            # Task checkbox on the left with a callback to toggle text color
            task_checkbox = ctk.CTkCheckBox(
                task_frame, text=task, font=(Constants.FONT, 15),
                text_color=Constants.MILK,
                command=lambda: self.toggle_task(task_checkbox)
            )
            task_checkbox.pack(side="left", padx=(10, 0))

            # Remove button on the right
            remove_button = ctk.CTkButton(
                task_frame, text="", fg_color="transparent", width=70, height=70, image=self.scaled_trash_image, hover_color="#FF6666",
                command=lambda: self.remove_task_item(task_frame)
            )
            self.buttons.append(remove_button)
            remove_button.pack(side="right", padx=(0, 10))

            self.task_entry.delete(0, ctk.END)
            
            self.frame_dict[self.calendar_frame.get_selected_date()] = self.tasks_frame
            self.calendar_frame.dot_update()

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
        self.switch_view(self.calendar_frame.get_selected_date())

class RentingView:
    def __init__(self,parent): 
        self.get_images()
        self.frame = CTkFrame(parent, fg_color=Constants.DARK_GREY)
        self.loading()
        parent.update_idletasks()
        self.frame.pack(fill="both", expand=True)
        self.scrolling_frame = ctk.CTkScrollableFrame(self.frame, fg_color=Constants.DARK_GREY)
        self.scrolling_frame.pack(fill="both", expand=True)
        self.rent_title = ctk.CTkLabel(self.scrolling_frame, text="Houses for rent near you", font=("Segoe UI", 30, "bold"))
        self.rent_title.pack(side="top", expand=True, fill="x")
        self.house_rows = []

        self.renter = RentFinder()
        house_list = self.renter.getHouses()
        count = 1
        self.current_house_row = ctk.CTkFrame(self.scrolling_frame, fg_color=Constants.DARK_GREY)
        for house in house_list:
            if count > 3:
                self.current_house_row.pack(padx=10, pady=10, expand=True, fill="x")
                self.current_house_row = ctk.CTkFrame(self.scrolling_frame, fg_color=Constants.DARK_GREY)
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
        self.loading_frame = ctk.CTkFrame(self.frame, width=self.frame.winfo_width()//2, height=self.frame.winfo_height()//2, fg_color=Constants.DARK_GREY)
        self.loading_frame.pack(fill="both", expand=True)
        self.loading_frame.pack_propagate(False)
        loading_frame_text = ctk.CTkLabel(self.loading_frame, text="Retrieving House Data...", font=(Constants.FONT, 100, "bold"), text_color=Constants.MILK)
        loading_frame_text.pack(expand=True, fill="both")
        
    def create_house(self, title, cost, address, link):
        house_frame = ctk.CTkFrame(self.current_house_row, width=400, height=400, fg_color=Constants.DARK_BROWN)
        house_frame.pack_propagate(False)
        house_cost = ctk.CTkLabel(house_frame, text=f"${cost}/month", font=(Constants.FONT, 20, "bold"), text_color=Constants.MILK)
        if cost is None:
            house_cost.configure(text="Inquire for price", font=(Constants.FONT, 20, "bold"))
        house_cost.pack(side="top", expand=True)
        house_img = ctk.CTkLabel(house_frame, text="", image=self.scaled_house_image, fg_color="transparent")
        house_img.pack(side="top", expand=True)
        house_title = ctk.CTkLabel(house_frame, text=f"{title}",font=(Constants.FONT, 14, "bold"),text_color=Constants.MILK)
        house_title.pack(side="top", expand=True)
        house_address = ctk.CTkLabel(house_frame, text=f"{address}", font=(Constants.FONT, 13),text_color=Constants.MILK)
        house_address.pack(side="top", expand=True)
        house_link = ctk.CTkLabel(house_frame, text="View more information", font=(Constants.FONT, 16, "underline"), text_color=Constants.LIGHT_GREY, cursor="hand2")
        house_link.bind("<Button-1>", lambda e: self.callback(link))
        house_link.pack(side="top", expand=True)
        house_frame.pack(side="left", expand=True, padx=10)
        
class JobsView:
    def __init__(self, root):
        self.frame = ctk.CTkFrame(root)
        self.frame.pack(expand=True, fill="both")
        
        root.update_idletasks()
        self.loading()
        root.update_idletasks()
        
        self.scroll_frame = ctk.CTkScrollableFrame(self.frame, fg_color=Constants.DARK_GREY)
        self.scroll_frame.pack(expand=True, fill="both")
        self.header = ctk.CTkLabel(self.scroll_frame, text="Job Postings Near You", font=(Constants.FONT, 40, "bold"))

        root.update_idletasks()
        self.header.pack(side="top", expand=True, pady=10)

        self.job_list_frame = ctk.CTkFrame(self.scroll_frame,fg_color=Constants.DARK_GREY)
        self.job_list_frame.pack(fill="x", padx=20)

        self.job_finder = JobFinder()

        self.display_jobs(self.job_finder.jobs)

        self.loading_frame.destroy()

    def loading(self):
        self.loading_frame = ctk.CTkFrame(self.frame, width=self.frame.winfo_width() // 2,
                                          height=self.frame.winfo_height() // 2,
                                          fg_color=Constants.DARK_GREY)
        self.loading_frame.pack_propagate(False)
        self.loading_frame.pack(fill="both", expand=True)
        loading_frame_text = ctk.CTkLabel(self.loading_frame, text="Retrieving Job Info...",
                                          font=(Constants.FONT, 100, "bold"),text_color=Constants.MILK)
        loading_frame_text.pack(expand=True, fill="both")

    def open_link(self, url):
        webbrowser.open(url)

    def display_jobs(self, job_data):
        if not job_data:
            no_job_label = ctk.CTkLabel(self.job_list_frame, text="No jobs found.", font=(Constants.FONT, 14))
            no_job_label.pack(pady=20)
            return

        for job in job_data:
            job_frame = ctk.CTkFrame(self.job_list_frame, border_width=2, corner_radius=8, fg_color=Constants.DARK_BROWN)
            job_frame.pack(fill="x", pady=10, padx=10)
            job_title = job.title
            company = job.company
            location = 'No location'
            date_posted = job.date
            salary = 'Not specified'
            link = job.link
            job_description = job.desc

            title_label = ctk.CTkLabel(job_frame, text=f"{job_title}", font=(Constants.FONT, 24, "bold"))
            title_label.pack(anchor="w", padx=10, pady=5)
            company_label = ctk.CTkLabel(job_frame, text=f"{company}", font=(Constants.FONT, 16,"bold"))
            company_label.pack(anchor="w", padx=10, pady=5)
            location_label = ctk.CTkLabel(job_frame, text=f"{location}", font=(Constants.FONT, 14,))
            location_label.pack(anchor="w", padx=10, pady=5)
            date_posted_label = ctk.CTkLabel(job_frame, text=f"{date_posted}", font=(Constants.FONT, 14,))
            date_posted_label.pack(anchor="w", padx=10, pady=5)
            salary_label = ctk.CTkLabel(job_frame, text=f"Salary: {salary}", font=(Constants.FONT, 14,))
            salary_label.pack(anchor="w", padx=10, pady=5)



            if link:
                link_label = ctk.CTkLabel(job_frame, text="Click here to view job", font=("Arial", 16, "underline"),
                                          text_color="#ADD8E6", cursor="hand2")
                link_label.pack(anchor="w", padx=10, pady=5)
                link_label.bind("<Button-1>", lambda e, url=link: self.open_link(url))


class RecipeViewer:
    def __init__(self, cooking_class, root, title, country, ingredients, recipes, difficulty, foods):
        self.frame = ctk.CTkFrame(root)
        self.frame.pack(expand=True, fill="both")
        self.cooking_class = cooking_class  # Large default window
        self.frame.configure(fg_color=Constants.DARK_GREY)  # Dark background
        self.difficulty = difficulty
        # Store parameters
        self.country = country  # Country of origin
        self.ingredients = ingredients  # List of ingredients
        self.recipes = recipes  # List of recipes
        self.foods = foods
        
        self.title = title

        # Create the title label at the top
        self.create_title()

        self.create_country_box()

        self.create_content_frame()

    def create_title(self):
        """Creates the centered title at the top."""
        self.title_label = ctk.CTkLabel(
            self.frame,
            text=f"{self.title}",
            font=(Constants.FONT, 50, "bold"),  # Large title font
            text_color=Constants.MILK
        )
        self.title_label.pack(pady=20)  # Space below the title

    def create_country_box(self):
        """Creates a country display box in the top-right corner."""
        country_frame = ctk.CTkFrame(self.frame, fg_color=Constants.DARK_BROWN, corner_radius=10, width=220,
                                     height=60)  # ✅ Wider box
        country_frame.place(relx=0.85, rely=0.05, anchor="ne")  # ✅ Position stays the same

        # Create a frame inside for horizontal layout
        inner_frame = ctk.CTkFrame(country_frame, fg_color="transparent")
        inner_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # "Country:" label
        country_label = ctk.CTkLabel(
            inner_frame,
            text="Country:",
            font=(Constants.FONT, 16, "bold"),
            text_color=Constants.MILK
        )
        country_label.pack(side="left", padx=5)  # ✅ Align to the left

        # Country name label (aligned horizontally)
        country_name_label = ctk.CTkLabel(
            inner_frame,
            text=self.country,
            font=(Constants.FONT, 18, "bold"),
            text_color="#FDFCF9"
        )
        country_name_label.pack(side="left", padx=5)  # ✅ Aligned next to "Country:"

    def create_content_frame(self):
        """Creates the main frame that contains Ingredients and Recipes."""
        # Main content frame
        content_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=20, pady=(20, 80))  # Added bottom padding for back button

        # Left Side: Ingredients
        self.create_ingredients_section(content_frame)

        # Vertical Divider Line
        divider = ctk.CTkFrame(content_frame, fg_color="white", width=2)
        divider.pack(side="left", fill="y", padx=10)

        # Right Side: Recipes
        self.create_recipes_section(content_frame)

        # Back Button Frame
        button_frame = ctk.CTkFrame(self.frame, fg_color="#C4A484", height=60)
        button_frame.pack(side="bottom", fill="x")
        button_frame.pack_propagate(False)  # Prevent frame from shrinking

        back_button = ctk.CTkButton(
            button_frame,
            text="Back",
            font=(Constants.FONT, 30, "bold"),
            fg_color=Constants.MILK,
            text_color=Constants.LIGHT_GREY,
            hover_color=Constants.DARK_GREY,
            corner_radius=10,
            command=lambda: self.cooking_class.create_recipe_page(self.difficulty, self.foods)
        )
        back_button.pack(side="right", padx=20, pady=10)

    def create_ingredients_section(self, parent):
        """Creates the Ingredients box with scrollbar on the left side."""
        # Container frame for ingredients
        ingredients_container = ctk.CTkFrame(parent, fg_color="transparent")
        ingredients_container.pack(side="left", expand=True, fill="both", padx=10, pady=10)

        # Title for Ingredients
        ingredients_title = ctk.CTkLabel(
            ingredients_container,
            text="Ingredients",
            font=(Constants.FONT, 30, "bold"),
            text_color=Constants.MILK
        )
        ingredients_title.pack(pady=10, fill="x")

        # Create scrollable frame for ingredients
        ingredients_scroll = ctk.CTkScrollableFrame(
            ingredients_container,
            fg_color=Constants.DARK_BROWN,
            corner_radius=10,
            orientation="vertical"
        )
        ingredients_scroll.pack(expand=True, fill="both")

        # Display each ingredient inside the scrollable frame
        for ingredient in self.ingredients:
            label = ctk.CTkLabel(
                ingredients_scroll,
                text=f"- {ingredient}",
                font=(Constants.FONT, 18),
                text_color=Constants.MILK,
                wraplength=400  # Increased wraplength for full width
            )
            label.pack(anchor="w", padx=20, pady=2, fill="x")

    def create_recipes_section(self, parent):
        """Creates the Recipes box with scrollbar on the right side."""
        # Container frame for recipes
        recipes_container = ctk.CTkFrame(parent, fg_color="transparent")
        recipes_container.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        # Title for Recipes
        recipes_title = ctk.CTkLabel(
            recipes_container,
            text="Instructions",
            font=(Constants.FONT, 30, "bold"),
            text_color=Constants.MILK
        )
        recipes_title.pack(pady=10, fill="x")

        # Create scrollable frame for recipes
        recipes_scroll = ctk.CTkScrollableFrame(
            recipes_container,
            fg_color=Constants.DARK_BROWN,
            corner_radius=10,
            orientation="vertical"
        )
        recipes_scroll.pack(expand=True, fill="both")

        # Display each recipe step inside the scrollable frame
        for recipe in self.recipes.split("\n"):
            label = ctk.CTkLabel(
                recipes_scroll,
                text=f"- {recipe}",
                font=(Constants.FONT, 18),
                text_color=Constants.MILK,
                wraplength=400  # Increased wraplength for full width
            )
            label.pack(anchor="w", padx=20, pady=2, fill="x")

class CookingRecipesView:
    def __init__(self, root):
        self.frame = ctk.CTkFrame(root)
        self.frame.pack(expand=True, fill="both")
        
        root.update_idletasks()
        self.loading()
        root.update_idletasks()
        
        self.recipe_generator = Recipes()
        self.main_menu()
        
        self.loading_frame.destroy()
    
    def loading(self):
        self.loading_frame = ctk.CTkFrame(self.frame, width=self.frame.winfo_width()//2, height=self.frame.winfo_height()//2)
        self.loading_frame.pack(fill="both", expand=True)
        self.loading_frame.pack_propagate(False)
        loading_frame_text = ctk.CTkLabel(self.loading_frame, text="Retrieving Recipe Data...", font=("Arial", 100, "bold"))
        loading_frame_text.pack(expand=True, fill="both")
    
    def main_menu(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        label = ctk.CTkLabel(self.frame, text="Cooking Recipes", font=("Segoe UI", 60, "bold"))
        label.pack(pady=30)

        button1 = ctk.CTkButton(self.frame, text="Easy", width=300, height=300, corner_radius=50,
                                command=self.easy_recipes,
                                fg_color=Constants.LIGHT_GREY, font=(Constants.FONT, 40, "bold"), hover_color="#4F7942")
        button1.pack(side="left", padx=10, expand=True)

        button2 = ctk.CTkButton(self.frame, text="Medium", width=300, height=300, corner_radius=50,
                                command=self.medium_recipes,
                                fg_color=Constants.DARK_GREY, font=(Constants.FONT, 40, "bold"), hover_color="#CC7722")
        button2.pack(side="left", padx=10, expand=True)

        button3 = ctk.CTkButton(self.frame, text="Hard", width=300, height=300, corner_radius=50,
                                command=self.hard_recipes,
                                fg_color="#40382E", font=(Constants.FONT, 40, "bold"), hover_color="#800000")
        button3.pack(side="left", padx=10, expand=True)

    def create_recipe_page(self, difficulty, food_names):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.recipe_frame = ctk.CTkFrame(self.frame)
        self.recipe_frame.pack(expand=True, fill="both")
        self.diff = difficulty
        self.foods = food_names
        label = ctk.CTkLabel(self.recipe_frame, text=f"{difficulty} Recipes", font=(Constants.FONT, 50, "bold"), text_color="#D9CDBF")
        label.pack(pady=20)

        for food in food_names:
            frame = ctk.CTkFrame(self.recipe_frame, fg_color="transparent")
            frame.pack(pady=10)

            button = ctk.CTkButton(frame, text=food.name, font=(Constants.FONT, 30, "bold"), fg_color="#4C4F52",
                                   hover_color="#676A6D",
                                   corner_radius=15, text_color=Constants.LIGHT_GREY,
                                   command=lambda f=food: self.food_clicked(f))
            button.pack(side="left", padx=20, expand=True)
            
            isFav = food.isFavorite()
            star_var = ctk.StringVar(value="☆" if not isFav else "★")

            def toggle_star(f=food, var=star_var):
                isFav = f.isFavorite()
                if(isFav):
                    f.unFavorite()
                else:
                    f.favorite()
                var.set("★" if not isFav else "☆")

            star_button = ctk.CTkButton(frame, textvariable=star_var, font=("Segoe UI", 40),
                                        fg_color="transparent", text_color="yellow", hover_color="#676A6D",
                                        command=toggle_star)
            star_button.pack(side="right", padx=20, expand=True)

        hotbar_frame = ctk.CTkFrame(self.recipe_frame, fg_color="#C4A484")
        hotbar_frame.pack(side="bottom", fill="x")

        refresh_button = ctk.CTkButton(hotbar_frame, text="Refresh", font=("Segoe UI", 30, "bold"), fg_color="#F2EBDC",
                                       hover_color="#D9CDBF", corner_radius=10,
                                       text_color=Constants.DARK_GREY,
                                       command=lambda: print("Refresh clicked!"))
        refresh_button.pack(side="left", pady=5, expand=True)

        back_button = ctk.CTkButton(hotbar_frame, text="Back", font=("Segoe UI", 30, "bold"), fg_color="#D9CDBF",
                                    hover_color="#C19A6B", corner_radius=10,
                                    text_color=Constants.DARK_GREY,
                                    command=self.main_menu)
        back_button.pack(side="right", pady=5, expand=True)

    def food_clicked(self, food):
        for widget in self.frame.winfo_children():
            widget.destroy()
        RecipeViewer(self, self.frame,  food.name, food.country, food.ingredients, food.instructions,self.diff, self.foods)

    def easy_recipes(self):
        self.create_recipe_page("Easy", self.recipe_generator.getEasy())

    def medium_recipes(self):
        self.create_recipe_page("Medium", self.recipe_generator.getMedium())

    def hard_recipes(self):
        self.create_recipe_page("Hard",  self.recipe_generator.getHard())


class ModernCalendar:
    def __init__(self, task_class, parent, event_callback=None, year=None, month=None):
        self.event_callback = event_callback
        self.parent = parent
        self.task_class = task_class
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.frame.pack(side="right", fill="both", padx=20, pady=10)
        self.calendar_frame = ctk.CTkFrame(self.frame, fg_color=Constants.LIGHT_GREY)
        self.calendar_frame.pack(side="right", expand=True)
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
        self.buttons_frame = ctk.CTkFrame(self.calendar_frame, fg_color="transparent")
        self.buttons_frame.pack(pady=(5, 10))

    def create_header(self):
        self.header_frame = ctk.CTkFrame(self.calendar_frame, fg_color="#D9CDBF")
        self.header_frame.pack(fill="x", pady=10)

        self.prev_button = ctk.CTkButton(
            self.header_frame, text="◀", width=30, fg_color="#8C877D",
            command=self.prev_month, font=("Segoe UI", 14, "bold")
        )
        self.prev_button.pack(side="left", padx=10, pady=5)

        self.month_label = ctk.CTkLabel(
            self.header_frame, text="", font=("Segoe UI", 16, "bold"),
            fg_color="transparent", text_color="black"
        )
        self.month_label.pack(side="left", expand=True)

        self.next_button = ctk.CTkButton(
            self.header_frame, text="▶", width=30, fg_color="#8C877D",
            command=self.next_month, font=("Segoe UI", 14, "bold")
        )
        self.next_button.pack(side="right", padx=10, pady=5)

    def create_day_labels(self):
        self.days_frame = ctk.CTkFrame(self.calendar_frame, fg_color="transparent")
        self.days_frame.pack()
        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

        for day in days:
            lbl = ctk.CTkLabel(
                self.days_frame, text=day, font=("Segoe UI", 11, "bold"),
                fg_color="transparent", text_color="#D9CDBF"
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

        for index, (cell_date, in_current) in enumerate(day_cells):
            r, c = divmod(index, 7)
            
            btn_fg = "#2c3e50" if in_current  else "#bdc3c7"
            btn_bg = "#CBAC8A" if self.selected_date == cell_date else "#ffffff"
            if cell_date in self.buttons_with_tasks:
                btn_bg="#E5D6C0"
            btn = ctk.CTkButton(
                self.buttons_frame, text=str(cell_date.day),
                font=("Segoe UI", 12, "bold"),
                fg_color=btn_bg, text_color=btn_fg, width=40, height=40,
                command=lambda d=cell_date: self.on_day_click(d),
                hover_color="#D9CDBF"
            )
            btn.grid(row=r, column=c, padx=5, pady=5)

    def on_day_click(self, cell_date):
        self.selected_date = cell_date
        self.task_class.switch_view(self.selected_date)
        self.task_class.task_entry.configure(placeholder_text="Enter the task")
        self.task_class.add_button.configure(state="normal")
        self.task_class.frame.focus_set()
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
# Data models (like APIs) and logic go here
# "models.py is responsible for interacting with data, whether it's from a database, file, or an external API."

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PieChartApp:
    def __init__(self, root):
        self.root = root
        
        
        self.labels = []
        self.sizes = []

        self.dark_theme_colors = [
            '#3B5D50', '#7D8F69', '#D4C8BE', '#A68A64', '#5C6D70', '#B22222', '#C2A878'
        ]

        if len(self.labels) > len(self.dark_theme_colors):
            raise ValueError("Not enough colors in the dark_theme_colors list.")

        self.fig = Figure(figsize=(15, 10), dpi=100, facecolor="#3C3D40")
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.draw_pie_chart()

    def draw_pie_chart(self):
        self.ax.clear()

        colors_to_use = self.select_colors(len(self.sizes))
        print(self.labels)
        print(self.sizes)
        self.ax.pie(self.sizes, labels=self.labels, autopct='%1.1f%%', colors=colors_to_use, startangle=90, textprops={'fontsize':20, 'color':'white'})
        self.ax.axis('equal')

        self.canvas.get_tk_widget().config(bg="black")

        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="left")

    def select_colors(self, num_colors):
        return self.dark_theme_colors[:num_colors]
    
    def update_chart(self, tracker):
        dic = tracker.portionCategory()
        self.labels = list(dic.keys())
        self.sizes = [dic[label] for label in self.labels]
        self.draw_pie_chart()

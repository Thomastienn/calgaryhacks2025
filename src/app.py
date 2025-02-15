# Initializes the main application
# Manages the app's core logic and flow

from src.views import MainView
from src.models import API

class App:
    def __init__(self):
        MainView()
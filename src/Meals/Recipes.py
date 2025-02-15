import requests
import json
class Recipes:
    def __init__(self):
        self.link = "https://www.themealdb.com/api/json/v1/1/random.php"
        
    def getMeal(self):
        return json.loads(requests.get(self.link).content)["meals"][0]
    
a = Recipes()
print(a.getMeal())
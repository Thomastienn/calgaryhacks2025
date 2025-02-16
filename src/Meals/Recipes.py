import requests
import json
from Food import Food
class Recipes:
    TOTAL_MEALS = 15
    EACH = TOTAL_MEALS//3
    def __init__(self):
        self.link = "https://www.themealdb.com/api/json/v1/1/random.php"
        self.meals = []
        self.initializeMeals()
        
    def getMeal(self):
        return json.loads(requests.get(self.link).content)["meals"][0]
    
    def initializeMeals(self):
        for _ in range(self.TOTAL_MEALS):
            meal = self.getMeal()
            ingre = []
            for key in meal:
                if "Ingredient" in key and meal[key]:
                    ingre.append(meal[key])
            my_meal = Food(id=int(meal["idMeal"]), name=meal["strMeal"], \
                        country=meal["strArea"], instructions=meal["strInstructions"], ingredients=ingre)
            self.meals.append(my_meal)
        self.meals.sort(key=lambda meal: len(meal.ingredients))
            
    def getEasy(self):
        assert self.meals, "No meals"
        return self.meals[:self.EACH]

    def getMedium(self):
        assert self.meals, "No meals"
        return self.meals[self.EACH: self.EACH*2]

    def getHard(self):
        assert self.meals, "No meals"
        return self.meals[-self.EACH:]

    
# a = Recipes()

# print(a.getEasy())
# print(a.getMedium())
# print(a.getHard())

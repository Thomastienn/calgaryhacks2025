import os
import requests
import json
from src.Meals.Food import Food
import pickle
class Recipes:
    TOTAL_MEALS = 15
    EACH = TOTAL_MEALS//3
    NUM_INGREDIENT_WEIGHT = 0.6
    NUM_STEPS_WEIGHT = 1-NUM_INGREDIENT_WEIGHT
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
        self.meals.sort(key=lambda meal: self.NUM_INGREDIENT_WEIGHT*len(meal.ingredients) + self.NUM_STEPS_WEIGHT*meal.instructions.count("\n"))
            
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

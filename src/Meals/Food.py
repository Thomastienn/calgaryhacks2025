import pickle
import os
class Food:
    FAVFOOD_DIR = "src/Databases/favorite_food.pkl"
    def __init__(self, id: int, name: str, country: str, instructions: str, ingredients: list):
        self.id = id
        self.name = name
        self.country = country
        self.instructions = instructions
        self.ingredients = ingredients
        
    def __hash__(self):
        return self.id
        
    def favorite(self):
        current = set()
        if os.path.exists(self.FAVFOOD_DIR):
            with open(self.FAVFOOD_DIR, "rb") as inp:
                try:
                    current = pickle.load(inp)
                except:
                    pass
        current.add(self.__hash__())
        with open(self.FAVFOOD_DIR, "wb") as out:
            pickle.dump(current,out,pickle.HIGHEST_PROTOCOL)
    
    def unFavorite(self):
        current = set()
        if os.path.exists(self.FAVFOOD_DIR):
            with open(self.FAVFOOD_DIR, "rb") as inp:
                current = pickle.load(inp)
        if current:
            current.discard(self.__hash__())
            with open(self.FAVFOOD_DIR, "wb") as out:
                pickle.dump(current,out,pickle.HIGHEST_PROTOCOL)
                
    def isFavorite(self):
        if os.path.exists(self.FAVFOOD_DIR):
            with open(self.FAVFOOD_DIR, "rb") as inp:
                current = pickle.load(inp)
                if self.__hash__() in current:
                    return True
        return False
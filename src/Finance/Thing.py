class Thing:
    GROCERY = 0
    INCOME = 1
    RENT = 2
    FOOD = 3
    SAVINGS = 4
    LEISURE = 5
    INVESTMENT = 6
    EMERGENCY_FUND = 7
    ESSENTIAL = {GROCERY, RENT, FOOD, SAVINGS, INVESTMENT, EMERGENCY_FUND}
    def __init__(self, name, amount,type):
        self.name = name
        self.amount = amount
        self.type = type
        
    def getAmount(self):
        return self.amount
    
    def isEssential(self) -> bool:
        return self.type in self.ESSENTIAL
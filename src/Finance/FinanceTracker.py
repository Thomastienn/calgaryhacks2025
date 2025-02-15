from datetime import datetime
from Thing import Thing
class FinanceTracker:
    def __init__(self):
        self.finance_list = {}
    def put(self, thing: str, money: float, category: int) -> None:
        year,month,day = map(int, datetime.now().date().split("-"))
        if year not in self.finance_list:
            self.finance_list[year] = {}
        if month not in self.finance_list[year]:
            self.finance_list[month] = {}
        if day not in self.finance_list[year][month]:
            self.finance_list[year][month][day] = {}
            self.finance_list[year][month][day] = []
        self.finance_list[year][month][day].append(Thing(name=thing, amount=money,type=category))
    def getAll(self) -> dict: 
        return self.finance_list
    
    def expenseSpecificDay(self, year:int, month:int, day:int) -> float:
        total = 0
        for stuff in self.finance_list[year][month][day]:
            if stuff.isEssential():
                total += stuff.getAmount()
        return total
    
    def expenseSpecificMonth(self, year:int, month: int) -> float:
        total = 0
        for day in self.finance_list[year][month]:
            total += self.expenseSpecificDay(year, month, day)
        return total
    def expenseSpecificYear(self, year:int) -> float:
        total = 0
        for month in self.finance_list[year]:
            total += self.expenseSpecificMonth(year, month)
        return total
    
    def incomeThisMonth(self, year:int, month:int) -> float:
        total = 0
        for day in self.finance_list[year][month]:
            for stuff in self.finance_list[year][month][day]:
                if stuff.type == Thing.INCOME:
                    total += stuff.getAmount()
        return total
        
    def incomeThisYear(self, year:int) -> float:
        total = 0
        for month in self.finance_list[year]:
            total += self.incomeThisMonth(year, month)
        return total

                

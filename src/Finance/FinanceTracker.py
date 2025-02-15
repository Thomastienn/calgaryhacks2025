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
    def expenseSpecificMonth(self, year:int, month: int) -> float:
        this_month = self.finance_list[year][month]
        total = 0
        for day in this_month:
            for stuff in day:
                if stuff.isEssential():
                    total += stuff.getAmount()
        return total

                

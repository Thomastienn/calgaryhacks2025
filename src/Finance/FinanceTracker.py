from datetime import datetime
from src.Finance.Thing import Thing
from src.Finance.FinanceDict import FinanceDict
class FinanceTracker:
    def __init__(self):
        self.finance_list = FinanceDict()
    def put(self, thing: str, money: float, category: str) -> None:
        year,month,day = map(int, str(datetime.now().date()).split("-"))
        item = Thing(name=thing, amount=money,type=Thing.OPTIONS_STR.index(category))
        self.finance_list.addItem(year,month,day,item)
    
    def getThingsDate(self, year: int, month: int, day: int) -> list[Thing]:
        return self.finance_list.d[year][month][day]
    
    def getThingsToday(self) -> list[Thing]:
        year,month,day = map(int, str(datetime.now().date()).split("-"))
        return self.getThingsDate(year,month,day)
    def expenseSpecificDay(self, year:int, month:int, day:int) -> float:
        total = 0
        for stuff in self.finance_list.getItem(year, month, day):
            if stuff.isEssential():
                total += stuff.getAmount()
        return total
    
    def expenseSpecificMonth(self, year:int, month: int) -> float:
        total = 0
        for day in self.finance_list.getDay(year, month):
            total += self.expenseSpecificDay(year, month, day)
        return total
    def expenseSpecificYear(self, year:int) -> float:
        total = 0
        for month in self.finance_list.getMonth(year):
            total += self.expenseSpecificMonth(year, month)
        return total
    
    def incomeThisMonth(self, year:int, month:int) -> float:
        total = 0
        for stuff in self.finance_list.getItemAllDay(year, month):
            if stuff.type == Thing.INCOME:
                total += stuff.getAmount()
        return total
        
    def incomeThisYear(self, year:int) -> float:
        total = 0
        for month in self.finance_list.getMonth(year):
            total += self.incomeThisMonth(year, month)
        return total


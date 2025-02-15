from datetime import datetime
from Thing import Thing
from FinanceDict import FinanceDict
class FinanceTracker:
    def __init__(self):
        self.finance_list = FinanceDict()
    def put(self, thing: str, money: float, category: int) -> None:
        year,month,day = map(int, datetime.now().date().split("-"))
        item = Thing(name=thing, amount=money,type=category)
        self.finance_list.addItem(year,month,day,item)
        
    
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

                

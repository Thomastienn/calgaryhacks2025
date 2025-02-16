from datetime import datetime
from src.Finance.Thing import Thing
from src.Finance.FinanceDict import FinanceDict
import os
import pickle

DATABASE_VIEW_DIR = "src/Databases/finance_track_view.pkl"
class FinanceTracker:
    DATABASE_DIR = "src/Databases/finance_track.pkl"
    def __init__(self, fin_list=None):
        if fin_list is None:
            self.finance_list = FinanceDict()
            if os.path.exists(self.DATABASE_DIR):
                with open(self.DATABASE_DIR, "rb") as inp:
                    self.finance_list = pickle.load(inp)
        else:
            self.finance_list = fin_list
    def put(self, thing: str, money: float, category: str, date:str=None) -> None:
        # date: yyyy-mm-dd
        dat = date
        if date == None:
            dat = str(datetime.now().date())
        year,month,day = map(int, dat.split("-"))
        item = Thing(name=thing, amount=money,type=Thing.OPTIONS_STR.index(category))
        self.finance_list.addItem(year,month,day,item)
        with open(self.DATABASE_DIR, "wb") as out:
            pickle.dump(self.finance_list, out, pickle.HIGHEST_PROTOCOL)        
        
    def dateEmpty(self, year: int, month:int, day:int) -> bool:
        return self.finance_list.emptyDate(year,month,day)
    
    def getThingsDate(self, year: int, month: int, day: int) -> list[Thing]:
        return self.finance_list.d[year][month][day]
    
    def getThingsToday(self) -> list[Thing]:
        year,month,day = map(int, str(datetime.now().date()).split("-"))
        return self.getThingsDate(year,month,day)
    
    def getAllThings(self):
        yield from self.finance_list.allItem()

    def expenseSpecificDay(self, year:int, month:int, day:int) -> float:
        total = 0
        for stuff in self.finance_list.getItem(year, month, day):
            if stuff.isExpenses():
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
    
    def totalThisMonth(self, year:int, month:int) -> float:
        total = 0
        for stuff in self.finance_list.getItemAllDay(year, month):
            total += stuff.getAmount()
        return total

    def essensialThisMonth(self, year:int, month:int) -> float:
        total_ess = 0
        total_non = 0
        for stuff in self.finance_list.getItemAllDay(year, month):
            if stuff.isEssential():
                total_ess += stuff.getAmount()
            else:
                total_non += stuff.getAmount()
        return total_ess, total_non
        
    
    def essensialThisYear(self, year:int) -> float:
        total_ess = 0
        total_non = 0
        for month in self.finance_list.getMonth(year):
            total_ess_month, total_non_month = self.essensialThisMonth(year, month)
            total_ess += total_ess_month
            total_non += total_non_month
        return total_ess, total_non
    
    def portionCategory(self) -> dict:
        year,_,_ = map(int, str(datetime.now().date()).split("-"))
        ans = {}
        for stuff in self.finance_list.getItemAllMonth(year):
            type_str = Thing.OPTIONS_STR[stuff.type]
            if type_str not in ans:
                ans[type_str] = 0
            ans[type_str] += stuff.getAmount()
        return ans
    
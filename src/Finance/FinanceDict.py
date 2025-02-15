from Thing import Thing
class FinanceDict:
    def __init__(self):
        self.d = {}
        
    def addItem(self, year: int, month: int, day: int, item: Thing):
        if year not in self.d:
            self.d[year] = {}
        if month not in self.d[year]:
            self.d[year][month] = {}
        if day not in self.d[year][month]:
            self.d[year][month][day] = []
        self.d[year][month][day].append(item)
        
    def getYear(self):
        for year in self.d:
            yield year
    def getMonth(self, year:int):
        for month in self.d[year]:
            yield month
    
    def getDay(self, year:int, month:int):
        for day in self.d[year][month]:
            yield day
    
    def getItem(self,year:int, month:int, day:int):
        for stuff in self.d[year][month][day]:
            yield stuff
            
    def getItemAllDay(self, year:int, month:int):
        for day in self.getDay(year,month):
            for stuff in self.getItem(year,month,day):
                yield stuff
    
    def getItemAllMonth(self, year: int):
        for month in self.getMonth(year):
            yield from self.getItemAllDay(year, month)
            
    def allItem(self):
        for year in self.getYear():
            yield from self.getItemAllMonth(year)
            
    def emptyDate(self, year:int, month:int, day:int)->bool:
        if year not in self.d:
            return True
        if month not in self.d[year]:
            return True
        return not(day in self.d[year][month])
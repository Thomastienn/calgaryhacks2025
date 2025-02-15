class FinanceTracker:
    def __init__(self):
        self.finance_list = {}
    def put(self, thing: str, money: float) -> None:
        self.finance_list[thing] = money
    def getAll(self) -> dict: 
        return self.finance_list
    
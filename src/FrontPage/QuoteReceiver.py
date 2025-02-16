import requests
import json
from Quote import Quote
class QuoteReceiver:
    def __init__(self):
        self.LINK = "https://qapi.vercel.app/api/random"
        
    def getQuote(self):
        data = json.loads(requests.get(self.LINK).text)
        return Quote(desc=data["quote"], author=data["author"])
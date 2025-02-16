from bs4 import BeautifulSoup
import requests
from House import House
class RentFinder:
    def __init__(self):
        self.LINK = "https://www.kijiji.ca/b-apartments-condos/calgary/c37l1700199"
        self.page = None
        self.soup = None
        self.houses = []
        self.refresh()
        
    def refresh(self):
        self.request()
        self.parseHouses()
        
    def request(self):
        self.page = requests.get(self.LINK)
        self.soup = BeautifulSoup(self.page.content, "html.parser")
    
    def getHouses(self) -> list:
        return self.houses
    
    def parseHouses(self) -> None:
        if self.soup == None:
            assert False, "Haven't request"
        cards = self.soup.find_all("section", {"data-testid": "listing-card"})
        for card in cards:
            price = card.find("p", {"data-testid": "listing-price"}).text
            if "$" == price[0]:
                price = float(price[1:].replace(",", ""))
            else:
                price = None
            link_tag = card.find("a", {"data-testid": "listing-link"})
            title = link_tag.text
            link = link_tag.get("href")
            address = card.find("li", {"aria-label": "Nearest intersection"}).find("p").text
            # house = House(title=title, cost=price, address=)            
            # self.houses.
            print(address)
            
            
# a = RentFinder()
# a.getHouses()
from bs4 import BeautifulSoup
import requests
from src.Job.Job import Job
class JobFinder:
    def __init__(self):
        self.LINK = "https://www.part-time.ca/search-jobs/alberta/calgary/?sort_order=2"
        self.page = None
        self.soup = None
        self.jobs = []
        self.refresh()
    
    def refresh(self):
        self.request()
        self.getJobs()
        
    def request(self):
        self.page = requests.get(self.LINK)
        self.soup = BeautifulSoup(self.page.content, "html.parser")
    
    def getJobs(self):
        if self.soup == None:
            assert False, "Haven't request"
        divs = self.soup.find_all("div", class_="details-wrapper")
        for div in divs:
            offer_detail = div.find("div", class_="offer-details")
            date = offer_detail.find("a", class_="date").text.strip()
            title_desc = offer_detail.find("a", class_="offer-name").text.strip().split("\n")
            title = title_desc[0].strip()
            company = div.find("a", class_="company").text.strip()
            link = div.find("a", class_="offer-name").get("href")
            desc = title_desc[-1].strip()
            job = Job(title,date,company,link, desc)
            self.jobs.append(job)
            
from bs4 import BeautifulSoup
from core.SearchEngine.Search import RequestDispatcher, Aljazeera
import threading
import queue
from core.TelegramBot.TelegramSender import SendToChannel
from core.appConfig import AppConfigurations
config = AppConfigurations()

class FindData(RequestDispatcher):
    def __init__(self, language):
        self.language = language

    def extractData(self, link) -> tuple:
        """method to extract title and tag"""
        try:
            if self.language == 'ar':
                text = self.MakeRequest(target=link)
                soup = BeautifulSoup(text, 'html.parser')
                title = soup.findAll("header", {"class": "article-header"})[0].h1.text
                category = soup.findAll("div", {"class": "topics"})[0].text
                published_date = soup.findAll("span", {"class": "article-dates__published"})[0].text
                print("Title: {}\nCategory: {}\nPublished Date: {}\nSource: @Aljazeera".format(title, category,
                                                                                               published_date))
                SendToChannel(title, published_date, category, link)
                return title, category
            else:
                text = self.MakeRequest(target=link)
                soup = BeautifulSoup(text, 'html.parser')
                title = soup.findAll("h1")[0].text
                category = soup.findAll("div", {"class": "topics"})[0].text
                published_date = soup.findAll("div", {"class": "date-simple"})[0].text
                print("Title: {}\nCategory: {}\nPublished Date: {}\nSource: @Aljazeera".format(title, category,
                                                                                   published_date))
                # SendToChannel(title, published_date, category, link)
                # return title, category
        except BaseException as e:
            
                config.debug(level=1, data=e)

    def performDataExtraction(self, links: list):
        DataFetcherQueue = queue.Queue()
        for link in links:
            DataFetcherQueue.put(link)
            DataFetcherThread = threading.Thread(target=self.extractData, args=(DataFetcherQueue.get(),))
            DataFetcherThread.start()


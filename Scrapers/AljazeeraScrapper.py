from bs4 import BeautifulSoup
from SearchEngine.Search import RequestDispatcher, Aljazeera, CNN
import threading
import queue
from TelegramBot.TelegramSender import SendToChannel

aljazeera_search = Aljazeera()
aljazeera_search.getNewsLinks(query='بايرن ميونخ')


class FindData(RequestDispatcher):
    def extractData(self, link: str) -> tuple:
        """method to extract title and tag"""
        try:
            text = self.MakeRequest(target=link)
            soup = BeautifulSoup(text, 'html.parser')
            title = soup.findAll("header", {"class": "article-header"})[0].h1.text
            category = soup.findAll("div", {"class": "topics"})[0].text
            published_date = soup.findAll("span", {"class": "article-dates__published"})[0].text
            print("Title: {}\nCategory: {}\nPublished Date: {}\nSource: @Aljazeera".format(title, category,
                                                                                           published_date))
            SendToChannel("Title: {}\nCategory: {}\nPublished Date: {}\nSource: [Visit]({})".format(title, category,
                                                                                                published_date,link))
            return title, category
        except BaseException as e:
            print(e)

    def performDataExtraction(self, links: list):
        DataFetcherQueue = queue.Queue()
        for link in links:
            DataFetcherQueue.put(link)
            DataFetcherThread = threading.Thread(target=self.extractData, args=(DataFetcherQueue.get(),))
            DataFetcherThread.start()


temp = FindData()
temp.performDataExtraction(aljazeera_search.newsLinks)

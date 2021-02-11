from core.SearchEngine import  RequestDispatcher,RT_SearchEngine
from bs4 import BeautifulSoup
import threading
import queue

from core.TelegramBot.TelegramSender import SendToChannel

rt = RT_SearchEngine(query='قطر')
rt.RunExtraction('ar')


class FindData(RequestDispatcher):
    def __init__(self):
        super().__init__()
        self.sourcePage = None

    def FindTags(self, target: dict) -> list:
        tags_container = list()
        soup = BeautifulSoup(self.sourcePage, 'html.parser')
        tags = soup.find('div', target)
        for tag in tags.a.find_next_siblings():
            tags_container.append(tag.text.strip())
        return tags_container

    def extractData(self, link: str) -> tuple:
        """method to extract title and tag"""
        text = self.MakeRequest(target=link)
        soup = BeautifulSoup(text, 'html.parser')
        self.sourcePage = text
        try:
            if "/arabic." in link:
                title = soup.find('h1', {"class": "heading"}).text
                category = self.FindTags({"class": 'news-tags news-tags_article'})
                published_date = soup.find('span', {"class": "date"}).text
                print("Title: {}\nCategory: {}\nPublished Date: {}".format(title, category, published_date))
                SendToChannel(title,published_date,category,link)
                return title, category
            else:
                title = soup.find('h1', {"class": 'article__heading'}).text.strip()
                published_date = soup.find('span', {"class": 'date date_article-header'}).text
                category = self.FindTags({"class": 'tags-trends'})
                print("Title: {}\nCategory: {}\nPublished Date: {}".format(title, category, published_date))
                SendToChannel(title,published_date,category,link)
        except AttributeError as e:
            print(e)
        except BaseException as e:
            print(e)

    def performDataExtraction(self, links: list):
        DataFetcherQueue = queue.Queue()
        for link in links:
            DataFetcherQueue.put(link)
            DataFetcherThread = threading.Thread(target=self.extractData, args=(DataFetcherQueue.get(),))
            DataFetcherThread.start()


temp = FindData()
temp.performDataExtraction(rt.Links)

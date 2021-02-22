import requests

from bs4 import BeautifulSoup
import threading
import queue

from core.TelegramBot.TelegramSender import SendToChannel
from core.appConfig import AppConfigurations
from core.ext.Utiltiy import write_json

config = AppConfigurations()


class RequestDispatcher:
    @staticmethod
    def MakeRequest(target: str, json=False, headers=None):
        if headers is None:
            headers = dict()
        try:
            req = requests.get(target, headers=headers)
            if req.status_code == 200:
                if json:
                    return req.json()
                return req.text
        except BaseException as e:

            config.debug(level=1, data=e)


class FindData(RequestDispatcher):
    def __init__(self):
        self.sourcePage = None
        self.Results = {'rt': []}

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
                self.Results.get("rt").append(
                    dict(title=title, category=category, published_date=published_date, link=link))
                # SendToChannel(title, published_date, category, link)

                return title, category
            else:
                title = soup.find('h1', {"class": 'article__heading'}).text.strip()
                published_date = soup.find('span', {"class": 'date date_article-header'}).text
                category = self.FindTags({"class": 'tags-trends'})
                print("Title: {}\nCategory: {}\nPublished Date: {}".format(title, category, published_date))
                # SendToChannel(title, published_date, category, link)
        except AttributeError as e:

            config.debug(level=1, data=e)
        except BaseException as e:

            config.debug(level=1, data=e)

    def performDataExtraction(self, links: list):
        DataFetcherQueue = queue.Queue()
        threads = []
        for link in links:
            DataFetcherQueue.put(link)
            DataFetcherThread = threading.Thread(target=self.extractData, args=(DataFetcherQueue.get(),))
            threads.append(DataFetcherThread)
        for thread_start in threads:
            thread_start.start()
        for thread_join in threads:
            thread_join.join()
        write_json(config.EnvironmentPath(), 'rt', self.Results)

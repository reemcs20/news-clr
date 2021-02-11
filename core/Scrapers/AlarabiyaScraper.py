import queue
import threading
from bs4 import BeautifulSoup
from core.SearchEngine.Search import RequestDispatcher
from core.TelegramBot.TelegramSender import SendToChannel


class FindData(RequestDispatcher):
    def __init__(self):
        self.sourcePage = None
        self.ResultsData = {'alarabiya': []}

    def FindTags(self, target: dict) -> list:
        tags_container = list()
        soup = BeautifulSoup(self.sourcePage, 'html.parser')
        tags = soup.find('ul', target)
        for tag in tags.li.find_next_siblings():
            tags_container.append("#"+tag.text.strip())
        return tags_container

    def extractData(self, link: str) -> tuple:
        """method to extract title and tag"""
        text = self.MakeRequest(target=link)
        soup = BeautifulSoup(text, 'html.parser')
        self.sourcePage = text
        try:
            # checks if the results are in English
            if '/english.' in link:
                title = soup.find('h1').text
                category = self.FindTags(target={"class": "tags-related"})
                published_date = soup.find('div', {"class": "article-info"}).text.strip().split('\n')[1]
                # self.ResultsData.get('alarabiya').append({"title":title,"category":category,"published_date":published_date,'link':link})
                print("Title: {}\nCategory: {}\nPublished Date: {}".format(title, category, published_date))
                SendToChannel(title, published_date, category, link)
                return title, category
            else:
                # results are in Arabic
                title = soup.find('h1', {"class": "headingInfo_title"}).text.strip()
                category = self.FindTags(target={"class": "tags"})
                published_date = soup.find('div', {"class": "timeDate"}).time.text
                self.ResultsData.get('alarabiya').append(
                    {"title": title, "category": category, "published_date": published_date, 'link': link})
                print("Title: {}\nCategory: {}\nPublished Date: {}\nSource: [Visit]({})".format(title, category, published_date,link))
                SendToChannel(title, published_date, category, link)
                return title, category
        except AttributeError as e:
            print(e, link)
        except BaseException as e:
            print(e, 38)

    def performDataExtraction(self, links: list):
        DataFetcherQueue = queue.Queue()
        threads = []
        for link in links:
            DataFetcherQueue.put(link)
            DataFetcherThread = threading.Thread(target=self.extractData, args=(DataFetcherQueue.get(),))
            threads.append(DataFetcherThread)
        for thread_starter in threads:
            thread_starter.start()
        for thread_joiner in threads:
            thread_joiner.join()



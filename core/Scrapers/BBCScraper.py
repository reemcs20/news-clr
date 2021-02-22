import queue
import threading

from bs4 import BeautifulSoup

from core.SearchEngine.Search import BBC, RequestDispatcher
from core.TelegramBot.TelegramSender import SendToChannel
from core.appConfig import AppConfigurations

config = AppConfigurations()


class Classification:
    def __init__(self):
        self.categories = {'science': 'علم وتقنية'
            , 'tv-and-radio': "اخبار منوعة"
            , 'sport': "رياضة"
            , 'else': "أخبار العالم"}

    def Filter(self, link: str) -> str:
        """Analyse the link and find the category """
        if 'sport' in link:
            return self.categories.get('sport')
        elif 'tv-and-radio' in link:
            return self.categories.get("tv-and-radio")
        elif 'science' in link:
            return self.categories.get('science')
        else:
            return self.categories.get('else')


class FindData(RequestDispatcher, Classification):
    def __init__(self):
        super().__init__()
        self.sourcePage = None

    def FindTags(self, target: dict) -> list:
        tags_container = list()
        soup = BeautifulSoup(self.sourcePage, 'html.parser')
        tags = soup.find('ul', target)
        for tag in tags.li.find_next_siblings():
            tags_container.append(tag.text.strip())
        return tags_container

    def extractData(self, link: str) -> tuple:
        """method to extract title and tag"""
        text = self.MakeRequest(target=link)
        soup = BeautifulSoup(text, 'html.parser')
        self.sourcePage = text
        try:
            if '/arabic/' in link:
                title = soup.find('h1', {"id": 'content'}).text
                title = soup.find('h1', {"id": 'content'}).text
                category = self.Filter(link)
                published_date = soup.find('time').text
                published_date = soup.find('time').text
                print("Title: {}\nCategory: {}\nPublished Date: {}".format(title, category, published_date))
                # SendToChannel(title, published_date, category, link)
                return title, category
            else:
                title = soup.find('h1', {"id": 'main-heading'}).text
                category = self.Filter(link)
                published_date = soup.find('span', {"data-testid": 'time-and-date:clock'}).text
                print("Title: {}\nCategory: {}\nPublished Date: {}".format(title, category, published_date))
                print("=" * 30)
        except AttributeError as e:
            
                config.debug(level=1, data=e)
        except BaseException as e:
            
                config.debug(level=1, data=e)

    def performDataExtraction(self, links: list):
        DataFetcherQueue = queue.Queue()
        for link in links:
            DataFetcherQueue.put(link)
            DataFetcherThread = threading.Thread(target=self.extractData, args=(DataFetcherQueue.get(),))
            DataFetcherThread.start()

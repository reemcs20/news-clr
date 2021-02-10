from googlesearch import search
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, quote


class Searcher:
    """A base class to search on google"""

    @staticmethod
    def performSearch(query, tld) -> list:
        """method to perform a search operation and returns a list of links"""
        try:
            links = [] # a list to store links from google
            results = search(query=query, num=5, stop=10, tld=tld)
            for link in results:
                links.append(link)  # add links to list
            return links
        except BaseException as e:
            print(e, 20)

    def Ensure_netloc(self, sch: str, target: str, exclude: str) -> bool:
        """
        check if the target contains a certain part of string
        :param exclude: value must not be in target url
        :param sch: site's netloc
        :param target: needed site's url
        :rtype: bool the state if the url is the needed site or not
        """
        return sch in target and exclude not in target

    def Ensure_Rules(self, link: str, rule: str) -> bool:
        """
        a method to make sure the provided phrase contains the rule
        :param link: a link from search results
        :param rule: a string value that is needed to be in link
        :return bool: a state if the link contains rule or not"""
        return rule in link

class RequestDispatcher:
    @staticmethod
    def MakeRequest(target: str):
        try:
            req = requests.get(target)
            if req.status_code == 200:
                return req.text
        except BaseException as e:
            print(e)


class RT_SearchEngine(RequestDispatcher):
    def __init__(self, query: str):
        self.Links = []
        self.query = query
        self.EN_searchEngineLink = 'https://www.rt.com/search?q='
        self.AR_searchEngine = 'https://arabic.rt.com/search?cx=012273702381800949580%3Aiy4mxcpqrji&cof=FORID%3A11&ie' \
                               '=utf8&q={}&sa=%D8%A7%D9%84%D8%A8%D8%AD%D8%AB '

    def getSourcePage(self, language='en'):
        if language == 'ar':
            response = self.MakeRequest(target=self.AR_searchEngine.format(self.query))
            return response
        else:
            response = self.MakeRequest(target=self.EN_searchEngineLink + self.query)
            return response

    def isLink(self, link: str) -> bool:
        return str(link).strip().startswith('http')

    def EN_extractNewsLinks(self):
        links = list()
        soup = BeautifulSoup(self.getSourcePage(), 'html.parser')
        news = soup.findAll('a', {'class': 'link link_hover'})
        for link in news:
            if self.isLink(link.text):
                links.append('https://rt.com'+link)
        self.Links.extend(links)
        return links

    def AR_extractNewsLinks(self):
        links = list()
        soup = BeautifulSoup(self.getSourcePage(language='ar'), 'html.parser')
        news = soup.findAll('a', {'class': 'list-search_media'})
        for link in news:
            print('https://arabic.rt.com' + link.get_attribute_list('href')[0])
            links.append('https://arabic.rt.com' + link.get_attribute_list('href')[0])
        self.Links.extend(links)
        return links

    def RunExtraction(self, lang):
        if lang == 'ar':
            self.AR_extractNewsLinks()
        else:
            self.EN_extractNewsLinks()


# @DeprecationWarning
# class CNN_SearchEngine(RequestDispatcher):
#     def __init__(self, query: str):
#         self.query = query
#         self.searchEngineURL = "https://search.api.cnn.io/content?size=20&q={}&category=us,politics,world,opinion," \
#                                "health ".format(self.query)
#
#     def MakeRequest(self, target) -> dict:
#         try:
#             req = requests.get(target)
#             if req.status_code == 200:
#                 return req.json()
#         except BaseException as e:
#             print(e)
#
#     def Response(self):
#         response = self.MakeRequest(target=self.searchEngineURL)
#         for link in response.get('result'):
#             print(link['url'])


class Aljazeera(Searcher):
    """Aljazeera search engine using google service"""

    def __init__(self):
        self.newsLinks = []

    @staticmethod
    def makeDorkSearch(query: str) -> str:
        """Make the search operation to best match """
        return '"aljazeera.net" "{}"'.format(query)

    def getNewsLinks(self, query: str):
        """Gather response links and store them into list"""
        results = self.performSearch(query=self.makeDorkSearch(query), tld='net')
        for newsLink in results:
            if self.Ensure_Rules(newsLink, 'news') or self.Ensure_Rules(newsLink,'sport'):
                print("Rules matched==>", newsLink)
                self.newsLinks.append(newsLink)


class CNN(Searcher):
    """CNN search engine using google service"""

    def __init__(self):
        self.newsLinks = []

    @staticmethod
    def makeDorkSearch(query: str) -> str:
        """Make the search operation to best match """
        return '"cnn.com " "{}"'.format(query)

    def getNewsLinks(self, query: str):
        """Gather response links and store them into list"""
        results = self.performSearch(query=self.makeDorkSearch(query), tld='com')
        for newsLink in results:
            if self.Ensure_Rules(newsLink, 'world') or self.Ensure_Rules(newsLink, 'article'):
                print("Rules matched==>", newsLink)
                self.newsLinks.append(newsLink)


class Alarabiya(RequestDispatcher):
    """Alarabiya search engine using google service"""

    def __init__(self, query):
        self.newsLinks = []
        self.SearchEngine = "https://www.alarabiya.net/tools/search?query={}".format(query)
        self.ENSearchEngine = "https://english.alarabiya.net/tools/search-results?q={}".format(query)

    def CombineURL(self, path: str) -> str:
        return 'https://www.alarabiya.net' + path

    def AR_getNewsLinks(self) -> list:
        """Gather response links and store them into list"""
        results = self.MakeRequest(self.SearchEngine)
        soup = BeautifulSoup(results, 'html.parser')
        news = soup.find_all('div', {"class": 'latest_content'})
        for link in news:
            print(self.CombineURL(link.a.get_attribute_list('href')[0]))
            self.newsLinks.append(self.CombineURL(link.a.get_attribute_list('href')[0]))
        return self.newsLinks

    def EN_getNewsLinks(self) -> list:
        """Gather response links and store them into list"""
        results = self.MakeRequest(self.ENSearchEngine)
        soup = BeautifulSoup(results, 'html.parser')
        news = soup.find_all('h3')
        for link in news:
            if link.a.get_attribute_list('href')[0]:
                print('https://english.alarabiya.net' + link.a.get_attribute_list('href')[0])
                self.newsLinks.append('https://english.alarabiya.net' + link.a.get_attribute_list('href')[0])
            else:
                print(link.a)
        return self.newsLinks

    def RunExtraction(self, lang):
        if lang == 'ar':
            self.AR_getNewsLinks()
        else:
            self.EN_getNewsLinks()


class BBC(Searcher):
    """BBC search engine using google service"""

    def __init__(self):
        self.newsLinks = []

    @staticmethod
    def makeDorkSearch(query: str) -> str:
        """Make the search operation to best match """
        return '"bbc.com" {}'.format(query)

    def getNewsLinks(self, query: str) -> None:
        """Gather response links and store them into list"""
        results = self.performSearch(query=self.makeDorkSearch(query), tld='net')
        for newsLink in results:
            if self.Ensure_Rules(newsLink, 'bbc.com'):
                print("Rules matched==>", newsLink)
                self.newsLinks.append(newsLink)


# class RT(Searcher):
#     """Russia Today search engine using google service"""
#
#     def __init__(self):
#         self.newsLinks = []
#
#     @staticmethod
#     def makeDorkSearch(query: str) -> str:
#         """Make the search operation to best match """
#         return '"rt.com" {}'.format(query)
#
#     def getNewsLinks(self, query: str) -> None:
#         """Gather response links and store them into list"""
#         results = self.performSearch(query=self.makeDorkSearch(query), tld='net')
#         for newsLink in results:
#             if self.Ensure_Rules(newsLink, 'rt.com'):
#                 print("Rules matched==>", newsLink)
#                 self.newsLinks.append(newsLink)
#             else:
#                 print("Out Of condition: ", newsLink)

# temp = RT_SearchEngine(query='الانتخابات الامركية')
# temp.AR_extractNewsLinks()
# temp = Alarabiya(query='Iran')
# temp.EN_getNewsLinks()

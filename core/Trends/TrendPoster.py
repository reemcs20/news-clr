import json
from bs4 import BeautifulSoup
from core.SearchEngine.Search import RequestDispatcher
import os
import threading


class ResultsSearch:
    def __init__(self, language: str = 'ar'):
        if language == 'ar':
            self.AllTrends = {'arTrends': []}
        else:
            self.AllTrends = {'enTrends': []}


class EN_Alarbya(RequestDispatcher, ResultsSearch):
    """
    a class to scrape the trends from Alarapyia site.
    """

    def __init__(self):
        super().__init__(language='en')
        self.TrendsPath = []
        self.Target: str = "https://english.alarabiya.net/News"
        self.cookies: dict = {
            'cookie': """beraredirectar=beta-ar; _fbp=fb.1.1612444680560.1540103053; _pk_id.1.3db0=4108da13bdb477c1.1612467545.; _ga=GA1.3.660409616.1612444680; __atuvc=5|5; _ga=GA1.1.660409616.1612444680; beraredirecten=beta-en; aaconsent=aaconsent; YPF8827340282Jdskjhfiw_928937459182JAX666=193.35.20.93; NEW_VISITOR=new; VISITOR=returning; _pk_ref.1.3db0=["","",1616943849,"https://www.alarabiya.net/"]; _pk_ses.1.3db0=1; AMP_TOKEN=$NOT_FOUND; _gid=GA1.3.1398592103.1616943851; _dc_gtm_UA-463820-31=1; _ga_576H90FZVV=GS1.1.1616943849.15.0.1616943849.60; JSESSIONID=2357072FF0744AE1F120A865E4FB9D4B"""}
        self.RequestText: str = self.MakeRequest(self.Target, headers=self.cookies)  # A HTTP Request to Alarbya site
        self.soup = BeautifulSoup(self.RequestText, 'html.parser')  # BeautifulSoup object
        self.HeaderTrends: list = self.soup.find_all('h2', {
            'class': 'sectionHero_title'})
        self.MiddleTrends: list = self.soup.find_all('a', {
            'class': ""})  # the path of trends in page header

    @staticmethod
    def Combine_URL(path):
        return "https://english.alarabiya.net" + path

    def RefineDataMiddleTrends(self):
        for trend in self.MiddleTrends:
            if trend.get_attribute_list('href')[0].startswith('/News/') and trend.get_attribute_list('href')[
                0].__len__() > 50:

                # print(trend.get_attribute_list('title')[0])
                # print(self.Combine_URL(trend.get_attribute_list('href')[0]))
                if trend.get_attribute_list('title')[0] and trend.get_attribute_list('href')[0]:
                    self.AllTrends.get('enTrends').append(dict(title=trend.get_attribute_list('title')[0],
                                                               link=self.Combine_URL(
                                                                   trend.get_attribute_list('href')[0])))

    def RefineDataHeaderTrend(self):
        for trend in self.HeaderTrends:
            if str(trend.text).strip().startswith('Coronavirus'):
                news = str(trend.text).split("""
                                    
                                """)[1].strip()
                # print(news)
                self.AllTrends.get("enTrends").append(dict(title=news, link='https://english.alarabiya.net/News'))
            else:
                # print(str(trend.text).replace('  ', '').strip().strip('\n'))
                self.AllTrends.get("enTrends").append(dict(title=str(trend.text).replace('  ', '').strip().strip('\n'),
                                                           link='https://english.alarabiya.net/News'))

    def GetTrends(self) -> dict:
        thread1 = threading.Thread(target=self.RefineDataHeaderTrend)
        thread2 = threading.Thread(target=self.RefineDataMiddleTrends)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        return self.AllTrends


class AJ_Trends(RequestDispatcher, ResultsSearch):
    """A class to scrape Trends from Aljazeera Platform"""

    def __init__(self):
        super().__init__(language='ar')
        self.TrendURL = 'https://www.aljazeera.net'
        self.trendsData = self.MakeRequest(target=self.TrendURL, json=False)

    def ExtractNews(self):
        soup = BeautifulSoup(self.trendsData, 'html.parser')
        headingTrends = soup.find_all('a', {'class': 'article-featured-top-related__title__link'})
        Vertical_header = soup.findAll('div', {'class': 'article-card__content-wrap'})
        for headTrend in headingTrends:
            news_title = headTrend.text
            news_link = 'https://www.aljazeera.net' + headTrend.get_attribute_list('href')[0]
            self.AllTrends.get('arTrends').append(dict(title=news_title, link=news_link))
        for Vertical_news in Vertical_header:
            news_title = Vertical_news.a.text
            news_link = 'https://www.aljazeera.net' + Vertical_news.a.get_attribute_list('href')[0]
            self.AllTrends.get('arTrends').append(dict(title=news_title, link=news_link))


class BBC_Trends(RequestDispatcher, ResultsSearch):
    """
    A class to scrape Trends from BBC Platform
    """

    def __init__(self):
        super().__init__(language='ar')
        self.TrendURL: str = 'https://www.bbc.com/arabic/mostread.json'
        self.trends: dict = self.MakeRequest(target=self.TrendURL, json=True)

    def formURL(self, url: str):
        """
        :param url: a short url from API response
        combine a url with the trend link
        """
        return 'https://www.bbc.com' + url

    def ParseJson(self):
        for Trend in self.trends.get('records'):
            title = Trend.get('promo').get('headlines').get('headline')
            link = Trend.get('promo').get('locators').get('assetUri')
            self.AllTrends.get('arTrends').append(dict(title=title, link=self.formURL(url=link)))

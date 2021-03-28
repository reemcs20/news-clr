import json
from bs4 import BeautifulSoup
from core.SearchEngine.Search import RequestDispatcher


class ResultsSearch:
    AllTrends = {'aljazeera': [], 'bbc': []}


class EN_Alarbya(RequestDispatcher, ResultsSearch):
    def __init__(self):
        self.Target: str = "https://english.alarabiya.net/"
        self.cookies: dict = {
            'cookie': """beraredirectar=beta-ar; _fbp=fb.1.1612444680560.1540103053; _pk_id.1.3db0=4108da13bdb477c1.1612467545.; _ga=GA1.3.660409616.1612444680; __atuvc=5|5; _ga=GA1.1.660409616.1612444680; beraredirecten=beta-en; aaconsent=aaconsent; YPF8827340282Jdskjhfiw_928937459182JAX666=193.35.20.93; NEW_VISITOR=new; VISITOR=returning; _pk_ref.1.3db0=["","",1616943849,"https://www.alarabiya.net/"]; _pk_ses.1.3db0=1; AMP_TOKEN=$NOT_FOUND; _gid=GA1.3.1398592103.1616943851; _dc_gtm_UA-463820-31=1; _ga_576H90FZVV=GS1.1.1616943849.15.0.1616943849.60; JSESSIONID=2357072FF0744AE1F120A865E4FB9D4B"""}
        self.RequestText: str = self.MakeRequest(self.Target, headers=self.cookies)  # A HTTP Request to Alarbya site
        self.soup = BeautifulSoup(self.RequestText, 'html.parser')  # BeautifulSoup object
        self.HeaderTrends: list = self.soup.find_all('h2', {
            'class': 'sectionHero_title'})  # the path of trends in page header

    def RefineData(self):
        for i in self.HeaderTrends:
            print(str(i.text).strip().strip("""
                                            
                                        """))


class AJ_Trends(RequestDispatcher, ResultsSearch):
    """A class to scrape Trends from Aljazeera Platform"""

    def __init__(self):
        self.TrendURL = 'https://www.aljazeera.net'
        self.trendsData = self.MakeRequest(target=self.TrendURL, json=False)

    def ExtractNews(self):
        soup = BeautifulSoup(self.trendsData, 'html.parser')
        headingTrends = soup.find_all('a', {'class': 'article-featured-top-related__title__link'})
        Vertical_header = soup.findAll('div', {'class': 'article-card__content-wrap'})
        for headTrend in headingTrends:
            news_title = headTrend.text
            news_link = 'https://www.aljazeera.net' + headTrend.get_attribute_list('href')[0]
            self.AllTrends.get('aljazeera').append(dict(title=news_title, link=news_link))
        for Vertical_news in Vertical_header:
            news_title = Vertical_news.a.text
            news_link = 'https://www.aljazeera.net' + Vertical_news.a.get_attribute_list('href')[0]
            self.AllTrends.get('aljazeera').append(dict(title=news_title, link=news_link))


class BBC_Trends(RequestDispatcher, ResultsSearch):
    """
    A class to scrape Trends from BBC Platform
    """

    def __init__(self):
        self.TrendURL: str = 'https://www.bbc.com/arabic/mostread.json'
        self.trends: dict = self.MakeRequest(target=self.TrendURL, json=True).get('records')

    def formURL(self, url: str):
        """
        :param url: a short url from API response
        combine a url with the trend link
        """
        return 'https://www.bbc.com' + url

    def ParseJson(self):
        for Trend in self.trends:
            title = Trend.get('promo').get('headlines').get('headline')
            link = Trend.get('promo').get('locators').get('assetUri')
            self.AllTrends.get('bbc').append(dict(title=title, link=self.formURL(url=link)))


temp = EN_Alarbya()
temp.RefineData()

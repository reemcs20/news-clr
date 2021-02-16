import json

from bs4 import BeautifulSoup

from core.SearchEngine.Search import RequestDispatcher


class ResultsSearch:
    AllTrends = {'aljazeera': [], 'bbc': []}


class AJ_Trends(RequestDispatcher, ResultsSearch):
    def __init__(self):
        # self.AllTrends = {'aljazeera': []}
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
            print(headTrend.text)
            print('https://www.aljazeera.net' + headTrend.get_attribute_list('href')[0])
        for Vertical_news in Vertical_header:
            news_title = Vertical_news.a.text
            news_link = 'https://www.aljazeera.net' + Vertical_news.a.get_attribute_list('href')[0]
            self.AllTrends.get('aljazeera').append(dict(title=news_title, link=news_link))
            print(news_title)
            print(news_link)


class BBC_Trends(RequestDispatcher,ResultsSearch):
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
            self.AllTrends.get('bbc').append(dict(title=title,link=self.formURL(url=link)))



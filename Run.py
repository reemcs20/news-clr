import argparse
import multiprocessing
import sys
import time

from core.SearchEngine.Search import *
from core.ext.Utiltiy import EchoResult

start_time = time.time()  # the time of start to be calculated later with the end time
args = argparse.ArgumentParser()
args.add_argument('-q', help="a query for searching it", type=str, required=False)
args.add_argument('-l', help="Language of search options", type=str, required=False)
args_parser = args.parse_args()
query: str = args_parser.q
language: str = args_parser.l
resultsManager = EchoResult()

if __name__ == '__main__':
    """
    determine if the search operation is arabic or english 
    some search engines are for AR or the opposite ir BOTH.
    """
    if language == 'ar':
        sky_news = SkyNews(query=query)
        aljazeera = Aljazeera(query=query.encode('utf-8'), language=language)
        alarabiya = Alarabiya(query=query)
        rt = RT_SearchEngine(query=query)
        aljazeera_process = multiprocessing.Process(target=aljazeera.getNewsLinks)
        alarabiya_process = multiprocessing.Process(target=alarabiya.RunExtraction, args=(language,))
        rt_process = multiprocessing.Process(target=rt.RunExtraction, args=(language,))
        sky_news_process = multiprocessing.Process(target=sky_news.RunExtraction,
                                                   args=(language,))
        sky_news_process.start()
        aljazeera_process.start()
        alarabiya_process.start()
        rt_process.start()
        sky_news_process.join()
        aljazeera_process.join()
        alarabiya_process.join()
        rt_process.join()
        resultsManager.ReadJson()
        sys.stdout.write(str(resultsManager.AllNews))
    else:
        aljazeera = Aljazeera(query=query.encode('utf-8'), language=language)
        foxnews = FoxNews_EN(query=query)
        alarabiya = Alarabiya(query=query)
        rt = RT_SearchEngine(query=query)
        cnn = CNN()
        aljazeera_process = multiprocessing.Process(target=aljazeera.getNewsLinks)
        alarabiya_process = multiprocessing.Process(target=alarabiya.RunExtraction, args=(language,))
        rt_process = multiprocessing.Process(target=rt.RunExtraction, args=(language,))
        foxnews_process = multiprocessing.Process(target=foxnews.parseResults)
        cnn_process = multiprocessing.Process(target=cnn.EN_CNN_Search, args=(query,))

        aljazeera_process.start()
        alarabiya_process.start()
        cnn_process.start()
        foxnews_process.start()
        rt_process.start()
        aljazeera_process.join()
        alarabiya_process.join()
        foxnews_process.join()
        cnn_process.join()
        rt_process.join()
        resultsManager.ReadJson()
        sys.stdout.write(str(resultsManager.AllNews))
    if config.DEBUG:
        "Calculate how long did the program take"
        print("Done! Taken Time:", time.time() - start_time)

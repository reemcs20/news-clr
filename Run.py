import multiprocessing
from core.SearchEngine.Search import BBC, Aljazeera, Alarabiya, RT_SearchEngine, CNN,FoxNews_EN,SkyNews
import time
import argparse

args = argparse.ArgumentParser()
args.add_argument('-q', default=None, help="a query for searching it", type=str,required=True)
args.add_argument('-l', default='ar', help="Language of search options", type=str,required=False)
args_parser = args.parse_args()


# ask user to input query and language
query = args_parser.q
language: str = args_parser.l

start_time = time.time()
bbc = BBC(query=query)
cnn = CNN()
aljazeera = Aljazeera(query=query,language=language)
alarabiya = Alarabiya(query=query)
rt = RT_SearchEngine(query=query)

if __name__ == "__main__":
    
    bbc_process_google = multiprocessing.Process(target=bbc.getNewsLinks)
    cnn_process_google = multiprocessing.Process(target=cnn.EN_CNN_Search, args=(query,))
    aljazeera_process_google = multiprocessing.Process(target=aljazeera.getNewsLinks)
    alarabiya_process = multiprocessing.Process(target=alarabiya.RunExtraction, args=(language,))
    rt_process = multiprocessing.Process(target=rt.RunExtraction, args=(language,))

    # creating processes
    rt_process.start()
    alarabiya_process.start()
    # starting processes
    bbc_process_google.start()
    cnn_process_google.start()
    aljazeera_process_google.start()
    rt_process.join()
    aljazeera_process_google.join()
    cnn_process_google.join()
    bbc_process_google.join()
    alarabiya_process.join()

    print("After all search engines have ended")
    # both processes finished
    print("Done! Taken Time:", time.time() - start_time)

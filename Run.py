import multiprocessing
from core.SearchEngine.Search import BBC, Aljazeera, Alarabiya, RT_SearchEngine, CNN
import time
import argparse

args = argparse.ArgumentParser()
args.add_argument('-q', default=None, help="a query for searching it", type=str,required=True)
args.add_argument('-l', default='ar', help="Language of search options", type=str,required=False)
args_parser = args.parse_args()


# ask user to input query and language
query = args_parser.q
language = args_parser.l

start_time = time.time()
bbc = BBC()
cnn = CNN()
aljazeera = Aljazeera()
alarabiya = Alarabiya(query=query)
rt = RT_SearchEngine(query=query)

if __name__ == "__main__":
    
    bbc_process_google = multiprocessing.Process(target=bbc.getNewsLinks, args=(query,))
    cnn_process_google = multiprocessing.Process(target=cnn.getNewsLinks, args=(query,))
    aljazeera_process_google = multiprocessing.Process(target=aljazeera.getNewsLinks, args=(query,))
    alarabiya_process = multiprocessing.Process(target=alarabiya.RunExtraction, args=(language,))
    rt_process = multiprocessing.Process(target=rt.RunExtraction, args=(language,))

    # creating processes
    rt_process.start()
    alarabiya_process.start()

    # starting processes
    bbc_process_google.start()
    bbc_process_google.join()
    cnn_process_google.start()
    cnn_process_google.join()
    aljazeera_process_google.start()
    aljazeera_process_google.join()
    alarabiya_process.join()
    rt_process.join()
    print("After all search engines have ended")
    # both processes finished
    print("Done! Taken Time:", time.time() - start_time)

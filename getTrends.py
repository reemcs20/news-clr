import argparse

from core.Trends.TrendPoster import AJ_Trends, BBC_Trends
import json
import sys
args = argparse.ArgumentParser()
args.add_argument('-p', default=None, help="Prettify JSON", type=str, required=False)
args_parser = args.parse_args()

t = BBC_Trends()
j = AJ_Trends()
j.ExtractNews()
t.ParseJson()


def PringJson():
    if args_parser.p:
        for news in t.AllTrends.get("bbc"):
            print(news.get("title"))
        for news in t.AllTrends.get("aljazeera"):
            print(news.get("title"))
    else:
        sys.stdout.write(json.dumps(t.AllTrends, indent=3, sort_keys=True))


PringJson()

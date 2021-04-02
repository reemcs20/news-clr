import argparse
import json

from core.Trends.TrendPoster import AJ_Trends, BBC_Trends, EN_Alarbya

args = argparse.ArgumentParser()
args.add_argument('-p', default=None, help="Prettify JSON", type=str, required=False)
args.add_argument('-l', default='ar', help="Trends Language", type=str, required=False)
args_parser = args.parse_args()
if args_parser.l == 'ar':
    t = BBC_Trends()
    j = AJ_Trends()
    j.ExtractNews()
    t.ParseJson()
else:
    en_trends = EN_Alarbya()


def PrintJson():

    if args_parser.l == 'ar':
        if args_parser.p:
            for news in t.AllTrends.get("arTrends"):
                print(news.get("title"))
        else:
            print(json.dumps(t.AllTrends, indent=3, sort_keys=True))
    else:
        if args_parser.p:
            for news in en_trends.GetTrends():
                print(news.get('title'))
        else:
            print(json.dumps(en_trends.GetTrends(), indent=4, sort_keys=True))


PrintJson()

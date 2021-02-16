from core.Trends.TrendPoster import AJ_Trends,BBC_Trends
import json
t = BBC_Trends()
j = AJ_Trends()
j.ExtractNews()
t.ParseJson()
print(json.dumps(t.AllTrends,indent=3,sort_keys=True))

from core.Trends.TrendPoster import AJ_Trends
import json
temp = AJ_Trends()
temp.ExtractNews()
print(json.dumps(temp.AllTrends, indent=2, sort_keys=True))

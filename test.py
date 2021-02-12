import requests
import json
query = 'Iran'
headers = {
    'Host': 'www.aljazeera.com',
    "Accept-Encoding":'gzip, deflate, br',
    "Accept-Language": "en-US,en;q=0.5",
    "Connection":'keep-alive',
    "If-None-Match": """W/"e0-c53f7wDo53oXBizh9J4Kc52/FPs""",

    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/88.0.4324.146 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    "wp-site":"aje",
    "X-KL-Ajax-Request": "Ajax_Request",
    'original-domain': 'www.aljazeera.com',
    'Referer': f'https://www.aljazeera.net/search/{query}',

}
Search_data = dict(query=query, start=1, sort="relevance")
req = requests.get('https://www.aljazeera.com/graphql?wp-site=aje&operationName=SearchQuery&variables={}&extensions={}'.format(json.dumps(Search_data),''),headers=headers)
print(req.text)
print(req.status_code)

import requests
query = 'iran'
headers = {
    'Host': 'www.aljazeera.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/88.0.4324.146 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'original-domain': 'www.aljazeera.com',
    'Referer': f'https://www.aljazeera.com/search/isis',

}
req = requests.get('https://www.aljazeera.com/graphql?wp-site=aje&operationName=SearchQuery&variables=%7B%22query%22%3A%22isis%22%2C%22start%22%3A1%2C%22sort%22%3A%22relevance%22%7D&extensions=%7B%7D')
print(req.text)
print(req.status_code)
print(req.headers)
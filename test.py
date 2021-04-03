from aiohttp import ClientSession

import asyncio
import requests
import time

results = []


async def print_info():
    while True:
        print("Function one say hi")
        await asyncio.sleep(2)


async def print_info2():
    while True:
        print("Function Two say hi")
        await asyncio.sleep(1)

loop = asyncio.get_event_loop()

loop.create_task(print_info())
loop.create_task(print_info2())
loop.run_forever()
# async def fetch(url, session: ClientSession, page_number):
#     headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
#                "Referer": "Referer: https://www.dnb.com/business-directory/company-search.html?term=wool&page={}".format(
#                    page_number),
#                "Cookie": cookie}
#     async with session.get(url, headers=headers) as response:
#         json_response = await response.read()
#         results.append(json_response.decode())
#         return json_response
#
#
# async def main():
#     tasks = []
#     async with ClientSession() as session:
#         for page_number in range(30):
#             url = "https://www.dnb.com/apps/dnb/thirdparty/dnbdirectutil?limited=false&returnNav=true&captchaDone=true&pageSize=25&pageNumber={}&criteriasearch=true&searchTerm=wool".format(
#                 page_number)
#             tasks.append(asyncio.create_task(fetch(url, session, page_number)))
#         response = await asyncio.gather(*tasks)
#         return response
#
#
# loop = asyncio.get_event_loop()
#
# loop.run_until_complete(main())
# print(results)

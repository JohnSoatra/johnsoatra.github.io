#!python3
import requests
import concurrent
from concurrent.futures import ThreadPoolExecutor

res = requests.get('https://www.niijima.com/website/sitemap.html')

print(res.status_code)

# base_url = 'http://www.town.mizuho.tokyo.jp/sitemap.html'
# threads = 100
# times = 1000

# def make_request(i):
#     res = requests.get(base_url)
#     return f'{i}, {res.status_code}, {res.url}'

# with ThreadPoolExecutor(max_workers=threads) as executor:
#     all_requests = {
#         executor.submit(make_request, i) for i in range(0, times)
#     }
#     for future_response in concurrent.futures.as_completed(all_requests):
#         try:
#             result = future_response.result()
#             print(result)

#         except Exception as ex:
#             print('Looks like something went wrong:', ex)

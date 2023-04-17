#!python3
import requests

headers = {
    # 'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Accept-Encoding': 'gzip, deflate',
    # 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0',
    # 'Referer' : 'http://sportsbeta.ladbrokes.com/football',
}

payload = {
    # 'N': '4294966750',
    # 'facetCount_156%23327': '12',
    # 'facetCount_157%23325': '8',
    # 'form-trigger':'moreId',
    # 'moreId':'156%23327',
    # 'pageId':'p_football_home_page',
    # 'pageType': 'EventClass',
    # 'type':'ajaxrequest'
}

url='https://google.com'

r = requests.get(url, data = payload, headers = headers)

print(r)

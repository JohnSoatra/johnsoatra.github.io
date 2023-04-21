from util.crawler import Crawler

# args = None
# '//table[@id="kyotenListHeader"]//a[text()="次へ"]'
# a = Crawler(
#     urls=[
#         'https://www.e-map.ne.jp/p/msins01/nmap.htm?&p_s1=msins01&p_f3=1&&cond1=1&cond6=1&&&his=el%2CelT&lat=35.9052889&lon=139.2299083'
#     ],
#     headless=False,
#     next_xpath='//table[@id="kyotenListHeader"]//a[text()="次へ"]'
# )
a = Crawler(
    headless=False,
    urls=[
        'https://www.mirasapo.jp/subsidy/35574'
    ],
    field_xpath={
        'title': '//div[@class="main-header"]/h1'
    }
)


a.run()
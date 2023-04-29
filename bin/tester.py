#!python3
import checker


# no information
obj = checker.view_page(
    # 'https://www.city.imabari.ehime.jp/kenchiku/yosiki/choki/'
    # 'https://www.town.matsuno.ehime.jp/soshiki/11/4603.html'
    # 'https://www.city.ichihara.chiba.jp/article?articleId=602371e7ece4651c88c1800c',
    # 'https://www.vill.mizukami.lg.jp/q/aview/1101/1377.html'
    # 'https://www.town.kiho.lg.jp/life/child/birth/birth_gift_money/'
    # 'https://www.city.sabae.fukui.jp/life_event/korei_kaigo/kokikoreishairyo/index.html'
    # 'https://www.city.tsuyama.lg.jp/index2.php?id=3326'
    # 'https://www.town.fujikawaguchiko.lg.jp/info/info.php?if_id=6293&ca_id=34'
    # 'https://www.city.saito.lg.jp/kenko_kyoiku/0201_1703310000000017.html'
    'https://www.vill.nishimera.lg.jp/village/a-00-villagelife/10000477'
    
)

for key in obj:
    print(f'{key}: {obj[key]}')
#!python3
from eyes import eyes

obj = eyes.view_page(
    'https://www.city.sabae.fukui.jp/life_event/korei_kaigo/kokikoreishairyo/index.html',
)

for key in obj:
    print(f'{key}: {obj[key]}')
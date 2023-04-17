#!python3
import re

url = 'https://www.city./chuo/chiba.jp/chibachi/chiikishinko/pulatto-wakaba.html'
# r".*^(?!.*you.*).*"
def contains(url):
    pattern = r".*^(?!.*/chuo/.*)^(?!.*/wakaba/.*).*"
    return re.match(pattern, url)

res = contains(url)
print(res)

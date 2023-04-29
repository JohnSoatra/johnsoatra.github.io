#!python3
import jellyfish
from zchecker.depends import depends


hight_point = 0
word = '404エラー'
take = ''

for depend in depends:
    s1 = jellyfish.jaro_similarity(depend, word)
    s2 = jellyfish.jaro_winkler_similarity(depend, word)
    point = (s1 + s2) / 2
    
    if hight_point < point:
        hight_point = point
        take = depend

print(hight_point)
print(take)
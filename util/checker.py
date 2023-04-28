#!python3
from xml.etree import ElementTree
from lxml import etree
from requests_html import HTML
from util.depends import depends
import requests
import jellyfish
import re

# helpers

def target_text(html):
    texts = []
    xpaths = [
        '//head//title//text()',
        '//body//h1//text()',
        '//body//h2//text()',
        '//body//h3//text()',
        '//body//h4//text()',
        '//body//h5//text()',
        '//body//h6//text()',
    ]

    for xpath in xpaths:
        h_list = html.xpath(xpath)
        
        for item in h_list:
            if item:
                texts.append(item)
        
        if len(texts):
            break
    
    text = ' '.join(texts)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def html_text(html):
    html = HTML(html=html)
    text = target_text(html)
    
    return text

def black_page(depends, target):
    for depend in depends:
        s1 = jellyfish.jaro_similarity(depend, target)
        s2 = jellyfish.jaro_winkler_similarity(depend, target)
        
        if (s1 + s2) / 2 > 0.5:
            return True
    
    return False

# =------------------------
def active_url(url):
    try:
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        html = response.text
        text = html_text(html)
        
        return not black_page(depends, text)

    except Exception as ex:
        print('Error: ', ex)
        pass
    
    return False

# testing
if __name__ == '__main__':
    url = 'https://www.town.shonai.lg.jp/business/shoukougyo/kensakithaihu.html'
    active = active_url(url)
    
    if active:
        print('The url is Active')
        
    else:
        print('The url is Inactive')
        

#!python3
from requests_html import HTML
from translate import Translator
import depends
import requests
import jellyfish
import re

__header_min_length = 3
__paragraph_min_length = 7

# helpers
def __specific_target(html):
    header_texts = []
    paragraph_texts = []
    
    header_xpaths = [
        '//title',
        '//h1',
        '//h2',
        '//h3',
        '//h4',
        '//h5',
        '//h6',
    ]
    paragraph_xpaths = [
        'p[@class="no_data"]',
        '//h1/descendant::p',
        '//*[self::*//h1]/following-sibling::*[1]//p[1]',
    ]

    for header_xpath in header_xpaths:
        header_list = html.xpath(f'{header_xpath}//text()')
        
        for header in header_list:
            if header and len(header) >= __header_min_length:
                header_texts.append(header)
        
        if len(header_texts):
            break
    
    for paragraph_xpath in paragraph_xpaths:
        paragraph_list = html.xpath(f'{paragraph_xpath}//text()')
        
        for paragraph in paragraph_list:
            if paragraph and len(paragraph) >= __paragraph_min_length:
                paragraph_texts.append(paragraph)
                break
    
    header_text = ' '.join(header_texts)
    header_text = re.sub(r'\s+', ' ', header_text).strip()
    
    paragraph_text = ' '.join(paragraph_texts)
    paragraph_text = re.sub(r'\s+', ' ', paragraph_text).strip()

    return {
        'header': header_text,
        'paragraph': paragraph_text
    }

def __html_target(html):
    html = HTML(html=html)
    target = __specific_target(html)
    
    return target

def __in_black_page(
    target,
    header_min_point,
    paragraph_min_point,
    _depends
):
    header_max_point = 0
    paragraph_max_point = 0
    
    header = target['header']
    paragraph = target['paragraph']
    
    # compare with header
    if header:
        for depend in depends.depends + (_depends if type(_depends) == list else []):
            for token_header in header.split(' '):
                if len(token_header) >= __header_min_length:
                    s1 = jellyfish.jaro_similarity(depend, token_header)
                    s2 = jellyfish.jaro_winkler_similarity(depend, token_header)
                    
                    points = (s1 + s2) / 2
                    
                    if points > header_max_point:
                        header_max_point = points
                        
                    if points >= header_min_point:
                        return ({
                            'active': False,
                            'checked': True,
                            'error': None,
                            'keyword': header,
                            'tag': 'header',
                            'similar-to': depend,
                            'points': round(points, 2),
                            'header-max-point': round(header_max_point, 2)
                        })

    # compare with paragraph
    if paragraph:
        for depend in depends.depends + (_depends if type(_depends) == list else []):
            for token_paragraph in paragraph.split(' '):
                if len(token_paragraph) >= __paragraph_min_length:
                    s1 = jellyfish.jaro_similarity(depend, token_paragraph)
                    s2 = jellyfish.jaro_winkler_similarity(depend, token_paragraph)
                    
                    points = (s1 + s2) / 2
                    
                    if points > paragraph_max_point:
                        paragraph_max_point = points
                        
                    if points >= paragraph_min_point:
                        return ({
                            'active': False,
                            'checked': True,
                            'error': None,
                            'keyword': paragraph,
                            'tag': 'paragraph',
                            'similar-to': depend,
                            'points': round(points, 2),
                            'header-max-point': round(header_max_point, 2),
                            'paragraph-max-point': round(paragraph_max_point, 2)
                        })
    
    return {
        'active': True,
        'checked': True,
        'error': None,
        'target': target,
        'header-max-point': round(header_max_point, 2),
        'paragraph-max-point': round(paragraph_max_point, 2)
    }

# =------------------------
def active_url(
    url,
    lang='ja',
    timeout=6,
    header_min_point=0.8,
    paragraph_min_point=0.8,
    depends=None,
    allow_redirects=False
):
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=allow_redirects)
        status_code = response.status_code
        redirected = response.is_redirect
        expired = response.headers.get('Expires')
        expired = expired if expired else response.headers.get('expires')
        
        if expired:
            return {
                'active': False,
                'checked': False,
                'error': f'Expired: {expired}',
                'redirected': redirected
            }
        
        if status_code >= 400 and status_code <= 499:
            return {
                'active': False,
                'checked': False,
                'error': f'Client error responses: {status_code}',
                'redirected': redirected
            }
            
        if status_code >= 500 and status_code <= 599:
            return {
                'active': False,
                'checked': False,
                'error': f'Server error responses: {status_code}',
                'redirected': redirected
            }
 
        response.encoding = response.apparent_encoding
        html = response.text
        target = __html_target(html)
        
        if not (lang == 'ja' or lang == 'en'):
            translate = Translator(from_lang=lang, to_lang='en')
            
            for key in target:
                target[key] = translate.translate(target[key])
        
        return {
            **__in_black_page(
                target,
                header_min_point,
                paragraph_min_point,
                depends
            ),
            'redirected': redirected
        }

    except Exception as error:
        return {
            'active': False,
            'checked': False,
            'error': error,
            'redirected': False
        }
        
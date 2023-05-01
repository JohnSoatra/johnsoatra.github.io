#!python3
from .depends.depends_no_data import depends as depends_no_data
from .depends.depends_404 import depends as depends_404
from urllib3.exceptions import InsecureRequestWarning
from translate import Translator
from requests_html import HTML
import requests
import jellyfish
import re

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# private global variables

__separator = '\||-|:'
__header_min_length = 3
__paragraph_min_length = 7
__container = 'self::div or self::span or self table'
__header_xpaths = [
    '//title',
    '//h1[self::*//text() and last()=1]',
    '(//h2[self::*//text() and last()=1])[1]'
]
__paragraph_xpaths = [
    'p[@class="no_data"]',
    '//h1[self::*//text()]/following-sibling::p[1]',
    '//h1[self::*//text()]/following-sibling::*//p[1]',
    f'//*[({__container}) and self::*//h1[self::*//text()] and self::*/*[last()=1]]/following-sibling::*[1][{__container}]//p[1]'
]
__content_xpath = [
    f'''
        //h1[self::*//text()]/following-sibling::*|
        //h1[self::*//text()]/following-sibling::*//*|
        //*[self::*//h1[self::*//text()] and self::*/*[last()=1]]/following-sibling::*[1]//*
    '''
]
# //h1[self::*//text()]/following-sibling::p[1]|//h1[self::*//text()]/following-sibling::*//p[1]|//*[({self::div or self::span}) and self::*//h1[self::*//text()] and self::*/*[last()=1]]/following-sibling::*[1][{self::div or self::span}]//p[1]
# ---------------------- helpers

def strip(text):
    return re.sub(r'\s+', ' ', text).strip()

def __get_highlight(
    html,
    header_xpath,
    paragraph_xpath
):
    html = HTML(html=html)
    highlight = __highlighter(
        html,
        header_xpath,
        paragraph_xpath
    )
    
    return highlight

def __highlighter(
    html,
    header_xpath,
    paragraph_xpath
):
    header_texts = []
    paragraph_texts = []
    
    for xpath in __header_xpaths + (header_xpath if type(header_xpath) == list else []):
        header_list = html.xpath(f'{xpath}//text()')
        
        for header in header_list:
            header = strip(header)
            
            if len(header) >= __header_min_length:
                header_texts.append(header)
    
    for xpath in __paragraph_xpaths + (paragraph_xpath if type(paragraph_xpath) == list else []):
        paragraph_list = html.xpath(f'{xpath}//text()')
        
        for paragraph in paragraph_list:
            paragraph = strip(paragraph)
            
            if len(paragraph) >= __paragraph_min_length:
                paragraph_texts.append(paragraph)

        if len(paragraph_texts):
            break

    return {
        'headers': header_texts,
        'paragraphs': paragraph_texts
    }

def __bad_page(
    highlight,
    separator,
    depends,
    header_min_point,
    paragraph_min_point,
    targets,
):
    header_max_point = 0
    paragraph_max_point = 0
    
    header_obj = {}
    paragraph_obj = {}
    
    headers = highlight['headers']
    paragraphs = highlight['paragraphs']
    
    page = {}
    
    if len(headers):
        header_similar = ''
        header_keyword = ''
        
        for depend in depends_404 + (depends if type(depends) == list else []):
            for header in headers:                
                for token_header in re.split(__separator + (separator if separator else ''), header):
                    token_header = strip(token_header)
                    
                    if len(token_header) >= __header_min_length:
                        s1 = jellyfish.jaro_similarity(depend, token_header)
                        s2 = jellyfish.jaro_winkler_similarity(depend, token_header)
                        
                        points = (s1 + s2) / 2
                        
                        if points > header_max_point:
                            header_max_point = points
                            header_similar = depend
                            header_keyword = token_header
                            
                        if points >= header_min_point:
                            return ({
                                'active': False,
                                'checked': True,
                                'error': False,
                                'highlight': highlight,
                                
                                'keyword': token_header,
                                'tag': 'header',
                                'similar-to': depend,
                                'points': round(points, 2),
                                'header-max-point': round(header_max_point, 2)
                            })

        header_obj = {
            'header-keyword': header_keyword,
            'header-similar-to': header_similar,
            'header-max-point': round(header_max_point, 2),
        }

    if len(paragraphs):
        paragraph_similar = ''
        paragraph_keyword = ''
        
        for depend in depends_no_data + (depends if type(depends) == list else []):
            for paragraph in paragraphs:
                for token_paragraph in re.split(__separator + (separator if separator else ''), paragraph):
                    token_paragraph = strip(token_paragraph)
                    
                    if len(token_paragraph) >= __paragraph_min_length:
                        s1 = jellyfish.jaro_similarity(depend, token_paragraph)
                        s2 = jellyfish.jaro_winkler_similarity(depend, token_paragraph)
                        
                        points = (s1 + s2) / 2
                        
                        if points > paragraph_max_point:
                            paragraph_max_point = points
                            paragraph_similar = depend
                            paragraph_keyword = token_paragraph
                            
                        if points >= paragraph_min_point:
                            return ({
                                'active': False,
                                'checked': True,
                                'error': False,
                                'highlight': highlight,
                                
                                'keyword': token_paragraph,
                                'tag': 'paragraph',
                                'similar-to': depend,
                                'points': round(points, 2),
                                'paragraph-max-point': round(paragraph_max_point, 2),
                                
                                **header_obj
                            })

        paragraph_obj = {
            'paragraph-keyword': paragraph_keyword,
            'paragraph-similar-to': paragraph_similar,
            'paragraph-max-point': round(paragraph_max_point, 2)        
        }
    
    return {
        'active': True,
        'checked': True,
        'error': False,
        'highlight': highlight,
        
        **header_obj,
        **paragraph_obj,
    }

# ------------------------ public function

def view_page(
    url,
    lang='ja',
    timeout=6,
    verify=False,
    depends=None,
    separator=None,
    header_xpath=None,
    paragraph_xpath=None,
    allow_redirects=True,
    header_min_point=0.8,
    paragraph_min_point=0.85,
    targets={
        'absent': True, # page in moved or change or not exited
        'ignorant': False # page is lack of information
    }
):
    try:
        response = requests.get(
            url,
            timeout=timeout,
            allow_redirects=allow_redirects,
            verify=verify
        )
        status_code = response.status_code
        redirected = response.is_redirect
        expired = response.headers.get('Expires')
        expired = expired if expired else (response.headers.get('expires') or False)
        
        if status_code >= 400 and status_code <= 499:
            return {
                'active': False,
                'checked': False,
                'expired': expired,
                'error': f'Client error responses: {status_code}',
                'redirected': redirected,
                'url': response.url,
            }
            
        if status_code >= 500 and status_code <= 599:
            return {
                'active': False,
                'checked': False,
                'expired': expired,
                'error': f'Server error responses: {status_code}',
                'redirected': redirected,
                'url': response.url,
            }
 
        html = response.content
        highlight = __get_highlight(
            html,
            header_xpath,
            paragraph_xpath,
        )
        
        if not (lang == 'ja' or lang == 'en'):
            translate = Translator(from_lang=lang, to_lang='en')
            
            for key in highlight:
                for i in range(0, len(highlight[key])):
                    highlight[key][i] = translate.translate(highlight[key][i])
        
        return {
            **__bad_page(
                highlight,
                separator,
                depends,
                header_min_point,
                paragraph_min_point,
                targets,
            ),
            'expired': expired,
            'redirected': redirected,
            'url': response.url,
        }

    except Exception as error:
        return {
            'active': False,
            'checked': False,
            'error': error,
            'redirected': False,
            'url': url,
        }

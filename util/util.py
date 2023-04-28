from selenium.webdriver.common.by import By
from datetime import datetime
from urllib.parse import urljoin
from gtts import gTTS
import re
import io
import contextlib
import time
import json

with contextlib.redirect_stdout(None):
    import pygame

# general

def time_passed(start, sec):
    return int(time.time()) - start >= sec

def alert_sound(text):
    try:
        sound = io.BytesIO()
        
        gt = gTTS(text)
        gt.write_to_fp(sound)
        
        sound.seek(0)
        
        pygame.mixer.init()
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
    except:
        pass

def now():
    now = datetime.now()
    return now.strftime("%H:%M:%S")

def find(check, items):
    return next((item for item in items if check(item)), None)

def write_file(save_to, content):
        f = open(save_to, "w")
        f.write(content)
        f.close()

#-------------------

# validator

def check_link(link):
    if (
        link and
        link.startswith('http') and
        not 'goo.gl/maps' in link
    ):
        return link
    else:
        return ''
    
#-------------------

# converter

def list_map(work, items):
    return list(map(work, items))

def text_link(text, link):
    return f'''=HYPERLINK("{link}";"{text}")'''

def content_to_text(content):
    text = content['text'] or content['image']
    link = content['link']
    
    return text_link(text, link) if link else text

#-------------------

# getting
def getText(selector):
    try:
        text = selector.text
        return re.sub(r'\s+', ' ', text).strip()
    except:
        return ''

def getHref(base, selector):
    try:
        href = selector.get_attribute('href')
        return urljoin(base, href)
    except:
        return ''

def getSrc(base, selector):
    try:
        src = selector.get_attribute('src')
        return urljoin(base, src)
    except:
        return ''

def get_content(base, selector):
    content = {}
    
    content['text'] = getText(selector)

    try:
        src = selector.get_attribute('src')
        if src:
            content['image'] = urljoin(base, src)
        else:
            img = selector.find_element(By.XPATH, './/img[@src]')
            if img:
                content['image'] = getSrc(base, img)
            else:
                content['image'] = ''
    except:
        content['image'] = ''

    try:
        href = selector.get_attribute('href')
        if href:
            link = urljoin(base, href)
            link = check_link(link)
            content['link'] = link
        else:
            a = selector.find_element(By.XPATH, './/a[@href]')
            if a:
                link = getHref(base, a)
                link = check_link(link)
                content['link'] = link
            else:
                content['link'] = ''
    except:
        content['link'] = ''

    return content

#-------------------
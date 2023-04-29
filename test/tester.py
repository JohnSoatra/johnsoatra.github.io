#!python3
from urllib3.exceptions import InsecureRequestWarning
import requests
from requests_html import HTML
import re


# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

res = requests.get(
    'https://google.com',
    verify=False,
    
)
print(res.url)
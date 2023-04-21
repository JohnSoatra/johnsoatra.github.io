#!python3
from util import util
import requests
import time
import pandas


class Test:
    
    def __init__(self) -> None:
        self.__a = 0
        
    def run(self):
        print(self.__a)

a = Test()
print(a.__a)

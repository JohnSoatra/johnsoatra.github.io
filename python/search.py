#!python3
import requests
import mechanize
import http.cookiejar as cookie

cookie_jar =  cookie.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cookie_jar)
br.open("https://data.digitalfuturelab.jp/login")

br.select_form(nr=0)
br.form['email'] = 'johnsoatra@gmail.com'
br.form['password'] = 'Admin@data'
br.submit()

def getOne(name = 'Bich JENLA'):
    for i in range(1, 50):
        response = requests.get(
            f'https://data.digitalfuturelab.jp/assigns/{i}/edit',
            cookies=cookie_jar
        )
        text = response.text # search with name
        if name in text:
            print(i)
            break

def getAll():
    for i in range(1, 50):
        response = requests.get(
            f'https://data.digitalfuturelab.jp/assigns/{i}/edit',
            cookies=cookie_jar
        )
        text = response.text
        print(f'\n--- {text} ---\n')

getOne('Try Kimtrai')
# getAll()
#!python3
import requests
import mechanize
import http.cookiejar as cookie

cj =  cookie.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)
br.open("https://data.digitalfuturelab.jp/login")

br.select_form(nr=0)
br.form['email'] = 'johnsoatra@gmail.com'
br.form['password'] = 'Admin@data'
br.submit()

a = requests.get('https://data.digitalfuturelab.jp/dashboard?cityId=0&areaId=0', cookies=cj)


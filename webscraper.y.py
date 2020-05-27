
import requests,re
from splinter import Browser
from bs4 import BeautifulSoup
url=r"https://mars.nasa.gov/news/"
from collections import namedtuple
TitleObject=namedtuple("TitleObject","title, body")

#you need to install "Gecko Chromedriver"
#installed
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)

html=requests.get(url).content
news_soup = BeautifulSoup(html, 'html.parser')
#titles=news_soup.findAll("div",class_="content_title")
#slide_elem = news_soup.select_one('ul.item_list li.slide')
#

title_objects=[]
# pull body from website
body = news_soup.findAll('div', class_="rollover_description")
# pull titles and body from website
results = news_soup.findAll('div', class_="slide")
for result in results:
    titles = result.find('div', class_="content_title")
    title = titles.find('a').text
    bodies = result.find('div', class_="rollover_description")
    body = bodies.find('div', class_="rollover_description_inner").text
    print('------------------------------------------------------------------------------------')
    print(title)
    print(body)
    tObj=TitleObject(title=title,body=body)
    title_objects.append(tobj)







"""
elem=news_soup.find("div", class_='content_title')
while elem is not None:
    title=elem.getText()
    print(title)
    titles.append(title)
    elem=elem.findNext("div", class_='content_title')
"""


#our titles are if ormat of:
"""
<div class="content_title">
<a href="[url]" target="_self">[some title]</a>


This is how to find this information by matching patterns in text
"""

#text_pattern=r"<div\sclass='content_title'>(.*?)<a\shref='.*?</a>"
#titles2=re.findall(r"<div\sclass='content_title'>(.*?)<a\shref='.*?</a>",html.decode("utf8").replace("\n",""),re.MULTILINE)

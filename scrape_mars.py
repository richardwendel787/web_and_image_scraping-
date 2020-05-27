import pandas as pd
import requests,re
from splinter import Browser
from bs4 import BeautifulSoup
from collections import namedtuple

def GetNewsTitles():
    url=r"https://mars.nasa.gov/news/"
    #executable_path = {'executable_path': 'chromedriver'}
    #browser = Browser('chrome', **executable_path)
    # html=requests.get(url).content
    #browser.visit(url)
    #html=browser.html
    response = requests.get(url)
    news_soup = BeautifulSoup(response.text, 'html.parser')
    TitleObject=[]
    # pull body from website
    body = news_soup.findAll('div', class_="rollover_description")
    # pull titles and body from website
    title_objects=[]
    results = news_soup.findAll('div', class_="slide")
    for result in results:
        titles = result.find('div', class_="content_title")
        title = titles.find('a').text.replace("\n","").strip()
        bodies = result.find('div', class_="rollover_description")
        body = bodies.find('div', class_="rollover_description_inner").text.replace("\n","").strip()
        #assign the text to variables that we can reference later
        title_objects.append({"title":title,"body":body})
    return pd.DataFrame(title_objects).to_html()

def GetMarsWeather():
    weather={}
    url = ('https://twitter.com/marswxreport?lang=en')
    strformat="InSight "
    strformatend="<a "
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    txt_content=str(soup)
    start=txt_content.find(strformat)
    end=start+txt_content[start:].find(strformatend)
    w=txt_content[start:end].replace("\r\n", " ").replace("\n"," ").strip()
    weather={"weather":[w]}
    return pd.DataFrame(weather).to_html(index=False)

def GetMarsFeatures():
    mars_facts_url = "https://space-facts.com/mars/"
    table = pd.read_html(mars_facts_url)
    table[0]
    df = table[0]
    df.columns = ["Facts", "Value"]
    df.set_index(["Facts"])
    return df.to_html(index=False)



def GetHemisphereImages():
    import http.client
    results=[]
    _TOKEN1="href=\""
    _TOKEN2="<img class=\"wide-image\" src=\""
    host_www_root='https://astrogeology.usgs.gov/'
    hemisphere_url ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    conn=http.client.HTTPSConnection("astrogeology.usgs.gov")
    conn.request("GET","/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
    res=conn.getresponse()
    if str(res.status)!="200":
        print("failure: {}".format(res.status))
        return None
    content=res.read().decode("utf8",errors='ignore')
    soup=BeautifulSoup(content,'html.parser')
    links = soup.find_all("div", class_="item")
    for link in links:
        img_dict = {}
        title = link.find("h3").text.replace("\n","").strip()
        link=str(link)
        start=link.index(_TOKEN1)+len(_TOKEN1) #find the first instands of "href=" from within the tag, and then advance over it
        end=start+link[start:].index("\"") #find the next occurance of the ""\"" character which will be at the end of the url
        link=link[start:end] #using the beginning and end indexes, extract the uri
        #conn=http.client.HTTPSConnection("astrogeology.usgs.gov")
        conn.request("GET",link)
        res=conn.getresponse()
        if str(res.status)!="200":
            print("failure: {}".format(res.status))
        #look for: <img class="wide-image" src="
        content=res.read().decode("utf8",errors='ignore')
        start=content.index(_TOKEN2)+len(_TOKEN2) #find the first instands of "href=" from within the tag, and then advance over it
        end=start+content[start:].index("\"") #find the next occurance of the ""\"" character which will be at the end of the url

        url=host_www_root+content[start:end]
        embedcode="<img src=\""+url+"\">"+title+"</img>"
        results.append({"title":title,"img_url":embedcode})
    return pd.DataFrame(results).to_html(index=False)

def Scrape():
    t1=GetNewsTitles()
    t2=GetMarsWeather()
    t3=GetMarsFeatures()
    t4=GetHemisphereImages()

    html_output="<html><head></head><body>"
    for table in [t1,t2,t3,t4]:
        html_output+="<div>"+table+"</div>"
    html_output+="</body></html>"
    print(html_output)

Scrape()

#from flask import Flask
#app=flask.run(__name__)

#@app.route("/")
def GetIndex():
    return "<html><head></head><body><h1>Hello!</h1></body></html>"

#@app.route("/scrape")
def getScrape():
    return Scrape()


from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

newsTitle=[]
newLine=[]
weather=[]
picUrl=[]
marsImagesList=[]
marsImagesTitle=[]

# Dictionary that contain the output response for all the scrapped data
mars = {
    "title": newsTitle,
    "news": newLine,
    "mars_weather": weather,
    "mars_pic": picUrl,
    "mars_pic_list":marsImagesList,
    "mars_pic_title":marsImagesTitle
}

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    news()   
    weather_info()
    mars_pic()
    mars_fact()
    mars_more_pics()
    # Return results
    return mars

# Below method gets NASA Mars News
def news():
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    # Get new title
    newsTitle.append(soup.find('div', class_='content_title').a.text)
    # Get latest news 
    newLine.append(soup.find('div', class_='article_teaser_body').text)

    browser.quit()
    # Return results
    return "success"

# This method return mars weather
def weather_info():
    browser = init_browser()
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    # Get the mars weather from the latest tweet 
    tweet=soup.find("p",class_="TweetTextSize")
    weather.append(tweet.text.replace(tweet.a.text, ""))
    browser.quit()
    return "Success"    

# Gather mars facts 
def mars_fact():
    browser = init_browser()
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the facts as table
    marsFact=soup.find("table",id="tablepress-p-mars")
    # convert the table into html string
    html_string = f'"""{marsFact}"""'
    # Convert string into dataframe
    mars_facts=pd.read_html(html_string)[0]
    mars_facts_rn=mars_facts.rename(columns={0:"fact",1:"value"})
    # onvert dataframe into dictionary
    mars_facts_dict=mars_facts_rn.to_dict('split')
    mars_facts_dict_data=mars_facts_dict["data"]

    mars["facts"]=mars_facts_dict_data
    browser.quit()

    return "success"      

def mars_pic():
    browser = init_browser()
    JPLMarsUrl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(JPLMarsUrl)
    time.sleep(1)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get featured image of mars
    featured_image_url=soup.find('article',class_='carousel_item')
    featured_image_url = featured_image_url['style'].split("'")[1]
    featured_image_url=f'https://www.jpl.nasa.gov{featured_image_url}'
    picUrl.append(featured_image_url)
    browser.quit()
    return "success"     

def mars_more_pics():

    browser = init_browser()
    marsImages="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(marsImages)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    images=soup.findAll("img",class_="thumb")

    for image in images:
        marsImagesList.append(f'https://astrogeology.usgs.gov{image["src"]}')
        marsImagesTitle.append(f'{image["alt"]}')    
    
    browser.quit()
    return "success"     
    
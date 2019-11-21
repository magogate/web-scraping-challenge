import requests
import bs4
import re
import pandas as pd
from splinter import Browser
from flask import Markup

executable_path = {"executable_path":"chromedriver.exe"}

def getLatestNews():
    baseUrl = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response = requests.get(baseUrl)    
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    newsLists = soup.find_all("div", class_="content_title", limit=1)
    #if u dont define environment variable in path, just give full exe path at below line.
    # D:\Software\chromedriver_win32
    # executable_path = {"executable_path":"D:\\Software\\chromedriver_win32\\chromedriver.exe"}    
    browser = Browser("chrome",**executable_path, headless=False)
    browser.visit(baseUrl)
    soup = bs4.BeautifulSoup(browser.html, "html.parser")
    newsLists = soup.find_all("div", class_="list_text", limit=1)
    news_dict = {}
    for news in newsLists:            
        news_title = news.find("div", class_="content_title").a.text
        news_p = news.find("div", class_="article_teaser_body").text
        news_dict["news_title"] = news_title
        news_dict["news_p"] = news_p
    
    # https://splinter.readthedocs.io/en/0.1/tutorial.html
    browser.quit()
    return news_dict

def getMarsFeaturedImage():
    browser = Browser("chrome",**executable_path, headless=False)
    baseUrl = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(baseUrl)
    soup = bs4.BeautifulSoup(browser.html, "html.parser")
    marsImages = soup.find_all("ul", class_="articles", limit=1)
    featuredImage = {}
    for image in marsImages:
        featured_image_url = "https://www.jpl.nasa.gov/" + image.find("div", class_="img").img["src"]
        featuredImage["feature_image"] = featured_image_url

    browser.quit()
    return featuredImage

def getLatestTwitt():
    browser = Browser("chrome",**executable_path, headless=False)
    baseUrl = "https://twitter.com/marswxreport?lang=en"
    browser.visit(baseUrl)
    soup = bs4.BeautifulSoup(browser.html, "html.parser")
    marsTwitts = soup.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text", limit=1)
    marsLatestTwitt = {}
    for twitt in marsTwitts:        
        mars_weather = twitt.text.replace("apic.twitter.com/iZwojPj9au","").replace("\n","")
        marsLatestTwitt["latest_twitt"] = mars_weather

    browser.quit()
    return marsLatestTwitt

def getMarsFacts():
    browser = Browser("chrome",**executable_path, headless=False)
    baseUrl = "https://space-facts.com/mars/"
    browser.visit(baseUrl)
    soup = bs4.BeautifulSoup(browser.html, "html.parser")
    marsInfo = {}

    tboday = soup.find_all("tbody", limit=1)
    for row in tboday:
        marsInfo[row.find("tr", class_="row-1").find("td", class_="column-1").strong.text] = row.find("tr", class_="row-1").find("td", class_="column-2").text
        marsInfo[row.find("tr", class_="row-2").find("td", class_="column-1").strong.text] = row.find("tr", class_="row-2").find("td", class_="column-2").text
        marsInfo[row.find("tr", class_="row-3").find("td", class_="column-1").strong.text] = row.find("tr", class_="row-3").find("td", class_="column-2").text
        marsInfo[row.find("tr", class_="row-4").find("td", class_="column-1").strong.text] = row.find("tr", class_="row-4").find("td", class_="column-2").text
        marsInfo[row.find("tr", class_="row-5").find("td", class_="column-1").strong.text] = row.find("tr", class_="row-5").find("td", class_="column-2").text
        marsInfo[row.find("tr", class_="row-6").find("td", class_="column-1").strong.text] = row.find("tr", class_="row-6").find("td", class_="column-2").text
        marsInfo[row.find("tr", class_="row-7").find("td", class_="column-1").strong.text] = row.find("tr", class_="row-7").find("td", class_="column-2").text
        marsInfo[row.find("tr", class_="row-8").find("td", class_="column-1").strong.text] = row.find("tr", class_="row-8").find("td", class_="column-2").text
        marsInfo[row.find("tr", class_="row-8").find("td", class_="column-1").strong.text] = row.find("tr", class_="row-9").find("td", class_="column-2").text

    browser.quit()
    # marsDF = pd.DataFrame(marsInfo, index=['1']).T
    # html = Markup(marsDF.to_html())    
    return marsInfo

def getHemisphereImages():
    hemisphere_image_urls = []
    browser = Browser("chrome",**executable_path, headless=False)
    baseUrl = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(baseUrl)
    browser.click_link_by_partial_text('Cerberus')
    soup = bs4.BeautifulSoup(browser.html, "html.parser")
    mars_dict = {}
    cnt = 0
    mars_dict["title"] = "Cerberus Hemisphere"
    images = soup.find_all("div", class_="downloads")
    for image in images:
        for i in image.find_all("li"):
            cnt += 1
            mars_dict["img_url" + str(cnt)] = i.a["href"]
    hemisphere_image_urls.append(mars_dict)

    browser.visit(baseUrl)
    browser.click_link_by_partial_text('Schiaparelli') 
    soup = bs4.BeautifulSoup(browser.html, "html.parser")
    mars_dict = {}
    cnt = 0
    mars_dict["title"] = "Schiaparelli Hemisphere"
    images = soup.find_all("div", class_="downloads")
    for image in images:
        for i in image.find_all("li"):
            cnt += 1            
            mars_dict["img_url" + str(cnt)] = i.a["href"]
    hemisphere_image_urls.append(mars_dict)

    browser.visit(baseUrl)
    browser.click_link_by_partial_text('Syrtis')  
    soup = bs4.BeautifulSoup(browser.html, "html.parser")
    mars_dict = {}
    cnt = 0
    mars_dict["title"] = "Syrtis Major Hemisphere"
    images = soup.find_all("div", class_="downloads")
    for image in images:
        for i in image.find_all("li"):
            cnt += 1            
            mars_dict["img_url" + str(cnt)] = i.a["href"]
    hemisphere_image_urls.append(mars_dict)

    browser.visit(baseUrl)
    browser.click_link_by_partial_text('Valles')  
    soup = bs4.BeautifulSoup(browser.html, "html.parser")
    mars_dict = {}
    cnt = 0
    mars_dict["title"] = "Valles Marineris Hemisphere"
    images = soup.find_all("div", class_="downloads")
    for image in images:
        for i in image.find_all("li"):
            cnt += 1            
            mars_dict["img_url" + str(cnt)] = i.a["href"]
    hemisphere_image_urls.append(mars_dict)
    browser.quit()
    return hemisphere_image_urls

def scrape():
    mars_scrap = {}
    mars_scrap["latest_news"] = getLatestNews()
    mars_scrap["featured_image"] = getMarsFeaturedImage()
    mars_scrap["latest_twitt"] = getLatestTwitt()
    mars_scrap["mars_facts"] = getMarsFacts()
    mars_scrap["hemisphere_images"] = getHemisphereImages()
    return mars_scrap


# scrape()
# print(mars)


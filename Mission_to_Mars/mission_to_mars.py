#!/usr/bin/env python
# coding: utf-8



from bs4 import BeautifulSoup
import requests
import pymongo
import pandas as pd
from splinter import Browser
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():

    all_scrapped = {}


    browser=init_browser()


    # # NASA MARS NEWS

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"


    browser.visit(url)
    time.sleep(5)

    html=browser.html

    soup = BeautifulSoup(html, "html.parser")

    news_title = soup.find("div", class_="content_title").a.text

    news_p = soup.find("div", class_="article_teaser_body").text


    all_scrapped["news_title"] = news_title
    all_scrapped["news_p"] = news_p

    browser.quit()

    ################################
    # # FEATURED IMAGE

    browser=init_browser()

    pic_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(pic_url)

    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(10)
    html = browser.html


    soup = BeautifulSoup(html, "html.parser")


    img = soup.find("div", class_="fancybox-inner").find("img", class_="fancybox-image")["src"]

    featured_image_url = "https://www.jpl.nasa.gov" + img


    all_scrapped["featured_image"] = featured_image_url

    browser.quit()

    ############################################
    # # MARS WEATHER

    browser=init_browser()

    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    html = browser.html

    time.sleep(5)

    soup = BeautifulSoup(html, "html.parser")


    mars_weather = soup.find("div", class_="js-tweet-text-container").p.text

    clean_weather = mars_weather.split("pic.")[0]


    all_scrapped["mars_weather"] = clean_weather

    browser.quit()

    ####################################################
    # # MARS FACTS

    facts_url = "https://space-facts.com/mars/"

    tables = pd.read_html(facts_url)

    df = tables[1]

    df.columns = ["Attribute", "Values"]

    ##df.to_html("mars_facts.html", index = False)

    mars_facts_html = df.to_html(index=False, justify='center')

    all_scrapped["mars_facts_html"] = mars_facts_html

    ##################################################
    # # MARS HEMISPHERES

    browser = init_browser()

    url ="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "lxml")

    img_divs = soup.find_all("div", class_ = "description")

    hemisphere_image_urls = []
    base_url = "https://astrogeology.usgs.gov"
    for img_div in img_divs:
        img_info = {}
        img_title = img_div.find("h3").text
        img_info["img_title"] = img_title
        partial_img_url = img_div.find("a", class_ = "itemLink product-item")["href"]
        full_img_url = base_url + partial_img_url
        browser.visit(full_img_url)
        full_img_url = browser.html
        soup = BeautifulSoup(full_img_url, "lxml")
        img_url = soup.find("div", class_ = "downloads").li.a["href"]    
        img_info["img_url"]=img_url
        hemisphere_image_urls.append(img_info)

    all_scrapped["hemispheres"] = hemisphere_image_urls
    
    browser.quit()


    return all_scrapped



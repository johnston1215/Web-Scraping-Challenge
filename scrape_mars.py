from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C://Chromedriver/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    #Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.
    browser = init_browser()
    data = {}

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    slide = soup.select_one("ul.item_list li.slide")
    data["title"]= slide.find("div", class_="content_title").get_text()
    data["paragraph"] = soup.find("div", class_="article_teaser_body").get_text()
    browser.quit()

    #Use splinter to navigate the site and find the image url for the current Featured Mars Image
    browser = init_browser()
    featpic = {}
    url1 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url1)
    time.sleep(3)

    base_url = "https://www.jpl.nasa.gov"
    browser.links.find_by_partial_text('FULL IMAGE').click()
    time.sleep(3)
    html1 = browser.html
    soup1 = BeautifulSoup(html1, "html.parser")

    featpic = soup1.find("img", class_="fancybox-image")["src"]
    fullurl = base_url+featpic
    data["featpic"]=fullurl
    browser.quit()

    url2 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url2)
    df = tables[0]

    df.rename(columns={0:"Description",1:"Mars"}, inplace=True)
    df = df.set_index('Description')
    data["html_table"] = df.to_html()

    #Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    browser = init_browser()
    url3 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url3)
    time.sleep(3)
    links = browser.find_by_tag("a")

    hemis = []
    for link in links:
        if "Enhanced" in link.text:
            hemis.append(link["href"])

    UrlPics=[]
    for h in hemis:
        browser.visit(h)
        time.sleep(3)
        soup2 = BeautifulSoup(browser.html, "html.parser")
        UrlPics.append("https://astrogeology.usgs.gov"+soup2.find("img", class_="wide-image")["src"])

    data["hemis"] = UrlPics
    browser.quit()

    return data
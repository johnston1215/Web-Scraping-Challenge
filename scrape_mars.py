from splinter import Browser
from bs4 import BeautifulSoup
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C://Chromedriver/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    news = {}

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    slide = soup.select_one("ul.item_list li.slide")
    news["title"]= slide.find("div", class_="content_title").get_text()
    news["paragraph"] = soup.find("div", class_="article_teaser_body").get_text()

    browser.quit()
    return news

    browser1 = init_browser()
    featpic = {}

    url1 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser1.visit(url1)
    time.sleep(1)

    html1 = browser1.html1
    soup1 = BeautifulSoup(html1, "html.parser")

    browser1.links.find_by_partial_text('FULL IMAGE').click()
    #featpic = soup1.find("")

    browser1.quit()
    #print(featpic)

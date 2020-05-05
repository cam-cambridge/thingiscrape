import argparse
import string
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


thingiverse_url = "https://www.thingiverse.com/"
browser = webdriver.Chrome("./chromedrivers/chromedriver81_mac")

def main():
    browser.get(thingiverse_url)
    # home_page = requests.get(thingiverse_url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    browser.close()
    thing_card_header = soup.select('span[class*="ThingCardHeader__"]')
    for thing in thing_card_header:
        print(thing.contents)
    browser.quit()

if __name__ == "__main__":
    main()
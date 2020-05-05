import argparse
import string
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

thingiverse_url = 'https://www.thingiverse.com/'
popular_sort_class = 'button[class*=Sort__dropdownButton--]'
browser = webdriver.Chrome('./chromedrivers/chromedriver81_mac')
def main():
    browser.get(thingiverse_url)
    dropdown = browser.find_elements_by_xpath('//button[starts-with(@class,"Sort__dropdownButton--")]')
    if len(dropdown) == 1:
        dropdown[0].click()
        button = browser.find_elements_by_xpath('//span[contains(text(),"Popular last 7 Days")]')
        button[0].click()
    time.sleep(2)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    browser.close()
    thing_card_header = soup.select('span[class*=ThingCardHeader__]')
    for thing in thing_card_header:
        print(thing.contents)
    browser.quit()

if __name__ == "__main__":
    main()
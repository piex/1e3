#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup

site = 'http://www.jianlaixiaoshuo.com/'


options = webdriver.ChromeOptions()

options.add_argument('headless')
options.add_argument('disable-gpu')

browser = webdriver.Chrome(executable_path="../Tools/chromedriver",
                           chrome_options=options)

browser.get(site)

print(browser.page_source)

dom = BeautifulSoup(browser.page_source, 'lxml')

chapter_list = dom.find_all('dd')

last_chapter = chapter_list[len(chapter_list) - 1]

last_chapter_link = last_chapter.find('a').get('href')

print(last_chapter_link, last_chapter.text)

browser.get(site + last_chapter_link)

print(browser.page_source)

browser.quit()

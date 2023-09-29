import time
from pymongo import MongoClient
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
# from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import json

from bs4 import BeautifulSoup
import requests
import pprint



chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
driver.maximize_window()
driver.get('https://www.gelbeseiten.de/Suche/Solartechnik/Bundesweit')

# soup = BeautifulSoup(html, 'html.parser')
# articles = soup.find_all('article')

previous_height = driver.execute_script(('return document.body.scrollHeight'))

def scroll_down():
  previous_height = driver.execute_script(('return document.body.scrollHeight'))
  while 1:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == previous_height:
      break
    previous_height = new_height

def parse_page(html):
  soup = BeautifulSoup(html, 'html.parser')
  articles =  soup.find_all('article')

  links = []
  for art in articles:
    if l:= art.find_all('a', href=True):
      for a in l:
        if 'https://www.gelbeseiten.de/gsbiz/' in a['href']:
          links.append(a['href'])

  # n = -10
  # if len(links) == 50:
  #   n = -50

  
  print(len(set(links)))
  
  # for i in links[n:]:
  #   try:
      
  #     print('=====================================')
  #     print(i)
  #     page = requests.get(i)
  #     soup2 = BeautifulSoup(page.content, 'html.parser')
      
  #     if name := soup2.find('h1', {'class': 'mod-TeilnehmerKopf__name'}):
  #       print(name.text)

  #   except Exception as e:
  #     print(e.args)
  #     print('niiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiichts')
  
def main():
  popup = driver.find_element_by_xpath("//a[contains(@class,'cmpboxbtn cmpboxbtnyes') ]")
  popup.click()
  while 1:
    scroll_down()
    time.sleep(3)
    html = driver.page_source
    parse_page(html)
    weiter = driver.find_element_by_xpath("//a[contains(@id,'mod-LoadMore--button') ]")
    weiter.click()
  

if __name__ == '__main__':
  main()


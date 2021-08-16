import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait


def main(url):
    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Chrome(
        executable_path=ChromeDriverManager().install(), options=options)
    browser.get(url)
    # xp = browser.find_element_by_xpath(
    #     '//*[@id="business-card"]/div[1]/div/div/div[2]/div/div[3]/div[1]/span/span/div/a/span')
    ele = wait(browser, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//span[text(),'Telefonnummer anzeigen']"))).click()
    print(ele)


if __name__ == '__main__':
    # url = 'https://www.wlw.de/de/firma/megapellet-gmbh-1759830'
    # url = 'https://www.wlw.de/de/firma/advisor-gesellschaft-fuer-energie-und-unternehmensberatung-mbh-1562173'
    # url = 'https://www.wlw.de/de/firma/mark-e-effizienz-gmbh-1430104'
    url = 'https://www.wlw.de/de/firma/ge-getec-holding-gmbh-516284'
    main(url)

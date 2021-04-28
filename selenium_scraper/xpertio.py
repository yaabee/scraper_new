from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import os


if __name__ == '__main__':

    #get set of unique plz from mongo,
    #scrape all architects mit plz bsp bremen
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-notifications")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get('https://www.xpertio.net')
    driver.implicitly_wait(10)
    cookie = driver.find_element_by_id('CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll').click()
    driver.refresh()
    driver.implicitly_wait(10)
    input = driver.find_element_by_id('cphContainer_csbHome_tbFreeText').send_keys('Architekt')
    # ActionChains(driver).move_to_element(input).send_keys('Architekt').perform()

    # cphContainer_csbHome_tbZipOrCity
    plz = driver.find_element_by_id('cphContainer_csbHome_tbZipOrCity').send_keys('28195')
    suchen = driver.find_element_by_id('cphContainer_csbHome_btnSearch').click()
    driver.implicitly_wait(10)
    links = driver.find_elements_by_css_selector('.content-box.lv-search-item.margin-top20')
    for i in links:
        driver.get(i.get_attribute('href'))
        business_class = driver.find_elements_by_css_selector('business-card-title').text
        print(business_class)
    driver.close()



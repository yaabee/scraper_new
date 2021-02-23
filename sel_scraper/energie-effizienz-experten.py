'''
die seite benutzt iframes, wir checken ob selenium taugt
'''
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
# import time
def energie_effizienz_experten(url):
    WINDOW_SIZE = "1920,1080"
    options = Options()
    options.add_argument("--disable--notifications")
    options.add_argument("--incognito")
    options.add_argument("--disable-extension")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-web-security")
    options.add_argument("--no-sandbox")
    # options.add_argument("--headless")

    options.add_argument("--window-size=%s" % WINDOW_SIZE)
    browser = webdriver.Chrome(executable_path=ChromeDriverManager().install() , options=options)
    browser.get(url)
    plz_field = browser.find_element_by_id('tx_wilgebaeudedb_projekt_suche_plz')
    plz_field.send_keys(200)
    try:
        # element = WebDriverWait(browser, 10).until(
        #     EC.presence_of_element_located((By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll'))
        # )
        # element.click()

        energieberatung_check = browser.find_element_by_xpath('/html/body/main/section/div/div/div[1]/div/div/div/form/div[2]/fieldset/label/span/')
        # energieberatung_check.location_once_scrolled_into_view
        actions = ActionChains(browser)
        actions.move_to_element(energieberatung_check).perform()
        energieberatung_check.click()
        effizienzhaus_check = browser.find_element_by_xpath('//*[@id="expert-search-form"]/fieldset[2]/div[1]/label/span')
        effizienzhaus_check.click()

        # effizienzhaus = browser.find_element_by_class_name('f-label')
        # if effizienzhaus.text() == 'Effizienzhaus (KfW)':
        #     print('found effizenz')
        #     effizienzhaus.click()
        # einzelmassnahmen = browser.find_element_by_class_name('f-label')
        # einzelmassnahmen.click()
    finally:
        while 1:
            pass
        browser.quit()

if __name__ == '__main__':
    url_private_bauherren = 'https://www.energie-effizienz-experten.de/fuer-private-bauherren/finden-sie-experten-in-ihrer-naehe'
    url_unternehmen_kommunen = 'https://www.energie-effizienz-experten.de/fuer-unternehmen-und-kommunen/finden-sie-experten-in-ihrer-naehe'
    energie_effizienz_experten(url_private_bauherren)




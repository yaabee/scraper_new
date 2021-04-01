from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os

def set_chrome_options():

    """
    Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """

    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs['download.prompt_for_download'] = 'false'
    chrome_prefs['download.directory_upgrade'] = 'true'
    chrome_prefs['download.default_directory'] = 'home/seluser/downloads'



    return chrome_options

if __name__ == "__main__":

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=set_chrome_options())
    
    driver.get('http://192.168.100.104:1111/')

    #plz 970, download, check header, check len(row) > x
    plz = driver.find_element_by_name('plz').send_keys('97084')
    export = driver.find_element_by_name('Export').click()
    
    
    driver.close()
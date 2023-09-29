from pprint import pprint
import requests
from bs4 import BeautifulSoup
from time import sleep


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")


driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

while True:
    page_num = 1
    page = f"https://klinikradar.de/psychiatrie/kliniken/{page_num}/"
    html = requests.get(page)
    soup = BeautifulSoup(html.content, "html.parser")
    href = soup.find_all("a")
    links = [
        x["href"] for x in href if all(y in x["href"] for y in ["http", "/kliniken/"])
    ]

    for link in links:
        driver.get(link)

        sleep(0.3)
        try:
            xpath = '//a[contains(text(), "Website")]'
            a_tag = driver.find_element_by_xpath(xpath)

            if a_tag:
                href = a_tag.get_attribute("href")
                print(href)
            else:
                print("Link not found.")
        except:
            pass


driver.quit()


print("============================================================")

from selenium import webdriver
import time
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import pyautogui
import ssl
from pymongo import MongoClient


# plz kriegen und dann durch alle loopen

client = MongoClient(
    "192.168.100.8:27017",
    username="mongoroot",
    password="9gCaPFhotG2CNEoBRdgA",
    authSource="admin",
    authMechanism="SCRAM-SHA-256",
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE,
)

# cursor = (
#     str(plz)
#     for plz in client["ZentralerFirmenstamm"]["ZentralerFirmenstamm"].distinct(
#         "PLZ", {"Land": "Deutschland"}
#     )
#     if len(plz) == 5 and plz.isnumeric()
# )

cursor = ["97080", "10115"]

for plz in cursor:
    url = "https://www.elektrohandwerk.de/fachbetriebssuche.html"

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-notifications")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    time.sleep(1)
    # deny cookies
    pyautogui.click(x=700, y=1875)
    time.sleep(1)
    # allow google maps
    pyautogui.click(x=149, y=925)
    time.sleep(1)
    # select address
    pyautogui.click(x=333, y=756)
    pyautogui.write(plz)
    time.sleep(1)
    # click on maps option
    pyautogui.click(x=252, y=814)
    time.sleep(1)
    # filter oeffnen
    pyautogui.click(x=960, y=784)
    # umkreis
    pyautogui.moveTo(x=150, y=969)
    pyautogui.dragTo(222, 968)

    pyautogui.click(x=781, y=761)
    # suchen
    pyautogui.click(x=249, y=811)

    adresse_feld = driver.find_element_by_class_name("fbsSearchField")
    time.sleep(15)
    go = True
    while go:
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        boxes = soup.find_all("div", class_="box1of3")
        for box in boxes:
            if firma := box.find("div", class_="icon"):
                print(firma.find_next("strong").text.strip())
            if adresse := box.find("span", class_="icon pin"):
                for i in adresse.find_next("p").stripped_strings:
                    print(i.strip())
            if telefon := box.find("span", class_="icon tel"):
                print(telefon.find_next("p").text.strip())
            if fax := box.find("span", class_="icon fax"):
                print(fax.find_next("p").text.strip())
            if email := box.find("span", class_="icon mail"):
                print(email.find_next("a").text.strip())
            if webseite := box.select_one('a:contains("Zur")'):
                print(webseite["href"])

            print("========================")
        if next_button := driver.find_element_by_css_selector("a[rel='next']"):
            next_button.click()
        else:
            go = False


if __name__ == "__main__":
    pyautogui.position()

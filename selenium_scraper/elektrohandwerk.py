from urllib.parse import urlsplit
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import pyautogui
import ssl
from pymongo import MongoClient
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from pprint import pprint


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

client_5 = MongoClient(
    "192.168.100.5:27017",
)


def insert_new_dataset_into_mdb(mdb_uri, datenbank, collection, datensatz):
    client = MongoClient(mdb_uri, 27017, maxPoolSize=500)
    db = client[datenbank]
    collection = db[collection]

    if "Error" in datensatz.keys() and not collection.find_one(
        {"PLZ": datensatz["PLZ"]}
    ):
        collection.insert_one(datensatz)
        return

    if not collection.find_one(
        {"Firma": datensatz["Firma"], "Telefon": datensatz["Telefon"]}
    ):
        collection.insert_one(datensatz)


def clean_url(url):
    # Split the URL into components
    url_components = urlsplit(url)

    # Get the netloc (domain)
    domain = url_components.netloc

    # Check if the domain starts with "www."
    if domain.startswith("www."):
        return domain
    else:
        return "www." + domain


bad_plzs = list(client_5["scrp_listen"]["BAD_PLZ"].distinct("PLZ"))
good_plzs = list(client_5["scrp_listen"]["Elektrohandwerk"].distinct("CurrentPLZ"))
print("bad plzs len", len(bad_plzs))
print("good plzs len", len(good_plzs))

cursor = (
    str(plz)
    for e, plz in enumerate(
        client["ZentralerFirmenstamm"]["ZentralerFirmenstamm"].distinct(
            "PLZ", {"Land": "Deutschland"}
        )
    )
    if len(plz) == 5
    and plz.isnumeric()
    and plz not in bad_plzs
    and plz not in good_plzs
    and e % 2 == 0
)


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
    # pyautogui.moveTo(x=150, y=969)
    # pyautogui.dragTo(222, 968)

    pyautogui.click(x=781, y=761)
    # suchen
    pyautogui.click(x=249, y=811)

    try:
        time.sleep(8)
        adresse_feld = driver.find_element_by_class_name("fbsSearchField")
        go = True
        while go:
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            boxes = soup.find_all("div", class_="box1of3")
            for box in boxes:
                complete_ds = {
                    "Firma": "",
                    "StrasseUndNr": "",
                    "PLZ": "",
                    "Ort": "",
                    "Telefon": "",
                    "Fax": "",
                    "Email": "",
                    "Internet": "",
                    "CurrentPLZ": "",
                }
                if firma := box.find("div", class_="dates name"):
                    complete_ds["Firma"] = firma.find_next("strong").text.strip()
                if adresse := box.find("span", class_="icon pin"):
                    split_adresse = list(adresse.find_next("p").stripped_strings)
                    plzUndort = split_adresse[1].split("\xa0")
                    plz_ = plzUndort[0]
                    ort_ = plzUndort[1]
                    complete_ds["StrasseUndNr"] = split_adresse[0]
                    complete_ds["PLZ"] = plz_
                    complete_ds["Ort"] = ort_
                if telefon := box.find("span", class_="icon tel"):
                    complete_ds["Telefon"] = telefon.find_next("p").text.strip()
                if fax := box.find("span", class_="icon fax"):
                    complete_ds["Fax"] = fax.find_next("p").text.strip()
                if email := box.find("span", class_="icon mail"):
                    complete_ds["Email"] = email.find_next("a").text.strip()
                if internet := box.select_one('a:-soup-contains("Zur")'):
                    complete_ds["Internet"] = clean_url(internet["href"])

                if [x for x in complete_ds.values() if x]:
                    complete_ds["CurrentPLZ"] = plz
                    insert_new_dataset_into_mdb(
                        mdb_uri="192.168.100.5",
                        datenbank="scrp_listen",
                        collection=f"Elektrohandwerk",
                        datensatz=complete_ds,
                    )
                    print("========================")
            if next_button := driver.find_element_by_css_selector("a[rel='next']"):
                next_button.click()
            else:
                go = False
                driver.close()

    except Exception as e:
        insert_new_dataset_into_mdb(
            mdb_uri="192.168.100.5",
            datenbank="scrp_listen",
            collection=f"BAD_PLZ",
            datensatz={"PLZ": plz, "Error": e.args},
        )
        driver.close()


if __name__ == "__main__":
    pyautogui.position()

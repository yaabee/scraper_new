
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient, errors
import pprint
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def insert_new_dataset_into_mdb(mdb_uri, datenbank, collection, datensatz):
    client = MongoClient(mdb_uri, 27017, maxPoolSize=500)
    db = client[datenbank]
    collection = db[collection]
    collection.insert_one(datensatz)


def main(url):
    page = requests.get(url)
    if page.ok:
        soup = BeautifulSoup(page.content, "html.parser")
        links = soup.find_all("a", href=True)
        links = [l["href"] for l in links if "/betriebe/" in l["href"]
                 and not '/betriebe/suche' in l['href']]
        pprint.pprint(links, indent=2)
        for link in links:
            data = {
                "Firma": "",
                "StrasseUndNr": "",
                "Ort": "",
                "PLZ": "",
                "Telefon": "",
                "Fax": "",
                "Internet": "",
                "Email": "",
                "Handy": ''
            }
            options = Options()
            options.add_argument('--headless')
            browser = webdriver.Chrome(
                executable_path=ChromeDriverManager().install(), options=options)
            browser.get("https://www.hwk-ufr.de" + link)
            try:
                betrieb_ele = browser.find_element_by_xpath(
                    '//*[@id="content"]/div/div[2]/div[1]/p')
                betrieb_ele = betrieb_ele.text.split('\n')
                print(betrieb_ele)
                data['Firma'] = betrieb_ele[0].strip()
                data['StrasseUndNr'] = betrieb_ele[1].strip()
                data['PLZ'] = betrieb_ele[2].split(
                    ' ')[0].replace('D-', '').strip()
                data['Ort'] = ' '.join(betrieb_ele[2].split(' ')[1:]).strip()
            except Exception as e:
                print(e.args)
                print('betrieb_ele nciht gefunden')
                pass
            try:
                ansprechpartner = browser.find_element_by_xpath(
                    '//*[@id="content"]/div/div[2]/div[2]/p')
                adresse = ansprechpartner.text.split('\n')
                print(adresse)
                for i in adresse:
                    if 'Telefon' in i:
                        data['Telefon'] = i.replace("Telefon", '').strip()
                    elif 'Fax' in i:
                        data['Fax'] = i.replace('Fax', '').strip()
                    elif 'Handy' in i:
                        data['Handy'] = i.replace('Handy', '').strip()
                    elif '@' in i:
                        data['Email'] = i
                    elif 'www' in i:
                        data['Internet'] = i

            except:
                print('ansprechpartner nciht gefunden')
                pass
            print("------------------------------------------------------")
            pprint.pprint(data, indent=2)
            try:
                insert_new_dataset_into_mdb(mdb_uri="192.168.100.5",
                                            datenbank='scrp_listen',
                                            collection='hwk_neu',
                                            datensatz=data)
            except errors.DuplicateKeyError:
                print('had duplicatekey error!!!!!!!!!!!!!!!!!!!!')
                pass


if __name__ == "__main__":
    offset = 7400
    while 1:
        url = f"https://www.hwk-ufr.de/betriebe/suche-78,0,bdbsearch.html?limit=10&search-searchterm=&search-local=&search-job=&search-filter-training=&search-filter-zipcode=(&search-filter-radius=20&search-filter-jobnr=&search-filter-experience=&offset={offset}"
        print('ooooooooooooooooooooooff', offset)
        main(url)
        offset += 10

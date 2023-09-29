from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pprint


def insert_new_dataset_into_mdb(mdb_uri, datenbank, collection, datensatz):
    client = MongoClient(mdb_uri, 27017, maxPoolSize=500)
    db = client[datenbank]
    collection = db[collection]
    collection.insert_one(datensatz)


options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument("--no-sandbox")
options.add_argument("--disable-notifications")
options.add_argument("start-maximized")
options.add_argument("disable-infobars")


driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


def main():
    driver.get("https://www.bsla.ch/de/buero-finden/")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    content = soup.find_all("div", class_="modal-content")
    for i in content:
        ds = dict()
        # print(i)
        if name := i.find("h2", class_="modal-title"):
            ds.update({"Firma": name.contents[0]})
        if offer := i.find("div", class_="bsla_company_offer"):
            for x in offer.contents:
                try:
                    if x:
                        ds.update({"Branche": x.strip()})
                except:
                    pass

        print("---------------------------------------------------")

        if address := i.find("div", class_="bsla_company_address"):
            ls = [x["href"] for x in address.find_all("a")]
            for x in ls:
                if "tel:" in x:
                    ds.update({"Telefon": x.replace("tel:", "")})
                if "mailto" in x:
                    ds.update({"Email": x.replace("mailto:", "")})
                if "https" in x:
                    ds.update({"Homepage": x.replace("https://", "")})

            add = []
            for a in address.contents:
                try:
                    if a.strip():
                        add.append(a.strip())
                except:
                    pass
            strasse = add[0]
            plz = add[1].split()[0]
            ort = add[1].split()[1]
            ds.update({"Straße": strasse})
            ds.update({"PLZ": plz})
            ds.update({"Ort": ort})
            ds.update({"Fax": "xxxxx"})
            print("==========================================")
        pprint.pprint(ds, indent=2)

        insert_new_dataset_into_mdb(
            mdb_uri="192.168.100.5", datenbank="scrp_listen", collection="lithonplus", datensatz=ds
        )


if __name__ == "__main__":
    main()

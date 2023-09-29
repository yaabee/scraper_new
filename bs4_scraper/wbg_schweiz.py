import requests
from bs4 import BeautifulSoup
import pprint
import re
from pymongo import MongoClient


def insert_new_dataset_into_mdb(mdb_uri, datenbank, collection, datensatz):
    client = MongoClient(mdb_uri, 27017, maxPoolSize=500)
    db = client[datenbank]
    collection = db[collection]
    collection.insert_one(datensatz)


def main(url):
    page = requests.post(url)
    soup = BeautifulSoup(page.content, "html.parser")
    soup = soup.find("div", class_="accordion")
    h3s = soup.find_all("h3")
    addresses = soup.find_all("div")
    for x, y in zip(h3s[:100], addresses[:100]):

        ds = dict(
            Firma="xxxxx", Straße="xxxxx", Ort="xxxxx", PLZ="xxxxx", Email="xxxxx", Internet="xxxxx", Fax="xxxxx"
        )

        if name := x.find("a").contents[0]:
            ds.update({"Firma": name})
        if strasse := y.contents[0]:
            if "Postfach" not in strasse:
                ds.update({"Straße": strasse})

        if addresse := y.contents[2]:
            if re.match(r"[0-9]{4}", addresse):
                add = addresse.split()
                ds.update({"PLZ": add[0]})
                ds.update({"Ort": add[1]})

        if email := y.find("a"):
            ds.update({"Email": email["href"].replace("mailto:", "")})
        if inet := y.find("a", class_="button std link-extern"):
            ds.update({"Internet": inet["href"]})

        pprint.pprint(ds, indent=2)

        insert_new_dataset_into_mdb(
            mdb_uri="192.168.100.5", datenbank="scrp_listen", collection="lithonplus", datensatz=ds
        )

        print("-------------------------------------------------")


if __name__ == "__main__":
    url = "https://www.wbg-schweiz.ch/information/wohnbaugenossenschaften_schweiz/mitglieder/genossenschaften"
    main(url)

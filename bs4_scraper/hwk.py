import requests
from bs4 import BeautifulSoup, Tag
from pymongo import MongoClient, errors
import pprint


def insert_new_dataset_into_mdb(mdb_uri, datenbank, collection, datensatz):
    client = MongoClient(mdb_uri, 27017, maxPoolSize=500)
    db = client[datenbank]
    collection = db[collection]
    collection.insert_one(datensatz)


def mainparser(url):
    page = requests.get(url)

    if page.ok:
        soup = BeautifulSoup(page.content, "html.parser")
        links = soup.find_all("a", href=True)
        links = [l["href"] for l in links if "/betriebe/" in l["href"]]
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
                "Branche": "",
                "Landkreis": "",
                "Cache": {'0': [], '1': [], '2': [], '3': []},
            }
            page = requests.get("https://www.hwk-ufr.de" + link)
            soup2 = BeautifulSoup(page.content, "html.parser")
            para = soup2.find_all("p")
            para = [p for p in para if len(para) < 11 and p.find("br")]
            links = [i.select("a[href]") for i in para if i.select("a[href]")]
            if links:
                links = [i.text for i in links[0]]
                inet = [i.replace("--at--", "@")
                        for i in links if "--at--" in i]
                if inet:
                    data['Internet'] = inet[0]
                mail = [i for i in links if "--at--" not in i]
                if mail:
                    data['Email'] = mail[0]
            para = [
                p for p in para if "Handwerkskammer für Unterfranken" not in p.text]
            cache = {}
            if para:
                for e, i in enumerate(para):
                    cache[f'{e}'] = []
                    for x in i:
                        if not isinstance(x, Tag) and x != "Tel. 0931 30908-0 ":
                            cache[f'{e}'].append(x)
                cache = {a: b for a, b in cache.items() if b}
                data["Firma"] = cache['0'][0].strip()
                data["Cache"] = cache
                for l in cache.values():
                    # check if numerals in l
                    if not [char for word in l for char in word if char.isdigit()]:
                        data['Branche'] = l
                    for y in l:
                        # case tele
                        if "Telefon" in y:
                            data["Telefon"] = y.replace("Telefon", "").strip()
                        elif "Fax" in y:
                            data["Fax"] = y.replace("Fax", "").strip()
                        try:
                            data["StrasseUndNr"] = cache['0'][1]
                            data["PLZ"] = cache['0'][2].split(
                                " ")[0].replace("D-", "")
                            data["Ort"] = ' '.join(
                                cache['0'][2].split(" ")[1:])
                            data["Landkreis"] = cache['0'][3]
                        except IndexError as e:
                            data['Adresse'] = cache['0']
                            pass
            pprint.pprint(data, indent=2)
            print("------------------------------------------------------")
            try:
                insert_new_dataset_into_mdb(mdb_uri="192.168.100.5",
                                            datenbank='scrp_listen',
                                            collection='hwk_neu',
                                            datensatz=data)
            except errors.DuplicateKeyError:
                print('had duplicatekey error!!!!!!!!!!!!!!!!!!!!')
                pass
    return


if __name__ == "__main__":
    offset = 0
    while 1:
        url = f"https://www.hwk-ufr.de/betriebe/suche-78,0,bdbsearch.html?limit=10&search-searchterm=&search-local=&search-job=&search-filter-training=&search-filter-zipcode=(&search-filter-radius=20&search-filter-jobnr=&search-filter-experience=&offset={offset}"
        print('ooooooooooooooooooooooff', offset)
        mainparser(url)
        offset += 10

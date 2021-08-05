import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from pymongo import MongoClient
import re
import pprint


def mainparser():
    offset = 0
    url = f"https://www.hwk-ufr.de/betriebe/suche-78,0,bdbsearch.html?limit=10&search-searchterm=&search-local=&search-job=&search-filter-training=&search-filter-zipcode=(&search-filter-radius=20&search-filter-jobnr=&search-filter-experience=&offset={offset}"
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
            }
            page = requests.get("https://www.hwk-ufr.de" + link)
            soup2 = BeautifulSoup(page.content, "html.parser")
            para = soup2.find_all("p")
            para = [p for p in para if len(para) < 11 and p.find("br")]
            links = [i.select("a[href]") for i in para if i.select("a[href]")]
            if links:
                links = [i.text for i in links[0]]
                inet = [i.replace("--at--", "@") for i in links if "--at--" in i]
                mail = [i for i in links if "--at--" not in i]
            if inet:
                data['Internet'] = inet[0]
            if mail:
                data['Email'] = mail[0]
            para = [p for p in para if "Handwerkskammer für Unterfranken" not in p.text]
            cache = {}
            if para:
                for e, i in enumerate(para):
                    cache[e] = []
                    for x in i:
                        if not isinstance(x, Tag) and x != "Tel. 0931 30908-0 ":
                            cache[e].append(x)
                cache = {a: b for a, b in cache.items() if b}
                # pprint.pprint(cache, indent=2)
                data["Firma"] = cache[0][0]
                for k, l in cache.items():
                    for y in l:
                        #case tele
                        if "Telefon" in y:
                            data["Telefon"] = y.replace("Telefon", "").strip()
                        elif "Fax" in y:
                            data["Fax"] = y.replace("Fax", "").strip()
                    for y in l:
                        #case adresse


                        elif len(cache[0]) == 4:
                            data["StrasseUndNr"] = cache[0][1]
                            data["PLZ"] = cache[0][2].split(" ")[0].replace("D-", "")
                            data["Ort"] = ' '.join(cache[0][2].split(" ")[1:])
                        elif len(cache[0]) == 3:
                            data['Adresse'] = cache[0]
                        #case branche !!!

                pprint.pprint(cache, indent=2)
                print('+++++++++++++++++++++++++++++++++++++')
                pprint.pprint(data, indent=2)
                print("------------------------------------------------------")


if __name__ == "__main__":
    mainparser()

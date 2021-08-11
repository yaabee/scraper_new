import requests
import json
import time
import ssl
from pymongo import MongoClient
from functools import lru_cache

# 57b083732db2cb4c1200002b

client = MongoClient(
    "192.168.100.239:27017",
    username="mongoroot",
    password="9gCaPFhotG2CNEoBRdgA",
    authSource="admin",
    authMechanism="SCRAM-SHA-256",
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE,
)

db = client["ZentralerFirmenstamm"]
firmenadresse = db["ZentralerFirmenstamm"]
client_5 = MongoClient("192.168.100.5:27017")
# hallenbau_cache = client_5['GoogleApi']['google_Hallenbau_Hallenbau']
google_api = client_5['GoogleApi']


def insert_new_dataset_into_mdb(mdb_uri, datenbank, collection, datensatz):
    client = MongoClient(mdb_uri, 27017, maxPoolSize=500)
    db = client[datenbank]
    collection = db[collection]
    collection.insert_one(datensatz)


def api_call(plz_or_city, suchbegriff, key, col_name="", place_id=[]):
    query = f"query={suchbegriff}+{plz_or_city}"
    count = 0
    already_in_db = 0
    cache = {}
    while True:
        url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?{query}&key={key}"
        req = requests.get(url)
        req_json = json.loads(req.text)
        count += 1
        for i in req_json["results"]:
            if i["place_id"] not in cache and i['place_id'] not in place_id:
                # append to result
                cache[i["place_id"]] = i["place_id"]
                details = get_places_details(i["place_id"], key)
                try:
                    i["Telefon"] = details["international_phone_number"]
                except KeyError:
                    i["Telefon"] = "xxxxx"
                try:
                    i["website"] = details["website"]
                except KeyError:
                    i["website"] = "xxxxx"
                i["formatted"] = True
                # add plz, ort, stra
                splitted_address = i["formatted_address"].split(",")
                if len(splitted_address) == 3:
                    try:
                        plz_und_ort = splitted_address[1].strip().split(" ")
                        i["StrasseUndNr"] = splitted_address[0]
                        i["PLZ"] = plz_und_ort[0]
                        i["Ort"] = plz_und_ort[1]
                        i["legit_address"] = True
                    except (KeyError, IndexError):
                        i["StrasseUndNr"] = "xxxxx"
                        i["PLZ"] = "xxxxx"
                        i["Ort"] = "xxxxx"
                        i["legit_address"] = False
                else:
                    i["StrasseUndNr"] = "xxxxx"
                    i["PLZ"] = "xxxxx"
                    i["Ort"] = "xxxxx"
                    i["legit_address"] = False
                # write too db
                insert_new_dataset_into_mdb(
                    mdb_uri="192.168.100.5",
                    datenbank="GoogleApi",
                    collection=f"google_{suchbegriff}_{col_name}",
                    datensatz=i,
                )
            if i['place_id'] in place_id:
                already_in_db += 1

        # next page & break con
        new_token = 0
        if "next_page_token" in req_json and new_token < 2:
            new_token += 1
            time.sleep(4)
            next_page = req_json["next_page_token"]
            query = f"pagetoken={next_page}"
        else:
            print('already_in_db', already_in_db)
            return count


@lru_cache(maxsize=None)
def get_places_details(place_id, key):
    url = (
        f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&"
        f"fields=formatted_phone_number,international_phone_number,website&key={key}"
    )
    get_details = requests.get(url)
    details_json = json.loads(get_details.text)["result"]
    return details_json


big_citys = [
    "Berlin",
    "Hamburg",
    "München",
    "Köln",
    "Frankfurt",
    "Stuttgart",
    "Düsseldorf",
    "Leipzig",
    "Dortmund",
    "Essen",
    "Bremen",
    "Dresden",
    "Hannover",
    "Nürnberg",
    "Duisburg",
    "Bochum",
    "Wuppertal",
    "Bielefeld",
    "Bonn",
    "Münster",
    "Karlsruhe",
    "Mannheim",
    "Augsburg",
    "Wiesbaden",
    "Mönchengladbach",
    "Gelsenkirchen",
    "Braunschweig",
    "Kiel",
    "Aachen",
    "Chemnitz",
    "Halle",
    "Magdeburg",
    "Freiburg im Breisgau",
    "Krefeld",
    "Lübeck",
    "Mainz",
    "Erfurt",
    "Oberhausen",
    "Rostock",
    "Kassel",
    "Hagen",
    "Saarbrücken",
    "Hamm",
    "Potsdam",
    "Ludwigshafen am Rhein",
    "Mülheim an der Ruhr",
    "Oldenburg",
    "Osnabrück",
    "Leverkusen",
    "Heidelberg",
    "Solingen",
    "Darmstadt",
    "Herne",
    "Neuss",
    "Regensburg",
    "Paderborn",
    "Ingolstadt",
    "Offenbach am Main",
    "Würzburg",
    "Fürth",
    "Ulm",
    "Heilbronn",
    "Pforzheim",
    "Wolfsburg",
    "Göttingen",
    "Bottrop",
    "Reutlingen",
    "Koblenz",
    "Bremerhaven",
    "Recklinghausen",
    "Bergisch Gladbach",
    "Erlangen",
    "Jena",
    "Remscheid",
    "Trier",
    "Salzgitter",
    "Moers",
    "Siegen",
    "Hildesheim",
    "Cottbus",
    "Bautzen",
    "Detmold",
    "Berlin",
    "Frankfurt / Oder",
    "Oranienburg",
    "Herford",
    "Wuppertal",
    "Wiesbaden",
    "Villingen-Schwenningen",
    "Landshut",
    "Kempten",
    "Amberg",
    "Passau",
    "Hof",
    "Bamberg",
    "Gütersloh",
    "Suhl",
]

# PLZ = ['80', '81', '82','83','84','85','86','87',
#       '90','91','92','93','94','95','96','97']

cursor = list(firmenadresse.find({"PLZ": {"$regex": "^9"}}))
cache_plz = {}
plzs = [x["PLZ"] for x in cursor]
for a in plzs:
    if (
        a not in cache_plz
        and len(a) == 5
        and a[1] != "8"
        and a[1] != "9"
        and a.isnumeric()
    ):
        cache_plz[a] = a
first = list(cache_plz.values())
plz = first[::3]

if __name__ == "__main__":
    # key = 'AIzaSyD_PdV1xDgjKOAurk3SWWsoOb4Lj3Jz8BU'  # franz key
    key = "AIzaSyDRGsKy8xvOixFivn2bCaaWpgO-SKhyNOo"  # nue key

    db = client_5['GoogleApi']
    cache = []
    for col in db.list_collection_names():
        cursor = db[col].distinct('place_id')
        cache += list(set(cursor))
    print(len(cache))
    count_apicalls = 0
    suchbegriff = "tga"
    plz_or_city = plz
    for i in plz_or_city:
        count_apicalls += api_call(
            i, suchbegriff,
            key, col_name=suchbegriff,
            place_id=cache
        )
        final_result = dict(anzahl_api_calls=count_apicalls)
        print(final_result)
        print(get_places_details.cache_info())
        print("====================================")
        # pass

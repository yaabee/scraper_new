from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional
import pandas as pd
import requests
import json
import time
import ssl
from pymongo import MongoClient
from functools import lru_cache
from pprint import pprint


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


def insert_new_dataset_into_mdb(mdb_uri, datenbank, collection, datensatz):
    client = MongoClient(mdb_uri, 27017, maxPoolSize=500)
    db = client[datenbank]
    collection = db[collection]
    collection.insert_one(datensatz)

# @dataclass
# class Location:
#     lat: float = 0
#     lng: float = 0

# @dataclass
# class Viewport:
#     northeast: Location = Location()
#     southwest: Location = Location()

# @dataclass
# class Geometry:
#     location: Location = Location()
#     viewport: Viewport = Viewport()

# @dataclass
# class OpeningHours:
#     open_now: Optional[bool] = False

# @dataclass
# class Photo:
#     height: int = 0
#     photo_reference: str = ''
#     width: int = 0
#     html_attributions: List[str] = field(default_factory=list)

# @dataclass
# class PlusCode:
#     compound_code: str = ''
#     global_code: str = ''

# @dataclass()
# class PlaceData:
#     business_status: str = ''
#     formatted_address: str = ''
#     geometry: Geometry = Geometry()
#     icon: str = ''
#     icon_background_color: str = ''
#     icon_mask_base_uri: str = ''
#     name: str = ''
#     opening_hours: OpeningHours = OpeningHours()  # Use the OpeningHours data class here
#     photos: Photo = Photo()  # Use the Photo data class here
#     place_id: str =''
#     plus_code: PlusCode = PlusCode()  # Use the PlusCode data class here
#     rating: float = 0
#     reference: str = ''
#     user_ratings_total: int = 0
#     types: List[str] = field(default_factory=list)  # Use the List of str directly for types

@dataclass
class Datensatz:
    StrasseUndNr: str = 'xxxxx'
    PLZ: str = 'xxxxx'
    Ort: str = 'xxxxx'
    legit_address: bool = False
    Telefon: str = 'xxxxx'
    Website: str = 'xxxxx'
    name: str = 'xxxxx'

def api_call(suchbegriff, key,col_name):
    params = {
    'query':suchbegriff,
    'key': key,
    }

    count = 0
    while True:
        # url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?{query}&key={key}"
        url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'

        results = requests.get(url, params=params).json()['results']

        count += 1

        for i in results[:1]:
            ds = Datensatz()
            details = get_places_details(i['place_id'], key)
            ds.Telefon = details.get("international_phone_number", "xxxxx")
            ds.Website = details.get("website", "xxxxx")
            ds.name = i.get('name', 'xxxxx')

            # add plz, ort, stra
            splitted_address = i['formatted_address'].split(",")
            if len(splitted_address) == 3:
                try:
                    plz_und_ort = splitted_address[1].strip().split(" ")
                    ds.StrasseUndNr = splitted_address[0]
                    ds.PLZ = plz_und_ort[0]
                    ds.Ort = plz_und_ort[1]
                    ds.legit_address = True
                except (KeyError, IndexError):
                    pass
                

            insert_new_dataset_into_mdb(
                mdb_uri="192.168.100.5",
                datenbank="GoogleApi",
                collection=f"google_{col_name}",
                datensatz=asdict(ds),
                )
            continue

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



begriffen = []

if __name__ == "__main__":
    # key = "AIzaSyD_PdV1xDgjKOAurk3SWWsoOb4Lj3Jz8BU"  # franz key
    # key = "AIzaSyDRGsKy8xvOixFivn2bCaaWpgO-SKhyNOo"  # nue key
    # key = "AIzaSyB4FQ8AkpBHa_5PXlhMpfylActZlZVKwvw"  # nue neu!
    key = 'AIzaSyByBRhsu7I6dQ3iE7MMy9Xcjx9G7yhZcjg' # teleaktivdev@gmail.com teleaktivdeveloper1996

    file = pd.read_excel('/home/user199/Desktop/master_listen/intersolar.xlsx')
    selected_column_index = 0  
    selected_column = file.iloc[:, selected_column_index]

    count_apicalls = 0
    collection_name = "Intersolar"

    for begriff in selected_column:
        count_apicalls += api_call(
            begriff,key, col_name=collection_name
        )
        final_result = dict(anzahl_api_calls=count_apicalls)
        print(final_result)
        print(get_places_details.cache_info())
        print("====================================")

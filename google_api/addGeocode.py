from typing import List, Literal, TypedDict, Any
from pymongo import MongoClient
from bson import ObjectId
from pprint import pprint
import requests
from tqdm import tqdm
import csv


class GoogleDatensatz(TypedDict):
    Ort: str  #'Berlin'
    PLZ: str  #'12277'
    StrasseUndNr: str  #'Motzener Str. 10A',
    Telefon: str  #'+49 30 71302620',
    _id: ObjectId
    business_status: str  #'OPERATIONAL',
    formatted_address: str  # 'Motzener Str. 10A, 12277 Berlin, Germany',
    geometry: Any  #
    icon: str  #'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/generic_business-71.png',
    icon_background_color: str  #'7B9EB0',
    icon_mask_base_uri: str  #'https://maps.gstatic.com/mapfiles/place_api/icons/v2/generic_pinlet',
    legit_address: bool  # True,
    name: str  #'e-vis',
    opening_hours: Any  # {'open_now': False},
    place_id: str  #'ChIJbVolZ3tFqEcRyfWTa0tGaZ0',
    plus_code: Any  # {'compound_code': 'C94G+RR Berlin', 'global_code': '9F4MC94G+RR'},
    rating: int  # 5,
    reference: str  #'ChIJbVolZ3tFqEcRyfWTa0tGaZ0',
    types: Literal["point_of_interest", "establishment"]
    user_ratings_total: int  # 4,
    website: str  #'http://www.e-vis.de/'
    StrassenId: str
    Suchbegriff: str
    ZFID: str
    Neuangelegt: bool


class GeocodeResult(TypedDict):
    geocode: Any
    plz: List[str]


class GeocodeResponse(TypedDict):
    ok: bool
    result: GeocodeResult


def addGeocodeFuerGoogleApi():
    client = MongoClient("192.168.100.5:27017")

    collection_names = [
        "google_Photovoltaik Anbieter_Photovoltaik Anbieter",
        "google_Solaranlageninstallationsservice_Solaranlageninstallationsservice",
        "google_Solaranlagentechnik Installateure_Solaranlagentechnik Installateure",
        "google_Solartechnikanbieter_Solartechnikanbieter",
        "google_Solartechnikservice_Solartechnikservice",
    ]

    for col in (client["GoogleApi"][col_name] for col_name in collection_names):
        for datensatz in tqdm(list(col.find({}))):
            ds: GoogleDatensatz = datensatz

            geocode: GeocodeResponse = requests.post(
                "http://192.168.100.239:9099/geocoder",
                json={
                    "Land": "Deutschland",
                    "Ort": ds["Ort"],
                    "PLZ": ds["PLZ"],
                    "StrasseUndNr": ds["StrasseUndNr"],
                    "options": {"returnMultiple": False},
                },
            ).json()

            suchbegriff = " ".join(
                list(set(x.lower() for x in col.name.split("_") if x and x != "google"))
            )

            if geocode["ok"]:
                strassen_id = geocode["result"]["geocode"]["StrassenId"]

                update = col.update_one(
                    {"_id": ds["_id"]},
                    {"$set": {"StrassenId": strassen_id, "Suchbegriff": suchbegriff}},
                )
            else:
                # kein geocode
                update = col.update_one(
                    {"_id": ds["_id"]},
                    {"$set": {"StrassenId": "xxxxx", "Suchbegriff": suchbegriff}},
                )
            # print(ds)
            # input()


class ZfNeuanlageResult(TypedDict):
    document: Any
    id: str
    neuangelegt: bool


class ZfAdresseNeuanlageResponse(TypedDict):
    ok: bool
    result: ZfNeuanlageResult


def addZFIDFuerGoogleApi():
    client = MongoClient("192.168.100.5:27017")

    collection_names = [
        "google_Photovoltaik Anbieter_Photovoltaik Anbieter",
        "google_Solaranlageninstallationsservice_Solaranlageninstallationsservice",
        "google_Solaranlagentechnik Installateure_Solaranlagentechnik Installateure",
        "google_Solartechnikanbieter_Solartechnikanbieter",
        "google_Solartechnikservice_Solartechnikservice",
    ]

    for col in (client["GoogleApi"][col_name] for col_name in collection_names):
        for datensatz in tqdm(
            list(
                col.find(
                    {
                        "ZFID": {"$exists": False},
                        "StrassenId": {"$ne": "xxxxx"},
                        "Telefon": {"$ne": "xxxxx"},
                    }
                )
            )
        ):
            ds: GoogleDatensatz = datensatz
            payload = dict(
                Firma=ds["name"],
                Straße=ds["StrasseUndNr"],
                PLZ=ds["PLZ"],
                Ort=ds["Ort"],
                Telefon=ds["Telefon"],
                Internet=ds["website"],
                Fax="xxxxx",
                options={
                    "ensureWrite": False,
                    "forceInsert": False,
                    "returnDocument": False,
                },
            )
            r: ZfAdresseNeuanlageResponse = requests.post(
                "http://192.168.100.239:9099/zf_adresse_neuanlageNachAccess",
                json=payload,
            ).json()
            if r["ok"]:

                update = col.update_one(
                    {"_id": ds["_id"]},
                    {
                        "$set": {
                            "ZFID": r["result"]["id"],
                            "Neuangelegt": r["result"]["neuangelegt"],
                        }
                    },
                )
            else:
                # kein geocode
                update = col.update_one(
                    {"_id": ds["_id"]},
                    {
                        "$set": {
                            "ZFID": r["result"]["id"],
                            "Neuangelegt": r["result"]["neuangelegt"],
                        }
                    },
                )
            # print(r["result"]["id"])
            # print(r["result"]["neuangelegt"])
            # input()


def csvZFID():
    client = MongoClient("192.168.100.5:27017")

    collection_names = [
        "google_Photovoltaik Anbieter_Photovoltaik Anbieter",
        "google_Solaranlageninstallationsservice_Solaranlageninstallationsservice",
        "google_Solaranlagentechnik Installateure_Solaranlagentechnik Installateure",
        "google_Solartechnikanbieter_Solartechnikanbieter",
        "google_Solartechnikservice_Solartechnikservice",
    ]

    with open("ZFIDs.csv", "w", newline="") as file:
        for col in (client["GoogleApi"][col_name] for col_name in collection_names):
            for datensatz in tqdm(
                list(
                    col.find(
                        {
                            "ZFID": {"$exists": True},
                        }
                    )
                )
            ):
                ds: GoogleDatensatz = datensatz
                writer = csv.DictWriter(file, fieldnames=["ZFID"])
                writer.writerow({"ZFID": ds["ZFID"]})


if __name__ == "__main__":
    # addGeocodeFuerGoogleApi()
    # addZFIDFuerGoogleApi()
    # csvZFID()
    pass

from typing import TypedDict
import pandas as pd
from pymongo import MongoClient
import ssl
import requests


client_8 = MongoClient(
    "mongodb://mongoroot:9gCaPFhotG2CNEoBRdgA@192.168.100.8:27017",
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE,
)


def getDataFrame(filepath):
    file = pd.read_excel(filepath)
    return pd.DataFrame(file).fillna("")


class resHausnummer(TypedDict):
    firma_hausnummer: str
    firma_strasse: str
    resultUsable: bool


def cleanHausnummer(hausnummer: str, default=None) -> resHausnummer:
    # clean inital field
    if len(hausnummer) > 6:
        hausnummer = "xxxxx"

    return requests.post(
        "http://192.168.100.239:9099/004hausnummern",
        json={"firma_strasse": i["Straße gm"]},
    ).json()
    # error handling


class resSanitizeStrasse(TypedDict):
    strasse_sanitized: str


def sanitizeStrasse(strasse: str, default=None) -> resSanitizeStrasse:
    return requests.post(
        "http://192.168.100.239:9099/027_sanitize_strasse",
        json={"firma_strasse": strasse},
    ).json()
    # error handling


class resPhone(TypedDict):
    firma_telefon: str
    firma_telefon_clean: str
    firma_telefon_ursprung: str


def cleanPhone(telefon: str, default=None) -> resPhone:
    # clean tele
    return requests.post(
        "http://192.168.100.239:9099/005phonenumbers",
        json={"firma_telefon": telefon},
    ).json()
    # error handling


def cleanPLZ(plz: str, default=None) -> str:
    if plz:
        plz = str(int(plz))
        if len(plz) == 4:
            plz = f"0{plz}"
    return plz


def dubletteZuId(zfid: str) -> str:
    cursor = client_8["ZentralerFirmenstamm"]["ZentralerFirmenstamm"].find_one(
        {"ZFID": zfid}, {"DubletteZuId": 1}
    )
    if cursor:
        return cursor["DubletteZuId"]
    return zfid


if __name__ == "__main__":
    frame = getDataFrame("/home/user199/Downloads/projektentwickler_champion.xlsx")
    count = 0
    gesamt = 0
    for index, i in frame.iterrows():
        count += 1

        if 1:
            print(i)
            # id = dubletteZuId(str(i["ZFID"]))
            # if id:
            #     update = client_8["ZentralerFirmenstamm"][
            #         "ZentralerFirmenstamm"
            #     ].update_one(
            #         {"ZFID": id},
            #         {
            #             "$addToSet": {
            #                 "Meta.BranchenDetails.Extern": {
            #                     "Name": "planer_hochbau/2",
            #                     "WZCode": 227111200,
            #                     "Herkunft": "20220913_Neuanlage_TA_WEDI",
            #                 }
            #                 # "Strassenname": sanitizeStrasse["strasse_sanitized"],
            #                 # "StrasseUndNr": strasseUndnr,
            #                 # "PLZ": plz,
            #                 # "Ort": ort,
            #                 # "Hausnummer": hausnummer,
            #                 # "Firma": firma,
            #                 # "Email": email,
            #                 # "Homepage": homepage,
            #                 # "Telefon": clean["firma_telefon"],
            #                 # "TelefonRaw": clean["firma_telefon_clean"],
            #                 # "Firma2": firma2,
            #             }
            #         },
            #     )
            # print(update.modified_count, id)
            # print("-----------------------------------------")


# update = client_8["ZentralerFirmenstamm"]["ZentralerFirmenstamm"].update_one(
#     {"ZFID": {"$in": [zfid, dubletteZuId]}},
#     {
#         "$set": {
#             "Meta.IstInaktiv": True,
#             "Meta.Inaktiv.Grund": i["Grund"],
#             "Meta.Inaktiv.Seit": datetime.utcnow().isoformat()[:-3] + "Z",
#             "Meta.Exportierbar": False,
#             "Meta.Geaendert.Am": datetime.utcnow().isoformat()[:-3] + "Z",
#         }
#     },
# )

# ort = i["Ort gm"] if i["Ort gm"] else i["Ort_ZF"]
# firma = i["Firmenname gm"] if i["Firmenname gm"] else i["Firma"]
# email = i["email gm"] if i["email gm"] else i["Email"]
# homepage = i["Homepage gm"] if i["Homepage gm"] else i["Web"]
# telefon = i["Telefon gm"] if i["Telefon gm"] else i["Telefon"]
# firma2 = i["Firma 2gm"] if i["Firma 2gm"] else i["Firma_2"]
# plz = plz if plz else i["PLZ_ZF"]

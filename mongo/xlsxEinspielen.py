from typing import Any
import requests
import pandas as pd
from pprint import pprint
from pymongo import MongoClient
import ssl

client_8 = MongoClient(
    "mongodb://mongoroot:9gCaPFhotG2CNEoBRdgA@192.168.100.8:27017",
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE,
)


def is_geo_valid(land: str, ort: str, plz: str, strasse_und_nr: str) -> bool:
    """momentan nur Deutschland?"""
    payload_geocoder = {
        "Land": land,
        "Ort": ort,
        "PLZ": plz,
        "StrasseUndNr": strasse_und_nr,
        "options": {"returnMultiple": False},
    }
    check = requests.post(
        "http://192.168.100.239:9099/geocoder", json=payload_geocoder
    ).json()

    if check["ok"]:
        return True
    return False


def xlsxEinspielen(path, branche, tmpDb):
    """Firma aus XLSX importieren"""
    count = 0
    gesamt = 0
    file = pd.read_excel(path)

    frame: pd.DataFrame = (file).fillna("xxxxx")
    for index, row in frame.iterrows():

        # if is_geo_valid(
        #     land=str("Deutschland"),
        #     ort=str(row["Ort"]),
        #     # plz=str(row[""]),
        #     plz="xxxxx",
        #     strasse_und_nr=str(row["Str. / HausNr"]),
        # ):
        if True:
            payload = {
                "options": {
                    "ensureWrite": False,
                    "forceInsert": False,
                    "returnDocument": False,
                },
                "Firma": "",
                "PLZ": "",
                "Ort": "",
                "Telefon": "",
                "Straße": "",
                "Email": "",
                "Internet": "",
                "Fax": "xxxxx",
            }

            if len(str(row["PLZ"])) == 4:
                row["PLZ"] = "0" + str(row["PLZ"])

            payload = {
                "options": {
                    "ensureWrite": False,
                    "forceInsert": False,
                    "returnDocument": False,
                },
                "Firma": row["Unternehmen"],
                "PLZ": str(row["PLZ"]),
                "Ort": row["Ort"],
                "Telefon": str(row["Tel. Nr."]),
                "Straße": row["Str. / HausNr"],
                # "Email": row["E-Mail"],
                "Email": "xxxxx",
                "Internet": row["Homepage"],
                "Fax": "xxxxx",
            }
            url = "http://192.168.100.239:9099/zf_adresse_neuanlageNachAccess"
            r = requests.post(url, json=payload).json()
            print(r)
            # in tmp collection einpsielen
            client_8["yb"][tmpDb].insert_one(
                {"ZFID": r["result"]["id"], "Firma": row["Unternehmen"]}
            )

            update = client_8["ZentralerFirmenstamm"][
                "ZentralerFirmenstamm"
            ].update_one(
                {"ZFID": r["result"]["id"]},
                {
                    "$addToSet": {
                        "Meta.BranchenDetails.Extern": branche,
                    }
                },
            )
            update = client_8["ZentralerFirmenstamm"][
                "ZentralerFirmenstamm"
            ].update_one(
                {"ZFID": r["result"]["id"]},
                {
                    "$set": {
                        "Meta.Branchen": [branche["WZCode"]],
                    }
                },
            )

            print("update", r, update.modified_count)
            pprint(payload)
            count += 1
        gesamt += 1
        print(gesamt)
        print(count)


if __name__ == "__main__":
    branche = {
        "Herkunft": "Top_100_Projektentwickler_Deutschland_Investvolumen_2008-2015_bearb_gm",
        "WZCode": 216841400,
        "Name": "projektentwickler/1",
    }
    xlsxEinspielen(
        "/home/user199/Downloads/Top_100_Projektentwickler_Deutschland_Investvolumen_2008-2015_bearb_gm.xlsx",
        branche,
        "Top_100_Projektentwickler_Deutschland_Investvolumen_2008-2015_bearb_gm",
    )

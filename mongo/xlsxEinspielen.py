import json
import requests
import pandas as pd
from pprint import pprint
from pymongo import MongoClient
import ssl
from dataclasses import asdict
from YB_TYPES.custom_types import PayloadDublettencheck, Branche


def save_list_to_text_file(file_path, string_list):
    try:
        with open(file_path, "w") as file:
            for item in string_list:
                file.write("%s\n" % item)
        print(f"Saved {len(string_list)} strings to {file_path}")
    except Exception as e:
        print(f"Error: {e}")


client_8 = MongoClient(
    "mongodb://mongoroot:9gCaPFhotG2CNEoBRdgA@192.168.100.8:27017",
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE,
)

ZF_8 = client_8["ZentralerFirmenstamm"]["ZentralerFirmenstamm"]


def xlsxEinspielen(path: str, branche: Branche, tmpDb: str, is_testing: bool):
    if is_testing:
        print("is testing")
        return

    count = 0
    gesamt = 0
    file = pd.read_excel(path)

    frame: pd.DataFrame = (file).fillna("xxxxx")
    failures = []
    for index, row in frame.iterrows():
        # if is_geo_valid(
        #     land=str("Deutschland"),
        #     ort=str(row["Ort"]),
        #     # plz=str(row[""]),
        #     plz="xxxxx",
        #     strasse_und_nr=str(row["Str. / HausNr"]),
        # ):
        if True:
            payload: PayloadDublettencheck = PayloadDublettencheck()

            if type(row["PLZ_Ort"]) == int:
                row["PLZ_Ort"] = "'" + str(row["PLZ_Ort"])
            else:
                row["PLZ_Ort"] = row["PLZ_Ort"].split(" ")[0]

            # if len(str(row["Shipping Zip/Postal Code"])) == 4:
            #     row["Shipping Zip/Postal Code"] = "0" + str(row["Shipping Zip/Postal Code"])
            # print(str(row["Shipping Zip/Postal Code"]))

            payload.Firma = row.Firma
            payload.PLZ = row.PLZ_Ort
            payload.Ort = row.Ort1
            payload.Telefon = str(row.Telefon)
            payload.Straße = row.Adresse2
            payload.Email = row.Email
            payload.Internet = "xxxxx"
            payload.Fax = "xxxxx"

            url = "http://192.168.100.239:9099/zf_adresse_dubcheck"
            r = requests.post(url, json=asdict(payload)).json()

            if not r["result"]["id"]:
                failures.append(json.dumps(asdict(payload)))

            # url = "http://192.168.100.239:9099/zf_adresse_neuanlageNachAccess"
            # r = requests.post(url, json=payload).json()
            # print(r)
            # # in tmp collection einpsielen
            # client_8["yb"][tmpDb].insert_one(
            #     {"ZFID": r["result"]["id"], "Firma": row["Unternehmen"]}
            # )
            else:
                update = ZF_8.update_one(
                    {"ZFID": r["result"]["id"]},
                    {
                        "$addToSet": {
                            "Meta.BranchenDetails.Extern": branche,
                        }
                    },
                )
                update = ZF_8.update_one(
                    {"ZFID": r["result"]["id"]},
                    {
                        "$addToSet": {
                            "Meta.Branchen": branche.WZCode,
                        }
                    },
                )
                print("update", r, update.modified_count)
                count += 1
        gesamt += 1
        print(gesamt)
        print(count)
    save_list_to_text_file("./failures.txt", failures)


if __name__ == "__main__":
    branche = Branche(Herkunft="", WZCode=0, Name="")

    xlsxEinspielen(
        # '/home/user199/Desktop/ausf_hkls,1.xlsx',
        # path='/home/user199/Desktop/master_listen/google_intersolar.xlsx',
        path="/home/user199/Downloads/20210315_fehlende_Städte_größer_20000.xlsx",
        branche=branche,
        tmpDb="Test",
        is_testing=True,
    )

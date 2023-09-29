import json
import requests
import pandas as pd
from pprint import pprint
from pymongo import MongoClient
import ssl
from dataclasses import dataclass, asdict


def save_list_to_text_file(file_path, string_list):
    try:
        with open(file_path, 'w') as file:
            for item in string_list:
                file.write("%s\n" % item)
        print(f'Saved {len(string_list)} strings to {file_path}')
    except Exception as e:
        print(f'Error: {e}')

client_8 = MongoClient(
    "mongodb://mongoroot:9gCaPFhotG2CNEoBRdgA@192.168.100.8:27017",
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE,
)

ZF_8 = client_8['ZentralerFirmenstamm']['ZentralerFirmenstamm']


@dataclass
class PayloadDublettencheckOptions:
    returnDocument: bool = False

@dataclass
class PayloadDublettencheck:
    options: PayloadDublettencheckOptions = PayloadDublettencheckOptions()
    Firma: str = ''
    PLZ: str = ''
    Ort: str = ''
    Telefon: str = ''
    Straße: str = ''
    Email: str = 'xxxxx'
    Internet: str = 'xxxxx'
    Fax: str = 'xxxxx'

@dataclass
class Branche:
    Herkunft: str
    WZCode: int
    Name: str


def xlsxEinspielen(path: str, branche: Branche, tmpDb: str, is_testing: bool):

    count = 0
    gesamt = 0
    file = pd.read_excel(path)

    frame: pd.DataFrame = (file).fillna("xxxxx")
    failures = []
    for index, row in frame.iterrows():


        payload: PayloadDublettencheck = PayloadDublettencheck()

        if type(row['PLZ_Ort']) == int:
            row['PLZ_Ort'] = "'" + str(row['PLZ_Ort'])
        else:
            row["PLZ_Ort"] = row['PLZ_Ort'].split(' ')[0]


        # if len(str(row["Shipping Zip/Postal Code"])) == 4:
        #     row["Shipping Zip/Postal Code"] = "0" + str(row["Shipping Zip/Postal Code"])
        # print(str(row["Shipping Zip/Postal Code"]))

        payload.Firma = row.Firma
        payload.PLZ= row.PLZ
        payload.Ort =  row.Ort
        payload.Telefon = str(row.Telefon)
        payload.Straße = row.Strasse
        payload.Email = row.Email


        url = 'http://192.168.100.239:9099/zf_adresse_dubcheck'
        r = requests.post(url, json=asdict(payload)).json()

        if is_testing:
            print('testing',r)
            pass

        # if not r['result']['id']:
        #     failures.append(json.dumps(asdict(payload)))
        
        # else:
        #     update = ZF_8.update_one(
        #         {"ZFID": r["result"]["id"]},
        #         {
        #             "$addToSet": {
        #                 "Meta.BranchenDetails.Extern": branche,
        #             }
        #         },
        #     )
        #     update = ZF_8.update_one(
        #         {"ZFID": r["result"]["id"]},
        #         {
        #             "$addToSet": {
        #                 "Meta.Branchen": branche.WZCode,
        #             }
        #         },
        #     )
        #     print("update", r, update.modified_count)
            count += 1
        gesamt += 1
        print(gesamt)
        print(count)
    save_list_to_text_file('./failures.txt',failures)


if __name__ == "__main__":
    branche = Branche(Herkunft='', WZCode=0, Name='')

    xlsxEinspielen(
        '/home/user199/Desktop/ausf_hkls,1.xlsx',
        # path='/home/user199/Desktop/master_listen/Misch_FHH,1.xlsx',
        branche=branche,
        tmpDb="Test",
        is_testing=True
    )





######################################################################################
###### OLD STUFF

# from typing import TypedDict
# import pandas as pd
# from pymongo import MongoClient
# import ssl
# import requests


# client_8 = MongoClient(
#     "mongodb://mongoroot:9gCaPFhotG2CNEoBRdgA@192.168.100.8:27017",
#     ssl=True,
#     ssl_cert_reqs=ssl.CERT_NONE,
# )


# def getDataFrame(filepath):
#     file = pd.read_excel(filepath)
#     return pd.DataFrame(file).fillna("")


# class resHausnummer(TypedDict):
#     firma_hausnummer: str
#     firma_strasse: str
#     resultUsable: bool


# # def cleanHausnummer(hausnummer: str, default=None) -> resHausnummer:
# #     # clean inital field
# #     if len(hausnummer) > 6:
# #         hausnummer = "xxxxx"

# #     return requests.post(
# #         "http://192.168.100.239:9099/004hausnummern",
# #         json={"firma_strasse": i["Straße gm"]},
# #     ).json()
#     # error handling


# class resSanitizeStrasse(TypedDict):
#     strasse_sanitized: str


# def sanitizeStrasse(strasse: str, default=None) -> resSanitizeStrasse:
#     return requests.post(
#         "http://192.168.100.239:9099/027_sanitize_strasse",
#         json={"firma_strasse": strasse},
#     ).json()
#     # error handling


# class resPhone(TypedDict):
#     firma_telefon: str
#     firma_telefon_clean: str
#     firma_telefon_ursprung: str


# def cleanPhone(telefon: str, default=None) -> resPhone:
#     # clean tele
#     return requests.post(
#         "http://192.168.100.239:9099/005phonenumbers",
#         json={"firma_telefon": telefon},
#     ).json()
#     # error handling


# def cleanPLZ(plz: str, default=None) -> str:
#     if plz:
#         plz = str(int(plz))
#         if len(plz) == 4:
#             plz = f"0{plz}"
#     return plz


# def dubletteZuId(zfid: str) -> str:
#     cursor = client_8["ZentralerFirmenstamm"]["ZentralerFirmenstamm"].find_one(
#         {"ZFID": zfid}, {"DubletteZuId": 1}
#     )
#     if cursor:
#         return cursor["DubletteZuId"]
#     return zfid


# if __name__ == "__main__":
#     frame = getDataFrame("/home/user199/Downloads/20210226_energie_effi_gesamt_ex.xlsx")
#     count = 0
#     gesamt = 0
#     for index, i in frame.iterrows():
#         count += 1

#         if 1:
#             # id = dubletteZuId(str(i["ZFID"]))
#             # if id:
#             update = client_8["ZentralerFirmenstamm"][
#                 "ZentralerFirmenstamm"
#             ].update_one(
#                 {"ZFID": str(i['ZFID'])},
#                 {
#                     "$addToSet": {
#                         "Meta.BranchenDetails.Extern": {
#                             "Name": "energieberater/1",
#                             "WZCode": 227491104,
#                             "Herkunft": "energie_effzienz",
#                         }
#                         # "Strassenname": sanitizeStrasse["strasse_sanitized"],
#                         # "StrasseUndNr": strasseUndnr,
#                         # "PLZ": plz,
#                         # "Ort": ort,
#                         # "Hausnummer": hausnummer,
#                         # "Firma": firma,
#                         # "Email": email,
#                         # "Homepage": homepage,
#                         # "Telefon": clean["firma_telefon"],
#                         # "TelefonRaw": clean["firma_telefon_clean"],
#                         # "Firma2": firma2,
#                     }
#                 },
#             )
#             print(update.modified_count, i['ZFID'])
#             # print(id)
#             print("-----------------------------------------")

# # if __name__ == '__main__':
# #     cursor = client_8['ZentralerFirmenstamm']['ZentralerFirmenstamm'].find({''})




# # update = client_8["ZentralerFirmenstamm"]["ZentralerFirmenstamm"].update_one(
# #     {"ZFID": {"$in": [zfid, dubletteZuId]}},
# #     {
# #         "$set": {
# #             "Meta.IstInaktiv": True,
# #             "Meta.Inaktiv.Grund": i["Grund"],
# #             "Meta.Inaktiv.Seit": datetime.utcnow().isoformat()[:-3] + "Z",
# #             "Meta.Exportierbar": False,
# #             "Meta.Geaendert.Am": datetime.utcnow().isoformat()[:-3] + "Z",
# #         }
# #     },
# # )

# # ort = i["Ort gm"] if i["Ort gm"] else i["Ort_ZF"]
# # firma = i["Firmenname gm"] if i["Firmenname gm"] else i["Firma"]
# # email = i["email gm"] if i["email gm"] else i["Email"]
# # homepage = i["Homepage gm"] if i["Homepage gm"] else i["Web"]
# # telefon = i["Telefon gm"] if i["Telefon gm"] else i["Telefon"]
# # firma2 = i["Firma 2gm"] if i["Firma 2gm"] else i["Firma_2"]
# # plz = plz if plz else i["PLZ_ZF"]


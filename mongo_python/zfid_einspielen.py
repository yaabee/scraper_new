from dataclasses import asdict, dataclass, field
from pymongo import MongoClient
import requests
import re
from collections import Counter
from tqdm import tqdm


def remove_escapechars(string_value):
    """
    remove escape chars from given field
    """
    assert isinstance(string_value, str), "field_value ist kein string"
    string_value = " ".join(string_value.splitlines())
    escapes = "".join([chr(char) for char in range(1, 32)])
    translator = str.maketrans("", "", escapes)
    return " ".join([x for x in string_value.translate(translator).split(" ") if x])


@dataclass
class EmailData:
    domain: str
    freemail_status: bool
    mail: str
    online: bool
    syntax_okay: bool


@dataclass
class Options:
    checkFakeFirma: bool = False
    ensureWrite: bool = False
    forceInsert: bool = False
    returnDocument: bool = True


@dataclass
class Payload_Neuanlage:
    Fax: str = "xxxxx"
    Firma: str = "xxxxx"
    Internet: str = "xxxxx"
    Land: str = "xxxxx"
    Ort: str = "xxxxx"
    PLZ: str = "xxxxx"
    Straße: str = "xxxxx"
    Telefon: str = "xxxxx"
    options: Options = field(default_factory=Options)


def zfid_einspielen(db_name, col_name):
    client = MongoClient("192.168.100.5:27017")
    collection = client[db_name][col_name]
    cursor = collection.find({"ZFID": {"$exists": False}})
    c = Counter()
    for i in tqdm(list(cursor)):
        payload: Payload_Neuanlage = Payload_Neuanlage()
        payload.Firma = i["Firma"].strip()
        payload.Straße = i["StrasseUndNr"].strip()
        payload.PLZ = i["PLZ"].strip()
        payload.Ort = i["Ort"].strip()
        payload.Telefon = i["Telefon"].strip()
        payload.Fax = i["Fax"].strip()
        payload.Internet = i["Internet"].strip()

        # print(payload)
        # print("---------------------------------------")

        # einspielen
        if payload.Telefon:
            url = "http://192.168.100.239:9099/zf_adresse_neuanlageNachAccess"
            r = requests.post(url, json=asdict(payload)).json()

            neuangelegt = r.get("result", {}).get("neuangelegt")
            zfid = r.get("result", {}).get("id", "xxxxx")

            # print("result", r.get("result", {}))

            if neuangelegt:
                c["true"] += 1

            if not neuangelegt:
                c["false"] += 1
            # print(c)

            collection.update_one(
                {"_id": i["_id"]},
                {"$set": {"ZFID": zfid, "Neuangelegt": neuangelegt}},
            )
        else:
            pass
    print(c)


if __name__ == "__main__":
    db_name = "scrp_listen"
    col_name = "Elektrohandwerk"
    zfid_einspielen(db_name, col_name)

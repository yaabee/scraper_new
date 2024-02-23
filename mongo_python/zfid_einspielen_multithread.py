from concurrent.futures import ThreadPoolExecutor
from pymongo import MongoClient
from collections import Counter
from dataclasses import asdict, dataclass, field
import requests


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


def process_document(document, collection):
    payload = Payload_Neuanlage()
    payload.Firma = document["Firma"].strip()
    payload.Straße = document["StrasseUndNr"].strip()
    payload.PLZ = document["PLZ"].strip()
    payload.Ort = document["Ort"].strip()
    payload.Telefon = document["Telefon"].strip()
    payload.Fax = document["Fax"].strip()
    payload.Internet = document["Internet"].strip()

    print(payload)
    print("---------------------------------------")

    if payload.Telefon:
        url = "http://192.168.100.239:9099/zf_adresse_neuanlageNachAccess"
        r = requests.post(url, json=asdict(payload)).json()

        neuangelegt = r.get("result", {}).get("neuangelegt")
        zfid = r.get("result", {}).get("id", "xxxxx")

        collection.update_one(
            {"_id": document["_id"]},
            {"$set": {"ZFID": zfid, "Neuangelegt": neuangelegt}},
        )


def zfid_einspielen_parallel(db_name, col_name):
    client = MongoClient("192.168.100.5:27017")
    collection = client[db_name][col_name]
    cursor = collection.find({"ZFID": {"$exists": False}})
    c = Counter()

    with ThreadPoolExecutor() as executor:
        executor.map(process_document(collection), list(cursor))

    print(c)

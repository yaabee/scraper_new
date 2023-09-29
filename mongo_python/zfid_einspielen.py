from dataclasses import asdict, dataclass
from pymongo import MongoClient
import requests
import re



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
    checkFakeFirma:bool = False
    ensureWrite:bool =   False
    forceInsert:bool = False
    returnDocument:bool = True
@dataclass
class Payload_Neuanlage:
    Fax: str = ''
    Firma: str =''
    Internet: str =''
    Land: str =''
    Ort: str =''
    PLZ: str = ''
    Straße: str = ''
    Telefon: str =''
    options: Options = Options()



def zfid_einspielen(db_name, col_name):
    client = MongoClient("192.168.100.5:27017")
    collection = client[db_name][col_name]
    cursor = collection.find({"ZFID": {"$exists": False}})
    for i in list(cursor):
        payload: Payload_Neuanlage = Payload_Neuanlage()
        payload.Firma  =   i["Firma"]
        payload.Straße =    i["StrasseUndNr"]
        payload.PLZ   =  i["PLZ"]
        payload.Ort  =   i["Ort"]
        payload.Telefon    = i["Telefon"]

        print(payload)
        print("---------------------------------------")

        # einspielen
        url = "http://192.168.100.239:9099/zf_adresse_neuanlageNachAccess"
        r = requests.post(url, json=asdict(payload)).json()

        neuangelegt = r.get("result", {}).get("neuangelegt")
        zfid = r.get("result", {}).get("id", "xxxxx")

        collection.update_one(
            {"_id": i["_id"]},
            {"$set": {"ZFID": zfid, "Neuangelegt": neuangelegt}},
        )


if __name__ == "__main__":
    db_name = "GoogleApi"
    col_name = "google_Intersolar"
    zfid_einspielen(db_name, col_name)

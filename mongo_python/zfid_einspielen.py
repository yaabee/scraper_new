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


# plz test
def check_website(website):
    if "https://www" in website:
        website = website.replace("https://www.", "www.info@")
    elif "https://" in website:
        website = website.replace("https://", "www.info@")
    elif "http://www" in website:
        website = website.replace("http://www.", "www.info@")
    elif "http://" in website:
        website = website.replace("http://", "www.info@")
    elif "www." in website and not "info@" in website:
        website = website.replace("www.", "www.info@")
    elif "www." not in website:
        website = f"www.info@{website}"
    if ".de/" in website or ".com/" in website or ".nl/" in website:
        ind = website.index("/")
        website = website[:ind]
    try:
        url = "http://192.168.100.239:9099/003mailcheck"
        payload = dict(firma_email=website)
        return requests.post(url, json=payload).json()
    except Exception as e:
        print(f"error: {e}")


def get_clean_telefon(tele):
    payload = {"firma_telefon": tele}
    return requests.post("http://192.168.100.239:9099/005phonenumbers", json=payload).json()


def zfid_einspielen(db_name, col_name):
    client = MongoClient("192.168.100.5:27017")
    collection = client[db_name][col_name]
    cursor = collection.find({"ZFID": {"$exists": False}})
    for i in cursor:
        check = {"ok": True}
        if check["ok"]:
            if not i["Telefon"] and i["Handy"]:
                i["Telefon"] = i["Handy"]

            payload = dict(
                Firma=remove_escapechars(i["Firma"]),
                Straße=remove_escapechars(i["Strasse_Firma"]),
                PLZ=i(i["PLZ_Firma"]),
                Ort=remove_escapechars(i["Ort_Firma"]),
                Telefon=get_clean_telefon(i["Telefon"])["firma_telefon"],
                Internet="xxxxx",
                Fax="xxxxx",
                options={
                    "ensureWrite": False,
                    "forceInsert": False,
                    "returnDocument": False,
                },
            )
            url = "http://192.168.100.239:9099/zf_adresse_neuanlageNachAccess"
            r = requests.post(url, json=payload).json()
            if r["result"]["id"]:
                zfid = r["result"]["id"]
            else:
                zfid = "xxxxx"
            collection.update_one(
                {"_id": i["_id"]}, {"$set": {"ZFID": zfid, "Neuangelegt": r["result"]["neuangelegt"]}}
            )
        print("no id")


if __name__ == "__main__":
    db_name = "AutomatischEingespielt"
    col_name = "WEDI_xlsx"
    zfid_einspielen(db_name, col_name)

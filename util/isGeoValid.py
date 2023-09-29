import requests


def is_geo_valid(land: str, ort: str, plz: str, strasse_und_nr: str) -> bool:
    """momentan nur Deutschland?"""
    payload_geocoder = {
        "Land": land,
        "Ort": ort,
        "PLZ": plz,
        "StrasseUndNr": strasse_und_nr,
        "options": {"returnMultiple": False},
    }
    check = requests.post("http://192.168.100.239:9099/geocoder", json=payload_geocoder).json()

    if check["ok"]:
        return True
    return False

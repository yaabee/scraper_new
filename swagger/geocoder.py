import requests

def get_geodata(url, plz, strasseundnr, ort):
    data = {
        'Land': '',
        'Ort': ort,
        'PLZ': plz,
        'StrasseUndNr': strasseundnr,
        "options": {
            "returnMultiple": True
        }
    }
    return requests.post(url, json=data)

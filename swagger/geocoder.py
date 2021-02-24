import requests

def get_geodata(plz, strasse):
    data = {
        'StrasseUndNr': strasse,
        'PLZ': plz,
        'Ort': '',
    }
    req = requests.post('', data={})
    return

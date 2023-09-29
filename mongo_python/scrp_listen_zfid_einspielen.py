from dataclasses import asdict, dataclass
from pymongo import MongoClient
import requests

from module.email_check import check_website



def remove_escapechars(string_value):
    '''
    remove escape chars from given field
    '''
    assert isinstance(string_value, str), 'field_value ist kein string'
    string_value = ' '.join(string_value.splitlines())
    escapes = ''.join([chr(char) for char in range(1, 32)])
    translator = str.maketrans('', '', escapes)
    return ' '.join([x for x in string_value.translate(translator).split(' ') if x])



def get_clean_telefon(tele):
    payload = {
        'firma_telefon': tele
    }
    return requests.post('http://192.168.100.239:9099/005phonenumbers', json=payload).json()

@dataclass
class Options:
    returnMultiple: bool = False

@dataclass
class Payload_Geocoder:
    Land: str = ''
    Ort: str = ''
    PLZ: str = ''
    StrasseUndNr: str = ''
    options: Options = Options()


def zfid_einspielen(db_name, col_name):
    client = MongoClient('192.168.100.5:27017')
    collection = client[db_name][col_name]
    cursor = collection.find({'ZFID': {'$exists': False}})
    if cursor[:1]:
        for i in cursor:
            payload_geo = Payload_Geocoder()
            payload_geo.Ort = i['Ort']
            payload_geo.PLZ = i['PLZ']
            payload_geo.StrasseUndNr = i['StrasseUndNr']

            check = requests.post(
                'http://192.168.100.239:9099/geocoder', json=asdict(payload_geo)).json()
            print(check)
            if check['ok']:
                # handy aber kein tele
                if not i['Telefon'] and 'Handy' in i and i['Handy']:
                    i['Telefon'] = i['Handy']

                payload_scrp_listen = dict(
                    Firma=remove_escapechars(i['Firma']),
                    Straße=remove_escapechars(i['StrasseUndNr']),
                    PLZ=i['PLZ'],
                    Ort=remove_escapechars(i['Ort']),
                    Telefon=get_clean_telefon(i['Telefon'])['firma_telefon'],
                    Internet=check_website(i['Website']).domain,
                    Fax='xxxxx',
                    options={
                        "ensureWrite": False,
                        "forceInsert": False,
                        "returnDocument": False,
                    }
                )
                print('payload scrp listen', payload_scrp_listen)
                url = "http://192.168.100.239:9099/zf_adresse_neuanlageNachAccess"
                r = requests.post(url, json=payload_scrp_listen).json()
                print('neuanlage', r)
                print('==================================================')
                # neu, alt flag!
                if r['result']['id']:
                    zfid = r['result']['id']
                else:
                    zfid = 'xxxxx'
                collection.update_one(
                    {'_id': i['_id']},
                    {'$set': {"ZFID": zfid,
                            'Neuangelegt': r['result']['neuangelegt']}}
                )
            else:
                print('++++++++++++++++++++++++++++')
                print('no id')
                print('++++++++++++++++++++++++++++')

if __name__ == '__main__':
    db_name = 'GoogleApi'
    col_name = 'google_Intersolar'
    zfid_einspielen(db_name, col_name)

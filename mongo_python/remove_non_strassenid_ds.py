from re import split
from pymongo import MongoClient
import ssl
import requests
import pprint



client_5 = MongoClient('192.168.100.5:27017')
client_239 = MongoClient('192.168.100.239:27017',
                     username='mongoroot',
                     password='9gCaPFhotG2CNEoBRdgA',
                     authSource='admin',
                     authMechanism='SCRAM-SHA-256',
                     ssl=True,
                     ssl_cert_reqs=ssl.CERT_NONE)

def remove_non_strassenid_ds(db_name, col_name):
    col_5 = client_5[db_name][col_name]
    cursor = col_5.find({})
    for i in cursor:
        split_adress = i['formatted_address'].split(',')
        #check if legit adress
        strasseundnr = split_adress[0].strip()
        plz = split_adress[1][:6].strip()
        ort = split_adress[1][6:].strip()
        payload = {
            "Land": '',
            "Ort": ort,
            "PLZ": plz,
            "StrasseUndNr": strasseundnr,
            "options": {
                "returnMultiple": False
            }
        }

        r = requests.post('http://192.168.100.239:9099/geocoder', json=payload)
        if len(r.json()['result']['plz']) == 1:
            # pprint.pprint(r.json()['result']['geocode'])
            # print('strassenid gefunden')
            pass
        else:
            print(split_adress)
            print(i['ZFID'])
            print(i['Telefon'])
            print('nicht eindeutig')
        print('====================')

if __name__ == '__main__':
    db_name = 'GoogleApi'
    col_name = 'google_technischer_berater_marburg'
    remove_non_strassenid_ds(db_name, col_name)

    #formatted_address str + nr , plz + ort , land

    #hausnummer an strasseundnr hausnummer schicken
    #if formatted_address returns strassenid, dann datensatz ergaenzen
    #else delete datensatz

#ergaenzen
'''
    BusinessStatus = business_status
    if permanently closed:
        Meta.InaktivGrund = 'Google Api'
'''

from pymongo import MongoClient
import ssl
import requests

client_5 = MongoClient('192.168.100.5:27017')
client_239 = MongoClient('192.168.100.239:27017',
                         username='mongoroot',
                         password='9gCaPFhotG2CNEoBRdgA',
                         authSource='admin',
                         authMechanism='SCRAM-SHA-256',
                         ssl=True,
                         ssl_cert_reqs=ssl.CERT_NONE)


zf_239 = client_239['ZentralerFirmenstamm']['ZentralerFirmenstamm']
odin_yb = client_239['odin']['ZOObjekte_yanghi']


def changeAnzahlMitarbeiter():

    pipeline_anzahl = [
        {'$match': {
            'Anzahl Mitarbeiter': {'$ne': []}
        }},
        {
            '$project': {
                '_id': 1,
                'Anzahl': '$Anzahl Mitarbeiter',
                'ZFID': '$ZFID',
            }
        },
        # {
        #     '$limit': 10
        # }
    ]

    scrp_listen = client_5['scrp_listen']['heinze_zfid']
    zob = client_239['ZentralerFirmenstamm']['ZentralerFirmenstamm']

    agg = list(scrp_listen.aggregate(pipeline_anzahl))

    for i in agg:
        anzahl = i['Anzahl']
        print(i)
        if anzahl:
            if anzahl == ['1-2']:
                # print('1-2 to 2')
                zob.update_one({'ZFID': i['ZFID']}, {'$set': {
                    'FirmaDaten.AnzahlMitarbeiter': 2
                }})
                print('zfid', i['ZFID'])
            elif anzahl == ['3-4']:
                # print('3-4 to 4')
                zob.update_one({'ZFID': i['ZFID']}, {'$set': {
                    'FirmaDaten.AnzahlMitarbeiter': 4
                }})
            elif anzahl == ['5-9']:
                # print('5-9 to 9')
                zob.update_one({'ZFID': i['ZFID']}, {'$set': {
                    'FirmaDaten.AnzahlMitarbeiter': 9
                }})
            elif anzahl == ['10-19']:
                # print('10-19 to 15')
                zob.update_one({'ZFID': i['ZFID']}, {'$set': {
                    'FirmaDaten.AnzahlMitarbeiter': 15
                }})
                pass
            elif anzahl == ['20-49']:
                # print('20-49 to 30')
                zob.update_one({'ZFID': i['ZFID']}, {'$set': {
                    'FirmaDaten.AnzahlMitarbeiter': 30
                }})
            elif anzahl == ['50-99']:
                # print('50-99 to 75')
                zob.update_one({'ZFID': i['ZFID']}, {'$set': {
                    'FirmaDaten.AnzahlMitarbeiter': 75
                }})
            elif anzahl == ['100-199']:
                # print('100-199 to 150')
                zob.update_one({'ZFID': i['ZFID']}, {'$set': {
                    'FirmaDaten.AnzahlMitarbeiter': 150
                }})
            elif anzahl == ['200-499']:
                # print('200-499 to 350')
                zob.update_one({'ZFID': i['ZFID']}, {'$set': {
                    'FirmaDaten.AnzahlMitarbeiter': 350
                }})
                print('ZFID', i['ZFID'])
            elif anzahl == ['500-999']:
                # print('500-999 to 750')
                zob.update_one({'ZFID': i['ZFID']}, {'$set': {
                    'FirmaDaten.AnzahlMitarbeiter': 750
                }})
            # else:
            #     pass
            #     # print('1000')


if __name__ == '__main__':
    changeAnzahlMitarbeiter()

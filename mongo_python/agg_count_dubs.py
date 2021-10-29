# from MongoEndpoints.mongo_239 import ZOOBJEKTE_YANGHI
# from MongoEndpoints.mongo_5 import SCRP_LISTEN_HEINZE
# from MongoEndpoints.mongo_5 import SCRP_LISTEN_HEINZE_BACK

"""
- Dublikate von einem Feld zaehlen 
- spaeter ausgeben und im view anzeigen
"""

from pymongo import MongoClient
import ssl
import pprint

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


def count_dublicates_rel_to_field():
    pipeline = [
        {'$match': {
            'Telefon': 'xxxxx'
        }},
        {
            '$group': {
                '_id': {
                    'Telefon': '$Telefon'
                },
                'uniqueIds': {
                    '$addToSet': '$_id'
                },
                'count': {
                    '$sum': 1
                }
            }
        }, {
            '$match': {
                'count': {
                    '$gt': 1
                }
            },
        }, {
            '$sort': {
                'count': 1
            }
        }]
    agg = list(client_5['scrp_listen']['heinze_zfid_back'].aggregate(pipeline))
    print(len(agg))
    for i in agg[:10]:
        pprint.pprint(i)


if __name__ == '__main__':
    count_dublicates_rel_to_field()

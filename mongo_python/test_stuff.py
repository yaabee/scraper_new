
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


zf_239 = client_239['ZentralerFirmenstamm']['ZentralerFirmenstamm']

odin_yb = client_239['odin']['ZOObjekte_yanghi']
scrp_listen = client_5['scrp_listen']['heinze_zfid_back']



# print(odin_yb.find_one({'ZOID': '530f5e39fa46343b048b48ec'})['Baukosten'])


pipeline = [
    {'$match': {
        'ZOID': '530f5e39fa46343b048b48ec'
    }},
    {
        '$set': {'Baukosten': 123123}
    }, ]

pipeline_gesamtanzahl = [
    {'$match': {
        'Meta.Nettokontakt.Gesamtanzahl': {'$exists': True}
    }}
]
agg = list(zf_239.aggregate(pipeline_gesamtanzahl))
print(len(agg))
for i in agg:
    # print(i['Meta']['Terminvormerkung'])
    pprint.pprint(i)
    zf_239.update_one({'ZFID': i['ZFID']}, {
                      '$set': {'Meta.Nettokontakt': {'Zuletzt': '', 'GesamtAnzahl': 0}}})
agg = list(zf_239.aggregate(pipeline_gesamtanzahl))
print(len(agg))
# print(odin_yb.find_one({'ZOID': '530f5e39fa46343b048b48ec'})['Baukosten'])

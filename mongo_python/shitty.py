
from enum import auto
from pymongo import MongoClient
import ssl
import requests
import pprint

import jsonpatch
import json

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
scrp_listen = client_5['scrp_listen']['heinze_zfid']
# zf_yb = ['ZentralerFirmenstamm']['ZentralerFirmenstamm_yan']
staticdata_access = client_239['staticdata']['AllgAllgemeineVorlagen_Branchenliste']
staticdata_dis = client_239['staticdata']['automatischeBranche']
original_zf = client_239['ZentralerFirmenstamm']['ZentralerFirmenstamm2']
original_new = client_239['ZentralerFirmenstamm']['ZentralerFirmenstamm_new2']


cursor = list(scrp_listen.find({'Planungsleistungen': {
              '$in': ['Stadtplanung']}}))


automatischeBranche = list(
    client_239['staticdata']['automatischeBranche'].find({}))
cache = {v['branche_id']: v['branche']
         for v in automatischeBranche if 'branche_id' in v.keys()}


zfids = [x['ZFID'] for x in cursor]
branche = {
    'Herkunft': 'scrp_listen_hnz',
    'Name': cache[227111600],
    'WZCode': 227111600,
}
print('old', zfids[:10])
old = list(zf_239.find({'ZFID': {'$in': zfids[:10]}}))
pprint.pprint([x['Meta']['BranchenDetails']['Extern'] for x in old])

zf_239.update_many({'ZFID': {'$in': zfids}}, {'$addToSet': {
                   'Meta.BranchenDetails.Extern': branche}})

new = list(zf_239.find({'ZFID': {'$in': zfids[:10]}}))
pprint.pprint([x['Meta']['BranchenDetails']['Extern'] for x in new])
print(branche)
print(len(zfids))

# wz = [
#     227111200,
#     164673100,
#     154322100,
#     154322100,
#     154322100,
#     154321100,
#     227111300,
#     154391200,
#     154391101,
#     154331100,
#     227111500,
#     154333101,
#     154200000,
#     154331100,
#     154331100,
#     164674200,
#     154411100
# ]

# counter = 0
# for i in cursor:
#     # print('_id', i['_id'])
#     # print('zfid ', i['ZFID'])
#     ds = zf_239.find_one({'ZFID': i['ZFID']})
#     if ds:
#         branche = {
#             'Herkunft': 'scrp_listen_hnz',
#             'Name': cache[227111200],
#             'WZCode': 227111200,
#         }
#         x = ds['Meta']['BranchenDetails']['Extern']
#         y = x.copy()
#         y += [branche]
#         # pprint.pprint(x, indent=2)
#         # pprint.pprint(y, indent=2)
#         old = zf_239.find_one({'ZFID': i['ZFID']})
#         print('old', old['Meta']['BranchenDetails']['Extern'])
#         zf_239.update_one({'ZFID': i['ZFID']}, {'$addToSet': {
#             'Meta.BranchenDetails.Extern': branche
#         }})
#         new = zf_239.find_one({'ZFID': i['ZFID']})
#         print('new', new['Meta']['BranchenDetails']['Extern'])
#         print('=================================')
#     else:
#         og = original_zf.find_one({'ZFID': i['ZFID']})
#         if og:
#             if og['Telefon'] != 'xxxxx':
#                 print('og', og['Telefon'])
#                 print('zfid', i['ZFID'])
#                 insert = zf_239.insert_one(og)
#                 print(
#                     f'inserted id {insert.inserted_id}, zfid {i["ZFID"]}')
#                 counter += 1
#         else:
#             print('no og')
#             og_new = original_new.find_one({'ZFID': i['ZFID']})
#             if og_new:
#                 if og_new['Telefon'] != 'xxxxx':
#                     print('og_new', og_new['Telefon'])
#                     print('zfid', i['ZFID'])
#                     insert = zf_239.insert_one(og_new)
#                     print(
#                         f'inserted id {insert.inserted_id}, zfid {i["ZFID"]}')
#                     # wenn tele, dann in zf_239 einspielen
#                     counter += 1
#             else:
#                 print('no og_new')
# print('counter', counter)

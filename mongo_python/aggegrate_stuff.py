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

pipeline = [
    {'$unwind': '$Meta.BranchenDetails.Stichwoerter'},
    {'$group': {'_id': '$Meta.BranchenDetails.Stichwoerter'}}
]

pipeline_einspielen = [
    {'$project': {
        '_id': 1,
        'Ansprechpartner': '$Ansprechpartner',
        'count': {'$size': '$Ansprechpartner'},
        'ZFID': '$ZFID',
    }}, ]

pipelineObjektdubs = [
    {"$project": {
        "_id": 1,
        "count": {"$size": "$PotenzielleDubletten"
                  }
    }
    },
    {"$match": {
        "count": {
            "$gt": 0
        }
    }
    }
]

pipeline_branchev = [
    {'$project': {
        '_id': '$_id',
        'Ansprechpartner': '$Ansprechpartner',
        'ZFID': '$ZFID',
        'Email': '$Email',
    }},
    {'$unwind': '$Ansprechpartner'
     },
    {'$match': {
        'Ansprechpartner.ap_mobil': {'$ne': 'xxxxx'}
    }}
]

pipeline_pruefen = [
    {'$project': {
        '_id': 1,
        'PruefungNotwendig': '$PruefungNotwendig',
        'DubletteZu': '$DubletteZu',
        'count': {'$size': '$DubletteZu'}
    }},
    {'$match': {
        'count': {
            '$gt': 0
        },
    }},

]

pipeline_branchendetails = [
    {'$match': {'ZFID': '57b083732db2cb4c1200002b',
                'Meta.BranchenDetails': {'$exists': True}}},
    {'$project': {
        '_id': 1,
        'branchen': {'$concatArrays': ['$Meta.BranchenDetails.Homepage',
                                       '$Meta.BranchenDetails.Stichwoerter',
                                       '$Meta.BranchenDetails.Access',
                                       '$Meta.BranchenDetails.Extern',
                                       ]
                     },
    }},
    {
        '$addFields': {
            'branchen': {
                '$map': {
                    'input': '$branchen',
                    'as': 'branche',
                    'in': {
                        '$mergeObjects': [
                            '$$branche',
                            {
                                'ZFID': '$_id'
                            }
                        ]
                    }
                }
            }
        }
    },
]

agg = list(zf_239.aggregate(pipeline_branchendetails))

for i in agg:
    pprint.pprint(i)


#         if i['ap_tel'] != 'xxxxx':
#             payload = {
#   "Abteilung": "Einkauf",
#   "Anrede": "Herr",
#   "Datenherkunft": "Velux",
#   "Email": "max.zeschitz@gmail.com",
#   "Fax": "0931803269",
#   "KeinKontaktErwuenscht": "Wahr",
#   "Mobil": "0175",
#   "Nachname": "Grasser",
#   "Position": "Geschäftsführung",
#   "Telefon": "0931803268",
#   "Titel": "Dr.",
#   "Vorname": i['ap_name'],
#   "ZFID": "57b0a7f52db2cb4c120137e1",
#   "options": {
#     "returnDocument": True
#   }
# }
#             requests.post('http://192.168.100.239:9099/zf_ansprechpartner_neuanlage', )

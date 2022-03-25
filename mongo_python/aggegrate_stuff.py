from enum import auto
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


# client_solaris = MongoClient(
#     "192.168.100.8:27018",
#     serverSelectionTimeoutMS=1000,
#     username="zo_objekt_reader",
#     password="",
#     authSource="solaris",
#     authMechanism="SCRAM-SHA-256",
# )


client_zo_reader = MongoClient('192.168.100.8:27017',
                         username='zo_objekt_reader',
                         password='s5FLwMszMHSMck4KL6Pm',
                         authSource='zo_objekt',
                         authMechanism='SCRAM-SHA-256',
                         tls=True,
                         tlsCAFile='/etc/ssl/certs/teleaktiv_rootCA.pem')


zf_239 = client_239['ZentralerFirmenstamm']['ZentralerFirmenstamm']
odin_yb = client_239['odin']['ZOObjekte_yanghi']
scrp_listen = client_5['scrp_listen']['heinze_zfid']
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
    {'$match': {
        'Hausnummer': {'$ne': ''},
        'Strasse': {'$ne': ''},
        'PLZ': {'$ne': ''},
    }},
    {'$group': {
        '_id': {
            'Strasse': '$Strasse',
            'Hausnummer': '$Hausnummer',
            'PLZ': '$PLZ',
        },
        'count': {'$sum': 1},
        'ZOIDS': {'$addToSet': '$_id'}
    }},
    {'$match': {
        'count': {
            '$gt': 1
        },
    }},
    # {'$limit': 10}

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

pipeline_zielgruppefalschgrund = [
    {'$match': {
        'Meta.ZielgruppeFalschGrund': {'$size': 2}
    }},
    {'$project': {
        '_id': 1,
        'Zielgruppe': '$Meta.ZielgruppeFalschGrund',
    }},
    {'$limit': 10}
]



#tele, strasse, plz, name gleich
pipeline_energie_effi_dubs = [
    {
        '$group': {
            '_id': {
                'Firma': '$Firma',
                'Telefon': '$Telefon',
                'StrasseUndNr': '$StrasseUndNr',
                'PLZ': '$PLZ',
                'name': '$name',
            },
            'uniqueIds': {'$addToSet': '$ZFID'},
            'count': {'$sum': 1},
        }
    },
    {
        '$project': {
            'size': {'$size': '$uniqueIds'},
            '_id': 1,
            'uniqueIds': 1,
            }
    },
    { '$match': {
        'size': {'$gt': 1}
    }},
]

# agg = list(client_5['scrp_listen']['energie_effizienz_full_06092021'].aggregate(pipeline_energie_effi_dubs))
# agg = list(client_zo_reader['zo_objekt']['zo_objekt'].aggregate(pipeline_pruefen))

pipeline = [{'$match': {}}]

agg = list(client_239['odin']['Cronjobs'].aggregate(pipeline))

for i in agg:
    update = client_239['odin']['Cronjobs'].update_one({'schnellfilter_name': i['schnellfilter_name']}, {'$set': {'MitLeeremBaubeginn': True}})
    print(i)
    


agg = list(client_239['odin']['Cronjobs'].aggregate(pipeline))
for k in agg:
    print(k)
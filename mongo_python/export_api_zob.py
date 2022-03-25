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


client_8 = MongoClient('192.168.100.8:27017',
                         username='zo_objekt_reader',
                         password='s5FLwMszMHSMck4KL6Pm',
                         authSource='zo_objekt',
                         authMechanism='SCRAM-SHA-256',
                         tls=True,
                         tlsCAFile='/etc/ssl/certs/teleaktiv_rootCA.pem')


zf_239 = client_239['ZentralerFirmenstamm']['ZentralerFirmenstamm']

odin_yb = client_239['odin']['ZOObjekte_yanghi']

pipeline = [
    {'$unwind': '$Meta.BranchenDetails.Stichwoerter'},
    {'$group': {'_id': '$Meta.BranchenDetails.Stichwoerter'}}
]

pipelineObjektdubs = [
    {"$project": {
        "_id": 1,
        "Hausnummer": "$Hausnummer",
        "count": {"$size": "$PotenzielleDubletten"
                  }
    }
    },
    {"$match": {
        "count": {
            "$gt": 0
        },
        "Hausnummer": {'$ne': ''}
    }
    }
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
]

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

pipeline_get_zfid = [
  {'$match': {'ZFID': {'$exists': True}}},
  {'$project': {
    '_id': '$ZFID'
  }}
]

pipeline_dublette_zu = [
  {'$project': {'_id': 1, 'DubletteZu': '$DubletteZu', 'size': {'$size': '$DubletteZu'}}},
  {'$match': {
    'size': {'$gt': 0}
  }}
]

pipeline_facility = [
    {'$match': {'ZFID': {'$exists': True}}}
]


agg = list(client_5['GoogleApi']['google_Facility_Facility'].aggregate(pipeline=pipeline_facility))
# agg = list(client_5['scrp_listen']['energie_effizienz_full_06092021'].aggregate(pipeline=pipeline_get_zfid))
zfids = []
for i in agg[:10]:
  print(i['_id'])
req = requests.post("http://localhost:5555/firmenadresse/",
                    json={"zfid": ','.join([x['ZFID'] for x in agg]), "ansprechpartner_switch": False})

#speichert in scraper_new
with open('Google_Facility.xlsx', mode='wb') as localfile:
    localfile.write(req.content)


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
    # {'$limit': 1000}
]
# ",".join([str(x["_id"]) for x in agg])


# agg = list(client_8['zo_objekt']['zo_objekt'].aggregate(pipeline=pipeline_pruefen))
agg = list(client_239['odin']['ZOObjekte'].aggregate(pipeline=pipeline_pruefen))
zoids = []
for i in agg:
    for k in i['ZOIDS']:
        zoids.append(str(k))
req = requests.post("http://192.168.100.104:5555/odinExport/",
                    json={"zoid": ','.join(zoids), "ansprechpartner_switch": False})

#speichert in scraper_new
with open('objekte_dubs_odin.xlsx', mode='wb') as localfile:
    localfile.write(req.content)

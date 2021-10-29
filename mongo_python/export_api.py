
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

pipeline_dubs = [

]


agg = list(odin_yb.aggregate(pipeline=pipelineObjektdubs))
print(len(agg))
req = requests.post("http://192.168.100.104:5555/odinExport/",
                    json={"zoid": ",".join([str(x["_id"]) for x in agg]), "ansprechpartner_switch": False})

#speichert in scraper_new
with open('objekte_dubs_hausnummer.xlsx', mode='wb') as localfile:
    localfile.write(req.content)


from types import coroutine
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


access = zf_239.find({'IstDublette': False,

  'Meta.BranchenDetails.Homepage': {'$elemMatch': {'WZCode': {'$in': [227111200,
                                                                    '227111200']}}},
  'Meta.IstGesperrt': False,
  'Meta.IstInaktiv': False})

# print(len(list(access)))

access_nin = zf_239.find({'IstDublette': False,

  'Meta.BranchenDetails.Homepage': {'$elemMatch': {'WZCode': {'$in': [227111200,
                                                                    '227111200']}}},
  'Meta.IstGesperrt': False,
  'Meta.IstInaktiv': False, 'Meta.Branchen': {'$nin': [227111200,
                                                                    '227111200']}})
                                                                  
print(len(list(access_nin)))


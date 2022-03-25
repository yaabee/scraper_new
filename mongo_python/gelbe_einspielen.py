from pymongo import MongoClient
import requests
import pprint
import ssl
import json

client = MongoClient(
    "mongodb://mongoroot:9gCaPFhotG2CNEoBRdgA@192.168.100.239:27017",
        ssl=True,
        ssl_cert_reqs=ssl.CERT_NONE,
    )
db = client["FirmenAdresse"]
gelbe_seiten = db["Gelbeseiten"]

cursor = list(gelbe_seiten.find({'branche': 'Solartechnik'}))
print(len(cursor))

for i in cursor:

  r = requests.post('http://192.168.100.239:9099/zf_adresse_neuanlageNachAccess', json={
  "Fax": '',
  "Firma": i['firma_name'],
  "Internet": '',
  "Ort": i['firma_ort'],
  "PLZ": i['firma_plz'],
  "Straße": i['firma_strasse'],
  "Telefon": i['telefon'],
  "options": {
    "ensureWrite": False,
    "forceInsert": False,
    "returnDocument": True
  }
})
  zfid = dict(json.loads(r.content)['result']['document'])['ZFID']
  print(zfid)
  gelbe_seiten.update_one({'telefon': i['telefon']}, {'$set': {'ZFID': zfid}})
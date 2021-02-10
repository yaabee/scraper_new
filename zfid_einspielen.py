from pymongo import MongoClient
import ssl
import requests

# client = MongoClient('192.168.100.239:27017',
#                      username='mongoroot',
#                      password='9gCaPFhotG2CNEoBRdgA',
#                      authSource='admin',
#                      authMechanism='SCRAM-SHA-256',
#                      ssl=True,
#                      ssl_cert_reqs=ssl.CERT_NONE)
def zfid_einspielen(db_name, col_name):
  client = MongoClient('192.168.100.5:27017')
  collection = client[db_name][col_name]
  cursor = collection.find({})
  for i in cursor:
    payload_google = dict(
      Firma=i['Firma'],
      Straße=i['Strasse'],
      PLZ=i['PLZ'],
      Ort=i['Ort'],
      Telefon=i['Telefon'],
      Internet=i['Internet'],
      Fax=i['Fax'],
      options={
        "ensureWrite": False,
        "forceInsert": False,
        "returnDocument": False,
      }
    )
    url = "http://192.168.100.239:9099/zf_adresse_neuanlageNachAccess"
    r = requests.post(url, json=payload_google).json()
    print(r)
    #neu, alt flag!
    if r['result']['id']:
      zfid = r['result']['id']
    else:
      zfid = 'xxxxx'
    collection.update_one(
      {'_id': i['_id']},
      {'$set': {"ZFID": zfid, 'Neuangelegt': r['result']['neuangelegt']}}
    )


if __name__ == '__main__':
  db_name = 'scrp_listen'
  col_name = 'heinze'
  zfid_einspielen(db_name, col_name)

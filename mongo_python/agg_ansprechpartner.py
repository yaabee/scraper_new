from pymongo import MongoClient
import ssl
import pprint
import requests

client_5 = MongoClient('192.168.100.5:27017')
client_239 = MongoClient('192.168.100.239:27017',
                         username='mongoroot',
                         password='9gCaPFhotG2CNEoBRdgA',
                         authSource='admin',
                         authMechanism='SCRAM-SHA-256',
                         ssl=True,
                         ssl_cert_reqs=ssl.CERT_NONE)


def main():
  pipeline = [
    {
      '$match': {
        'Ansprechpartner': {'$elemMatch': {'ap_name': {'$ne': 'xxxxx'},'ap_tel': {'$ne': 'xxxxx'}, 'ap_rolle': {'$in': ['Bauleiter:in']}}},
        'ZFID': {'$exists': True},
      }
    },
    {'$project': {
      '_id': 1,
      'Ansprechpartner': 1,
      'ZFID': 1,
    }}
  ]
  agg = list(client_5['scrp_listen']['heinze_zfid'].aggregate(pipeline))

  for i in agg:
    print(i['ZFID'])
    zfid = i['ZFID']
    for k in i['Ansprechpartner']:
      if k['ap_tel'] != 'xxxxx' and len(k['ap_name']) < 30:
        #clean tele
        tel = k['ap_tel'].replace('-', '')
        tel = tel.replace('/', '')
        tel = tel.replace('Tel.', '')
        tel = tel.strip()
        tel = tel.replace('(', '')
        tel = tel.replace(')', '')
        #tele norm
        firma_telefon = requests.post('http://192.168.100.103:9099/005phonenumbers', json={'firma_telefon': tel}).json()

        name = k['ap_name'].split(' ')
        for i in name:
          if 'Dr.' in i or 'Ing.' in i or 'Architekt' in i or 'Ingenieur' in i or 'Dipl.' in i or '-Ing' in i or 'M.Eng.' in i:
            pass
            
          else:
            print(k['ap_name'])
            print(firma_telefon['firma_telefon'])
            print(name[0], name[-1])
            #ap einspielen
            payload = {
              "Abteilung": "xxxxx",
              "Anrede": "xxxxx",
              "Datenherkunft": "5_scrp_listen__heinz_zfid",
              "Email": "xxxxx",
              "Fax": "xxxxx",
              "KeinKontaktErwuenscht": "Falsch",
              "Mobil": "xxxxx",
              "Nachname": name[-1],
              "Position": 'Bauleitung',
              "Telefon": firma_telefon['firma_telefon'],
              "Titel": "xxxxx",
              "Vorname": name[0],
              "ZFID": zfid,
              "options": {
                "returnDocument": True
              }
            }
            print(len(agg))
            einspielen = requests.post('http://192.168.100.103:9099/zf_ansprechpartner_neuanlage', json=payload).json()
            pprint.pprint(einspielen)

if __name__ == '__main__':
  main()




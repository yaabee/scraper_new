import requests
import json
import time
import ssl
from pymongo import MongoClient
from functools import lru_cache

client = MongoClient('192.168.100.239:27017',
                     username='mongoroot',
                     password='9gCaPFhotG2CNEoBRdgA',
                     authSource='admin',
                     authMechanism='SCRAM-SHA-256',
                     ssl=True,
                     ssl_cert_reqs=ssl.CERT_NONE)

db = client['ZentralerFirmenstamm']
firmenadresse = db['ZentralerFirmenstamm']

client_5 = MongoClient('192.168.100.5:27017')

def insert_new_dataset_into_mdb(mdb_uri, datenbank, collection, datensatz):
  client = MongoClient(mdb_uri, 27017, maxPoolSize=500)
  db = client[datenbank]
  collection = db[collection]
  collection.insert_one(datensatz)
  
def api_call(plz_or_city, suchbegriff, key, col_name=''):
  query = f'query={suchbegriff}+{plz_or_city}'
  count = 0
  cache = {}
  while True:
    url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?{query}&key={key}'
    req = requests.get(url)
    req_json = json.loads(req.text)
    print('req_json', req_json)
    # count api calls
    count += 1
    for i in req_json['results']:
      if i['place_id'] not in cache:
        # append to result
        cache[i['place_id']] = i['place_id']
        details = get_places_details(i['place_id'], key)
        try:
          i['Telefon'] = details['international_phone_number']
        except KeyError:
          i['Telefon'] = 'xxxxx'
        try:
          i['website'] = details['website']
        except KeyError:
          i['website'] = 'xxxxx'
        i['formatted'] = True
        # add plz, ort, stra
        splitted_address = i['formatted_address'].split(',')
        if len(splitted_address) == 3:
          try:
            plz_und_ort = splitted_address[1].strip().split(' ')
            i['StrasseUndNr'] = splitted_address[0]
            i['PLZ'] = plz_und_ort[0]
            i['Ort'] = plz_und_ort[1]
            i['legit_address'] = True
          except (KeyError, IndexError):
            i['StrasseUndNr'] = 'xxxxx'
            i['PLZ'] = 'xxxxx'
            i['Ort'] = 'xxxxx'
            i['legit_address'] = False
        else:
          i['StrasseUndNr'] = 'xxxxx'
          i['PLZ'] = 'xxxxx'
          i['Ort'] = 'xxxxx'
          i['legit_address'] = False
        # write too db
        insert_new_dataset_into_mdb(mdb_uri="192.168.100.5",
                                    datenbank='GoogleApi',
                                    collection=f'google_{suchbegriff}_{col_name}',
                                    datensatz=i)
      else:
        print('found in list')
    
    # next page & break con
    if 'next_page_token' in req_json:
      time.sleep(4)
      next_page = req_json['next_page_token']
      query = f'pagetoken={next_page}'
    else:
      return count

@lru_cache(maxsize=None)
def get_places_details(place_id, key):
  url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&' \
        f'fields=formatted_phone_number,international_phone_number,website&key={key}'
  get_details = requests.get(url)
  details_json = json.loads(get_details.text)['result']
  return details_json

big_citys = [
  'Berlin', 'Hamburg', 'München', 'Köln', 'Frankfurt',
  'Stuttgart', 'Düsseldorf', 'Leipzig', 'Dortmund', 'Essen',
  'Bremen', 'Dresden', 'Hannover', 'Nürnberg', 'Duisburg',
  'Bochum', 'Wuppertal', 'Bielefeld', 'Bonn', 'Münster',
  'Karlsruhe', 'Mannheim', 'Augsburg', 'Wiesbaden', 'Mönchengladbach',
  'Gelsenkirchen', 'Braunschweig', 'Kiel', 'Aachen', 'Chemnitz',
  'Halle', 'Magdeburg', 'Freiburg im Breisgau', 'Krefeld', 'Lübeck',
  'Mainz', 'Erfurt', 'Oberhausen', 'Rostock', 'Kassel',
  'Hagen', 'Saarbrücken', 'Hamm', 'Potsdam', 'Ludwigshafen am Rhein',
  'Mülheim an der Ruhr', 'Oldenburg', 'Osnabrück', 'Leverkusen', 'Heidelberg',
  'Solingen', 'Darmstadt', 'Herne', 'Neuss', 'Regensburg',
  'Paderborn', 'Ingolstadt', 'Offenbach am Main', 'Würzburg', 'Fürth',
  'Ulm', 'Heilbronn', 'Pforzheim', 'Wolfsburg', 'Göttingen',
  'Bottrop', 'Reutlingen', 'Koblenz', 'Bremerhaven', 'Recklinghausen',
  'Bergisch Gladbach', 'Erlangen', 'Jena', 'Remscheid', 'Trier',
  'Salzgitter', 'Moers', 'Siegen', 'Hildesheim', 'Cottbus',
  'Bautzen', 'Detmold', 'Berlin', 'Frankfurt / Oder', 'Oranienburg',
  'Herford', 'Wuppertal', 'Wiesbaden', 'Villingen-Schwenningen', 'Landshut',
  'Kempten', 'Amberg', 'Passau', 'Hof', 'Bamberg',
  'Gütersloh', 'Suhl'
]

if __name__ == "__main__":
  # key = 'AIzaSyD_PdV1xDgjKOAurk3SWWsoOb4Lj3Jz8BU'  # franz key
  key = 'AIzaSyDRGsKy8xvOixFivn2bCaaWpgO-SKhyNOo' # nue key
  count_apicalls = 0
  suchbegriff = 'Stadtplaner'
  plz_or_city = big_citys
  for i in plz_or_city:
    count_apicalls += api_call(i, suchbegriff, key, col_name=suchbegriff)
    final_result = dict(anzahl_api_calls=count_apicalls)
    print(i)
    print(final_result)
    print(get_places_details.cache_info())
    print('====================================')
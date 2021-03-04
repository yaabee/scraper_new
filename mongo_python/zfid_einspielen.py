from typing import overload
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
def remove_escapechars(string_value):
    '''
    remove escape chars from given field
    '''
    assert isinstance(string_value, str), 'field_value ist kein string'
    string_value = ' '.join(string_value.splitlines())
    escapes = ''.join([chr(char) for char in range(1, 32)])
    translator = str.maketrans('', '', escapes)
    return ' '.join([x for x in string_value.translate(translator).split(' ') if x])


#plz test


def check_website(website):
  if 'https://www' in website:
    website = website.replace('https://www.', 'www.info@')
  elif 'https://' in website:
    website = website.replace('https://', 'www.info@')
  elif 'http://www' in website:
    website = website.replace('http://www.', 'www.info@')
  elif 'http://' in website:
    website = website.replace('http://', 'www.info@')
  elif 'www.' in website and not 'info@' in website:
    website = website.replace('www.', 'www.info@')
  elif 'www.' not in website:
    website = f'www.info@{website}'
  if '.de/' in website or '.com/' in website or '.nl/' in website:
    ind = website.index('/')
    website = website[:ind]
  try: 
    url = 'http://192.168.100.239:9099/003mailcheck' 
    payload = dict(firma_email=website)
    return requests.post(url, json=payload).json()
  except Exception as e:
    print(f'error: {e}')
  


def zfid_einspielen(db_name, col_name):
  client = MongoClient('192.168.100.5:27017')
  collection = client[db_name][col_name]
  cursor = collection.find({'ZFID': {'$exists': False}})
  for i in cursor:
    payload_google = dict(
      Firma=remove_escapechars(i['Firma']),
      Straße=remove_escapechars(i['StrasseUndNr']),
      PLZ=i['PLZ'],
      Ort=remove_escapechars(i['Ort']),
      Telefon=i['Telefon'],
      Internet=check_website(i['Homepage'])['domain'],
      # Fax=i['Fax'],
      Fax='xxxxx',
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
  #google_google_gebäudetechnik_marburg_xlsx
  db_name = 'scrp_listen'
  col_name = 'energie_effizienz_full'
  zfid_einspielen(db_name, col_name)

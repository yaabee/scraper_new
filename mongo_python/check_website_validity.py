
from pymongo import MongoClient
import requests
import pandas as pd

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

def check_email_validiy(db_name, col_name):
  client = MongoClient('192.168.100.5:27017')
  collection = client[db_name][col_name]
  cursor1 = collection.find({'WebsiteStatus.online': False, 'WebsiteStatus.mail': {'$ne': 'www.info@xxxxx'}})
  cursor2 = collection.find({'WebsiteStatus.online': True})
  cursor3 = collection.find({'WebsiteStatus.online': {'$exists': True}, 'WebsiteStatus.mail': {'$ne': 'www.info@xxxxx'}})
  print(len(list(cursor1)))
  print(len(list(cursor2)))
  print(len(list(cursor3)))
  # for i in cursor:
  #   print(i['Internet'])
  #   r = check_website(i['Internet'])
  #   collection.update_one(
  #     {'ZFID': i['ZFID']},
  #     {'$set': {'WebsiteStatus': r}}
  #   )

if __name__ == '__main__':
  db_name = 'scrp_listen'
  col_name = 'heinze_zfid'
  check_email_validiy(db_name, col_name)


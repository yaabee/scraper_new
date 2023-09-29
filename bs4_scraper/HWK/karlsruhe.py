import time
from typing import List, Union
from bs4 import BeautifulSoup, Tag, NavigableString
import requests
import re
import pprint
import datetime
from pymongo import MongoClient

def insert_new_dataset_into_mdb(mdb_uri, datenbank, collection, datensatz):
  client = MongoClient(mdb_uri, 27017, maxPoolSize=500)
  db = client[datenbank]
  collection = db[collection]
  collection.insert_one(datensatz)

def is_new_dataset(mdb_uri, datenbank, collection, firmenname):
  client = MongoClient(mdb_uri, 27017, maxPoolSize=500)
  db = client[datenbank]
  collection = db[collection]
  ds = collection.find_one({'Firma': firmenname})
  return not bool(ds)


# client = MongoClient('192.168.100.5', 27017, maxPoolSize=500)
# col = client['scrp_listen']['hwk_karlsruhe']

def clean_paragraph(p_tag: Union[Tag, NavigableString, None]) -> List[str]:
    if not p_tag:
        return []
    # Get the text content of the <p> tag and split it by <br> tags
    split_text = p_tag.get_text(separator='br/').split('br/')
    # Clean up the text and remove leading/trailing whitespaces
    split_text = [text.strip() for text in split_text if text.strip()]
    return split_text

def get_unix_timestamp():
    current_datetime = datetime.datetime.now()
    return int(current_datetime.timestamp())

offset = 9400
while 1:
    url = f'https://www.hwk-karlsruhe.de/betriebe/suche-63,0,bdbsearch.html?limit=&search-searchterm=&search-job=&search-local=&search-filter-zipcode=*&search-filter-radius=20&search-filter-jobnr=&search-filter-training=&offset={offset}'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    if soup.find('li',class_="next disabled"):
        break

    links = soup.find_all("a", href=re.compile("betriebe/"))
    filtered_links = [x['href'] for x in links if 'suche' not in  x['href']]

    for link in filtered_links:
        single_page = requests.get('https://www.hwk-karlsruhe.de' + link)
        soup_single_page = BeautifulSoup(single_page.content, 'html.parser')

        complete_ds = {
            'Firma': '',
            'Telefon': '',
            'Fax': '',
            'StrasseUndNr': '',
            'PLZ': '',
            'Ort': '',
            'Email': '',
            'Homepage': '',
            'Branche': [],
            'ISO': datetime.datetime.today().isoformat(),
            'Timestamp': get_unix_timestamp()
        }


        #BETRIEB
        if betrieb := soup_single_page.find('h5', text='Betrieb'):
            betrieb_clean = clean_paragraph(betrieb.find_next())
            complete_ds['Firma'] = betrieb_clean[0]
            if len(betrieb_clean) > 1:
                complete_ds['StrasseUndNr'] = betrieb_clean[1]
            if len(betrieb_clean) > 2:
                complete_ds['PLZ'] = betrieb_clean[2].split(' ')[0][2:]
                complete_ds['Ort'] = betrieb_clean[2].split(' ')[1].strip()
        
        #Kontakt
        if adresse := soup_single_page.find('span', class_="glyphicon glyphicon-ansprechpartner"):
            adresse_clean = clean_paragraph(adresse.find_next())
            complete_ds['Telefon'] = ''.join([x.replace('Telefon', '').strip() for x in adresse_clean if 'Telefon' in x])
            complete_ds['Fax'] = ''.join([x.replace('Fax', '').strip() for x in adresse_clean if 'Fax' in x])
            complete_ds['Handy'] = ''.join([x.replace('Handy', '').strip() for x in adresse_clean if 'Handy' in x])
            complete_ds['Email'] = ''.join([x.replace('--at--', '@').strip() for x in adresse_clean if '--at--' in x])
            complete_ds['Homepage'] = ''.join([x.strip() for x in adresse_clean if 'www.' in x])

        #BRANCHE
        if branche := soup_single_page.find('h5', text='Eingetragene Berufe'):
            branche_clean = clean_paragraph(branche.find_next())
            complete_ds['Branche'] = branche_clean
        
        # pprint.pprint(complete_ds)
        # print('+++++++++++++++++++++++++++++++++++++')


        is_new_data = is_new_dataset(mdb_uri="192.168.100.5",
                                datenbank='scrp_listen',
                                collection='hwk_karlsruhe',
                                firmenname=complete_ds['Firma'])


        if is_new_data:

            insert_new_dataset_into_mdb(mdb_uri="192.168.100.5",
                                datenbank='scrp_listen',
                                collection='hwk_karlsruhe',
                                datensatz=complete_ds)
        else:
            print('found', complete_ds['Firma'])
        
        time.sleep(8)
        print('mannheim',offset)


    offset += 50

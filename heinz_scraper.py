from pymongo import MongoClient, errors
from bs4 import BeautifulSoup, SoupStrainer
import requests
from pprint import pprint
from time import sleep
import unicodedata

def insert_new_dataset_into_mdb(mdb_uri, datenbank, collection, datensatz):
  client = MongoClient(mdb_uri, 27017, maxPoolSize=500)
  db = client[datenbank]
  collection = db[collection]
  collection.insert_one(datensatz)

page_nr = 1
while page_nr <= 2895:
    # url = 'https://www.heinze.de/expertenprofile-zu/?s=1&d=c'
    url = f'https://www.heinze.de/expertenprofile-zu/?s=1&p={page_nr}&d=c'
    req = requests.get(url)
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    soup = BeautifulSoup(req.text, 'html.parser')
    links = soup.find_all('a', class_='cssHeadline')
    for link in links:
        complete_dataset = {}
        req = requests.get(f"https://www.heinze.de{link['href']}")
        soup_2 = BeautifulSoup(req.text, 'html.parser')
        name = soup_2.find('p', itemprop='legalName').get_text(strip=True)
        complete_dataset['Firma'] = name
        if strasse := soup_2.find('p', itemprop='streetAddress'):
            complete_dataset['Strasse'] = strasse.text.strip()
        else:
            complete_dataset['Strasse'] = 'xxxxx'
        if plz := soup_2.find('span', itemprop='postalCode'):
            complete_dataset['PLZ'] = plz.text.strip()
        else:
            complete_dataset['PLZ'] = 'xxxxx'
        if ort := soup_2.find('span', itemprop='addressLocality'):
            complete_dataset['Ort'] = ort.text.strip()
        else:
            complete_dataset['Ort'] = 'xxxxx'
        if land := soup_2.find('p', itemprop='addressCountry'):
            complete_dataset['Land'] = land.text.strip()
        else:
            complete_dataset['Land'] = 'xxxxx'
        if tel := soup_2.find('a', itemprop='telephone'):
            tel = tel.get_text(strip=True)
            if 'Tel. ' in tel:
                tel = tel.replace('Tel. ', '')
        else:
            tel = 'xxxxx'
        complete_dataset['Telefon'] = tel
        if fax := soup_2.find('a', itemprop='faxNumber'):
            fax = fax.get_text(strip=True)
            if 'Fax ' in fax:
                fax = fax.replace('Fax ', '')
        else:
            fax = 'xxxxx'
        complete_dataset['Fax'] = fax
        if email := soup_2.find('a', itemprop='email'):
            email = email.get_text(strip=True)
        else:
            email = 'xxxxx'
        complete_dataset['Email'] = email
        if web := soup_2.find('a', itemprop='url'):
            web = web.get_text(strip=True)
            if 'http://' in web:
                web = web.replace('http://', '')
            elif 'https://' in web:
                web = web.replace('https://', '')
        else:
            web = 'xxxxx'
        complete_dataset['Internet'] = web
        complete_dataset['Ansprechpartner'] = []
        if card_texts := soup_2.find_all('div', class_='cardText'):
            for card in card_texts:
                ap_card = {}
                if ap_name := card.find(['p','a'], class_='cssHeadline'):
                    ap_card['ap_name'] = ap_name.get_text(strip=True)
                else:
                    ap_card['ap_name'] = 'xxxxx'
                if ap_rolle := card.find('div', class_='cssText').p:
                    ap_card['ap_rolle'] = ap_rolle.get_text(strip=True)
                else:
                    ap_card['ap_rolle'] = 'xxxxx'
                if ap_tel := card.find('div', class_='cssText').a:
                    if 'Tel. ' in ap_tel:
                        ap_card['ap_tel'] = ap_tel.get_text(strip=True)
                    else:
                        ap_card['ap_tel'] = 'xxxxx'
                else:
                    ap_card['ap_tel'] = 'xxxxx'
                complete_dataset['Ansprechpartner'].append(ap_card)
        if profile := soup_2.find_all('p', {'class': ['cssValue', 'cssKey']}):
            value = []
            cur_titel = 'xxxxx'
            for profil in profile:
                if 'cssKey' in profil['class']:
                    cur_titel = profil.get_text(strip=True)
                    complete_dataset[cur_titel] = []
                elif 'cssValue' in profil['class']:
                    clean_profile = unicodedata.normalize("NFKD", profil.text.strip())
                    complete_dataset[cur_titel].append(clean_profile)
        try:
            insert_new_dataset_into_mdb(mdb_uri="192.168.100.5",
                                datenbank='scrp_listen',
                                collection='heinze',
                                datensatz=complete_dataset)
        except errors.DuplicateKeyError:
            print('had duplicatekey error!!!!!!!!!!!!!!!!!!!!')
            continue

        pprint(complete_dataset, indent=2)
        print('page_nr', page_nr)
        print('----------------------')
    page_nr += 1


    """ 
    name +
    strasse +
    plz + ort +
    land +
    tel +
    mail +
    web +
    team +
    gewerk +
    anzahl mitarbeiter +
    leistungsprofil +
    """
    


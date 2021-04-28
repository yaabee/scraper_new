from pymongo import MongoClient, errors
from bs4 import BeautifulSoup, SoupStrainer
import requests
from pprint import pprint
from time import sleep
import unicodedata
import re

def insert_new_dataset_into_mdb(mdb_uri, datenbank, collection, datensatz):
  client = MongoClient(mdb_uri, 27017, maxPoolSize=500)
  db = client[datenbank]
  collection = db[collection]
  collection.insert_one(datensatz)

num = 129430
counter = 0
#1000000
while num < 129431:
    url = f'https://www.xpertio.net/atelier-reissbrett_bruchhausen-vilsen/10/{num}'

    page = requests.get(url)
    if page.ok:
        counter += 1
        print('num', num)
        print('counter', counter)
        complete_dataset = {}
        soup = BeautifulSoup(page.content, 'html.parser')
        if business_card_title := soup.find('header', {'class': 'business-card-title'}):
            complete_dataset['business_card'] = business_card_title.text.strip()
        else:
            complete_dataset['business_card'] = 'xxxxx'

        if firma := soup.find('h1', {'class': 'h2'}):
            complete_dataset['Firma'] = firma.text.strip()
        else:
            complete_dataset['Firma'] = 'xxxxx'
        if adresse := soup.find('a', {'class': 'business-card-address'}):
            complete_dataset['Addresse'] = adresse.text.strip()
        else:
            complete_dataset['Addresse'] = 'xxxxx'
        if  tele := soup.find('span', {'class': 'business-card-phone display-block margin-left20'}):
            complete_dataset['Telefon'] = tele.text.strip()
        else:
            complete_dataset['Telefon'] = 'xxxxx'
        if  fax := soup.find('span', {'class': 'business-card-fax display-block margin-left20'}):
            complete_dataset['Fax'] = fax.text.strip()
        else:
            complete_dataset['Fax'] = 'xxxxx'
        if  ap := soup.find('span', {'class': 'business-card-person display-block margin-left20'}):
            complete_dataset['Ansprechpartner'] = ap.text.strip().split('Ansprechpartner:')[1].strip()
        else:
            complete_dataset['Ansprechpartner'] = 'xxxxx'
        if  inet := soup.find('a', {'id': 'cphContainer_cphMain_cBusinessCard_hlWebsite'}):
            complete_dataset['Internet'] = inet.text.strip()
        else:
            complete_dataset['Internet'] = 'xxxxx'
        
        sidebar = soup.find_all('p', {'class': 'h4 sidebar-title-open'})
        for i in sidebar:
            print(i)
            if i.text.strip() == 'Branche':
                ticks = soup.find('ul', {'class': 'ticks'})
                branchen = ticks.find_all('a')
                complete_dataset['Branche'] = [t.text.strip() for t in branchen]
            elif i.text.strip() == 'Leistungen':
                tags = soup.find('ul', {'class': 'tags'})
                leistungen = tags.find_all('a')
                complete_dataset['Leistungen'] = [l.text.strip() for l in leistungen]
            elif i.text.strip() == 'Unternehmensprofil':
                unter_profil = soup.find('div', {'id': 'cphContainer_cphMain_ccdwCompanyData_pnlCompanyData'})
                print(unter_profil)


        print(len(sidebar))
        pprint(complete_dataset, indent=2)

    else:
        print(f'nada {num}')

    num += 1

    # print(soup.prettify())

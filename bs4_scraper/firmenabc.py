from bs4 import BeautifulSoup
import requests
import pprint
import re
from pymongo import MongoClient
import time

def insert_new_dataset_into_mdb(mdb_uri, datenbank, collection, datensatz):
  client = MongoClient(mdb_uri, 27017, maxPoolSize=500)
  db = client[datenbank]
  collection = db[collection]
  collection.insert_one(datensatz)

def main():
  n = 612800
  while n < 715300:
    url = f'https://www.firmenabc.at/result.aspx?what=&where=%c3%96sterreich&exact=false&inTitleOnly=false&l=&si={n}&iid=&sid=&did=&cc='
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    links = soup.find_all('a', itemprop='url')
    for link in links:
      data = {'Firma': '', 'StrasseUndNr': '', 'PLZ': '', 'Ort': '', 'Telefon': '', 'Fax': '', 'Email':'', 'Homepage': '', 'Suchbegriffe': [], 'Branchen': []}

      
      homepage = requests.get(link['href'])
      homepage_soup = BeautifulSoup(homepage.content, 'html.parser')
      if name := homepage_soup.find('div', itemprop='name'):
        data['Firma'] = name.text.strip()
      if strasse := homepage_soup.find('span', itemprop='streetAddress'):
        data['StrasseUndNr'] = strasse.text.strip()
      if plz := homepage_soup.find('span', itemprop='postalCode'):
        data['PLZ'] = plz.text.strip()
      if ort := homepage_soup.find('span', itemprop='addressLocality'):
        data['Ort'] = ort.text.strip()
      if tele := homepage_soup.find('span', itemprop='telephone'):
        data['Telefon'] = tele.text.strip()
      if homepage := homepage_soup.find('a', itemprop='url'):
        data['Homepage'] = homepage.text.strip()
      if email := homepage_soup.find('a', text=re.compile('@')):
        data['Email'] = email.text.replace('\u200b', '').strip()
      
      if suchbegriffe := homepage_soup.find_all('a', class_='label'):
        data['Suchbegriffe'] = [x.text.strip() for x in suchbegriffe]

      if fax := homepage_soup.find('span', itemprop='faxNumber'):
         data['Fax']= fax.text.strip()

      if branchen := homepage_soup.find_all('ol', class_='breadcrumb search'):
        lis = [x.text.strip() for x in branchen]
        for li in lis:
          data['Branchen'].append(li.split(',')[0].split('in')[0].strip())

      pprint.pprint(data, indent=2)

      insert_new_dataset_into_mdb(mdb_uri="192.168.100.5",
                          datenbank='scrp_listen',
                          collection='firmenabc_gesamt',
                          datensatz=data)
    time.sleep(0.5)
    n += 50


if __name__ == '__main__':
  main()
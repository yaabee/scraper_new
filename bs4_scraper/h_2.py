from pymongo import MongoClient, errors
from bs4 import BeautifulSoup, SoupStrainer
import requests
from pprint import pprint
from time import sleep
import unicodedata
import ssl
import pprint


client_5 = MongoClient('192.168.100.5:27017')
client_239 = MongoClient('192.168.100.239:27017',
                         username='mongoroot',
                         password='9gCaPFhotG2CNEoBRdgA',
                         authSource='admin',
                         authMechanism='SCRAM-SHA-256',
                         ssl=True,
                         ssl_cert_reqs=ssl.CERT_NONE)


zf_239 = client_239['ZentralerFirmenstamm']['ZentralerFirmenstamm']
odin_yb = client_239['odin']['ZOObjekte_yanghi']
scrp_listen = client_5['scrp_listen']['heinze_zfid']
# zf_yb = ['ZentralerFirmenstamm']['ZentralerFirmenstamm_yan']
staticdata_access = client_239['staticdata']['AllgAllgemeineVorlagen_Branchenliste']
staticdata_dis = client_239['staticdata']['automatischeBranche']
original_zf = client_239['ZentralerFirmenstamm']['ZentralerFirmenstamm2']
original_new = client_239['ZentralerFirmenstamm']['ZentralerFirmenstamm_new2']


def insert_new_dataset_into_mdb(mdb_uri, datenbank, collection, datensatz):
    client = MongoClient(mdb_uri, 27017, maxPoolSize=500)
    db = client[datenbank]
    collection = db[collection]
    collection.insert_one(datensatz)


page_nr = 685
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
        complete_dataset['Ansprechpartner'] = []
        if card_texts := soup_2.find_all('div', class_='cardText'):
            for card in card_texts:
                ap_card = {}
                if ap_name := card.find(['p', 'a'], class_='cssHeadline'):
                    ap_card['ap_name'] = ap_name.get_text(strip=True)
                else:
                    ap_card['ap_name'] = 'xxxxx'
                if ap_rolle := card.find('div', class_='cssText').p:
                    ap_card['ap_rolle'] = ap_rolle.get_text(strip=True)
                else:
                    ap_card['ap_rolle'] = 'xxxxx'
                if ap_tel := card.find('div', class_='cssText').a:
                    if 'tel:' in ap_tel['href']:
                        ap_card['ap_tel'] = ap_tel['href'].replace(
                            'tel:', '').strip()
                    else:
                        ap_card['ap_tel'] = 'xxxxx'
                else:
                    ap_card['ap_tel'] = 'xxxxx'
                complete_dataset['Ansprechpartner'].append(ap_card)
        # if profil := soup_2.find('div', class_='cardText').a:
        #     if 'profil' in profil['href']:
        #         print(f'https://www.heinze.de{profil["href"]}')
        #         req = requests.get(f'https://www.heinze.de{profil["href"]}')
        #         soup_3 = BeautifulSoup(req.text, 'html.parser')
        #         links = soup_3.find(
        #             'div', class_='cssASideContact cssNewBlock').a
        #         # for i in links:
        #         #     print(i['href'])
        #         print(links['href'])
        #         print(ap_card['ap_tel'])

        pipeline = [
            {'$match': {
                'Firma': complete_dataset['Firma']
            }}
        ]

        agg = list(scrp_listen.aggregate(pipeline))

        if agg:
            pprint.pprint(agg[0]['ZFID'])
            scrp_listen.update_one(
                {'ZFID': agg[0]['ZFID']}, {'$set': {'Ansprechpartner': complete_dataset['Ansprechpartner']}})
            print(complete_dataset['Ansprechpartner'])

        # pprint(complete_dataset, indent=2)
        print('page_nr', page_nr)
        print('----------------------')
    page_nr += 1

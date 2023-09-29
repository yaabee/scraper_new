#baunetz.de

from typing import Any, Dict, List, TypedDict
import requests
from  pymongo import MongoClient, errors
from bs4 import BeautifulSoup
import ssl
from pprint import pprint

client_8 = MongoClient(
    "mongodb://mongoroot:9gCaPFhotG2CNEoBRdgA@192.168.100.8:27017",
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE,
)
client = MongoClient("192.168.100.5:27017")

def insert_new_dataset_into_mdb(mdb_uri, datenbank, collection, datensatz):
    client = MongoClient(mdb_uri, 27017, maxPoolSize=500)
    db = client[datenbank]
    collection = db[collection]
    collection.insert_one(datensatz)

class TOptions(TypedDict):
    checkFakeFirma: bool
    ensureWrite: bool
    forceInsert: bool
    returnDocument: bool

class FirmaAnlegenPaylod(TypedDict):
    options: TOptions
    Firma: str
    PLZ:str
    Ort: str
    Telefon: str
    Straße: str
    Email: str
    Internet: str
    Fax: str


class Result(TypedDict):
    document: Any
    id: str
    neuangelegt: bool


class FirmaAnlegenResponse(TypedDict):
    ok: bool
    result: Result

def firmaAnlegen(payload: Dict[str, FirmaAnlegenPaylod])-> FirmaAnlegenResponse:
    url = "http://192.168.100.239:9099/zf_adresse_neuanlageNachAccess"
    r: FirmaAnlegenResponse  = requests.post(url, json=payload).json()
    return r 

#finde eine nummer im List[str]
def stripInsideString(string_array: List[str])-> List[str]:
    """
    parameter: [
        'Sauerbruch Hutton', 'Lehrter Straße 57', 'D-10557 Berlin', '+49 (0) 30 397821-0', '+49 (0) 30 39782-30', 'www.sauerbruchhutton.com']
    """
    y= [(x, e ) for e, x in enumerate(string_array) if '-' in x or '/' in x]

    rs = [(requests.post('http://192.168.100.239:9099/005phonenumbers', json={'firma_telefon': x[0]}), x[1]) for x in y]
    rs = [(x[0].json(),x[1]) for x in rs]
    rs = [(x[0]['firma_telefon_clean'], x[1]) for x in rs if x[0]['firma_telefon_clean'][0] == '+']

    idxs = [e[1] for e in rs]

    telefon_cleans = [x[0] for x in rs] 
    telefon_cleans.sort() #fax sollte groesser sein als tele

    string_array = [x for e , x in enumerate(string_array) if e not in idxs] #parse ohne tele/fax

    if telefon_cleans:
        string_array += [f'telefon: {telefon_cleans[0]}'] #adde tele
        if len(telefon_cleans)> 1:
            string_array += [f'fax: {telefon_cleans[1]}'] # adde fax

    return string_array
    

def getContact(link: str, firma: str) -> str:
    """
    parsed seite nach ds,
    spielt ds ein
    return zfid
    """
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    if address := soup.find('div', {'class': 'profile-meta-contact profile-meta-contact--active'}):
        tokens = [x.strip() for x in address.getText().replace('[email\xa0protected]', '').replace('\n', ';').split(';') if x]
        tokens = stripInsideString(tokens)
        try:
            r = requests.post('http://192.168.100.239:9099/impressumsparser/getParsedText', json={'textarray': tokens}).json()
            if r:
                r = r['responseData']
                payload = {
                    "Fax": r['fax'] if r['fax'] else '',
                    "Firma": firma,
                    "Internet": 'xxxxx',
                    "Ort": r['Ort'],
                    "PLZ":r['PLZ'],
                    "Straße": r['StrasseUndNr'],
                    "Telefon": r['telefon'] if r['telefon'] else '',
                    "options": {
                        "checkFakeFirma": False,
                        "ensureWrite": False,
                        "forceInsert": False,
                        "returnDocument": False
                    }
                }
                r = firmaAnlegen(payload)
                print(r)
                if r['ok'] and r['result']['id'] != '618cecec8abb08d5ed76bd50':
                    return r['result']['id']
        except Exception as e:
            print(f'error with {firma} {link}')
            print(e.args)
    return ''



def main():
    for i in range(3):
        page = requests.get(f'https://www.baunetz.de/ranking/?area=ranking&type=nat&page={i + 1}')
        soup = BeautifulSoup(page.content, 'html.parser')
        all_tr = soup.find_all('tr')
        count = 0
        count_links= 0
        count_none=0
        for tr in all_tr[1:]:
            x = {
                'rank': '',
                'firma': '',
                'link': '',
                'zfid': '',
                'firma_tele': '',
                'ort': ''
            }
            if ort := tr.find('td', {'class': 'zweitwert'}):
                x['ort'] = ort.text
            rank = tr.find('td', {'class': 'first'})
            x['rank'] = rank.text
            wert = tr.find('td', {'class': 'wert'})
            if link:= wert.find('a'):
                firma = link.find('span').text
                x['firma']= firma
                x['link']=link['href']
            else:
                x['firma'] =  wert.text

            if ds := client_8['ZentralerFirmenstamm']['ZentralerFirmenstamm'].find_one({'Firma': {'$regex': x['firma']}, 'Ort': x['ort']}):
                x['zfid'] = ds['ZFID']
                x['firma_tele'] = ds['Firma']
                count += 1
            elif x['link']:
                r = getContact(x['link'], x['firma'])
                if r:
                    x['firma_tele'] = x['firma']
                    x['zfid'] = r
                count_links +=1
            else:
                count_none +=1 
            pprint(x, indent=2)
            try:
                insert_new_dataset_into_mdb(mdb_uri="192.168.100.5",
                                            datenbank='scrp_listen',
                                            collection='ranking300',
                                            datensatz=x)
            except errors.DuplicateKeyError:
                print('had duplicatekey error!!!!!!!!!!!!!!!!!!!!')
                continue
        print(i, count, count_links, count_none)
    

if __name__ == '__main__':
    print(any([]))
# add parent-module-path
from re import S
from bs4 import BeautifulSoup
import requests
from pprint import pprint
from pymongo import MongoClient, errors
import time


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


def insert_new_dataset_into_mdb(mdb_uri, datenbank, collection, datensatz):
    client = MongoClient(mdb_uri, 27017, maxPoolSize=500)
    db = client[datenbank]
    collection = db[collection]
    collection.insert_one(datensatz)


def get_clean_telefon(url, tele):
    payload = {
        'firma_telefon': tele
    }
    return requests.post(url, json=payload).json()


def get_geodata(url, plz, strasseundnr, ort):
    data = {
        'Land': '',
        'Ort': ort,
        'PLZ': plz,
        'StrasseUndNr': strasseundnr,
        "options": {
            "returnMultiple": False
        }
    }
    return requests.post(url, json=data)


def remove_escapechars(string_value):
    '''
    remove escape chars from given field
    '''
    assert isinstance(string_value, str), 'field_value ist kein string'
    string_value = ' '.join(string_value.splitlines())
    escapes = ''.join([chr(char) for char in range(1, 32)])
    translator = str.maketrans('', '', escapes)
    return string_value.translate(translator)


def energie_effizienz_experten(url):
    # private Bauherrern
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    experten_db = soup.find_all('div', class_='expertendb_single')
    for single in experten_db:
        complete_dataset = {}
        if name := single.find('div', class_='header-text'):
            name = remove_escapechars(name.text).strip()
            name = ' '.join([x.strip() for x in name.split(' ') if x])
            complete_dataset['name'] = name
        else:
            name = 'xxxxx'
        complete_dataset['name'] = name
        if tele := single.find('div', class_='telefon'):
            tele = tele.text
        else:
            tele = 'xxxxx'
        tele = get_clean_telefon(
            'http://192.168.100.239:9099/005phonenumbers', tele)
        complete_dataset['Telefon'] = tele['firma_telefon']
        complete_dataset['TelefonRaw'] = tele['firma_telefon_clean']
        try:
            if email := single.find('div', class_='email'):
                at = '@'
                email.select_one('.print-color').replaceWith(at)
                email = email.text.strip()
            else:
                email = 'xxxxx'
        except AttributeError as e:
            email = 'xxxxx'
            print(e.args)
        complete_dataset['Email'] = email
        adress = single.find('p', class_='adresse')
        split_adress = [x.strip() for x in adress.text.split('\n')]
        firma = split_adress[0]
        if firma:
            firma = firma
        else:
            firma = name
        complete_dataset['Firma'] = remove_escapechars(firma.strip())
        strasseundnr = split_adress[1]
        plz = split_adress[2][:5]
        ort = split_adress[2][6:]
        geodata = get_geodata('http://192.168.100.239:9099/geocoder',
                              plz, strasseundnr, ort).json()['result']['geocode']
        try:
            if homepage := single.find('div', class_='www'):
                page = homepage.find('a')
                homepage = check_website(page['href'])['domain']
            else:
                homepage = 'xxxxx'
        except Exception as e:
            homepage = 'xxxxx'
            print(e.args)
        complete_dataset['Homepage'] = homepage

        if geodata['Full Address'] != ['xxxxx']:
            complete_dataset['Ort'] = geodata['Ort']
            complete_dataset['StrasseUndNr'] = geodata['StrasseUndNr']
            complete_dataset['PLZ'] = geodata['PLZ']
            complete_dataset['StrassenId'] = geodata['StrassenId']
            complete_dataset['Strassenname'] = geodata['Strassenname']
            complete_dataset['Hausnummer'] = geodata['Hausnummer']
            complete_dataset['Location'] = geodata['Location']
            complete_dataset['Bundesland'] = geodata['Bundesland']
            complete_dataset['Land'] = geodata['Land']
        else:
            complete_dataset['Ort'] = 'xxxxx'
            complete_dataset['StrasseUndNr'] = 'xxxxx'
            complete_dataset['PLZ'] = 'xxxxx'
            complete_dataset['StrassenId'] = 'xxxxx'
            complete_dataset['Strassenname'] = 'xxxxx'
            complete_dataset['Hausnummer'] = 'xxxxx'
            complete_dataset['Location'] = 'xxxxx'
            complete_dataset['Bundesland'] = 'xxxxx'
            complete_dataset['Land'] = 'xxxxx'
        if branche := single.find('div', class_='expertendb_details toggle__target'):
            branche = [x.text for x in branche.find_all('dd')]
        else:
            branche = ['xxxxx']
        complete_dataset['branche'] = branche
        if studium := single.find('p', class_='berufsgruppe'):
            studium = studium.text.strip()
        else:
            studium = 'xxxxx'
        complete_dataset['Berufsgruppe'] = remove_escapechars(studium)
        if foerderung := single.find('div', class_='fp fp--privat'):
            small_col = foerderung.find(
                'div', class_='c-column c-column--small')
            # Energieberatung
            energieberatung = small_col.find_all('dd')
            img_ = small_col.find_all('img')
            for a, b in zip(energieberatung, img_):
                if b['src'] == '/typo3conf/ext/ww_site/Resources/Public/img/checkbox.svg':
                    b = True
                elif b['src'] == '/typo3conf/ext/ww_site/Resources/Public/img/checkbox--empty.svg':
                    b = False
                titel = '_'.join(a.text.split(' '))
                complete_dataset[titel] = b
            large_col = foerderung.find(
                'div', class_='c-column c-column--large')
            # Bundesfoerderung(Wohngebaeude)
            bafa = large_col.find_all('dd')
            checks = large_col.find_all('img')
            for i, j in zip(bafa, checks):
                if j['src'] == '/typo3conf/ext/ww_site/Resources/Public/img/checkbox.svg':
                    j = True
                elif j['src'] == '/typo3conf/ext/ww_site/Resources/Public/img/checkbox--empty.svg':
                    j = False
                titel = '_'.join(i.text.split(' '))
                complete_dataset[titel] = j
        try:
            insert_new_dataset_into_mdb(mdb_uri="192.168.100.5",
                                        datenbank='scrp_listen',
                                        collection='energie_effizienz_full_06092021',
                                        datensatz=complete_dataset)
        except errors.DuplicateKeyError:
            print('had duplicatekey error!!!!!!!!!!!!!!!!!!!!')
            continue
        pprint(complete_dataset, indent=2)
        print('==========================================')


if __name__ == '__main__':
    # ca10k
    # ca3k

    # url_private_bauherren = f'https://www.energie-effizienz-experten.de/fuer-private-bauherren/finden-sie-experten-in-ihrer-naehe/suchergebnis?tx_wwdenaexpertendb_pi1%5Bcontroller%5D=Search&tx_wwdenaexpertendb_pi1%5Bpage%5D={n}'
    n = 0
    while n <= 686:
        url_unternehmen_kommunen = f'https://www.energie-effizienz-experten.de/fuer-unternehmen-und-kommunen/finden-sie-experten-in-ihrer-naehe/suchergebnis?tx_wwdenaexpertendb_pi1%5Bcontroller%5D=Search&tx_wwdenaexpertendb_pi1%5Bpage%5D={n}'
        print(n)
        energie_effizienz_experten(url_unternehmen_kommunen)
        time.sleep(1.5)
        n += 1

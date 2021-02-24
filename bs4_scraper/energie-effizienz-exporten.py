#add parent-module-path
from bs4 import BeautifulSoup
import requests
import re


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
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    experten_db = soup.find_all('div', class_='expertendb_single')
    for single in experten_db:
        if name := single.find('div', class_='header-text'):
            name = remove_escapechars(name.text).strip()
            name = ' '.join([x.strip() for x in name.split(' ') if x])
            print(name)
        if tele := single.find('div', class_='telefon'):
            print(tele.text)
        else:
            tele = 'xxxxx'
            print(tele)
        if email := single.find('div', class_='email'):
            at = '@'
            email.select_one('.print-color').replaceWith(at)
            print(email.text.strip())
        adress = single.find('p', class_='adresse')

        # firma = adress.strong.text
        # if firma:
        #     firma = firma
        # else:
        #     firma = 'xxxxx'
        # print(firma)
        split_adress = [x.strip() for x in adress.text.split(r'\n')]
        firma = split_adress[0]
        strasse = split_adress[1]
        plz_ort = split_adress[2]
        print(firma)
        print(strasse)
        print(adress)
        # print(single.prettify())
        print('==========================================')

if __name__ == '__main__':
    #ca10k
    url_private_bauherren = 'https://www.energie-effizienz-experten.de/fuer-private-bauherren/finden-sie-experten-in-ihrer-naehe/suchergebnis?tx_wwdenaexpertendb_pi1%5Bcontroller%5D=Search'
    #ca3k
    url_unternehmen_kommunen = 'https://www.energie-effizienz-experten.de/fuer-unternehmen-und-kommunen/finden-sie-experten-in-ihrer-naehe'
    energie_effizienz_experten(url_private_bauherren)
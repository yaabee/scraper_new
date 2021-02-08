from bs4 import BeautifulSoup, SoupStrainer
import requests
from pprint import pprint

url = 'https://www.heinze.de/expertenprofile-zu/?ft=1&sf=T1717T14935869'
req = requests.get(url)
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}
soup = BeautifulSoup(req.content, 'html.parser')
links = soup.find_all('a', class_='cssHeadline')
for link in links:
    req = requests.get(f"https://www.heinze.de{link['href']}")
    soup_2 = BeautifulSoup(req.content, 'html.parser')
    name = soup_2.find('p', itemprop='legalName').text.strip()
    print(name)
    strasse = soup_2.find('p', itemprop='streetAddress').text.strip()
    print(strasse)
    plz = soup_2.find('span', itemprop='postalCode').text.strip()
    print(plz)
    ort = soup_2.find('span', itemprop='addressLocality').text.strip()
    print(ort)
    land = soup_2.find('p', itemprop='addressCountry').text.strip()
    print(land)
    if tel := soup_2.find('a', itemprop='telephone'):
        tel = tel.text.strip()
        if 'Tel. ' in tel:
            tel = tel.replace('Tel. ', '')
        print(tel)
    else:
        tel = 'xxxxx'
        print(tel)
    if fax := soup_2.find('a', itemprop='faxNumber'):
        fax = fax.text.strip()
        if 'Fax ' in fax:
            fax = fax.replace('Fax ', '')
        print(fax)
    else:
        fax = 'xxxxx'
        print(fax)
    if email := soup_2.find('a', itemprop='email'):
        print(email.text.strip())
    else:
        email = 'xxxxx'
        print(email)
    if web := soup_2.find('a', itemprop='url'):
        web = web.text.strip()
        if 'http://' in web:
            web = web.replace('http://', '')
        elif 'https://' in web:
            web = web.replace('https://', '')
        print(web)
    else:
        web = 'xxxxx'
        print(web)

    if card_texts := soup_2.find_all('div', class_='cardText'):
        for card in card_texts:
            if ap_name := card.find(['p','a'], class_='cssHeadline'):
                print(ap_name.text.strip())
            if ap_rolle := card.find('div', class_='cssText').p:
                print(ap_rolle.text.strip())
            if ap_tel := card.find('div', class_='cssText').a:
                if 'Tel. ' in ap_tel:
                    print(ap_tel.text.replace('Tel. ', '').strip())
            print('++++++++++++++++++++++++')
    profile = soup.find_all('p', {'class': ['cssValue', 'cssKey']})
    print('profile len', len(profile))
    # for profil in profile:
    #     print(profil)
    
    print('==========================================')





    """ 
    name +
    strasse +
    plz + ort +
    land +

    tel +

    mail +
    web +

    team +

    gewerk
    anzahl mitarbeiter
    leistungsprofil
    """
    


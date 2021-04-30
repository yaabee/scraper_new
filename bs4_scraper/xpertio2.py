from pymongo import MongoClient, errors
from bs4 import BeautifulSoup
import requests
from pprint import pprint
from multiprocessing import Process
import threading

def insert_new_dataset_into_mdb(mdb_uri, datenbank, collection, datensatz):
  client = MongoClient(mdb_uri, 27017, maxPoolSize=500)
  db = client[datenbank]
  collection = db[collection]
  collection.insert_one(datensatz)


# num = 129430

def get_xpertio(kategorie, num, till):

    # num = 0
    counter = 0
    # kategorie = 10
    #1000000
    while num < till:
        try:
            url = f'https://www.xpertio.net/atelier-reissbrett_bruchhausen-vilsen/{kategorie}/{num}'
            page = requests.get(url)
            if page.ok:
                counter += 1
                complete_dataset = {}
                soup = BeautifulSoup(page.content, 'html.parser')
                projects = []
                refs = []
                if id := soup.select_one("[rel='canonical']"):
                    complete_dataset['ID'] = id['href']
                else:
                    complete_dataset['ID'] = 'xxxxx'
                if proj := soup.select_one("[id='cphContainer_cphMain_Tabs_Tab1']"):
                    all_projects = proj.find_all('a')
                    projects += [p['href'] for p in all_projects if 'http' in p['href']]
                    complete_dataset['Projekte'] = projects
                else:
                    complete_dataset['Projekte'] = []
                if referenz := soup.select_one("[id='cphContainer_cphMain_Tabs_Tab1_cProjects_upTabObjects']"):
                    all_referenzen = referenz.find_all('a')
                    refs += [r['href'] for r in all_referenzen if 'http' in r['href']]
                    complete_dataset['Referenzen'] = refs
                else:
                    complete_dataset['Referenzen'] = []
                if beschreibung := soup.select_one("[id='cphContainer_cphMain_secDescriptionView']"):
                    all_p = beschreibung.find_all('p')
                    complete_dataset['Beschreibung'] = [p.text.strip() for p in all_p] 
                else:
                    complete_dataset['Beschreibung'] = []
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
                elif adresse := soup.find('span', {'class': 'business-card-address'}):
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
                if sidebar := soup.find_all('p', {'class': 'h4 sidebar-title-open'}):
                    branche_arr = []
                    leistung_arr = []
                    profil = []
                    zertifikate = []
                    for i in sidebar:
                        if i.text.strip() == 'Branche':
                            ticks = soup.find('ul', {'class': 'ticks'})
                            branchen = ticks.find_all('a')
                            branche_arr = [t.text.strip() for t in branchen]
                            if ticks_more := soup.find('ul', {'class': 'ticks ticks-more'}):
                                branchen_more = ticks_more.find_all('a')
                                branche_arr += [tm.text.strip() for tm in branchen_more]
                        elif i.text.strip() == 'Leistungen':
                            tags = soup.find('ul', {'class': 'tags'})
                            leistungen = tags.find_all('a')
                            leistung_arr = [l['title'].strip() for l in leistungen]
                        elif i.text.strip() == 'Unternehmensprofil':
                            unter_profil = soup.find('div', {'id': 'cphContainer_cphMain_ccdwCompanyData_pnlCompanyData'})
                            all_grids = unter_profil.find_all('div', {'class': ['grid-span4', 'grid-span3']})
                            cur_titel = ''
                            cur_value = ''
                            for grid in all_grids:
                                if 'grid-span4' in grid['class']:
                                    cur_titel = grid.text.strip()
                                if 'grid-span3' in grid['class']:
                                    cur_value = grid.get_text(strip=True)
                                if cur_titel and cur_value:
                                    profil.append({cur_titel: cur_value})
                                    cur_value = ''
                                    cur_titel = ''
                        elif i.text.strip() == 'Zertifikate':
                            zerts = soup.find('ul', {'class': 'tags-silent-white margin-left10'})
                            zerts_a = zerts.find_all('a')
                            zertifikate = [a['title'] for a in zerts_a]
                        complete_dataset['Unternehmensprofil'] = profil
                        complete_dataset['Branche'] = branche_arr
                        complete_dataset['Leistungen'] = leistung_arr
                        complete_dataset['Zertifikate'] = zertifikate
                print(f'found {num}, counter {counter}')
                try:
                    insert_new_dataset_into_mdb(mdb_uri="192.168.100.5",
                                        datenbank='scrp_listen',
                                        collection='xpertio',
                                        datensatz=complete_dataset)
                except errors.DuplicateKeyError:
                    print('had duplicatekey error!!!!!!!!!!!!!!!!!!!!')
                    continue

            else:
                print(f'nada {num}, counter {counter}')
            num += 1
        except Exception as e:
            print(f'error @ {num}, counter {counter}')
            print(e.args)
            pass


if __name__ == '__main__':
    '''
    projekte = 0
    fachunternehmen = 11
    haendler / 
    cphContainer_cphMain_Tabs_Tab1_cProjects_upTabObjects
    '''
    # get_xpertio(10, 500)
    t1 = threading.Thread(target=get_xpertio, args=(10, 300000, 400000),)
    t2 = threading.Thread(target=get_xpertio, args=(10, 400000, 500000),)
    t3 = threading.Thread(target=get_xpertio, args=(10, 500000, 600000),)
    t4 = threading.Thread(target=get_xpertio, args=(10, 600000, 700000),)
    t5 = threading.Thread(target=get_xpertio, args=(10, 700000, 800000),)
    t6 = threading.Thread(target=get_xpertio, args=(10, 800000, 900000),)

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()

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


client = MongoClient('192.168.100.5:27017')
# num = 129430
xpertio_col = client['scrp_listen']['xpertio']

def get_xpertio(url):
    

    # num = 0
    counter = 0
    # kategorie = 10
    #1000000
    try:
        page = requests.get(url)
        if page.ok:
            counter += 1
            complete_dataset = {}
            soup = BeautifulSoup(page.content, 'html.parser')
            if sidebar := soup.find_all('p', {'class': 'h4 sidebar-title-open'}):
                produkte = []
                uk_inhalt = []
                uk_titles =[]
                for i in sidebar:
                    if i.text.strip() == 'Produkte':
                        tags = soup.find('ul', {'class': 'tags'})
                        products = tags.find_all('a')
                        produkte = [p['title'].strip() for p in products]
                    if i.text.strip() == 'Produktkaegorien':
                        uk_titles = [ukt.text.strip() for ukt in soup.find_all('span', {'class': 'copytext-bold margin-left10 display-inline-block'})]
                        uk_inhalt = [ukI.find_all('a')['title'] for soup.find_all('ul', {'class': 'circles'})

            # xpertio_col.update_one({'ID': url}, {
            #     '$set': {'Produkte': produkte}
            # })
            



                    # if i.text.strip() == 'Branche':
                    #     ticks = soup.find('ul', {'class': 'ticks'})
                    #     branchen = ticks.find_all('a')
                    #     branche_arr = [t.text.strip() for t in branchen]
                    #     if ticks_more := soup.find('ul', {'class': 'ticks ticks-more'}):
                    #         branchen_more = ticks_more.find_all('a')
                    #         branche_arr += [tm.text.strip() for tm in branchen_more]
                    # elif i.text.strip() == 'Leistungen':
                    #     tags = soup.find('ul', {'class': 'tags'})
                    #     leistungen = tags.find_all('a')
                    #     leistung_arr = [l['title'].strip() for l in leistungen]
                    # elif i.text.strip() == 'Unternehmensprofil':
                    #     unter_profil = soup.find('div', {'id': 'cphContainer_cphMain_ccdwCompanyData_pnlCompanyData'})
                    #     all_grids = unter_profil.find_all('div', {'class': ['grid-span4', 'grid-span3']})
                    #     cur_titel = ''
                    #     cur_value = ''
                    #     for grid in all_grids:
                    #         if 'grid-span4' in grid['class']:
                    #             cur_titel = grid.text.strip()
                    #         if 'grid-span3' in grid['class']:
                    #             cur_value = grid.get_text(strip=True)
                    #         if cur_titel and cur_value:
                    #             profil.append({cur_titel: cur_value})
                    #             cur_value = ''
                    #             cur_titel = ''
                    # elif i.text.strip() == 'Zertifikate':
                    #     zerts = soup.find('ul', {'class': 'tags-silent-white margin-left10'})
                    #     zerts_a = zerts.find_all('a')
                    #     zertifikate = [a['title'] for a in zerts_a]
                    # complete_dataset['Unternehmensprofil'] = profil
                    # complete_dataset['Branche'] = branche_arr
                    # complete_dataset['Leistungen'] = leistung_arr
                    # complete_dataset['Zertifikate'] = zertifikate
            pprint(complete_dataset, indent=2)

            # print(f'found {num}, counter {counter}')
            # try:
            #     insert_new_dataset_into_mdb(mdb_uri="192.168.100.5",
            #                         datenbank='scrp_listen',
            #                         collection='xpertio',
            #                         datensatz=complete_dataset)
            # except errors.DuplicateKeyError:
            #     print('had duplicatekey error!!!!!!!!!!!!!!!!!!!!')
            #     continue

        # else:
        #     print(f'nada {num}, counter {counter}')
        # num += 1
    except Exception as e:
        # print(f'error @ {num}, counter {counter}')
        print(f'error @ url: {url}')
        print(e.args)
        pass


if __name__ == '__main__':
    '''
    projekte = 0
    fachunternehmen = 11
    haendler / 
    cphContainer_cphMain_Tabs_Tab1_cProjects_upTabObjects
    '''

    #get all unique urls hersteller/haendler
    get_xpertio('https://www.xpertio.net/dreilich-edelstahlverarbeitung-gmbh_sembach/14/144146')
    # t1 = threading.Thread(target=get_xpertio, args=(10, 0),)
    # t2 = threading.Thread(target=get_xpertio, args=(11, 0),)
    # t3 = threading.Thread(target=get_xpertio, args=(14, 0),)

    # t1.start()
    # t2.start()
    # t3.start()
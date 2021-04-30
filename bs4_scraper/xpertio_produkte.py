
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
                        # uk_inhalt = [ukI.find_all('a')['title'] for soup.find_all('ul', {'class': 'circles'})
            print(complete_dataset)
    except:
        print('exception')

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
from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint


def remove_escapechars(string_value):
    '''
    remove escape chars from given field
    '''
    assert isinstance(string_value, str), 'field_value ist kein string'
    string_value = ' '.join(string_value.splitlines())
    escapes = ''.join([chr(char) for char in range(1, 32)])
    translator = str.maketrans('', '', escapes)
    return ' '.join([x for x in string_value.translate(translator).split(' ') if x])


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

def get_clean_telefon(tele):
    payload = {
        'firma_telefon': tele
    }
    return requests.post('http://192.168.100.239:9099/005phonenumbers', json=payload).json()

def get_gaertner():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://bgv-bayern.de/gaertnereien-finden/fachbetriebssuche?tx_storefinder_map%5Baction%5D=map&tx_storefinder_map%5Bcontroller%5D=Map&cHash=dba599bf7ea8ba25053b1ff547807224')
    driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div/main/div/div/div/div/form/fieldset[1]/div/div/div[3]/input').click()
    driver.implicitly_wait(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    all_ds = []
    complete_dataset = {}
    for i in soup.select('div.mapHeader'):
        if name := i.find('h3', class_='storename'):
            complete_dataset['Firma'] = remove_escapechars(name.text.strip())
        else:
            complete_dataset['Firma'] = 'xxxxx'
        if ap := i.find('div', class_='contactperson'):
            complete_dataset['Ansprechpartner'] = remove_escapechars(ap.text.strip()).replace('Inh.', 'Inhaber')
        else:
            complete_dataset['Ansprechpartner'] = 'xxxxx'
        if strasse := i.find('div', class_='street'):
            complete_dataset['StrasseUndNr'] = remove_escapechars(strasse.text.strip())
        else:
            complete_dataset['StrasseUndNr'] = 'xxxxx'
        if city := i.find('div', class_='city'):
            city = city.text.split(' ')
            complete_dataset['PLZ'] = remove_escapechars(city[0].strip())
            complete_dataset['Ort'] = remove_escapechars(' '.join(city[1:]).strip())
        else:
            complete_dataset['PLZ'] = 'xxxxx'
            complete_dataset['Ort'] = 'xxxxx'
        if phone := i.find('div', class_='phone'):
            complete_dataset['Telefon'] = get_clean_telefon(remove_escapechars(phone.text.replace('Telefon: ', '')))['firma_telefon']
        else:
            complete_dataset['Telefon'] = 'xxxxx'
        if fax := i.find('div', class_='fax'):
            complete_dataset['Fax'] = get_clean_telefon(remove_escapechars(fax.text.replace('Fax: ', '')))['firma_telefon']
        else:
            complete_dataset['Fax'] = 'xxxxx'
        if email := i.find('div', class_='email'):
            complete_dataset['Email'] = remove_escapechars(email.text.replace('Email: ', '').replace('(at)', '@'))
        else:
            complete_dataset['Email'] = 'xxxxx'

        if inet := i.find('div', class_='url'):
            r = check_website(inet.text.replace('Internet:', '').strip())
            complete_dataset['Internet'] = r['domain']
        else:
            complete_dataset['Internet'] = 'xxxxx'
        
        fach_dienst_dt = i.find_all('dt')
        fach_dienst_dd = i.find_all('dd')
        for x, y in zip(fach_dienst_dt, fach_dienst_dd):
            complete_dataset[x.text.replace(':', '').strip().replace(' ', '')] = remove_escapechars(', '.join([a for a in y.text.strip().split(', ')]))
        insert_new_dataset_into_mdb(mdb_uri="192.168.100.5",
                                datenbank='scrp_listen',
                                collection='bgv_bayern_gaertner',
                                datensatz=complete_dataset)
        complete_dataset = {}
        all_ds.append(complete_dataset)
        # pprint(complete_dataset, indent=2)

        print('==================================')
    driver.close()
    print(len(all_ds))
if __name__ == '__main__':
    get_gaertner()
from pymongo import MongoClient
import requests

def email_to_homepage(email):
    try: 
        url = 'http://192.168.100.239:9099/003mailcheck' 
        payload = dict(firma_email=email)
        return requests.post(url, json=payload).json()
    except Exception as e:
        print(f'error: {e}')

def homepage_einspielen(db_name, col_name, field_name, field_value):
    pass


if __name__ == '__main__':
    client = MongoClient('192.168.100.5:27017')
    db_name = 'scrp_listen'
    col_name = 'energie_effizienz_private'
    field_name = 'Homepage'
    # field_value = 

    collection = client[db_name][col_name]
    cursor = list(collection.find({}, {'Email': 1}))
    for i in cursor[:100]:
        field_value = email_to_homepage(i['Email'])['domain']
        print(field_value)
        # collection.update_one({'$set': {field_name: field_value}})
        
    # email_to_homepage()
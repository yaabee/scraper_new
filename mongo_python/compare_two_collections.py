from pymongo import MongoClient
import pandas as pd

def getDistinct(db_name, col_name, distinct_field, distinct_que):
    client = MongoClient('192.168.100.5:27017')
    db_5 = client[db_name][col_name]
    return db_5.distinct(distinct_field, distinct_que)
    
if __name__ == '__main__':
    distinct_que_2 = {'Telefon': {'$eq': 'xxxxx'}, 'business_card': 'Architekt / Planer'}
    distinct_que = {'firma_telefon': {'$eq': 'KA'}}
    old = getDistinct('yanghi', 'xpertio', 'firma_telefon',  distinct_que=distinct_que)
    new = getDistinct('scrp_listen', 'xpertio', 'Telefon', distinct_que=distinct_que_2)
    firma = getDistinct('scrp_listen', 'xpertio', 'Firma', distinct_que=distinct_que_2)
    firma_2 = getDistinct('yanghi', 'xpertio', 'firma_name', distinct_que=distinct_que)
    # print('old', len(old))
    # print('new', len(new))

    # old_filter = [x.replace(' ', '').replace('/', '').replace('+', '') for x in old]
    # new_filter = [y.replace(' ', '').replace('/', '').replace('+', '') for y in new]

    # print(set(old_filter + new_filter))

    

    print(len(firma))
    print(len(firma_2))

    # print(old_filter)
    # print(new_filter)

    # print(len(list(set(old_filter + new_filter))))






    # diff = [i for i in old if i not in new]
    # print('len diff', len(diff))

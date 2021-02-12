from pymongo import MongoClient

def print_data(db_name, col_name, field_name):
    client = MongoClient('192.168.100.5:27017')
    collection = client[db_name][col_name]
    cursor = collection.find({})
    cursor1 = collection.find({'WebsiteStatus.online': False, 'WebsiteStatus.mail': {'$ne': 'www.info@xxxxx'}})
    cursor2 = collection.find({'WebsiteStatus.online': True})
    for data_set in cursor:
        try:
            print(data_set[field_name])
        except KeyError:
            continue

if __name__ == '__main__':
    db_name = 'scrp_listen'
    col_name = 'heinze_zfid'
    field_name = 'WebsiteStatus'
    print_data(db_name, col_name, field_name)
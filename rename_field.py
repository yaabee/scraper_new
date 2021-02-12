from pymongo import MongoClient

def rename_field(db_name, col_name, field_name_old, field_name_new):
    client = MongoClient('192.168.100.5:27017')
    collection = client[db_name][col_name]
    cursor = collection.find({})
    for data_set in cursor:
        update = collection.update_one({'_id': data_set['_id']}, {'$rename': {field_name_old: field_name_new}})
        print(update.modified_count)

if __name__ == '__main__':
    db_name = 'scrp_listen'
    col_name = 'heinze_zfid'
    field_name_old = 'Schwerpunkte im Bereich Sanierung'
    field_name_new = 'SchwerpunkteImBereichSanierung'
    rename_field(db_name, col_name, field_name_old, field_name_new)
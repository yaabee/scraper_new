from pymongo import MongoClient
from bson import ObjectId

def split_str_inside_array_to_new_array(data_set):
    '''
    parameter:
        data_set: ["ladida, ladida2, ladida3"]
    return:
        ["ladida", "ladida2", "ladida3"]
    '''
    old_value = data_set[field_name][0]
    new_value = [x.strip() for x in old_value.split(',')]
    return new_value
    

def clean_collection(db_name, col_name, field_name):
    '''
    parameter:
        db_name: string,
        col_name: string,
        field_name: string (str[] ?)
        task: string (str[])
    funktion:
        ein einzelnes feld aendern
    '''
    client = MongoClient('192.168.100.5:27017')
    collection = client[db_name][col_name]
    cursor_as_list = collection.find({}, {field_name: 1})
    for data_set in cursor_as_list:
        try:
            new_value = split_str_inside_array_to_new_array(data_set)
            collection.update_one(
                {'_id': ObjectId(data_set['_id'])},
                {'$set': {field_name: new_value}}
            )
        except KeyError as e:
            print(e)
            #set key: ['']
            continue

if __name__ == '__main__':
    db_name = 'scrp_listen'
    col_name = 'heinze'
    field_name = 'Fachgruppe, Fachbereich, Gewerk'
    clean_collection(db_name, col_name, field_name)

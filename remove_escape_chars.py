from pymongo import MongoClient

def remove_escapechars(string_value):
    '''
    remove escape chars from given field
    '''
    assert isinstance(string_value, str), 'field_value ist kein string'
    string_value = ' '.join(string_value.splitlines())
    escapes = ''.join([chr(char) for char in range(1, 32)])
    translator = str.maketrans('', '', escapes)
    return string_value.translate(translator)

def remove_escape_chars(db_name, col_name, field_name):
    client = MongoClient('192.168.100.5:27017')
    collection = client[db_name][col_name]
    cursor = collection.find({})
    for data_set in cursor:
        new_value = remove_escapechars(data_set[field_name])
        update_ds = collection.update_one(
            {'_id': data_set['_id']},
            {'$set': {field_name: new_value}}
        )
        print(update_ds.modified_count)

if __name__ == '__main__':
    db_name = 'scrp_listen'
    col_name = 'heinze_zfid'
    field_name = 'Firma'
    remove_escape_chars(db_name, col_name, field_name)



from pymongo import MongoClient
import pprint

def remove_duplicates(db_name, col_name):
    '''
    parameter:
        db_name, col_name
    description:
        remove duplicates
    funktion:
        build cache with dataset
        if zfid in cache:
            remove from collection
    return:
        void
    '''
    client = MongoClient('192.168.100.5:27017')
    collection = client[db_name][col_name]
    cursor = collection.find({})
    cache = {}
    #no cache_key_name
    for i in cursor:
        to_delete = i.pop('_id')
        pprint.pprint(i, indent=2)
        print('todelete', to_delete)
        i_values = i.values()
        cache_key_name = hash(i_values)
        if cache_key_name in cache:
            try:
                delete_one = collection.delete_one({'_id': to_delete})
                print(delete_one.deleted_count)
            except Exception as e:
                print('error with del dataset:', i)
                print(e.args)
        else:
            cache[cache_key_name] = i
    # print(len(cache.values()))


    # cache_values = cache.values()
    # for k in cache_values:
    #     try:
    #         insert_one = collection.insert_one(k)
    #         print(insert_one.inserted_id)
    #     except Exception as e:
    #         print('error with ins dataset:', k)
    #         print(e.args)


if __name__ == '__main__':
    db_name = 'scrp_listen'
    col_name = 'heinze'
    remove_duplicates(db_name, col_name)
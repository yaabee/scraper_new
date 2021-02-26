from pymongo import MongoClient

def remove_duplicates(db_name, col_name, cache_key_name):
    '''
    parameter:
        db_name, col_name
        cache_key_name: required in collection!
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
    for i in cursor:
        if i[cache_key_name] in cache:
            try:
                delete_one = collection.delete_one({'_id': i['_id']})
                print(delete_one.deleted_count)
            except Exception as e:
                print('error with del dataset:', i)
                print(e.args)
        else:
            cache[i[cache_key_name]] = i
    print(len(cache.keys()))


if __name__ == '__main__':
    db_name = 'scrp_listen'
    col_name = 'energie_effizienz_full'
    use_as_cache_key = 'ZFID'
    remove_duplicates(db_name, col_name, use_as_cache_key)
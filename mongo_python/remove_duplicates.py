from pymongo import MongoClient
import ssl
import pprint

client_239 = MongoClient('192.168.100.239:27017',
                         username='mongoroot',
                         password='9gCaPFhotG2CNEoBRdgA',
                         authSource='admin',
                         authMechanism='SCRAM-SHA-256',
                         ssl=True,
                         ssl_cert_reqs=ssl.CERT_NONE)
client_5 = MongoClient('192.168.100.5:27017')

staticdata_access = client_239['staticdata']['AllgAllgemeineVorlagen_Branchenliste']
staticdata_dis = client_239['staticdata']['automatischeBranche']
original_zf = client_239['ZentralerFirmenstamm']['ZentralerFirmenstamm2']
original_new = client_239['ZentralerFirmenstamm']['ZentralerFirmenstamm_new2']


def remove_duplicates(db_name, col_name, cache_key_name):
    '''
    description:
        takes a field and deletes all 
        occurences except for 1
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
    collection = client_5[db_name][col_name]
    cursor = collection.find({'ZFID': {'$exists': True}})
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


def agg_remove(pipeline, db, col, target_db, target_col, which_client=5, delete=False):
    client = client_5
    if which_client == 239:
        client = client_239
    """
    """
    agg = list(client[db][col].aggregate(pipeline))
    for i in agg:
        pprint.pprint(i['Telefon'])
        print('ZFID', i['ZFID'])
        og = original_zf.find_one({'ZFID': i['ZFID']})
        if og:
            try:
                if og['Telefon'] != 'xxxxx':
                    insert = original_zf.insert_one(og)
                    print(
                        f'inserted id {insert.inserted_id}, zfid {i["ZFID"]}')
                    break
            except Exception:
                print('was there', i['ZFID'])

    print(len(agg))


if __name__ == '__main__':
    # cache part
    # db_name = 'scrp_listen'
    # col_name = 'heinze_zfid'
    # use_as_cache_key = 'Firma'
    # remove_duplicates(db_name, col_name, use_as_cache_key)

    # agg part
    pipeline = [
        {'$match': {
            'Telefon': {'$ne': 'xxxxx'}
        }},
        {
            '$group': {
                '_id': {
                    'Telefon': '$Telefon',
                },
                'uniqueIds': {
                    '$addToSet': '$_id'
                },
                'count': {'$sum': 1},
            }},
        {
            '$match': {
                'count': {'$gt': 1}
            }
        },
        {'$limit': 100}
    ]

    pipeline_xxxxx = [
        {'$match': {
            'Telefon': 'xxxxx'
        }},
        {'$group': {
            '_id': {'Telefon': '$Telefon'},
            'uniqueIds': {'$addToSet': '$_id'},
            'uniqueZfid': {'$addToSet': '$ZFID'}
        }}
    ]

    pipeline_anzahl = [
        {'$match': {
            'Anzahl Mitarbeiter': {'$ne': []},
            # 'Telefon': {'$eq': 'xxxxx'}
        }},
        {
            '$project': {
                '_id': 1,
                # 'Anzahl': '$Anzahl Mitarbeiter',
                'Telefon': '$Telefon',
                'ZFID': '$ZFID',
            }
        },
        # {
        #     '$limit': 1000
        # }
    ]

    # voraussetzung ist es gibt schon zfid
    db = 'scrp_listen'
    col = 'heinze_zfid_back'
    target_db = 'ZentralerFirmenstamm'
    target_col = 'ZentralerFirmenstamm'
    agg_remove(pipeline_anzahl, db, col, target_db, target_col, delete=False)

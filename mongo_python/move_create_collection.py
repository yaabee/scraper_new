import ssl
from pymongo import MongoClient

client_239 = MongoClient('192.168.100.239:27017',
                         username='mongoroot',
                         password='9gCaPFhotG2CNEoBRdgA',
                         authSource='admin',
                         authMechanism='SCRAM-SHA-256',
                         ssl=True,
                         ssl_cert_reqs=ssl.CERT_NONE)


def main(db_name, col_name, target_db, target_col, query, lim):
    if lim:
        cursor = client_239[db_name][col_name].find(query).limit(lim)
    else:
        cursor = client_239[db_name][col_name].find(query)

    if cursor:
        for i in cursor:
            insert = client_239[target_db][target_col].insert_one(i)
            print(insert.inserted_id)
    print('werden')


if __name__ == '__main__':
    db_name = 'odin'
    col_name = 'ZOObjekte'
    target_db = 'odin'
    target_col = 'fake_objekte'
    query = {}
    lim = 20

    main(db_name, col_name, target_db, target_col, query, lim)

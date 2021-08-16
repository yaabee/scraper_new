
from pymongo import MongoClient
import ssl


client_239 = MongoClient('192.168.100.239:27017',
                         username='mongoroot',
                         password='9gCaPFhotG2CNEoBRdgA',
                         authSource='admin',
                         authMechanism='SCRAM-SHA-256',
                         ssl=True,
                         ssl_cert_reqs=ssl.CERT_NONE)
client_5 = MongoClient('192.168.100.5:27017')


def main():
    col_1 = list(client_5['GoogleApi']
                 ['google_Architekt'].find({}))

    cache = []
    place_id = client_5['GoogleApi']['architekt'].distinct(
        'place_id')
    print('place id', place_id)
    for i in [col_1]:
        for x in i:
            if x['place_id'] not in cache and x['place_id'] not in place_id:
                insert = client_5['GoogleApi']['architekt'].insert_one(
                    x)
                cache.append(x['place_id'])
                print(insert.inserted_id)
            else:
                print('not')


if __name__ == '__main__':
    main()

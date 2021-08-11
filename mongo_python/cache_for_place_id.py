from pymongo import MongoClient
import ssl

client_5 = MongoClient('192.168.100.5:27017')
client_239 = MongoClient('192.168.100.239:27017',
                         username='mongoroot',
                         password='9gCaPFhotG2CNEoBRdgA',
                         authSource='admin',
                         authMechanism='SCRAM-SHA-256',
                         ssl=True,
                         ssl_cert_reqs=ssl.CERT_NONE)


def main():
    db = client_5['GoogleApi']
    cache = []
    for col in db.list_collection_names():
        cursor = db[col].distinct('place_id')
        cache += list(set(cursor))


if __name__ == '__main__':
    main()

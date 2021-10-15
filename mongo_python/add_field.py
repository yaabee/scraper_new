
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


def main(db, col, fieldname, value):
    client_239[db][col].update_many({}, {'$set': {fieldname: value}})


if __name__ == '__main__':
    db = 'odin'
    col = 'ZOObjekte_yanghi'
    fieldname = 'PotenzielleDubletten'
    value = []

    main(db, col, fieldname, value)

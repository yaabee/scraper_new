
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

#'Anzahl Mitarbeiter'

def main(db, col, fieldname, value, which_client):
    client = client_5
    if which_client == 239:
        client = client_239
    client[db][col].update_many({fieldname: {'$exists': False}}, {
                                '$set': {fieldname: value}})


if __name__ == '__main__':
    db = 'odin'
    col = 'Cronjobs'
    fieldname = 'BeteiligteFirmen'
    value = 'nur'
    which_client = 239

    main(db, col, fieldname, value, which_client)

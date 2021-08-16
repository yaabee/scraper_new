
from pymongo import MongoClient
import ssl
import re

client_5 = MongoClient('192.168.100.5:27017')
client_239 = MongoClient('192.168.100.239:27017',
                         username='mongoroot',
                         password='9gCaPFhotG2CNEoBRdgA',
                         authSource='admin',
                         authMechanism='SCRAM-SHA-256',
                         ssl=True,
                         ssl_cert_reqs=ssl.CERT_NONE)


def main(plz, db_name, col_name, name_contains):
    col = client_5[db_name][col_name]
    print(f'{plz}: ', len(col.distinct(
        'name', {'PLZ': {'$regex': re.compile(plz)}, 'name': {'$regex': re.compile(name_contains)}})))


if __name__ == '__main__':
    db_name = 'GoogleApi'
    col_name = "google_Technischer Berater_Technischer Berater"
    name_contains = 'Techni'

    # col_name = 'google_Ingenieur_Ingenieur'
    # name_contains = 'Ing.'
    main('^81', db_name, col_name, name_contains)
    main('^82', db_name, col_name, name_contains)
    main('^83', db_name, col_name, name_contains)
    main('^84', db_name, col_name, name_contains)
    main('^85', db_name, col_name, name_contains)
    main('^86', db_name, col_name, name_contains)
    main('^87', db_name, col_name, name_contains)
    main('^91', db_name, col_name, name_contains)
    main('^92', db_name, col_name, name_contains)
    main('^93', db_name, col_name, name_contains)
    main('^94', db_name, col_name, name_contains)
    main('^95', db_name, col_name, name_contains)
    main('^96', db_name, col_name, name_contains)
    main('^97', db_name, col_name, name_contains)

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


def main(db_from, col_from, db_to, col_to):
    a = client_5[db_from][col_from]
    b = client_5[db_to][col_to]

    cursor_a = list(a.find({'Branche': {'$exists': False}}))

    for i in cursor_a:
        a.update_one({'ZFID': i['ZFID']}, {'$set': {'Branche': []}})


if __name__ == '__main__':
    db_from = 'scrp_listen'
    db_to = 'scrp_listen'
    col_from = 'hwk_neu'
    col_to = 'hwk_neu_neu'
    main(db_from=db_from, db_to=db_to, col_from=col_from, col_to=col_to)

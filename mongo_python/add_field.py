from pymongo import MongoClient
import ssl

from mongo.mongo_connections import client_8

# client_239 = MongoClient('192.168.100.239:27017',
#                          username='mongoroot',
#                          password='9gCaPFhotG2CNEoBRdgA',
#                          authSource='admin',
#                          authMechanism='SCRAM-SHA-256',
#                          ssl=True,
#                          ssl_cert_reqs=ssl.CERT_NONE)
# client_5 = MongoClient('192.168.100.5:27017')

#'Anzahl Mitarbeiter'


# if __name__ == '__main__':
#     db = 'odin'
#     col = 'Cronjobs'
#     fieldname = 'BeteiligteFirmen'
#     value = 'nur'
#     which_client = 239

#     all = (x['zfid'] for x in client_5['scrp_listen']['ranking300'].find({}))

#     all_exportierbar = (x for x in client_8['Zentral'])


#     main(db, col, fieldname, value, which_client)

from pymongo import MongoClient
import ssl
import pprint

client_5 = MongoClient('192.168.100.5:27017')
client_239 = MongoClient('192.168.100.239:27017',
                         username='mongoroot',
                         password='9gCaPFhotG2CNEoBRdgA',
                         authSource='admin',
                         authMechanism='SCRAM-SHA-256',
                         ssl=True,
                         ssl_cert_reqs=ssl.CERT_NONE)


def main_5():
    pass


def main_239(db, col, pipeline):
    odin_yb = client_239[db][col]
    cursor = list(odin_yb.aggregate(pipeline))
    for i in cursor:
        # pprint.pprint(i, indent=2)
        tmp = i['potDubs']
        tmp.sort()
        odin_yb.update_one({'ZOID': str(i['_id'])}, {
                           '$addToSet': {'DubletteZu': tmp[0]}})
        odin_yb.update_one({'ZOID': str(i['_id'])}, {
                           '$set': {'PruefungNotwendig': True}})


if __name__ == '__main__':
    pipeline = [
        {'$project': {
            '_id': 1,
            'count': {'$size': '$PotenzielleDubletten'},
            'potDubs': '$PotenzielleDubletten'

        }}, {'$match': {
            'count': {
                '$gt': 0
            }
        }
        }
    ]
    db = 'odin'
    col = 'ZOObjekte_yanghi'
    main_239(db, col, pipeline)

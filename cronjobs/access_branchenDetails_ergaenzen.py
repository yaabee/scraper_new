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


def main():
    allgemeineBranchenliste = list(
        client_239['staticdata']['AllgemeineVorlagen_Branchenliste'].find({}))

    cache = {v['BranchenID']: v['Branche'] for v in allgemeineBranchenliste}

    col = client_239['ZentralerFirmenstamm']['ZentralerFirmenstamm']

    pipelineAccess = [
        {"$project": {
            "_id": 1,
            "Access": "$Meta.BranchenDetails.Access",
            "count": {"$size": "$Meta.BranchenDetails.Access"
                      }
        }},
        {"$match": {
            "count": {
                "$gt": 0
            }
        }},
    ]

    cursor = list(col.aggregate(pipelineAccess))
    for i in cursor:
        # um den pointer zu aendern...
        origin = [{**x} for x in i['Access']].copy()
        tmp = []
        try:
            for k in i['Access']:
                keys = cache.keys()
                if not k['Name'] and k['WZCode'] in keys:
                    k['Name'] = cache[k['WZCode']]
                    if k not in tmp:
                        tmp.append(k)
                elif k not in tmp:
                    tmp.append(k)
            if tmp:
                # print(str(i['_id']))
                # pprint.pprint(tmp)
                # print('------------------------------------')
                # pprint.pprint(origin)
                # print('====================================')
                col.update_one({'ZFID': str(i['_id'])}, {
                    '$set': {'Meta.BranchenDetails.Access': tmp}})
        except KeyError:
            print(i['_id'])
            continue


if __name__ == '__main__':
    main()

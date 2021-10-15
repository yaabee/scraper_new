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
    odin_yb = client_239['odin']['ZOObjekte_yanghi']
    zob = client_239['ZentralerFirmenstamm']['ZentralerFirmenstamm']

    pipelineAccess = [
        {"$project": {
            "_id": 1,
            "Beteiligte": "$Beteiligte",
            "count": {"$size": "$Beteiligte"
                      }
        }},
        {"$match": {
            "count": {
                "$eq": 15
            }
        }}, {'$limit': 1}
    ]

    cursor = list(odin_yb.aggregate(pipelineAccess))
    for agg in cursor:
        # um den pointer zu aendern...
        origin = [{**x} for x in agg['Beteiligte']].copy()
        tmp = []
        for beteiligter in agg['Beteiligte']:
            firmenadresse = zob.find_one({'ZFID': beteiligter['ZAID']})
            if firmenadresse['DubletteZuId'] != firmenadresse['ZFID']:
                # tmp.append({'Anlagedatum': ds['']})
                dub = zob.find_one({'ZFID': firmenadresse['DubletteZuId']})
                beteiligter_neu = {
                    'Anlagedatum': beteiligter['Anlagedatum'],
                    'Herkunft': beteiligter['Herkunft'],
                    'Rolle': beteiligter['Rolle'],
                    'Ursprungsrolle': beteiligter['Ursprungsrolle'],
                    'ZAID': dub['ZFID']
                }
                if beteiligter_neu not in tmp:
                    tmp.append(beteiligter_neu)
            elif beteiligter not in tmp:
                tmp.append(beteiligter)

        zaid_vorhanden = []
        for bet in tmp:
            if bet['ZAID'] not in zaid_vorhanden:
                if bet['Rolle'] != 'Unbekannt':
                    zaid_vorhanden.append(bet['ZAID'])
        # print('zaid_vorhanden', zaid_vorhanden)
        tmp_final = []
        for bet in tmp:
            if bet['Rolle'] == 'Unbekannt':
                if bet['ZAID'] not in zaid_vorhanden:
                    tmp_final.append(bet)
            else:
                tmp_final.append(bet)
        pprint.pprint(tmp_final, indent=2)
        print('laenge neu', len(tmp_final))
        print('---------------------------------------')
        pprint.pprint(origin, indent=2)
        print('laenge alt', len(origin))
        print('=======================================')
        update = odin_yb.update_one({'ZOID': str(agg['_id'])}, {'$set': {
            'Beteiligte': tmp_final
        }})
        print(agg['_id'])
        print(update.acknowledged)


if __name__ == '__main__':
    main()

from pymongo import MongoClient
import ssl
import pprint

client_239 = MongoClient('192.168.100.239:27017',
                         username='mongoroot',
                         password='9gCaPFhotG2CNEoBRdgA',
                         authSource='admin',
                         authMechanism='SCRAM-SHA-256',
                         ssl=True,
                         ssl_cert_reqs=ssl.CERT_NONE)

odin_yb = client_239['odin']['ZOObjekte_yanghi']


def setDubs():
    # gleiche strasse und plz
    cursor = list(
        odin_yb.aggregate([
            {'$match': {
                'IstDublette': False
            }},
            {
                '$group': {
                    '_id': {
                        'PLZ': '$PLZ',
                        'Strasse': '$Strasse',
                    },
                    'uniqueIds': {
                        '$addToSet': '$_id'
                    },
                    'count': {
                        '$sum': 1
                    }
                }
            }, {

                '$match': {
                    'count': {
                        '$gt': 0
                    }
                },
            }, {
                '$sort': {
                    'count': 1
                }
            }]))
    dubs = []
    print(len(cursor))
    for i in cursor:
        if i['_id']['PLZ'] and i['_id']['Strasse']:
            for j in i['uniqueIds']:
                for k in i['uniqueIds']:
                    if j != k:
                        tmp = [str(j), str(k)]
                        tmp.sort()
                        if tmp not in dubs:
                            dubs.append(tmp)
                            up1 = odin_yb.update_one({'ZOID': tmp[1]}, {'$set': {
                                'PruefungNotwendig': True,
                            }})
                            odin_yb.update_one({'ZOID': tmp[1]}, {'$addToSet': {
                                'PotenzielleDubletten': tmp[0]
                            }})
    # for x, y in dubs:
    #     odin_yb.update_one({'ZOID': y}, {'$set': {
    #         'PruefungNotwending': True,
    #     }})
    #     odin_yb.update_one({'ZOID': y}, {'$addToSet': {
    #         'PotenzielleDubletten': x
    #     }})


if __name__ == '__main__':
    setDubs()


"""
case:
  zoo_lam {
    DubZu: [x,y]
    Pruefen: True
    IstDub: False
  }

    zoo_x {
      DubZu: [a, b]
      Pruefen: True
      IstDub: False
    }
      zoo_a: {
        DubZu: [l]
        Pruefen: True
        IstDub: True
      }
        zoo_l: {
          DubZu: []
          Pruefen: False
          IstDub: False
        }

      zoo_b {
        DubZu: [y]
        Pruefen: False
        IstDub: True
      }
        zoo_y: {
          DubZu: []
        }

    zoo_y {
      DubZu: []
      Pruefen: False
      IstDub: False
    }
"""

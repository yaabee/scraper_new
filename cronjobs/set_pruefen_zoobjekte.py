from pymongo import MongoClient
import ssl

client_239 = MongoClient('192.168.100.239:27017',
                         username='mongoroot',
                         password='9gCaPFhotG2CNEoBRdgA',
                         authSource='admin',
                         authMechanism='SCRAM-SHA-256',
                         ssl=True,
                         ssl_cert_reqs=ssl.CERT_NONE)

odin_yb = client_239['odin']['ZOObjekte_yanghi']
# alle die gleiche plz und strasse besitzen
cursor = list(
    odin_yb.aggregate([{
        '$group': {
            '_id': {
                'PLZ': '$PLZ',
                'Strasse': '$Strasse'
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
                '$gt': 1
            }
        },
    }, {
        '$sort': {
            'count': 1
        }
    }]))
dubs = []
payload = []
for i in cursor[:100]:
    if i['_id']['PLZ'] and i['_id']['Strasse']:
        for j in i['uniqueIds']:
            for k in i['uniqueIds']:
                if j != k:
                    tmp = [j, k]
                    tmp.sort()
                    if tmp not in dubs:
                        dubs.append(tmp)
for x, y in dubs:
    odin_yb.update_one({'ZOID': y}, {'$set': {
        'PruefungNotwending': True,
        'IstDublette': True,
        'DubletteZu': {'$addToset': x}
    }})

"""
if IstDublette => len(DubletteZu) = 1
check age by sort
"""
""" 
#ds y
#dub zu x
if found:
  set Pruefen True
  set DubletteZu [x]
"""

"""
find_furthest_dub((a, b)):
  if b dub zu c and IstDublette:
    find_furthest_dub((b, c))
  else:
    return 'furthest dub': a
"""

""" 
# y => x dub
#View (x, y)
  if (x, y) dub:
    set y Pruefen False
    fur = find_furthest_dub(x, y)
    set y IstDublette True
    set y DubletteZu = fur
  else:
"""

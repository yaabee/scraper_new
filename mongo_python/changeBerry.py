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

planerhkls = dict(
    Herkunft='Google',
    Name='planer_hkls',
    WZCode=227132102
)
planerhochbau = dict(
    Herkunft='Google',
    Name='planer_hochbau',
    WZCode=227111200
)
ausf_hkls = dict(
    Herkunft='Google',
    Name='ausf_hkls',
    WZCode=154322100
)
solaranlagen_anbieter = dict(
    Herkunft='Google',
    Name='solaranlagenanbieter',
    WZCode=14
)
solaranlagen_installateur = dict(
    Herkunft='Google',
    Name='solaranlageninstallationsservice',
    WZCode=13
)
fachplaner_elektro = dict(
    Herkunft='Google',
    Name='fachplaner_elektro',
    WZCode=227132103
)
ausf_gala = dict(
    Herkunft='Google',
    Name='ausf_gala',
    WZCode=154411100
)
ingenieur = dict(
    Herkunft='Google',
    Name='ingenieur',
    WZCode=2
)
ausf_tiefbau = dict(
    Herkunft='Google',
    Name='ausf_tiefbau',
    WZCode=154200000
)
misch_bautraeger = dict(
    Herkunft='Google',
    Name='misch_bautraeger',
    WZCode=154110000,
)
generalübernehmer = dict(
    Herkunft='Google',
    Name='misch_gu/gue',
    WZCode=216841500,
)
seb = dict(
    Herkunft='Google',
    Name='seb',
    WZCode=88,
)
fensterbauer = dict(
    Herkunft='Google',
    Name='fensterbauer',
    WZCode=1988,
)

energieberater = dict(
    Herkunft='Google',
    Name='energieberater/1',
    WZCode=227491104,
)

technischer_berater = dict(
    Herkunft='Google',
    Name='technischer_berater',
    WZCode='',
)

hallenbauer_hwk = dict(
    Herkunft='hwk',
    Name='hallen_bauer',
    WZCode='',
)
hallenbauer_ta = dict(
    Herkunft='ta',
    Name='hallen_bauer',
    WZCode='',
)

hallen_bauer = dict(
    Herkunft='Google',
    Name='hallen_bauer',
    WZCode='',
)

# gebaeudetechnik
hkls = dict(
    Herkunft='Google',
    Name='hkls',
    WZCode='1',
)

col = client_239['odin']['ZOObjekte']
col_zob = client_239['ZentralerFirmenstamm']['ZentralerFirmenstamm']

allgemeineBranchenliste = list(
    client_239['staticdata']['AllgemeineVorlagen_Branchenliste'].find({}))
cache = {v['BranchenID']: v['Branche'] for v in allgemeineBranchenliste}

pipeline = [
    {'$match': {
        'PruefungNotwendig': True
    }},
    # {'$limit': 10}
]

cursor = list(client_239['odin']['ZOObjekte_yanghi'].aggregate(pipeline))
for i in cursor:
    client_239['odin']['ZOObjekte_yanghi'].update_one({'ZOID': i['ZOID']}, {
        '$set': {
            'PruefungNotwendig': False
        }
    })

# ds = zf.find_one({'ZFID': i['ZFID']})
# zf.update_one(
#     {'ZOID': i['ZOID']},
#     {'$set': {'IstDublette': True, 'DubletteZu': []}}
# )

# zf.update_one(
#     {'ZFID': i['ZFID']},
#     {'$addToSet': {'Meta.BranchenDetails.Extern': technischer_berater}}
# )

# zf.update_one(
#   {'ZFID': i['ZFID']},
#   {'$set': {'Land': False, 'Meta.Inaktiv.Grund': ''}}
# )

# delete field
# {"$unset": {"Meta.BranchenDetails.Extern": ""}}

# remove from array
# zf.update_one(
#     {'ZFID': i['ZFID']},
#     {'$pull': {'Meta.BranchenDetails.Extern': hallenbauer_ta}}
# )

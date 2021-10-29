from pymongo import MongoClient
import ssl

client239 = MongoClient('192.168.100.239:27017',
                        username='mongoroot',
                        password='9gCaPFhotG2CNEoBRdgA',
                        authSource='admin',
                        authMechanism='SCRAM-SHA-256',
                        ssl=True,
                        ssl_cert_reqs=ssl.CERT_NONE)

client_solaris = MongoClient("mongodb://solaris:!+m4cbDmEqPn7RW@192.168.100.8:27018/solaris",
                             serverSelectionTimeoutMS=1000)

clientMongoAccess = MongoClient("192.168.100.239:27099")

"""Mongo Instanz 192.168.100.239:27017 ----- Alle verfügbaren MongoDB Collection Anbindungen"""
COLLECTION_PROJEKTE = client239["staticdata"]["projekte"]
COLLECTION_ZENTRALER_FIRMENSTAMM = client239["ZentralerFirmenstamm"]["ZentralerFirmenstamm"]
COLLECTION_ANSPRECHPARTNER = client239["ZentralerFirmenstamm"]["Ansprechpartner"]
COLLECTION_BETEILIGTE_FIRMEN = client239["odin"]["beteiligteFirmen"]
ZOOBJEKTE_YANGHI = client239["odin"]["ZOObjekte_yanghi"]
ZOOBJEKTE = client239['odin']['ZOObjekte']
COLLECTION_ZF_LOGS = client239["logs"]["zf"]

"""Mongo Instanz 192.168.100.239:27099 ----- Alle verfügbaren MongoDB Collection Anbindungen"""
COLLECTION_ANRUFLISTE_RAW_CLEAN = clientMongoAccess["Anrufliste"]["AnruflisteRawClean"]
COLLECTION_WLB_NEWSLETTER = clientMongoAccess["Cleverreach"]["WLBNewsletter"]

"""Mongo Instanz 192.168.100.230/solaris Solaris"""
COLLECTION_SOLARIS = client_solaris["solaris"]["objects"]

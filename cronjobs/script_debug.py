from pymongo import MongoClient
import ssl
import pprint

client_zo_reader = MongoClient(
    "mongodb://zo_objekt_reader:s5FLwMszMHSMck4KL6Pm@192.168.100.8:27017/zo_objekt",
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE,
)

client_solaris = MongoClient(
    "mongodb://mongoroot:9gCaPFhotG2CNEoBRdgA@192.168.100.8:27018", serverSelectionTimeoutMS=1000
)

client_239 = MongoClient(
    "mongodb://mongoroot:9gCaPFhotG2CNEoBRdgA@192.168.100.239:27017",
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE,
)

client_5 = MongoClient("mongodb://192.168.100.5:27017")

""" prob: es werden zu wenige objekte eingelesen """


#die cronjob listen ziehen
cronjobs = list(client_239["odin"]["Cronjobs"].find({'Einmalig': False}))

for i in cronjobs:
  print(i[''])
# pprint.pprint(cronjobs, indent=2)


""" anzahl client_239 und zo_reader lesen """
""" stats is wrong? """

""" update baubeginn von nicht gescheit... """


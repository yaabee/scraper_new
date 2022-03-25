from pymongo import MongoClient
import ssl
import requests
import datetime

client = MongoClient(
    "192.168.100.239:27017",
    username="mongoroot",
    password="9gCaPFhotG2CNEoBRdgA",
    authSource="admin",
    authMechanism="SCRAM-SHA-256",
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE,
)

client_zo_reader = MongoClient(
    "192.168.100.8:27017",
    username="zo_objekt_reader",
    password="s5FLwMszMHSMck4KL6Pm",
    authSource="zo_objekt",
    authMechanism="SCRAM-SHA-256",
    tls=True,
    tlsCAFile="/etc/ssl/certs/teleaktiv_rootCA.pem",
)

zoo_col = client_zo_reader["zo_objekt"]["zo_objekt"]
cronjobs = client["odin"]["Cronjobs"]

# 1 = montag ... 7 = sonntag
weekday = datetime.datetime.now().isoweekday()
# yyyy-mm-ddT...
month = datetime.datetime.now().isoformat()

transformer = {
    "1": "Montags",
    "2": "Dienstags",
    "3": "Mittwochs",
    "4": "Donnerstags",
    "5": "Freitags",
}

gesamt = []
wochencj = []
monatcj = []

if str(weekday) in transformer.keys():
    wochencj = list(
        cronjobs.find({"Einmalig": False, "Cronjob": transformer[str(weekday)]})
    )

# print('transformer', transformer[str(weekday)])
# print('now', month)
# print('now', month[8:10])
if month[8:10] == "01":
    monatcj = list(cronjobs.find({"Einmalig": False, "Cronjob": "Monatsanfang"}))

if wochencj:
    gesamt += wochencj
if monatcj:
    gesamt += monatcj

if gesamt:
    for i in gesamt:
        del i["_id"]
        res = requests.post("http://192.168.100.239:5555/odinListe/", json=i)
        try:
            original_zoid = i["ZOIDS"]
            old_zoids = [z for z in original_zoid.keys()]
            new_zoids = [y["ZOID"] for y in res.json()]
            zoids_for_update = [x for x in new_zoids if x not in old_zoids]
            datum = datetime.datetime.now().isoformat()
            # die liste nochmal durchgehen und nur beteiligte exists beruecksichtigen
            final = []
            for b in new_zoids:
                ds = zoo_col.find_one({"ZOID": b, "Beteiligte": {"$exists": True}})
                if ds and ds["Beteiligte"]:
                    final.append(ds["ZOID"])
            for a in final:
                original_zoid[a] = {
                    "ErstellungsDatum": datum,
                    "Eingespielt": False,
                    "EinspielDatum": "",
                    "Status": "",
                }
            # update = cronjobs.update_one(
            #     {"schnellfilter_name": i["schnellfilter_name"]},
            #     {"$set": {"ZOIDS": original_zoid, "AnzahlNeu": len(zoids_for_update)}},
            # )
            print('original_zoid', original_zoid)
            print('len original_zoid', len(original_zoid))
            print('===================================')
            print('zoid for updates', zoids_for_update)
            print('len zoid for updates', len(zoids_for_update))
            print('===================================')
            print('new_zoids', new_zoids)
            print('len new_zoids', len(new_zoids))
            print('===================================')
            print('final', final)
            print('len final', len(final))
        except Exception as e:
            print(e.args)
            print("ex")

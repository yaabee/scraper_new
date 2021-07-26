from pymongo import MongoClient
import ssl
import datetime
from dateutil.relativedelta import relativedelta

client_239 = MongoClient(
    "192.168.100.239:27017",
    username="mongoroot",
    password="9gCaPFhotG2CNEoBRdgA",
    authSource="admin",
    authMechanism="SCRAM-SHA-256",
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE,
)


def main():
    cronjobs = client_239["odin"]["Cronjobs"]
    cursor = list(cronjobs.find({"Einmalig": False}))
    date = datetime.datetime.now()
    for i in cursor:
        dateSixMonthAgo = date - relativedelta(months=6)
        dateSixMonthFut = date + relativedelta(months=i["AnzahlMonate"])
        dateSixMonthAgo = dateSixMonthAgo.isoformat()
        dateSixMonthFut = dateSixMonthFut.isoformat()
        if i["Baubeginn"]["Von"] and not i["Baubeginn"]["Bis"]:
            cronjobs.update_one(
                {"schnellfilter_name": i["schnellfilter_name"]},
                {"$set": {"Baubeginn.Von": dateSixMonthFut}},
            )
        elif not i["Baubeginn"]["Von"] and not i["Baubeginn"]["Bis"]:
            cronjobs.update_one(
                {"schnellfilter_name": i["schnellfilter_name"]},
                {"$set": {"angelegt_ab": dateSixMonthAgo}},
            )


if __name__ == "__main__":
    main()

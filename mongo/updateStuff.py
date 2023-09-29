from mongo_connections import client_8


cursor = client_8["ZentralerFirmenstamm"]["ZentralerFirmenstamm"].find({"Telefon": {"$type": "array"}})
for i in list(cursor):
    print("zfid", i["ZFID"])
    update = {
        "Telefon": i["Telefon"][0],
        "TelefonRaw": i["TelefonRaw"][0],
        "Fax": i["Fax"][0],
        "FaxRaw": i["FaxRaw"][0],
    }

    mod = client_8["ZentralerFirmenstamm"]["ZentralerFirmenstamm"].update_one({"ZFID": i["ZFID"]}, {"$set": update})
    print(mod.acknowledged)

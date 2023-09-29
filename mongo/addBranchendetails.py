from mongo_connections import client_5, client_8


def rmBranchenDetailsExtern(zfids, rmBranchendetail):
    remove = client_8["ZentralerFirmenstamm"]["ZentralerFirmenstamm"].update_many(
        {"ZFID": {"$in": zfids}},
        {"$pull": {"Meta.BranchenDetails.Extern": rmBranchendetail}},
    )
    print(remove.modified_count)


def addBranchenDetailsExtern(zfids, addBranchendetail):
    for zfid in zfids:
        insert = client_8["ZentralerFirmenstamm"]["ZentralerFirmenstamm"].update_one(
            {"ZFID": zfid},
            {"$addToSet": {"Meta.BranchenDetails.Extern": addBranchendetail}},
        )
        print(insert.modified_count)
        print(zfid)
        print(addBranchendetail)


def getZFIDS():
    cursor = client_5["GoogleApi"]["google_Intersolar"].find(
        {"ZFID": {"$exists": True}}
    )
    return [x["ZFID"] for x in list(cursor)]


if __name__ == "__main__":
    zfids = getZFIDS()
    addBranchendetail = dict(
        Name="solaranlageninstallationsservice", Herkunft="intersolar", WZCode=13
    )
    addBranchenDetailsExtern(zfids, addBranchendetail)

from module.mongo_connections import ZF_8, client_5
import requests


def main(cursor):
    for i in cursor:
        payload = {
            **i,
            "options": {
                "ensureWrite": False,
                "forceInsert": False,
                "returnDocument": False,
            },
            "Land": "Schweiz",
        }
        # url = "http://192.168.100.239:9099/zf_adresse_neuanlageNachAccess"
        # r = requests.post(url, json=payload).json()

        # dubletteZuId = ZF_8.find_one({"ZFID": r["result"]["id"]}, {"DubletteZuId"})
        # update = client_8["ZentralerFirmenstamm"]["ZentralerFirmenstamm"].update_one(
        #     {"ZFID": dubletteZuId["DubletteZuId"]},
        #     {
        #         "$pull": {
        #             "Meta.BranchenDetails.Extern": {
        #                 "Name": "ausf_dachdecker/2",
        #                 "Herkunft": "Google",
        #                 "WZCode": 154391101,
        #             },
        #         }
        #     },
        # )
        # if 'Branche' in i:
        #   update = ZF_8.update_one(
        #       {"ZFID": dubletteZuId["DubletteZuId"]},
        #       {
        #           "$addToSet": {
        #               "Meta.BranchenDetails.Extern": {
        #                   "Name": "Landschaftsarchitekt",
        #                   "Herkunft": "lithonplus",
        #                   "WZCode": 11111111111,
        #               },
        #               "Meta.Branchen": 154322100,
        #           }
        #       },
        #   )

        # print("update", r, update.modified_count)
        # print("dubletteZuId", dubletteZuId)


def getCursor5(db, col):
    return list(client_5[db][col].find({}))


if __name__ == "__main__":
    cursor = getCursor5("scrp_listen", "lithonplus")
    main(cursor)

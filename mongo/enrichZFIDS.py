from typing import Any
from module.mongo_connections import client_8, client_5

zfids = (
    x["zfid"]
    for x in client_5["scrp_listen"]["ranking300"].find(
        {"zfid": {"$ne": ""}}, {"zfid": 1}
    )
)


query = {"ZFID": {"$in": list(zfids)}}
project = {"Meta.Exportierbar": 1, "ZFID": 1, "_id": 0}

exportierbars = (
    x
    for x in client_8["ZentralerFirmenstamm"]["ZentralerFirmenstamm"].find(
        query, project
    )
)


for i in exportierbars:
    client_5["scrp_listen"]["ranking300"].update_many(
        {"zfid": i["ZFID"]}, {"$set": {"Exportierbar": i["Meta"]["Exportierbar"]}}
    )


if __name__ == "__main__":
    client_5["scrp_listen"]["ranking300"].update_many(
        {"Exportierbar": {"$exists": False}}, {"$set": {"Exportierbar": True}}
    )

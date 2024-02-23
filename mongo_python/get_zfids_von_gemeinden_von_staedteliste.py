import pandas as pd
from pymongo import MongoClient
import ssl
from module.BranchenDeteilsExtern import addBranchenDetailsExtern, rmBranchenDetailsExtern

"""
get ids von xlsx liste
get zfids von gemeinden collection
addbranche zu den zfids
"""

client_239 = MongoClient(
    "mongodb://mongoroot:9gCaPFhotG2CNEoBRdgA@192.168.100.239:27017",
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE,
)


def get_column_of_xlsx(path: str, column_name: str) -> set[str]:
    file = pd.read_excel(path, index_col=1)
    frame: pd.DataFrame = (file).fillna("xxxxx")

    column = frame[column_name]
    print("column", len(column))
    print("set column", len(set(column)))
    return set(column)


def get_ZFIDs_from_collection(
    db_name: str, col_name: str, key: str, search_values: set[str]
) -> set[str]:
    zfids = {
        x["ZFID"]
        for x in client_239[db_name][col_name].find(
            {f"{key}": {"$in": list(search_values)}}, {"ZFID": 1}
        )
    }
    print(zfids)
    print("zfids", len(zfids))

    print("set zfids", len(set(zfids)))
    return zfids


if __name__ == "__main__":
    gemeinde_ids = get_column_of_xlsx(
        "/home/user199/Downloads/20191217_Gemeinden_ab_20000_Gesamtliste_OB-Bürgerm.xlsx",
        "_id",
    )
    zfids = get_ZFIDs_from_collection(
        db_name="Gemeinden", col_name="DE_Gemeinden", key="_id", search_values=gemeinde_ids
    )
    branche = dict(Name="staedte", Herkunft="1", WZCode=248411103)
    addBranchenDetailsExtern(zfids=zfids, branche=branche)


"""
warum diskrepanz von 22
"""

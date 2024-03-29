from pymongo import MongoClient
import pandas as pd


def search_for_zfids_for_export(db_name, col_name, query):
    client = MongoClient("192.168.100.5:27017")
    collection = client[db_name][col_name]
    cursor = collection.find(query, {"ZFID": 1})
    return [[x["ZFID"]] for x in cursor]


def make_xlsx(array, file_name):
    df1 = pd.DataFrame(array)
    df1.to_excel(f"~/Desktop/{file_name}.xlsx")


if __name__ == "__main__":
    db_name = "scrp_listen"
    col_name = "Fahrschule"
    query = {"ZFID": {"$exists": True}}

    zfid_array = search_for_zfids_for_export(db_name, col_name, query)
    file_name = "Fahrschule_zfids"
    make_xlsx(zfid_array, file_name)

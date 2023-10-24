from typing import Dict
from pymongo import MongoClient
import pandas as pd
from dataclasses import asdict
from YB_TYPES.custom_types import Branche
from module.BranchenDetails import solaranalgenanbieter_2, ausf_solar_2
from module.mongo_connections import ZF_8

def getDistinct(db_name, col_name, distinct_field, distinct_que):
    client = MongoClient('192.168.100.5:27017')
    db_5 = client[db_name][col_name]
    return db_5.distinct(distinct_field, distinct_que)

def compare_two_collections_8():
    cursor1 = set(x['ZFID'] for x in ZF_8.find({'Meta.BranchenDetails.Extern': {'$elemMatch': asdict(solaranalgenanbieter_2)}}))
    cursor2 = set(x['ZFID'] for x in ZF_8.find({'Meta.BranchenDetails.Extern': {'$elemMatch':asdict(ausf_solar_2) }}))


    print(cursor2.difference(cursor1))
    print(len(cursor2.difference(cursor1)))



    
if __name__ == '__main__':
    compare_two_collections_8()
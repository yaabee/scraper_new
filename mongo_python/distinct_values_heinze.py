from pymongo import MongoClient
from pprint import pprint
import pandas as pd


def count_number_of_hits_in_array(db_name, col_name, field_name):
    client = MongoClient('192.168.100.5:27017')
    collection = client[db_name][col_name]
    cursor = collection.find({})
    cache = {}

    for i in cursor:
        print(i[field_name])
    # for data_set in cursor:
    #     for ap in data_set['Ansprechpartner']:
    #         print(ap['ap_rolle'])
    #         if ap['ap_rolle'] in cache:
    #             cache[ap['ap_rolle']] += 1
    #         else:
    #             cache[ap['ap_rolle']] = 1
    #     # try:
    #     #     #str[]
    #     #     field_value = data_set[field_name]
    #     #     for branche in field_value:
    #     #         if branche in cache:
    #     #             cache[branche] += 1
    #     #         else:
    #     #             cache[branche] = 1
    #     # except KeyError:
    #     #     continue
    # return cache


def make_xlsx(cache_dict):
    # df1 = pd.DataFrame([['a', 'b'], ['c', 'd']],
    #                index=['row 1', 'row 2'],
    #                columns=['col 1', 'col 2'])
    # df1.to_excel("output.xlsx")

    keys = list(cache_dict.keys())
    values = list(cache_dict.values())
    # print(keys)
    # print(values)

    df1 = pd.DataFrame([keys, values])
    df1.to_excel("output.xlsx")


def check_webpage():
    pass


if __name__ == '__main__':
    db_name = 'scrp_listen'
    col_name = 'hwk_neu'
    field_name = 'Email'
    cache_dict = count_number_of_hits_in_array(db_name, col_name, field_name)
    # make_xlsx(cache_dict)
    # print(cache_dict.items())

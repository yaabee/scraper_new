from pymongo import MongoClient
import pandas as pd

def search_for_zfids_for_export(db_name, col_name, query):
    client = MongoClient('192.168.100.5:27017')
    collection = client[db_name][col_name]
    cursor = collection.find(query, {'ZFID': 1})
    return [[x['ZFID']] for x in cursor]
    
def make_xlsx(array, file_name):
    df1 = pd.DataFrame(array)
    df1.to_excel(f"~/Desktop/{file_name}.xlsx")  
    
if __name__ == '__main__':
    db_name = 'cleaned_xlsx'
    col_name = 'google_tga_xlsx'
    # search_for_plz = {'PLZ': {'$regex': r'^97'}}
    search_for_plz = {}
    zfid_array = search_for_zfids_for_export(db_name, col_name, search_for_plz)
    file_name = 'google_tga_marburg'
    make_xlsx(zfid_array, file_name)
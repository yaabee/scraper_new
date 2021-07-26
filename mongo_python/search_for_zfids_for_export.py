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
    db_name = 'GoogleApi'
    col_name = 'google_Konferenzraumtechnik_Konferenzraumtechnik'
    # search_for_plz = {'PLZ': {'$regex': r'^97'}}
    query = {'ZFID': {'$exists': True}
        # '$or': [
        #    {'PLZ': {'$regex': '^20'}}, 
        #    {'PLZ': {'$regex': '^29'}}, 
        #    {'PLZ': {'$regex': '^30'}}, 
        #    {'PLZ': {'$regex': '^31'}}, 
        #    {'PLZ': {'$regex': '^32'}}, 
        #    {'PLZ': {'$regex': '^33'}}, 
        #    {'PLZ': {'$regex': '^34'}}, 
        #    {'PLZ': {'$regex': '^35'}}, 
        #    {'PLZ': {'$regex': '^36'}}, 
        #    {'PLZ': {'$regex': '^37'}}, 
        #    {'PLZ': {'$regex': '^38'}}, 
        #    {'PLZ': {'$regex': '^39'}}, 
        #     ], 
            # "Energieberatung_für_Wohngebäude_(BAFA)": True,
            # "Effizienzhaus_(KfW)": True,
            # 'Einzelmaßnahmen': True
    # query = {
    #     '$or': [
    #        {'PLZ': {'$regex': '^10'}}, 
    #        {'PLZ': {'$regex': '^12'}}, 
    #        {'PLZ': {'$regex': '^13'}}, 
    #        {'PLZ': {'$regex': '^14'}}, 
    #        {'PLZ': {'$regex': '^15'}}, 
    #        {'PLZ': {'$regex': '^01'}}, 
    #        {'PLZ': {'$regex': '^04'}}, 
    #        {'PLZ': {'$regex': '^09'}}, 
    #     ],
    #     "Energieberatung_für_Wohngebäude_(BAFA)": True,
    #     "Effizienzhaus_(KfW)": True,
    #     'Einzelmaßnahmen': True
    }

    zfid_array = search_for_zfids_for_export(db_name, col_name, query)
    file_name = 'google_Konferenzraumtechnik_Konferenzraumtechnik'
    make_xlsx(zfid_array, file_name)
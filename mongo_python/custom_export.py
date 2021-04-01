from pymongo import MongoClient
import pandas as pd

def make_xlsx(array, file_name):
    df1 = pd.DataFrame(array)
    df1.to_excel(header=False, index=False, excel_writer=f"~/Desktop/{file_name}.xlsx")  

def custom_export(db_name, col_name, file_name, keys, query, header):
    col = MongoClient('192.168.100.5:27017')[db_name][col_name]
    cursor = col.find(query)
    export_arr = [header]
    for ds in cursor:
        # export_arr.append([row.append(ds[key]) if key in ds else row.append('xxxxx') for key in keys])
        row = []
        for key in keys:
            if key in ds:
                if ds[key]:
                    row.append(ds[key])
                else:
                    row.append('xxxxx')
            else:
                row.append('xxxxx')
        export_arr.append(row)
        row = []
    make_xlsx(export_arr, file_name=file_name)

if __name__ == '__main__':
    query = {
        '$or': [
           {'PLZ': {'$regex': '^95'}}, 
           {'PLZ': {'$regex': '^92'}}, 
           {'PLZ': {'$regex': '^93'}}, 
           {'PLZ': {'$regex': '^94'}}, 
           {'PLZ': {'$regex': '^85'}}, 
           {'PLZ': {'$regex': '^84'}}, 
           {'PLZ': {'$regex': '^83'}}, 
        ]
    }
    db_name = 'scrp_listen'
    col_name = 'bgv_bayern_gaertner'
    file_name = 'bgv_bayern_gaertner_holger_kierstein'
    keys = ['Firma', 'Ansprechpartner', 'Telefon', 'Fax', 'StrasseUndNr', 'PLZ', 'Ort', 'Email', 'Internet', 'Fachsparten', 'Dienstleistungen', 'WeitereDienstleistungen']
    header = ['Firma', 'Kontaktperson', 'Telefon', 'Fax', 'Straße', 'PLZ', 'Ort', 'Email', 'Internet', 'Fachsparten', 'Dienstleistungen', 'WeitereDienstleistungen']


    custom_export(db_name=db_name, col_name=col_name, file_name=file_name, keys=keys, query=query, header=header)


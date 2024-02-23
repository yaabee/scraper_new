from pymongo import MongoClient
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
from mgn_module.mongo_connections import SOLARIS_8
from bson import ObjectId

def dateXMonthPast(anzahl_monate: int) -> str:
    date = datetime.datetime.now()
    dateXMonthFuture = date - relativedelta(months=anzahl_monate)
    return dateXMonthFuture.isoformat()[:10] + "T00:00:00.000Z"

def make_xlsx(array, file_name):
    df1 = pd.DataFrame(array)
    df1.to_excel(header=False, index=False, excel_writer=f"~/Desktop/{file_name}.xlsx")

client_8 = MongoClient('192.168.100.8:27017',
                         username='zo_objekt_reader',
                         password='s5FLwMszMHSMck4KL6Pm',
                         authSource='zo_objekt',
                         authMechanism='SCRAM-SHA-256',
                         tls=True,
                         tlsCAFile='/etc/ssl/certs/teleaktiv_rootCA.pem')



ZO_OBJEKT_LIEFERANT_HERKUNFT_ZU_NUMMER = {
    "Unbekannt": 0,
    "AlteZO": 1,
    "IBAU": 2,
    "DTAD": 3,
    "Bindexis": 4,
    "Infoteam": 5,
    "ICB": 6,
    "Competition": 7,
    "Uponor": 8,
    "Hoermann": 9,
    "Thomas_Daily": 10,
    "Heinze": 11,
    "VIP": 12,
    "CISION": 13,
}

ZO_OBJEKT_IDNUMMER_ZU_LIEFERANTENNUMMER = {
    0: 'Unbekannt',
    1: 'AlteZO',
    2: 'IBAU',
    3: 'DTAD',
    4: 'Bindexis',
    5: 'Infoteam',
    6: 'ICB',
    7: 'Competition',
    8: 'Uponor',
    9: 'Hoermann',
    10: 'Thomas_Daily',
    11: 'Heinze',
    12: 'VIP',
    13: 'CISION'
}


header = [
    'ZOID', 
    'Objektname',
    'OriginalObjektname',
    'Straße',
    'PLZ',
    'Ort', 
    "IBAU",
    "DTAD",
    "Bindexis",
    "Infoteam",
    "ICB",
    "Competition",
    "Uponor",
    "Hoermann",
    "Thomas_Daily",
    "Heinze",
    "VIP",
    "CISION",
    "AlteZO",
    "Unbekannt",
]

if __name__ == "__main__":

    query = {
            "Meta.Erstellung": {"$gte": dateXMonthPast(12)},
            "IstDublette": False,
            "Meta.Pruefungsgrund": {"$in": ["Das Feld 'strasse' darf nicht leer sein."]},
    }

    opt = {'ZOID': 1, 'Lieferanten': 1, '_id': 0}
    cursor = list(client_8['zo_objekt']['zo_objekt'].find(query))

    ogSolaris = {str(x['_id']): x['OdinOriginalData']['ObjektText'] for x in  SOLARIS_8.find({'_id': {'$in': [ObjectId(x['ZOID']) for x in cursor]}}, {'OdinOriginalData': 1})}

    


    
    export_arr_of_arrs = [header]
    for i in cursor:
        row = []
        row.append(i['ZOID'])
        row.append(i['Objektname'])
        if i['ZOID'] in ogSolaris.keys(): row.append(ogSolaris[i['ZOID']])
        else:
            row.append('')
        row.append(i['Strasse'])
        row.append(i['PLZ'])
        row.append(i['Ort'])
        for key in header[6:]:
            cell = ''
            for lieferant in i['Lieferanten'] :
                if key == ZO_OBJEKT_IDNUMMER_ZU_LIEFERANTENNUMMER.get(lieferant['LieferantId']) and lieferant['LieferantId']:
                   cell = lieferant['LieferantObjektnummer']
            row.append(cell)

        export_arr_of_arrs.append(row)
    
    file_name = "keine_strasse_mit_lieferanten_info"
    make_xlsx(export_arr_of_arrs, file_name)





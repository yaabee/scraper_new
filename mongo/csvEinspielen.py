import pandas as pd
import requests
from mgn_types.TFirmenadresseInAccessEinspielen import TFirmenadresseInAccessEinspielen

old_file_path = '/home/user199/Desktop/master_listen/stadtwerke_bearbeitet.csv'
new_file_path =  '/home/user199/Desktop/master_listen/stadtwerke_bearbeitet_mit_zfids.csv'

df = pd.read_csv(old_file_path).fillna('')

df_new = pd.DataFrame()


new_columns = ['Firma', 'Ort', 'PLZ', 'StrasseUndNr', 'Telefon', 'ZFID', 'Neu']
dtype_dict = {'PLZ': str}
pd.DataFrame(columns=new_columns).to_csv(new_file_path, index=False)


for idx, row in df.iterrows():
    payload = TFirmenadresseInAccessEinspielen(Firma=f"{row['Firmenname']} {row['Firma2']} {row['Firma3']}", Straße=f"{row['Straße']} {row['Hausnummer']}", PLZ=row['PLZ'] if len(row['PLZ']) == 5 else '0' + row['PLZ'], Ort=row['Ort'], Internet='xxxxx', Fax='xxxxx', Telefon=row['Telefonnummer'], Land='Deutschland')
    res = requests.post('http://192.168.100.239:9099/zf_adresse_neuanlageNachAccess', json=payload.model_dump())
    data = res.json()
    new_row = {
        'Firma': row['Firmenname'], # new : old
        'Ort': row['Ort'],
        'PLZ': row['PLZ'] if len(row['PLZ']) == 5 else '0' + row['PLZ'],
        'StrasseUndNr': row['Straße'] + ' ' + row['Hausnummer'],
        'Telefon': row['Telefonnummer'],
        'ZFID': data['result']['id'] if data['ok'] else 'xxxxx',
        'Neu': data['result']['neuangelegt']
    }

    new_row_df = pd.DataFrame([new_row])
    new_row_df['PLZ'] = new_row_df['PLZ'].astype(str)
    new_row_df.to_csv(new_file_path, mode='a', header=False, index=False)



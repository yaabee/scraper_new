from tqdm import tqdm
import pandas as pd
from dataclasses import asdict, dataclass, field
import requests
from dataclasses import asdict
from tqdm import tqdm
from playsound import playsound
@dataclass
class Options:
    checkFakeFirma: bool = False
    ensureWrite: bool = False
    forceInsert: bool = False
    returnDocument: bool = True

@dataclass
class ZF_Anlegen_nach_Access:
    Fax: str = ''
    Firma: str = ''
    Internet: str = ''
    Land: str = ''
    Ort: str = ''
    PLZ: str = ''
    Straße: str = ''
    Telefon: str = ''
    options: Options = field(default_factory=Options)



def xlsxStandardtisieren(path: str):
    df = pd.read_excel(path)
    df = df.fillna('xxxxx')
    df = df.replace('keine', 'xxxxx')

    header = ['Firma','Firma2', 'StrasseUndNr', 'PLZ','Ort', 'Telefon','Fax', 'Email','Homepage']
    required_set = {'Firma', 'StrasseUndNr', 'PLZ','Ort', 'Telefon'}
    if requi := required_set.difference(set(list(df.columns))):
        print(f'!!!!{requi}, fehlt als Header!!!!')
        return


    if 'Firma2' not in df.columns:
        df['Firma2'] = pd.Series(dtype='object')
    if 'Email' not in df.columns:
        df['Email'] = pd.Series(dtype='object')
    if 'Fax' not in df.columns:
        df['Fax'] = pd.Series(dtype='object')
    if 'Homepage' not in df.columns:
        df['Homepage'] = pd.Series(dtype='object')


    #get ZFID
    for idx, _ in tqdm(list(df['Firma'].iteritems())):

        plz = df['PLZ'].astype(str)[idx] 
        df.at[idx,'PLZ'] = str(plz) if len(str(plz)) == 5 else '0' + str(plz)

        payload = ZF_Anlegen_nach_Access()
        payload.Firma = df['Firma'].astype(str)[idx]
        payload.PLZ= df['PLZ'].astype(str)[idx]
        payload.Ort =  df['Ort'].astype(str)[idx]
        payload.Telefon = df['Telefon'].astype(str)[idx]
        payload.Straße = df['StrasseUndNr'].astype(str)[idx]
        payload.Internet = df['Homepage'].astype(str)[idx]
        payload.Fax = df['Fax'].astype(str)[idx]
        url = 'http://192.168.100.239:9099/zf_adresse_neuanlageNachAccess'
        r = requests.post(url, json=asdict(payload)).json()
        df.at[idx, 'ZFID'] = r['result']['id']


    #header sortieren
    remaining_columns = [x for x in df.columns if x not in header]
    remaining_columns.sort()

    df = df[header + remaining_columns]
    df.to_excel(path, index=False)
    playsound('/home/user199/Downloads/codec.mp3')

if __name__ == '__main__':
    # playsound('/home/user199/Downloads/codec.mp3')
    xlsxStandardtisieren('/home/user199/Desktop/master_listen/ausf_elektro_2_standardtisiert.xlsx')

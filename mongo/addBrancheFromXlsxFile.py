from typing import Dict, List
import pandas as pd
from pprint import pprint
from pymongo import MongoClient
import ssl
from dataclasses import asdict
from YB_TYPES.custom_types import Branche
from module.BranchenDetails import ausf_elektro
from tqdm import tqdm
from playsound import playsound


def save_list_to_text_file(file_path, string_list):
    try:
        with open(file_path, 'w') as file:
            for item in tqdm(string_list):
                file.write("%s\n" % item)
        print(f'Saved {len(string_list)} strings to {file_path}')
    except Exception as e:
        print(f'Error: {e}')

client_8 = MongoClient(
    "mongodb://mongoroot:9gCaPFhotG2CNEoBRdgA@192.168.100.8:27017",
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE,
)

ZF_8 = client_8['ZentralerFirmenstamm']['ZentralerFirmenstamm']


def addBranchenDetailsExtern(zfids: List[str], addBranchendetail: Dict):
    input('wirklich starten?')
    for zfid in tqdm(zfids):
        client_8["ZentralerFirmenstamm"]["ZentralerFirmenstamm"].update_one(
            {"ZFID": zfid},
            {"$addToSet": {"Meta.BranchenDetails.Extern": addBranchendetail}},
        )


def xlsxEinspielen(path: str, branche: Dict, zfids: List[str] = []):
    file = pd.read_excel(path)
    frame: pd.DataFrame = (file).fillna("xxxxx")
    if not 'ZFID' in frame.columns:
        raise Exception('ZFID')
    if zfids:
        addBranchenDetailsExtern(zfids, branche)
    addBranchenDetailsExtern(list(frame['ZFID']),branche)

    playsound('/home/user199/Downloads/codec.mp3')


if __name__ == "__main__":

    xlsxEinspielen(

        '/home/user199/Desktop/master_listen/ausf_elektro_2_standardtisiert.xlsx',
        branche=asdict(Branche(Name='ausf_elektro', Herkunft='2', WZCode=154321100)),
    )




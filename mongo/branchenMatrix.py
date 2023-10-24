import re
import ssl
import pandas as pd
from pprint import pprint
from pymongo import MongoClient

client = MongoClient(
    "192.168.100.8:27017",
    username="mongoroot",
    password="9gCaPFhotG2CNEoBRdgA",
    authSource="admin",
    authMechanism="SCRAM-SHA-256",
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE,
)

client_239 = MongoClient(
    "192.168.100.239:27017",
    username="mongoroot",
    password="9gCaPFhotG2CNEoBRdgA",
    authSource="admin",
    authMechanism="SCRAM-SHA-256",
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE,
)

client_239_1 = MongoClient("192.168.100.239:27099")

ZF_8 = client['ZentralerFirmenstamm']['ZentralerFirmenstamm']
ALLG_BRANCHEN = client_239['staticdata']['AllgemeineVorlagen_Branchenliste']
AUTO_BRANCHEN = client_239['staticdata']['automatischeBranche']
BRANCHEX = client_239_1["BrancheX"]["ZFID_Liste_mit_branchenstring"]


df = pd.read_excel('/home/user199/pp/scraper_new/mongo/20220323_Matrix_Signalwörter_ACCESS.xlsx')
df = df.fillna(True)
df = df.replace('x', False)

columns = [x.replace('Nicht ', '') for x in df.columns]

ausf_wzcodes = list(set(x['BranchenID'] for x in ALLG_BRANCHEN.find({'Branche': re.compile('Ausf', re.IGNORECASE)}))) + list(set(x['branche_id'] for x in AUTO_BRANCHEN.find({'branche': re.compile('ausf', re.IGNORECASE)})))
gemeinde_stadt_wzcode = ['248411103']
planer_wzcodes = list(set(x['BranchenID'] for x in ALLG_BRANCHEN.find({'Branche': re.compile('Planer', re.IGNORECASE)}))) + list(set(x['branche_id'] for x in AUTO_BRANCHEN.find({'branche': re.compile('planer', re.IGNORECASE)})))
misch_bautraeger = ['154110000']
misch_gu_gue = ['216841500']
misch_fhh = ['154121200']
misch_mhh = ['154121100']
misch_wowi = ['216811100']

# print(len(ausf_wzcodes))
# print(len(planer_wzcodes))


counter = 1
for idx, value in df.iterrows():
    row = list(zip(columns[1:], value.values[1:]))
    signal = list(x['branche_id'] for x in AUTO_BRANCHEN.find({'signalwoerter': {'$in': [row[0][1]]}}))
    print(row, signal)
    #generate wzcode list
    yes_wzcodes = signal
    no_wzcodes = []
    for branche, value in row:
        if branche == 'ausf':
            if not value:
                no_wzcodes += ausf_wzcodes
        elif branche == 'gemeinde/stadt':
            if not value:
                no_wzcodes += gemeinde_stadt_wzcode
        elif branche == 'planer':
            if not value:
                no_wzcodes += planer_wzcodes
        elif branche == 'misch_bautraeger':
            if not value:
                no_wzcodes += misch_bautraeger
        elif branche == 'misch_gu/gue':
            if not value:
                no_wzcodes += misch_gu_gue
        elif branche == 'misch_fhh':
            if not value:
                no_wzcodes += misch_fhh
        elif branche == 'misch_mhh':
            if not value:
                no_wzcodes += misch_mhh
        elif branche == 'misch_wowi':
            if not value:
                no_wzcodes += misch_wowi

    for no in no_wzcodes:
        mongoquery = {'Meta.Branchen': {'$all': yes_wzcodes + [no] }}
        pot_zfids_l = [x['ZFID'] for x in ZF_8.find(mongoquery, {'ZFID': 1})]
        pot_zfids_s = set(x['ZFID'] for x in ZF_8.find(mongoquery, {'ZFID': 1}))
        branche_x_zfids = set(x['ZFID'] for x in BRANCHEX.find({'ZFID': {'$in': pot_zfids_l}}, {'ZFID': 1}))

        no_allg_name = [x['Branche'] for x in ALLG_BRANCHEN.find({'BranchenID': no})]
        no_auto_name = [x['branche'] for x in AUTO_BRANCHEN.find({'branche_id': int(no)})]
        yes_allg_name = [x['Branche'] for x in ALLG_BRANCHEN.find({'BranchenID': yes_wzcodes[0]})]
        yes_auto_name = [x['branche'] for x in AUTO_BRANCHEN.find({'branche_id': int(yes_wzcodes[0])})]

        no_name = no_allg_name + no_auto_name
        yes_name = yes_allg_name + yes_auto_name

        zfids_gesamt = pot_zfids_s.difference(branche_x_zfids)
        if zfids_gesamt:
            widerspruch = f'Widerspruch: wenn {yes_name}{yes_wzcodes} dann darf nicht {no_name}{[no]}'
            for zfid in zfids_gesamt:
                # print('=================================')
                # print(zfid, widerspruch)
                ZF_8.update_one({'ZFID': zfid}, {'$addToSet': {'Meta.PruefenGrund': widerspruch}, '$set': {'Meta.ZuPruefen': True}})
    #             break
    #         break
    #     continue
    # break

    if counter == 64:
        break
    else:
        counter += 1

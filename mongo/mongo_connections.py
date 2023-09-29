from pymongo import MongoClient
import ssl


client_zo_reader = MongoClient(
    "mongodb://zo_objekt_reader:s5FLwMszMHSMck4KL6Pm@192.168.100.8:27017/zo_objekt",
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE,
)

client_solaris = MongoClient(
    "mongodb://mongoroot:9gCaPFhotG2CNEoBRdgA@192.168.100.8:27018", serverSelectionTimeoutMS=1000
)

client_239 = MongoClient(
    "mongodb://mongoroot:9gCaPFhotG2CNEoBRdgA@192.168.100.239:27017",
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE,
)
client_8 = MongoClient(
    "mongodb://mongoroot:9gCaPFhotG2CNEoBRdgA@192.168.100.8:27017",
    ssl=True,
    ssl_cert_reqs=ssl.CERT_NONE,
)

client_5 = MongoClient("mongodb://192.168.100.5:27017")
ZF_8 = client_8["ZentralerFirmenstamm"]["ZentralerFirmenstamm"]
ANSPRECHPARTNER_8 = client_8["ZentralerFirmenstamm"]["Ansprechpartner"]  # ap_collection
FA_239 = client_239["FirmenAdresse"]["FirmenAdresse"]  # fa_collection
AUTOMATISCHE_BRANCHE_239 = client_239["staticdata"]["automatischeBranche"]
ALLGEMEINE_BRANCHE_239 = client_239["staticdata"]["AllgemeineVorlagen_Branchenliste"]
WER_ZU_WEM_5 = client_5["Werzuwem"]["0_xlsx"].find({})  # WZW
GELBESEITEN = client_239["ZentralerFirmenstamm"]["Gelbeseiten"]
GEMEINDEN = client_239["Gemeinden"]["DE_Gemeinden"]

# odin
ODIN_8 = client_8["zo_objekt"]["zo_objekt"]
ODIN_MOEGLICHE_DUBS = client_zo_reader["zo_objekt"]["zo_moegliche_dubs"]
RESULT_NACH_ODIN_5 = client_5["AutoImport"]["ResultNachOdin"]
COMBINED_ZOO_5 = client_5["AutoImport"]["CombinedZOObjekt"]
CRONJOBS_239 = client_239["odin"]["Cronjobs"]
CATEGORY_REF_239 = client_239["odin"]["ObjectCategoriesReferenceList"]
RULESETS = client_239["odin"]["RuleSets"]

# Solaris
SOLARIS_8 = client_solaris["solaris"]["objects"]


# ?
wz_codes = list(AUTOMATISCHE_BRANCHE_239.find({"branche_id": {"$exists": True}}))
wz_codes_timo = list(ALLGEMEINE_BRANCHE_239.find({}))
wz_cache = {}

for i in wz_codes_timo:
    if i["BranchenID"] not in wz_cache:
        wz_cache[i["BranchenID"]] = i["Branche"]
for j in wz_codes:
    if j["branche_id"] not in wz_cache:
        wz_cache[j["branche_id"]] = j["branche"]

WZ_CACHE_239 = wz_cache

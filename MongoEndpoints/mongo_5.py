from pymongo import MongoClient

client5 = MongoClient('192.168.100.5:27017')

# ZentralerFirmenstamm

# scrp_listen
SCRP_LISTEN_HEINZE_BACK = client5['scrp_listen']['heinze_zfid_back']
SCRP_LISTEN_HEINZE = client5['scrp_listen']['heinze_zfid']

# GoogleApi

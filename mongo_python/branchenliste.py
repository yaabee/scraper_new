from pymongo import MongoClient
import ssl

client = MongoClient('mongodb://mongoroot:9gCaPFhotG2CNEoBRdgA@192.168.100.239:27017',
  ssl=True,
  ssl_cert_reqs=ssl.CERT_NONE
)

agg = list(client['staticdata']['automatischeBranche'].find({}))


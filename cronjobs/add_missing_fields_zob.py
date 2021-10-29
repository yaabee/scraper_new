from pymongo import MongoClient
import ssl
import pprint

client_5 = MongoClient('192.168.100.5:27017')
client_239 = MongoClient('192.168.100.239:27017',
                         username='mongoroot',
                         password='9gCaPFhotG2CNEoBRdgA',
                         authSource='admin',
                         authMechanism='SCRAM-SHA-256',
                         ssl=True,
                         ssl_cert_reqs=ssl.CERT_NONE)


zob = client_239['ZentralerFirmenstamm']['ZentralerFirmenstamm']


def main():
    pass


if __name__ == '__main__':
    main()

import ssl
from pymongo import MongoClient
import requests

client_239 = MongoClient('192.168.100.239:27017',
                         username='mongoroot',
                         password='9gCaPFhotG2CNEoBRdgA',
                         authSource='admin',
                         authMechanism='SCRAM-SHA-256',
                         ssl=True,
                         ssl_cert_reqs=ssl.CERT_NONE)


def main():
    # requests.post('192.168.100.104:5555/zobListe/', json=payload)
    pass


if __name__ == '__main___':
    main()

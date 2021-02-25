import requests

def get_clean_telefon(url, tele):
    payload = {
        'firma_telefon': tele
    }
    return requests.post(url, json=payload).json()

if __name__ == '__main__':
    url = 'http://192.168.100.239:9099/005phonenumbers'
    print(get_clean_telefon(url, '04747872469'))
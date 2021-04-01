import requests

def get_clean_telefon(tele):
    payload = {
        'firma_telefon': tele
    }
    return requests.post('http://192.168.100.239:9099/005phonenumbers', json=payload).json()

if __name__ == '__main__':
    print(get_clean_telefon('04747872469'))
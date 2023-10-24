import requests
from dataclasses import dataclass


@dataclass
class resHausnummer:
    firma_hausnummer: str
    firma_strasse: str
    resultUsable: bool


# neu
# def cleanHausnummer(hausnummer: str, default=None) -> resHausnummer:
#     # clean inital field
#     if len(hausnummer) > 6:
#         hausnummer = "xxxxx"

#     return requests.post(
#         "http://192.168.100.239:9099/004hausnummern",
#         json={"firma_strasse": i["Straße gm"]},
#     ).json()


@dataclass
class resSanitizeStrasse:
    strasse_sanitized: str


def sanitizeStrasse(strasse: str, default=None) -> resSanitizeStrasse:
    return requests.post(
        "http://192.168.100.239:9099/027_sanitize_strasse",
        json={"firma_strasse": strasse},
    ).json()
    # error handling


@dataclass
class resPhone:
    firma_telefon: str
    firma_telefon_clean: str
    firma_telefon_ursprung: str


def cleanPhone(telefon: str, default=None) -> resPhone:
    return requests.post(
        "http://192.168.100.239:9099/005phonenumbers",
        json={"firma_telefon": telefon},
    ).json()


def cleanPLZ(plz: str, default=None) -> str:
    return plz if len(plz) == 5 else '0' + plz

@dataclass
class EmailData:
    domain: str
    freemail_status: bool
    mail: str
    online: bool
    syntax_okay: bool

def check_website(website: str) -> EmailData:
    if "https://www" in website:
        website = website.replace("https://www.", "www.info@")
    elif "https://" in website:
        website = website.replace("https://", "www.info@")
    elif "http://www" in website:
        website = website.replace("http://www.", "www.info@")
    elif "http://" in website:
        website = website.replace("http://", "www.info@")
    elif "www." in website and not "info@" in website:
        website = website.replace("www.", "www.info@")
    elif "www." not in website:
        website = f"www.info@{website}"
    if ".de/" in website or ".com/" in website or ".nl/" in website:
        ind = website.index("/")
        website = website[:ind]
    url = "http://192.168.100.239:9099/003mailcheck"
    payload = dict(firma_email=website)
    response =  requests.post(url, json=payload).json()
    if response.status_code >= 500:
        raise Exception('email check ging nicht [check_website]')
    return response
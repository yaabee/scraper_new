from dataclasses import dataclass
import requests


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

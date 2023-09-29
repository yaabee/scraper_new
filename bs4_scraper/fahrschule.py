import re
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from pprint import pprint


def insert_new_dataset_into_mdb(mdb_uri, datenbank, collection, datensatz):
    client = MongoClient(mdb_uri, 27017, maxPoolSize=500)
    db = client[datenbank]
    collection = db[collection]
    collection.insert_one(datensatz)


def extract_digits(s):
    return "".join(re.findall(r"\d+", s))


def separate_address(address_string):
    parts = address_string.replace(",", "").replace("D-", "").split("\r")
    street_address = parts[0].strip()
    postal_city = parts[1].strip()
    postal_code, city = postal_city.split(" ", 1)
    return street_address, postal_code, city


def parse_telefon_mobile(telefon):
    if "," not in telefon:
        return telefon.replace("Telefon:", ""), ""
    splitted = telefon.split(",")
    return splitted[0].replace("Telefon:", ""), splitted[1].replace("Mobile:", "")


def scrape_fahrschule_map():
    # Initialize a list to store the results
    results = []

    # Loop over all pages of search results
    page_num = 1
    while True:
        # Make a GET request to the current search results page
        url = f"https://fahrschulenmap.de/fahrschule-80/0/{page_num}.html"
        response = requests.get(url)

        # Stop the loop if the page doesn't exist
        if response.status_code != 200 or page_num > 15:
            break

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the information for each driving school on the page
        driving_schools = soup.find_all("span", {"class": "scline"})
        for driving_school in driving_schools:
            name = driving_school.find("h2").text.strip()
            address = (
                driving_school.find("div", {"class": "adresse"})
                .text.strip()
                .replace("\n", ", ")
            )

            strasse, plz, ort = separate_address(address)

            phone = (
                driving_school.find("div", {"class": "telefon"})
                .text.strip()
                .replace("\n", ", ")
            )

            tele, mobil = parse_telefon_mobile(phone)

            result = {
                "Firma": name,
                "Telefon": tele,
                "Mobil": mobil,
                "PLZ": plz,
                "Ort": ort,
                "StrasseUndNr": strasse,
            }

            if result not in results:
                results.append(result)

        # Move to the next page of search results
        page_num += 1

    # print(len(results))
    return results


if __name__ == "__main__":
    results = scrape_fahrschule_map()

    for result in results:
        insert_new_dataset_into_mdb(
            mdb_uri="192.168.100.5",
            datenbank="scrp_listen",
            collection="Fahrschule",
            datensatz=result,
        )

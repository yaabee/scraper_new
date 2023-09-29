from pymongo import MongoClient
import pandas as pd


def make_xlsx(array, file_name):
    df1 = pd.DataFrame(array)
    df1.to_excel(header=False, index=False, excel_writer=f"~/Desktop/{file_name}.xlsx")
    print(file_name)


def custom_export(db_name, col_name, file_name, keys, query, header):
    col = MongoClient("192.168.100.5:27017")[db_name][col_name]
    cursor = list(col.find(query))
    print(len(cursor))
    export_arr = [header]
    for ds in cursor:
        row = []
        for key in keys:
            print(key)
            print(ds[key])
            if key in ds:
                if ds[key]:
                    row.append(str(ds[key]))

                else:
                    row.append("")
        export_arr.append(row)
        row = []
    make_xlsx(export_arr, file_name=file_name)


"""Fahschule"""
fahrschule = {
    "keys": ["Firma", "StrasseUndNr", "PLZ", "Ort", "Telefon", "Mobil"],
    "header": ["Firma", "StrasseUndNr", "PLZ", "Ort", "Telefon", "Mobil"],
}
"""Fahschule"""
google_api = {
    "keys": ["Firma", "StrasseUndNr", "PLZ", "Ort", "Telefon", "Website"],
    "header": ["Firma", "StrasseUndNr", "PLZ", "Ort", "Telefon", "Website"],
}
google = {
    "keys": [
        "business_card",
        "Firma",
        "Ansprechpartner",
        "Telefon",
        "Fax",
        "Addresse",
        "Internet",
        "Objektkategorie",
        "Maßnahme",
        "Branche",
        "Leistungen",
        "Zertifikate",
        "Objektdaten",
    ],
    "header": [
        "Typ",
        "Firma",
        "Ansprechpartner",
        "Telefon",
        "Fax",
        "Addresse",
        "Internet",
        "Objektkategorie",
        "Maßnahme",
        "Branche",
        "Leistungen",
        "Zertifikate",
        "Objektdaten",
    ],
}


"""baunetz"""
baunetz = {
    "keys": ["firma", "firma_tele", "link", "rank", "zfid"],
    "header": ["Firma", "Firma In ZF", "Link", "Rang", "ZFID"],
}

""" google """
google = {
    "keys": [
        "business_card",
        "Firma",
        "Ansprechpartner",
        "Telefon",
        "Fax",
        "Addresse",
        "Internet",
        "Objektkategorie",
        "Maßnahme",
        "Branche",
        "Leistungen",
        "Zertifikate",
        "Objektdaten",
    ],
    "header": [
        "Typ",
        "Firma",
        "Ansprechpartner",
        "Telefon",
        "Fax",
        "Addresse",
        "Internet",
        "Objektkategorie",
        "Maßnahme",
        "Branche",
        "Leistungen",
        "Zertifikate",
        "Objektdaten",
    ],
}


""" scraper """
scraper = {
    "keys": [
        "Firma",
        "Ort",
        "PLZ",
        "StrasseUndNr",
        "Telefon",
        "Fax",
        "Handy",
        "Email",
        "Internet",
        "Branche",
        "ZFID",
    ],
    "header": [
        "Firma",
        "Ort",
        "PLZ",
        "StrasseUndNr",
        "Telefon",
        "Fax",
        "Handy",
        "Email",
        "Internet",
        "Branche",
        "ZFID",
    ],
}
""" Energie-Effizienz """
energie_effizienz = {
    "keys": [
        "Firma",
        "Ort",
        "PLZ",
        "StrasseUndNr",
        "Telefon",
        "Effizienzhaus_(KfW)",
        "Effizienzhaus_Denkmal_(und_besonders_erhaltenswerte_Bausubstanz)_(KfW)",
        "Einzelmaßnahmen",
        "Energieberatung_für_Wohngebäude",
        "Fenster_und_Türen",
        "Heizung",
        "Lüftung",
        "Wärmedämmung",
        "Berufsgruppe",
        "Homepage",
        "Email",
        "name",
        "StrassenId",
        "branche",
        "Neuangelegt",
        "ZFID",
    ],
    "header": [],
}


""" Gelbesetien """
gelbeseiten = {
    "keys": [
        "firma_name",
        "firma_ort",
        "firma_plz",
        "firma_strasse",
        "firma_telefon_ursprung",
    ],
    "header": [
        "Firma",
        "Ort",
        "PLZ",
        "StrasseUndNr",
        "Telefon",
    ],
}

lithonplus = [
    "Firma",
    "Straße",
    "PLZ",
    "Ort",
    "Telefon",
    "Fax",
    "Email",
    "Internet",
    "Branche",
]

google_api = {
    "keys": ["Firma", "Telefon", "StrasseUndNr", "PLZ", "Ort", "Website", 'ZFID'],
    "header": ["Firma", "Telefon", "StrasseUndNr", "PLZ", "Ort", "Internet", 'ZFID'],
}


if __name__ == "__main__":
    query = {}
    db_name = "GoogleApi"
    col_name = "google_Intersolar"
    file_name = "google_Intersolar"

    custom_export(
        db_name=db_name,
        col_name=col_name,
        file_name=file_name,
        keys=google_api["keys"],
        query=query,
        header=google_api["header"],
    )

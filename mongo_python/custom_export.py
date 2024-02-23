from pymongo import MongoClient
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta


def dateXMonthPast(anzahl_monate: int) -> str:
    date = datetime.datetime.now()
    dateXMonthFuture = date - relativedelta(months=anzahl_monate)
    return dateXMonthFuture.isoformat()[:10] + "T00:00:00.000Z"

def make_xlsx(array, file_name):
    df1 = pd.DataFrame(array)
    df1.to_excel(header=False, index=False, excel_writer=f"~/Desktop/{file_name}.xlsx")
    print(file_name)


def custom_export(db_name, col_name, file_name, keys, query, header):
    col = MongoClient("192.168.100.5:27017")[db_name][col_name]
    cursor = list(col.find(query))
    export_arr = [header]
    for ds in cursor:
        row = []
        for key in keys:
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
    "keys": ["Firma", "Telefon", "StrasseUndNr", "PLZ", "Ort", "Fax", "Email", "Internet"],
    "header": ["Firma", "Telefon", "StrasseUndNr", "PLZ", "Ort", "Fax", "Email", "Internet"],
}

zfids = {"keys": ["ZFID"], "header": ["ZFID"]}

# Equivalent of TZOObjektLieferantHerkunftZuNummer and TLieferanten
ZO_OBJEKT_LIEFERANT_HERKUNFT_ZU_NUMMER = {
    "Unbekannt": 0,
    "AlteZO": 1,
    "IBAU": 2,
    "DTAD": 3,
    "Bindexis": 4,
    "Infoteam": 5,
    "ICB": 6,
    "Competition": 7,
    "Uponor": 8,
    "Hoermann": 9,
    "Thomas_Daily": 10,
    "Heinze": 11,
    "VIP": 12,
    "CISION": 13,
}

# Function equivalent to getLieferantenNummerFromHerkunft
def get_lieferanten_nummer_from_herkunft(herkunft):
    return ZO_OBJEKT_LIEFERANT_HERKUNFT_ZU_NUMMER.get(herkunft, 0)  # Returns 0 if herkunft not found

# Function equivalent to getLieferantenTypFromNumber
def get_lieferanten_typ_from_number(number):
    # Reverse the dictionary to map numbers to names
    number_to_name = {v: k for k, v in ZO_OBJEKT_LIEFERANT_HERKUNFT_ZU_NUMMER}



if __name__ == "__main__":
    query = {        "$and": [
            # {"Baubeginn": "1970-01-01T00:00:00.000Z"},
            # {"Meta.Exportierbar": True},
            {"Meta.Erstellung": {"$gte": dateXMonthPast(12)}},
            {"IstDublette": False},
            {"Meta.Pruefungsgrund": {"$in": ["Das Feld 'beteiligte' muss mindestens 1 Einträge beinhalten."]}},
        ]}
    db_name = "zo_objekt"
    col_name = "zo_objekt"
    file_name = "beteiligte_mit_lieferanten_info"

    custom_export(
        db_name=db_name,
        col_name=col_name,
        file_name=file_name,
        keys=google_api["keys"],
        query=query,
        header=google_api["header"],
    )



from pymongo import MongoClient
import pandas as pd


def make_xlsx(array, file_name):
    df1 = pd.DataFrame(array)
    df1.to_excel(header=False, index=False,
                 excel_writer=f"~/Desktop/{file_name}.xlsx")


def custom_export(db_name, col_name, file_name, keys, query, header):
    col = MongoClient("192.168.100.5:27017")[db_name][col_name]
    cursor = col.find(query)
    export_arr = [header]
    for ds in cursor:
        # export_arr.append([row.append(ds[key]) if key in ds else row.append('xxxxx') for key in keys])
        row = []
        for key in keys:
            if key in ds:
                if ds[key]:
                    row.append(ds[key])
                else:
                    row.append("xxxxx")
            else:
                row.append("xxxxx")
        export_arr.append(row)
        row = []
    make_xlsx(export_arr, file_name=file_name)


if __name__ == "__main__":
    query = {}
    db_name = "scrp_listen"
    col_name = "hwk_neu"
    file_name = "hwk_branchen"
    """ google """
    # keys = [
    #     "business_card",
    #     "Firma",
    #     "Ansprechpartner",
    #     "Telefon",
    #     "Fax",
    #     "Addresse",
    #     "Internet",
    #     "Objektkategorie",
    #     "Maßnahme",
    #     "Branche",
    #     "Leistungen",
    #     "Zertifikate",
    #     "Objektdaten",
    # ]
    # header = [
    #     "Typ",
    #     "Firma",
    #     "Ansprechpartner",
    #     "Telefon",
    #     "Fax",
    #     "Addresse",
    #     "Internet",
    #     "Objektkategorie",
    #     "Maßnahme",
    #     "Branche",
    #     "Leistungen",
    #     "Zertifikate",
    #     "Objektdaten",
    # ]
    """ scraper """
    keys = [
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
    ]
    header = [
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
    ]

    custom_export(
        db_name=db_name,
        col_name=col_name,
        file_name=file_name,
        keys=keys,
        query=query,
        header=header,
    )

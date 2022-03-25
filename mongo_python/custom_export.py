from pymongo import MongoClient
import pandas as pd
import ssl


def make_xlsx(array, file_name):
    df1 = pd.DataFrame(array)
    df1.to_excel(header=False, index=False,
                 excel_writer=f"~/Desktop/{file_name}.xlsx")


def custom_export(db_name, col_name, file_name, keys, query, header):
    # col = MongoClient("192.168.100.5:27017")[db_name][col_name]
    col = MongoClient("mongodb://mongoroot:9gCaPFhotG2CNEoBRdgA@192.168.100.239:27017",
     ssl=True,
     ssl_cert_reqs=ssl.CERT_NONE)[db_name][col_name]
    cursor = col.find(query)
    export_arr = [header]
    for ds in cursor:
        row = []
        for key in keys:
            if key in ds:
                if ds[key]:
                    row.append(str(ds[key]))
                # else:
                #     row.append("xxxxx")
            # else:
            #     row.append("xxxxx")
        export_arr.append(row)
        row = []
    make_xlsx(export_arr, file_name=file_name)


if __name__ == "__main__":
    query = {}
    db_name = "staticdata"
    col_name = "AllgemeineVorlagen_Branchenliste"
    file_name = "branchenliste_me"
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
    # keys = [
    #     "Firma",
    #     "Ort",
    #     "PLZ",
    #     "StrasseUndNr",
    #     "Telefon",
    #     "Fax",
    #     "Handy",
    #     "Email",
    #     "Internet",
    #     "Branche",
    #     "ZFID",
    # ]
    # header = [
    #     "Firma",
    #     "Ort",
    #     "PLZ",
    #     "StrasseUndNr",
    #     "Telefon",
    #     "Fax",
    #     "Handy",
    #     "Email",
    #     "Internet",
    #     "Branche",
    #     "ZFID",
    # ]
    """ Energie-Effizienz """
    # keys = [
    #     "Firma",
    #     "Ort",
    #     "PLZ",
    #     "StrasseUndNr",
    #     "Telefon",
    #     "Effizienzhaus_(KfW)",
    #     "Effizienzhaus_Denkmal_(und_besonders_erhaltenswerte_Bausubstanz)_(KfW)",
    #     "Einzelmaßnahmen",
    #     "Energieberatung_für_Wohngebäude",
    #     "Fenster_und_Türen",
    #     "Heizung",
    #     "Lüftung",
    #     "Wärmedämmung",
    #     "Berufsgruppe",
    #     "Homepage",
    #     "Email",
    #     "name",
    #     "StrassenId",
    #     "branche",
    #     "Neuangelegt",
    #     "ZFID",
    # ]
    keys = ['Branche', 'BranchenID']
    """ automatischeBranchen"""

    custom_export(
        db_name=db_name,
        col_name=col_name,
        file_name=file_name,
        keys=keys,
        query=query,
        header=keys,
    )

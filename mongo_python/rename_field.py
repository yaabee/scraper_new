from pymongo import MongoClient
import ssl


def rename_field(db_name, col_name, field_name_old, field_name_new):
    # client = MongoClient('192.168.100.5:27017')
    client_239 = MongoClient('192.168.100.239:27017',
                             username='mongoroot',
                             password='9gCaPFhotG2CNEoBRdgA',
                             authSource='admin',
                             authMechanism='SCRAM-SHA-256',
                             ssl=True,
                             ssl_cert_reqs=ssl.CERT_NONE)
    collection = client_239[db_name][col_name]
    update = collection.update(
        {}, {'$rename': {field_name_old: field_name_new}}, False, True)
    # cursor = collection.find({})
    # for data_set in cursor:
    #     update = collection.update_one({'_id': data_set['_id']}, {
    #                                    '$rename': {field_name_old: field_name_new}})
    #     print(update.modified_count)
    #     update = collection.update(
    #         {}, {'$rename': {field_name_old: field_name_new}}, False, True)


if __name__ == '__main__':
    db_name = 'ZentralerFirmenstamm'
    col_name = 'ZentralerFirmenstamm'
    field_name_old = 'Meta.Terminvormerkung.Gesamtanzahl'
    field_name_new = 'Meta.Terminvormerkung.GesamtAnzahl'
    rename_field(db_name, col_name, field_name_old, field_name_new)

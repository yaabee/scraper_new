from pymongo import MongoClient
import ssl

""" 
needz:
    mongo cleaned_xlsx
    => get zfids, + name

    mongo googleapi
    => get status

    insert into zob


    {Meta: google_business_status: ... }
"""

def business_status_einspielen(cleaned_xlsx_col_name, googleApi_col_name):
    client_239 = MongoClient('192.168.100.239:27017',
                        username='mongoroot',
                        password='9gCaPFhotG2CNEoBRdgA',
                        authSource='admin',
                        authMechanism='SCRAM-SHA-256',
                        ssl=True,
                        ssl_cert_reqs=ssl.CERT_NONE)
    client_5 = MongoClient('192.168.100.5:27017')
    #get zfids
    cleaned_xlsx = client_5['cleaned_xlsx'][cleaned_xlsx_col_name].find({})

    #get business_status
    google_api = client_5['GoogleApi'][googleApi_col_name]

    #insert zob 239
    zob_col = client_239['ZentralerFirmenstamm']['ZentralerFirmenstamm']


    for ds in cleaned_xlsx:
        print('zfid', ds['ZFID'])
        print('name', ds['Firma'])
        business_status_per_name = google_api.find_one({'name': ds['Firma']})['business_status']
        print('business_status', business_status_per_name)

        insertion = zob_col.update_one(
          {'ZFID': ds['ZFID']},
          {'$set': 
          {
              'Meta.GoogleBusinessStatus': business_status_per_name}
          }
        )
        print('inserted', str(insertion.acknowledged))

if __name__ == '__main__':
    business_status_einspielen('google_tga_xlsx', 'google_tga')

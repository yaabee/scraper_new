from pymongo import MongoClient

def anzahl_value_heinze(db_name, col_name, key_name):
    '''
    parameter:
        key_name ist der Suchbegriff
    funktion:
        cache = {
            key: {
                value1, anzahl_value1
                value2, anzahl_value2
                .
                .
                valueN, anzahl_valueN
            }
        }
    return:
        als xlsx

        | Key    | Anzahl |
        | value1 | x      |
        | .      | x      |
        | .      | x      |
        | valueN | x      |
    
    Bsp heinze:
        KEY = FACHGRUPPE, FACHBEREICH, GEWERKE:
        VALUE = ['Baustoffhandel']
        Anzahl Begriff
    '''

    client = MongoClient('192.168.100.5:27017')
    collection = client[db_name][col_name]
    key_value = collection.find({}, {key_name: 1})

    return key_value

if __name__ == '__main__':
    key_name = 'Fachgruppe, Fachbereich, Gewerk'
    db_name = 'scrp_listen'
    col_name = 'heinze'
    cursor = list(anzahl_value_heinze(db_name, col_name, key_name))


    for i in cursor:
        try:
            print(i[key_name])
        except KeyError:
            continue
    





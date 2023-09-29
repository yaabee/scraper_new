import pandas as pd

def xlsxStandardtisieren(path: str):
    df = pd.read_excel(path)

    required = {'Firma', 'Telefon','PLZ', 'Ort', 'StrasseUndNr'}
    
    if requi := required.difference(set(list(df.columns))):
        print(f'!!!!{requi}, fehlt als Header!!!!')
        return
    
    #Firma std
    #Telefon std
        #TelefonRaw
    #Fax std
        #FaxRaw
    #PLZ std
        #string
        #5stellig
    #Ort std
    #StrasseUndNr std
        #Strassenname
        #Hausnummer
    #Email std
    #Homepage std

if __name__ == '__main__':
    xlsxStandardtisieren('/home/user199/Desktop/master_listen/misch_bauträger_1_standardtisiert.xlsx')



    '''
    df = pd.read_excel(path)

    alternative_names = []
    print('same: 0')
    print('Firma: 1')
    print('Straße: 2')
    print('PLZ: 3')
    print('Ort: 4')
    print('Telefon: 5')
    print('retry Key Number')
    required = ['Firma', 'Telefon','PLZ', 'Ort', 'Straße']
    print(required)
    for i in df.columns:
        first_value = ''
        for j in df[i]:
            first_value = j
            if first_value:
                break

        alternative_name = input(f"'{i}' [{first_value}] soll werden: ")

        if alternative_name == '0':
            alternative_name = i
        if alternative_name == '1':
            alternative_name = 'Firma'
        if alternative_name == '2':
            alternative_name = 'Telefon'
        if alternative_name == '3':
            alternative_name = 'PLZ'
        if alternative_name == '4':
            alternative_name = 'Ort'
        if alternative_name == '5':
            alternative_name = 'Straße'

        alternative_names.append(alternative_name)
    

    print(list(enumerate(list(zip(df.columns, alternative_names)))))
    index = input('retry @ index: ')
    '''
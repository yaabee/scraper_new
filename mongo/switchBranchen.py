from typing import Dict, Union
from mongo_connections import client_8
import pymongo
from pprint import pprint
from dataclasses import dataclass, asdict

"""
finde alle ds mit branche 
addtoset neue_branche
pull alte branche
"""



@dataclass
class Branche:
    Name: str
    WZCode: Union[int, str]
    Herkunft: str

def switch_branchen_extern_stich_home(path: str,db: str, col: str,ctrl_begriff:str, alt_branche:Dict, neu_branche: Dict, debug: bool = True):
    collection = client_8[db][col]

    if not debug:
        print('scharf')
        updated_extern_add = collection.find({path: {'$elemMatch': alt_branche}})
        for i in updated_extern_add:
            collection.update_one({'ZFID': i['ZFID']},{'$addToSet': {path: neu_branche}})
            collection.update_one({'ZFID': i['ZFID']},{'$pull': {path: alt_branche}})
            print('========================================')
            print('=== extern ===')
            pprint(i['ZFID'])
        
    
    if 'Extern' in path:
        count_extern = collection.count_documents({path: {'$elemMatch': {'Name':ctrl_begriff}}})
        print('extern', count_extern)

    if 'Stichwoerter' in path:
        count_stich = collection.count_documents({path: {'$elemMatch': {'Name':ctrl_begriff}}})
        print('extern', count_stich)

    if 'Homepage' in path:
        count_home = collection.count_documents({path: {'$elemMatch': {'Name':ctrl_begriff}}})
        print('extern', count_home)

if __name__ == '__main__':

    """
    words to check:
        intersolar
        Branche: solaranlageninstallationsservice, Herkunft: Google

    """

    ctrl_begriff = 'misch_fhh/1'
    debug = False
    neu_branche: Branche = Branche(Name='misch_fhh', Herkunft="1", WZCode=154121200)
    alt_branche: Branche = Branche(Name=ctrl_begriff, Herkunft="Town&Country", WZCode='154121200')
    path = 'Meta.BranchenDetails.Extern'
    # path = 'Meta.BranchenDetails.Stichwoerter'
    # path = 'Meta.BranchenDetails.Homepage'

    
    switch_branchen_extern_stich_home(path=path, db='ZentralerFirmenstamm', col='ZentralerFirmenstamm',ctrl_begriff=ctrl_begriff, alt_branche=asdict(alt_branche), neu_branche=asdict(neu_branche), debug=debug)
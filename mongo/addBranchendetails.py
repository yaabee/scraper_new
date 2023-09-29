from mongo_connections import client_5, client_239

def rmBranchenDetailsExtern(zfids, rmBranchendetail):
  remove = client_239['ZentralerFirmenstamm']['ZentralerFirmenstamm'].update_many({'ZFID': {'$in': zfids}}, {'$pull': {'Meta.BranchenDetails.Extern': rmBranchendetail}})
  print(remove.modified_count)

def addBranchenDetailsExtern(zfids, addBranchendetail):
  insert = client_239['ZentralerFirmenstamm']['ZentralerFirmenstamm'].update_many({'ZFID': {'$in': zfids}}, {'$addToSet': {'Meta.BranchenDetails.Extern': addBranchendetail}})
  print(insert.modified_count)

def getZFIDS():
  cursor = client_5['GoogleApi']['google_Solaranlageninstallationsservice_Solaranlageninstallationsservice'].find({'ZFID': {'$exists': True}})
  return [x['ZFID'] for x in list(cursor)]

if __name__ == '__main__':
  zfids = getZFIDS()
  # rmBranchendetail = dict(Name='ausf_HKLS/13', Herkunft='Google', WZCode='154322100')
  # rmBranchenDetailsExtern(zfids, rmBranchendetail)
  addBranchendetail = dict(Name='ausf_HKLS/13', Herkunft='Google', WZCode=154322100)
  addBranchenDetailsExtern(zfids, addBranchendetail)


  
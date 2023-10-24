from YB_TYPES.custom_types import Branche

AUSF_HKLS = 154322100
AUSF_SOLAR = 154321101
AUSF_DACHDECKER = 154391101
AUSF_ELEKTRO = 154321100

MISCH_BAUTRAEGER = 154110000
MISCH_WOWI = 216811100
MISCH_GU = 216841500
MISCH_FHH = 154121200

PROJEKTENTWICKLER = 216841400
PLANER_HOCHBAU = 227111200
PLANER_ELEKTRO = 227132103
PLANER_HKLS = 227132102

BRAUEREI = 121105100
ENERGIEBERATER = 227491104
SOLARANLAGENANBIETER = 133511200

STADT_GEMEINDE = 248411103
STADTWERKE = 133513110



"""AUSFUEHRUNG"""
ausf_solar_1: Branche = Branche(Name='ausf_solar', Herkunft='1', WZCode=154321101)
ausf_solar_2: Branche = Branche(Name='ausf_solar', Herkunft='2', WZCode=154321101)

ausf_hkls_1: Branche = Branche(Name='ausf_hkls',Herkunft='1', WZCode=154322100)
ausf_hkls_2: Branche = Branche(Name='ausf_hkls',Herkunft='2', WZCode=154322100)
ausf_hkls_3: Branche = Branche(Name='ausf_hkls',Herkunft='3', WZCode=154322100)
ausf_hkls_4: Branche = Branche(Name='ausf_hkls',Herkunft='4', WZCode=154322100)
ausf_hkls_5: Branche = Branche(Name='ausf_hkls',Herkunft='5', WZCode=154322100)
ausf_hkls_6: Branche = Branche(Name='ausf_hkls',Herkunft='6', WZCode=154322100)
ausf_hkls_7: Branche = Branche(Name='ausf_hkls',Herkunft='7', WZCode=154322100)
ausf_hkls_8: Branche = Branche(Name='ausf_hkls',Herkunft='8', WZCode=154322100)
ausf_hkls_9: Branche = Branche(Name='ausf_hkls',Herkunft='1', WZCode=154322100)
ausf_hkls_10: Branche = Branche(Name='ausf_hkls',Herkunft='10', WZCode=154322100)
ausf_hkls_11: Branche = Branche(Name='ausf_hkls',Herkunft='11', WZCode=154322100)
ausf_hkls_12: Branche = Branche(Name='ausf_hkls',Herkunft='12', WZCode=154322100)
ausf_hkls_13: Branche = Branche(Name='ausf_hkls',Herkunft='13', WZCode=154322100)
ausf_hkls_14: Branche = Branche(Name='ausf_hkls',Herkunft='14', WZCode=154322100)
ausf_hkls_15: Branche = Branche(Name='ausf_hkls',Herkunft='14', WZCode=154322100)

ausf_dachdecker: Branche = Branche(Name='ausf_dachdecker', Herkunft='2', WZCode=154391101)

ausf_elektro: Branche = Branche(Name='ausf_elektro', Herkunft='1', WZCode=154321100)


"""PLANER"""

planer_elektro_1: Branche = Branche(Name='planer_elektro', Herkunft='1', WZCode=227132103)
planer_elektro_2: Branche = Branche(Name='planer_elektro', Herkunft='1', WZCode=227132103)
planer_elektro_3: Branche = Branche(Name='planer_elektro', Herkunft='1', WZCode=227132103)

planer_elektro_3: Branche = Branche(Name='planer_elektro', Herkunft='uf', WZCode=227132103)

planer_hkls_unternehmensflat: Branche = Branche(Name='planer_hkls', Herkunft='unternehmensflat', WZCode=227132102)
planer_hkls_1: Branche = Branche(Name='planer_hkls', Herkunft='1', WZCode=227132102)
planer_hkls_2: Branche = Branche(Name='planer_hkls', Herkunft='2', WZCode=227132102)



"""MISC"""

misch_bauträger_1: Branche = Branche(Name='misch_bauträger', Herkunft='1', WZCode=154110000)
misch_bauträger_2: Branche = Branche(Name='misch_bauträger', Herkunft='2', WZCode=154110000)
solaranalgenanbieter_1: Branche = Branche(Name='solaranlagenanbieter', Herkunft='1', WZCode=133511200)
solaranalgenanbieter_2: Branche = Branche(Name='solaranlagenanbieter', Herkunft='2', WZCode=133511200)

planer_hochbau_1: Branche = Branche(Name='planer_hochbau', Herkunft='1', WZCode=227111200)
planer_hochbau_2: Branche = Branche(Name='planer_hochbau', Herkunft='2', WZCode=227111200)
planer_hochbau_heinze: Branche = Branche(Name='planer_hochbau', Herkunft='heinze', WZCode=227111200)

brauerei: Branche = Branche(Name='brauerei', Herkunft='1', WZCode=121105100)

misch_fhh: Branche = Branche(Name='misch_fhh', Herkunft='1', WZCode=154121200)

misch_wowi: Branche = Branche(Name='misch_wowi',Herkunft='1', WZCode=216811100)

projektentwickler: Branche = Branche(Name='projektentwickler', Herkunft='1', WZCode=216841400)

misch_gu_gue: Branche = Branche(Name='misch_gu/gü', Herkunft='1', WZCode=216841500)

engergieberater: Branche = Branche(Name='engergieberater', Herkunft='1', WZCode=227491104)

stadt_gemeinde: Branche = Branche(Name='Stadt/Gemeinde', Herkunft='1', WZCode=248411103)
stadt_gemeinde: Branche = Branche(Name='Stadt/Gemeinde', Herkunft='at', WZCode=248411103)

# hallenbau: Branche = Branche(Name='Hallenbau', Herkunft='1',WZCode=)

stadtwerke: Branche = Branche(Name='stadtwerke', Herkunft='1', WZCode=133513110)


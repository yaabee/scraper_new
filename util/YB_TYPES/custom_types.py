from dataclasses import dataclass, field
from typing import Any, List, Union
from datetime import datetime

@dataclass
class PayloadDublettencheckOptions:
    returnDocument: bool = False

@dataclass
class PayloadDublettencheck:
    options: PayloadDublettencheckOptions = PayloadDublettencheckOptions()
    Firma: str = ''
    PLZ: str = ''
    Ort: str = ''
    Telefon: str = ''
    Straße: str = ''
    Email: str = ''
    Internet: str = ''
    Fax: str = 'xxxxx'

@dataclass
class Branche:
    Herkunft: str
    WZCode: int
    Name: str



@dataclass
class FirmaDaten:
    WohnbestandEigen: int = 0
    WohnbestandVerwaltet: int = 0
    HaeuserProJahr: int = 0
    WohnbestandGesamt: int = 0
    AnzahlMitarbeiter: int = 0
    AnzahlBetten: int = 0
    AnzahlZimmer: int = 0
    Hauptsitz: bool = False
    HauptsitzId: str = ""
    Schwerpunkte: List[Any] = field(default_factory=list)


@dataclass
class TKommunikationsarten:
    Typ: str = ""
    Nummer: str = ""
    LetzterKontaktAm: datetime = datetime.now()


@dataclass
class Location:
    type: str = ""
    coordinates: List[str] = field(default_factory=list)


@dataclass
class TStichwoerter:
    Herkunft: str = ""
    WZCode: int = 0
    Name: str = ""


@dataclass
class TBranchenDetails:
    Access: List[Any] = field(default_factory=list)
    Stichwoerter: List[TStichwoerter] = field(default_factory=list)
    Extern: List[Any] = field(default_factory=list)
    Homepage: List[Any] = field(default_factory=list)


@dataclass
class Gesperrt:
    Seit: datetime = datetime.now()
    Grund: str = ""


@dataclass
class TGespraechtermin:
    Zuletzt: str = ""
    GesamtAnzahl: int = 0


@dataclass
class HilfenDublettenabgleich:
    TokenAlsString: str = ""


@dataclass
class KeinKontaktErwuenscht:
    Seit: datetime = datetime.now()


@dataclass
class Pruefung:
    Fax: bool = False
    Telefon: bool = False
    Adresse: bool = False
    Email: bool = False
    Homepage: bool = False


@dataclass
class TAngelegt:
    Am: datetime = datetime.now()
    VonId: str = ""
    VonKuerzel: str = ""


@dataclass
class Meta:
    SchemaId: int = 0
    SchemaVersion: int = 0
    Version: int = 0
    LetzteSpeicherung: datetime = datetime.now()
    Angelegt: TAngelegt = TAngelegt()
    Geaendert = TAngelegt()
    IstInaktiv: bool = False
    Inaktiv = Gesperrt()
    Gesperrt = Gesperrt()
    IstGesperrt: bool = False
    Geprueft = TAngelegt()
    ZuPruefen: bool = False
    Pruefung = Pruefung()
    IstKeinKontaktErwuenscht: bool = False
    KeinKontaktErwuenscht = KeinKontaktErwuenscht()
    HilfenDublettenabgleich = HilfenDublettenabgleich()
    FirmaTokenized: List[str] = field(default_factory=list)
    FirmaTokenizedClean: List[str] = field(default_factory=list)
    APVorhanden: bool = False
    Exportierbar: bool = False
    BereitsTerminvormerkung: bool = False
    BereitsNettokontakt: bool = False
    BereitsGespraechstermin: bool = False
    Nettokontakt: TGespraechtermin = TGespraechtermin()
    Terminvormerkung: TGespraechtermin = TGespraechtermin()
    Gespraechtermin: TGespraechtermin = TGespraechtermin()
    ZielgruppeFalschGrund: List[Any] = field(default_factory=list)
    Branchen: List[int] = field(default_factory=list)
    BranchenDetails: TBranchenDetails = TBranchenDetails()
    FakeFirma: bool = False


@dataclass
class Firmenadresse:
    id: str = ""
    Firma: str = ""
    Firma2: str = ""
    Firmenname: str = ""
    FirmaId: int = 0
    StrassenId: str = ""
    Strassenname: str = ""
    Hausnummer: str = ""
    StrasseUndNr: str = ""
    PLZ: str = ""
    Ort: str = ""
    Email: str = ""
    Bundesland: str = ""
    Land: str = ""
    Telefon: str = ""
    TelefonRaw: str = ""
    FaxRaw: str = ""
    Fax: str = ""
    Location = Location()
    IstDublette: bool = False
    HatDublette: bool = False
    ZFID: str = ""
    DubletteZuId: str = ""
    Homepage: str = ""
    Kommunikationsarten: List[TKommunikationsarten] = field(default_factory=list)
    FirmaDaten = FirmaDaten()
    Meta = Meta()


import { Select, Tabs, SelectProps, Modal, Form } from "antd";
import "./index.css";
import MUIDataTable, { MUIDataTableOptions } from "mui-datatables";
import { useEffect, useRef, useState } from "react";
import "antd/dist/antd.css";

type TStatus = "Fehler" | "Offen" | "Erledigt" | "Format unbekannt";
interface ImportQuelle {
	_id: string;
	Anlagedatum: string;
	DsGespeichert: boolean;
	EmailBody: string;
	EmailFrom: string;
	EmailId: string;
	EmailSubject: string;
	Fehler: string;
	FeldUeberschriften: string[];
	FeldnamenUeberschrieben: boolean;
	FileHash: string;
	FilePath: string;
	FormatId: string;
	ImportiertAm: string;
	ProjectId: string;
	SourceType: string;
	Status: TStatus;
	UeberschriftHash: string;
	ZwischenFormatHash: string;
	Data?: any[];
}

interface ImportQuellDS {
	"0": string;
	"1": string;
	"2": string;
	"3": string;
	"4": string;
	"5": string;
	"6": string;
	"7": string;
	"8": string;
	"9": string;
	"10": string;
	"11": string;
	"12": string;
	"13": string;
	"14": string;
	"15": string;
	"16": string;
	"17": string;
	"18": string;
	"19": string;
	"20": string;
	"21": string;
	"22": string;
	"23": string;
	"24": string;
	"25": string;
	"26": string;
	"27": string;
	"28": string;
	"29": string;
	"30": string;
	"31": string;
	"32": string;
	"33": string;
	"34": string;
	"35": string;
	"36": string;
	"37": string;
	"38": string;
	"39": string;
	"40": string;
	"41": string;
	"42": string;
	"43": string;
	"44": string;
	"45": string;
	"46": string;
	"47": string;
	"48": string;
	"49": string;
	"50": string;
	"51": string;
	"52": string;
	"53": string;
	"54": string;
	"55": string;
	"56": string;
	"57": string;
	"58": string;
	"59": string;
	"60": string;
	"61": string;
	"62": string;
	"63": string;
	"64": string;
	"65": string;
	"66": string;
	"67": string;
	"68": string;
	"69": string;
	"70": string;
	"71": string;
	"72": string;
	"73": string;
	"74": string;
	"75": string;
	"76": string;
	"77": string;
	"78": string;
	"79": string;
	"80": string;
	"81": string;
	"82": string;
	"83": string;
	"84": string;
	"85": string;
	"86": string;
	"87": string;
	"88": string;
	"89": string;
	"90": string;
	"91": string;
	"92": string;
	"93": string;
	"94": string;
	"95": string;
	"96": string;
	"97": string;
	"98": string;
	"99": string;
	"100": string;
	"101": string;
	"102": string;
	"103": string;
	"104": string;
	"105": string;
	"106": string;
	"107": string;
	"108": string;
	"109": string;
	"110": string;
	"111": string;
	"112": string;
	"113": string;
	"114": string;
	"115": string;
	"116": string;
	"117": string;
	"118": string;
	"119": string;
	"120": string;
	"121": string;
	_id: string;
	_importQuellId: string;
	_rowId: number;
}

const dummyImportDS: ImportQuellDS = {
	"0": "1936564",
	"1": "Neubau einer Wohnanlage (192 WE)",
	"2": "Diskussion",
	"3": "40.000.000 €",
	"4": "beschränkt an Generalunternehmer/Generalübernehmer oder nach Einzelgewerken",
	"5": "64293",
	"6": "Darmstadt",
	"7": "Gräfenhäuser Str. 71",
	"8": "6411000",
	"9": "05.10.2022",
	"10": "",
	"11": "24.05.2019",
	"12": "",
	"13": "steht noch nicht fest",
	"14": "Auf dem Areal zwischen Gräfenhäuser Str. und Benzweg sollen in mehreren Gebäuden knapp 100 neue Wohnungen sowie ein Boardinghouse mit 92 Zimmern und Service-Apartments gebaut werden.<br/>Davon könnten 52 Wohneinheiten für den geförderten Wohnungsbau und 47 für den freien Markt oder an Studenten vermietet werden.<br/><br/>Das vorhaben bezogene Bebauungsplanverfahren läuft noch. Konkrete Termine und ein Baubeginn ist noch in Abstimmung, hier steht noch nichts fest. <br/><br/>Anfragen und Bewerbungen sind aufgrund des frühen Projektstadiums nicht erwünscht.",
	"15": "Begrünung und Bepflanzung",
	"16": "EMON Vermögensverwaltung GmbH",
	"17": "Marienburgstr. 27",
	"18": "64297",
	"19": "Darmstadt",
	"20": "06151 8609148",
	"21": "06151 8609149",
	"22": "info@emon-gmbh.de",
	"23": "",
	"24": "",
	"25": "",
	"26": "",
	"27": "",
	"28": "",
	"29": "",
	"30": "",
	"31": "",
	"32": "",
	"33": "",
	"34": "",
	"35": "",
	"36": "",
	"37": "",
	"38": "",
	"39": "",
	"40": "",
	"41": "",
	"42": "",
	"43": "",
	"44": "",
	"45": "",
	"46": "",
	"47": "",
	"48": "",
	"49": "",
	"50": "",
	"51": "EMON Vermögensverwaltung GmbH",
	"52": "Marienburgstr. 27",
	"53": "64297",
	"54": "Darmstadt",
	"55": "06151 8609148",
	"56": "06151 8609149",
	"57": "info@emon-gmbh.de",
	"58": "",
	"59": "",
	"60": "",
	"61": "",
	"62": "",
	"63": "",
	"64": "",
	"65": "",
	"66": "",
	"67": "",
	"68": "",
	"69": "",
	"70": "",
	"71": "",
	"72": "",
	"73": "",
	"74": "",
	"75": "",
	"76": "",
	"77": "",
	"78": "",
	"79": "",
	"80": "",
	"81": "",
	"82": "",
	"83": "",
	"84": "",
	"85": "",
	"86": "",
	"87": "",
	"88": "",
	"89": "",
	"90": "",
	"91": "",
	"92": "",
	"93": "",
	"94": "",
	"95": "",
	"96": "",
	"97": "",
	"98": "",
	"99": "",
	"100": "",
	"101": "",
	"102": "",
	"103": "",
	"104": "",
	"105": "",
	"106": "",
	"107": "",
	"108": "",
	"109": "",
	"110": "",
	"111": "",
	"112": "",
	"113": "",
	"114": "",
	"115": "",
	"116": "",
	"117": "",
	"118": "",
	"119": "",
	"120": "",
	"121":
		"Projektentwicklung: EMON Vermögensverwaltung GmbH, Marienburgstr. 27, 64297 Darmstadt, tel: 06151 8609148, fax: 06151 8609149, email: info@emon-gmbh.de, Planung Bebauungsplan: planquadrat Elfers, Geskes, Krämer, Architekten und Stadtplaner Part.G., Platz der deutschen Einheit 21, 64293 Darmstadt, tel: 06151 81969 0, fax: 06151 81969 99, email: architekten@planquadrat.com",
	_id: "6364dce5a06a86a4be9fcb3a",
	_importQuellId: "6364dce5a06a86a4be9fcb38",
	_rowId: 1,
};

const dummyImportQuelle: ImportQuelle[] = [
	{
		_id: "6364dce5a06a86a4be9fcb38",
		Anlagedatum: "2022-11-04T09:35:33.358Z",
		DsGespeichert: true,
		EmailBody: "",
		EmailFrom: "",
		EmailId: "",
		EmailSubject: "",
		Fehler: "",
		FeldUeberschriften: [],
		FeldnamenUeberschrieben: false,
		FileHash: "ccb69fd4d70f721373d97740f2684397",
		FilePath: "dtad.csv",
		FormatId: "",
		ImportiertAm: "1970-01-01T00:00:00.000Z",
		ProjectId: "",
		SourceType: "file",
		Status: "Format unbekannt",
		UeberschriftHash: "1b775331a12b1c5c06fc4b3eaba88a17",
		ZwischenFormatHash: "",
	},

	{
		_id: "635b02a44aab3e7b4296860a",
		Anlagedatum: "2022-10-27T22:13:56.360Z",
		Data: [],
		DsGespeichert: true,
		EmailBody: "",
		EmailFrom: "",
		EmailId: "",
		EmailSubject: "",
		Fehler: "IllegalOperationError: Channel closed",
		FeldUeberschriften: [],
		FeldnamenUeberschrieben: true,
		FileHash: "2e636007bfc5bcc5dd7843097e9ab359",
		FilePath: "dtad.csv",
		FormatId: "63492024aad07c3bb035df59",
		ImportiertAm: "1970-01-01T00:00:00.000Z",
		ProjectId: "",
		SourceType: "file",
		Status: "Erledigt",
		UeberschriftHash: "2de9b8311e237b1cc9b101d3ad47c294",
		ZwischenFormatHash: "0a7fd3a9e26ab38e859f2fc0424e2464",
	},
];

const getImportQuelle = async (): Promise<ImportQuelle[]> => {
	return new Promise((res) => {
		setTimeout(() => res(dummyImportQuelle), 1000);
	});
};

const filterByStatus = (
	status: string[],
	data: ImportQuelle[]
): ImportQuelle[] => {
	return data.filter((x) => status.includes(x.Status));
};

const App = () => {
	// const [ImportQuelleCache, setImportQuelleCache] = useState<ImportQuelle[]>(
	// 	[]
	// );
	// const [ShowImportQuellDS, setShowImportQuellDS] = useState<boolean>(false);
	// const [DataSource, setDataSource] = useState<ImportQuelle[]>([]);
	// const [status, setStatus] = useState<string[]>(["Erledigt"]);
	// const [CurrentQuellDS, setCurrentQuellDS] = useState<ImportQuellDS>();

	// useEffect(() => {
	// 	getImportQuelle().then((data) => {
	// 		setImportQuelleCache(data);
	// 		//get ImportQuellDS
	// 	});
	// 	setDataSource(filterByStatus(status, ImportQuelleCache));
	// }, [status, ImportQuelleCache]);

	// const columns = [
	// 	{
	// 		name: "FeldUeberschriften",
	// 		label: "FeldUeberschriften",
	// 		options: {
	// 			filter: false,
	// 			sort: true,
	// 		},
	// 	},
	// 	{
	// 		name: "UeberschriftHash",
	// 		label: "UeberschriftHash",
	// 		options: {
	// 			filter: false,
	// 			sort: true,
	// 		},
	// 	},
	// 	{
	// 		name: "Status",
	// 		label: "Status",
	// 		options: {
	// 			filter: false,
	// 			sort: true,
	// 		},
	// 	},
	// 	// {
	// 	// 	name: "Baubeginn",
	// 	// 	label: "Baubeginn",
	// 	// 	options: {
	// 	// 		filter: false,
	// 	// 		sort: true,
	// 	// 		// customBodyRender: (
	// 	// 		//   value: any,
	// 	// 		//   tableMeta: MUIDataTableMeta,
	// 	// 		//   updateValue: any,
	// 	// 		// ) => parseDate(value).toLocaleDateString('uk-UA'),
	// 	// 	},
	// 	// },
	// ];

	const options: MUIDataTableOptions = {
		selectableRowsHideCheckboxes: true,
		draggableColumns: { enabled: true },
		enableNestedDataAccess: ".",
		print: false,
		download: false,
		filter: false,
		viewColumns: false,
		onRowClick: function (rowData: string[]) {
			// () =>
			// 	new Promise((res) => res(dummyImportDS)).then((data: ImportQuellDS) => {
			// 		setCurrentQuellDS(data);
			// 		setShowImportQuellDS(true);
			// 		console.log(true);
			// 	});
			// setShowImportQuellDS(true);
			// console.log(ShowImportQuellDS);
		},
	};
	/**
	 * 
		Quellen mit Status (Filterbar nach Status: Offen, Fehler,
		Erledigt)
		Evlt. sollten wir hier die Fehlerhaften und Offenen standardmäßig
		anzeigen
		
		Suche mind. nach Name
		
		ImportQuelle auswählbar =&gt; Neuer View über den dann die
		ImportQullDS und die dazu 

		gehörenden Ergebnisse angezeigt werden. Damit können dann fehlerhafte
		DS geprüft, korrigiert und
		
		nochmal frei geschaltet werden. (Wenn DS freigeschlatet =&gt;
		ImportQuelle auch auf Offen setzen

		[evtl. sollten wird das als extra Dienst machen... nochmal drüber
		Nachdenken und absprechen])
	 * 
	 */

	/**
	  * 
		Liste von bekannten ImportZielen (Nur Aktive im Standard anzeigen,
		Inaktive zuschaltbar)
		Suche nach mind. nach Name
	  */

	/**
	 * 
		Liste von bekannten ImportFormaten (Nur Aktive im Standard anzeigen,
		Inaktive zuschaltbar)
		<br />
		Suche nach mind. nach Name
		*/

	const { Item } = Form;
	const layout = {
		labelCol: { span: 8 },
		wrapperCol: { span: 16 },
	};

	return (
		<div>
			<h2>Importe</h2>
			<Modal width={1000} title={"lass"} open={true}>
				<p>lass werden</p>
			</Modal>
		</div>
	);
};
export default function Root(props) {
	return <App />;
}

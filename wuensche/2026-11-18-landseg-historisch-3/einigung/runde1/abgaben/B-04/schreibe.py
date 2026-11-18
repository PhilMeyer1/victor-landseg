import json
A = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde1/auftraege-B/B-04/auftrag.json"
OUT = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde1/abgaben/B-04/einigung_abgabe.json"
auftrag = json.load(open(A, encoding="utf-8"))

GEH = ("Beide Stücke gehören zu derselben dunklen, lappig-unregelmäßigen Masse an der Ecke des Feldes "
       "nordwestlich der Kreuzung (Ausschnitt x 485–505, y 470–510), die die dunkle Saumlinie am Feldrand "
       "fortsetzt und scharf an die helle Straße grenzt; keine Bildkante an der Naht. Krone und eigener "
       "Schatten sind im Schwarz-Weiß nicht zu trennen, ein Gebäude als Schattenwerfer fehlt, darum die "
       "Elternklasse Gehölz für die ganze Kette 100218, 200100, 200115, 400037.")

E = {
    "r0c0:100218|r0c1:200100": ("gleich", "4", GEH),
    "r0c0:100218|r0c1:200115": ("gleich", "4", GEH),
    "r0c1:200115|r1c1:400037": ("gleich", "4", GEH),
    "r0c1:200100|r1c1:400037": ("gleich", "4", GEH),
    "r0c0:100229|r1c0:300004": ("gleich", "6.1",
        "Das Kernstück von 100229 (19 Bildpunkte, x 480–487, y 497–499) liegt gut 15 Bildpunkte nördlich der "
        "Straße in derselben mittelgrauen Feldfläche, die unterhalb der Naht als Feld 300004 weiterläuft; kein "
        "Helligkeitssprung, also kein Straßenrand, sondern Feld."),
    "r0c0:100218|r1c0:300004": ("grenze", None,
        "Gehölzmasse an der Feldecke gegen das mittelgraue Feld; an der Naht selbst liegt das untere Ende der "
        "dunklen Masse noch im Feldsegment 300004 (dessen Urteil nennt das Gehölz an der Ecke selbst), die "
        "Flächen sind aber verschieden."),
    "r1c0:300004|r1c1:400037": ("grenze", None,
        "Dunkle Gehölzmasse an der Kreuzung gegen das Feld 300004; die Naht schneidet durch das dunkle Ende, "
        "das fälschlich im Feldsegment steckt, die Segmente meinen aber Feld und Gehölz."),
    "r1c0:300004|r1c1:400064": ("grenze", None,
        "Helle Landstraße an der Kreuzung gegen das mittelgraue Feld; die Feldecke reicht an der Naht in die "
        "hellen Straßenpixel hinein, die Flächen sind aber klar verschieden."),
    "r1c0:300010|r1c1:400072": ("grenze", None,
        "Südkante der hellen Landstraße gegen den dunkleren, fleckigen Rain südlich davon; heller Belag und "
        "Saum sind verschiedene Flächen."),
    "r1c0:300004|r1c1:400072": ("grenze", None,
        "Das Feld 300004 liegt nördlich der Landstraße; an der Naht berührt nur ein abgetrenntes Stückchen von "
        "ihm südlich der Straße den dunklen Rain 400072 – das Stückchen gehört zum Rain, das Feldsegment als "
        "Ganzes aber nicht."),
    "r1c0:300027|r1c0:300032": ("grenze", None,
        "Unterkante des hellen, schmalen Feldwegs gegen das mittelgraue Feld darunter; weicher, aber sichtbarer "
        "Hell-Dunkel-Übergang zwischen Weg und Feld."),
    "r1c0:300027|r1c0:300066": ("grenze", None,
        "Ende des hellen Feldwegs an der Landstraße gegen die fleckige, mittelgraue Brache nördlich davon; die "
        "Segmente berühren sich nur an einem Punkt in der Einmündung."),
    "r1c0:300010|r1c0:300066": ("grenze", None,
        "Breites, sehr helles Band der Landstraße gegen die fleckige, mittelgraue Brache nördlich davon; klare "
        "Straßenkante."),
}

paare = []
for p in auftrag["paare"]:
    e, k, g = E[p["paar"]]
    paare.append({"paar": p["paar"], "entscheidung": e, "klasse": k, "grund": g})
assert len(paare) == len(E) == len(auftrag["paare"])

abgabe = {
    "schema": "landseg-einigung-abgabe/1", "fassung": "B", "buendel": "B-04",
    "bearbeiter": "agent:einigung-B-04:20261118i-r1",
    "paare": paare,
    "offen": [
        "Grenze statt Klasse: Feldsegment r1c0:300004 enthält an der Kreuzung (x 485–500, y 500–512) das untere "
        "Ende der Gehölzmasse und helle Straßenpixel und südlich der Landstraße (x 490–500, y 523–531) ein "
        "Stückchen des Rains; das klärt nur eine Grenzkorrektur in r1c0 (Paare 4, 10, 11, 13 bleiben deshalb grenze).",
        "Gehölz-Kette 100218/200100/200115/400037 nur als Elternklasse 4 gesetzt: Gebüsch (4.2) oder "
        "Baum/Gebüsch (4.4) und der Anteil Eigenschatten sind im Scan nicht sicher zu trennen.",
    ],
    "nicht_geprueft": [],
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(abgabe, f, ensure_ascii=False, indent=1)
print("ok", len(paare))

import json
E = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/naht-B"
m = json.load(open(E + "/_werk/mass.json", encoding="utf-8"))
kat = json.load(open("C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/kategorien-b.json", encoding="utf-8"))
name = {c["code"]: c["name"] for c in kat["classes"]}
BEST = {  # Nr -> Grund (Paar gilt nur an dieser einen Stelle)
 24: "Die Ecke der dunklen Hoffläche stößt an das helle Straßenband; die Kante kreuzt die Naht schräg und ist im Scan um einen Bildpunkt verwischt.",
 51: "Der Unterrand des dunklen Gartens kreuzt die Naht neben dem hellen Hofstreifen; echte, im Scan weiche Kante.",
 92: "Der linke Rand des schwarzen Schattenblocks kreuzt die Naht senkrecht; daneben liegt die mittelgraue Fläche, die Kante ist nur weich.",
 94: "Das rechte Ende des Schattenblocks stößt schräg an das helle Dach; Übergang dunkel–hell kreuzt die Naht, im Scan verwischt.",
 95: "Das linke Ende des hellen Langhausdachs stößt an den dunklen Schatten; die Dachkante kreuzt die Naht schräg und weich.",
 98: "Die Unterkante des hellen Langhausdachs liegt an dieser Stelle auf der Naht; der Bildpunkt darunter ist schon Übergangsgrau zum Hof.",
 132: "Die helle Hoffläche stößt an den dunklen schrägen Streifen; deren Kante kreuzt die Naht und ist im Scan um einen Bildpunkt verwischt.",
 136: "Der Unterrand des Schattens liegt an dieser Stelle auf der Naht, darunter beginnt die mittelgraue Straße; weiche, aber echte Kante.",
 148: "Der Unterrand der hellen Straße kreuzt die Naht schräg zum dunkleren Wegrain; der Übergang ist im Scan drei Bildpunkte breit verwischt.",
 151: "Der Oberrand des hellen Feldwegs kreuzt die Naht schräg zum dunklen Feld; echte Kante, an der Naht verwischt.",
 154: "Der Unterrand des hellen Feldwegs kreuzt die Naht schräg zum Feld; echte Kante, an der Naht verwischt.",
}
FELD = {65, 75, 150, 158, 160, 157}
GRUND_OFFEN = ("Fassung B hat je Teilkachel eigene IDs (100000er, 200000er, … Bereich, an keiner Naht eine gemeinsame ID), "
               "die Gegenseite steht in keinem Kontextrand, und eingriff kann keine fremde ID setzen")
verst, best, offen = [], [], []
for o in m:
    n, (a, b) = o["n"], o["ids"]
    ka, kb = o["kl"]
    if n in BEST:
        verst.append(dict(naht=o["naht"], ids=[a, b], art="ohne_kante", entscheidung="bestaetigt", teilkachel=None,
                          text=BEST[n]))
        best.append(dict(naht=o["naht"], ids=[a, b], grund=BEST[n]))
        continue
    if n in FELD:
        t = f"Dieselbe Ackerfläche mit gleichem Korn läuft ungebrochen über die Naht (Grauwert {o['gL']}/{o['gR']}); {a} ({ka} {name.get(ka,'')}) und {b} ({kb} {name.get(kb,'')}) sind ein Feld."
    elif o["d"] >= 30:
        t = (f"Grenze beider Seiten versetzt: an der Naht liegt auf beiden Seiten dieselbe Fläche (Grauwert {o['gL']}/{o['gR']}), "
             f"eine Seite hat sie dem Nachbarsegment zugeschlagen ({a} {ka} {name.get(ka,'')} gegen {b} {kb} {name.get(kb,'')}).")
    else:
        t = (f"Dieselbe Fläche ohne Kante auf beiden Seiten (Grauwert {o['gL']}/{o['gR']}, Kante höchstens {o['k']}); "
             f"{a} ({ka} {name.get(ka,'')}) und {b} ({kb} {name.get(kb,'')}) sind dort ein Segment.")
    if ka != kb:
        t += f" Klassen verschieden, bei der ID-Angleichung nach dem Bild zu entscheiden."
    verst.append(dict(naht=o["naht"], ids=[a, b], art="ohne_kante", entscheidung="offen", teilkachel=None, text=t))
    offen.append(f"Verstoß {n} (Naht {o['naht']}, {a}|{b}, {o['L']} Bildpunkte ab x {o['von'][0]}, y {o['von'][1]}): "
                 f"gleiche Fläche, braucht eine gemeinsame ID über die Naht; nicht angleichbar, weil {GRUND_OFFEN}.")
ab = {"runde": 1, "bearbeiter": "agent:naht-B:20261118i", "verstoesse": verst, "naht_bestaetigt": best,
      "einheiten": [], "offen": offen,
      "nicht_geprueft": ["Klassenwahl für die offenen Paare (bei 132 von 169 Verstößen tragen die Seiten verschiedene Klassen): erst nach einer gemeinsamen ID sinnvoll.",
                         "Lage der Grenzen abseits der Naht (nur die Nahtstellen ±24 Bildpunkte angesehen)."]}
json.dump(ab, open(E + "/naht_abgabe.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
import collections
print(collections.Counter(v["entscheidung"] for v in verst), len(best))

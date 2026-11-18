"""Baut naht_abgabe.json, den Probe-Auftrag zusammentragen.json und entscheidungen.json (Bildtexte)."""
import json
from pathlib import Path

WERK = Path(__file__).parent
ERG = WERK.parent
C = Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste")
BEARBEITER = "agent:naht-C:20261118i"

GRUND_ID = ("IDs sind je Teilkachel vergeben (100xxx, 200xxx, 300xxx, 400xxx); die ID der Gegenseite steht "
            "in keinem Kontextrand, Angleichen mit eingriff verschmelzen ist daher nicht möglich")

# bestätigte echte Grenzen: (naht, a, b) -> Grund
BESTAETIGT = {
    ("r0c0|r0c1", 100042, 200004): "Helles Dach endet 1–2 Bildpunkte links der Naht, rechts liegt dunkle Fläche; echte Dachkante knapp außerhalb des Prüfbands.",
    ("r0c0|r0c1", 100111, 200042): "Dunkle Hoffläche gegen helle Straße; die Kante kreuzt die Naht an dieser Stelle schräg.",
    ("r0c0|r0c1", 100215, 200047): "Heller Straßenrand gegen dunkles Dach; die Kante kreuzt die Naht schräg.",
    ("r0c0|r0c1", 100218, 200100): "Dunkle Gehölz- bzw. Schattenfläche gegen hellen Weg; die Kante liegt 2–3 Bildpunkte rechts der Naht.",
    ("r0c0|r1c0", 100223, 300002): "Rand des Feldrains gegen den Acker; die Kante kreuzt die Naht.",
    ("r0c0|r1c0", 100154, 300080): "Acker gegen den dunklen Streifen; dessen Oberkante kreuzt die Naht schräg.",
    ("r0c0|r1c0", 100224, 300080): "Graue Ackerfläche gegen den dunklen Streifen; dessen Oberkante liegt auf der Naht.",
    ("r0c0|r1c0", 100224, 300075): "Graue Fläche gegen das dunkle Gebäude; dessen Oberkante liegt auf der Naht, unscharf.",
    ("r0c0|r1c0", 100220, 300075): "Heller offener Boden gegen das dunkle Gebäude; dessen Oberkante liegt auf der Naht, unscharf.",
    ("r0c0|r1c0", 100225, 300006): "Dunkler Gehölzstreifen gegen Acker; die Kante kreuzt die Naht.",
    ("r0c0|r1c0", 100195, 300004): "Dunkler Acker gegen hellen Acker; die Schlaggrenze kreuzt die Naht schräg.",
    ("r0c0|r1c0", 100229, 300004): "Dunkle Fläche gegen hellen Acker; die Kante kreuzt die Naht.",
    ("r0c0|r1c0", 100219, 300079): "Acker gegen dunkles Gehölz; die Gehölzkante kreuzt die Naht schräg.",
    ("r0c1|r1c1", 200100, 400037): "Heller Weg gegen dunkles Gehölz; die Gehölzkante kreuzt die Naht steil, 1–3 Bildpunkte daneben.",
    ("r0c1|r1c1", 200121, 400006): "Helles Dach gegen den dunklen Gebäudeblock; Dachecken liegen auf der Naht.",
    ("r0c1|r1c1", 200063, 400011): "Dunkler Fleck (Baum oder Schatten) gegen graue Straße; die Kante kreuzt die Naht.",
    ("r0c1|r1c1", 200063, 400042): "Dunkle Gasse gegen helles Dach; die Kante kreuzt die Naht.",
    ("r0c1|r1c1", 200111, 400042): "Ecke des hellen Dachs an der dunklen Gasse; die Kante kreuzt die Naht.",
    ("r0c1|r1c1", 200124, 400029): "Rand des dunklen Flecks gegen graue Straße; die Kante kreuzt die Naht.",
    ("r1c0|r1c1", 300010, 400072): "Unterkante der hellen Straße gegen dunklen Streifen; die Kante kreuzt die Naht schräg.",
    ("r1c0|r1c1", 300011, 400110): "Dunkler Acker gegen helle Fläche an der Straße; die Kante kreuzt die Naht schräg.",
    ("r1c0|r1c1", 300030, 400118): "Unterkante der hellen Straße gegen den dunklen Acker; die Kante kreuzt die Naht.",
    ("r1c0|r1c1", 300023, 400118): "Heller Feldrain gegen dunklen Acker; die Kante läuft steil an der Naht entlang.",
}

# offene Stellen: (naht, a, b) -> was das Bild zeigt
OFFEN = {
    ("r0c0|r0c1", 100032, 200004): "Dunkle Hof- bzw. Schattenfläche zwischen Dächern läuft ohne Kante über die Naht.",
    ("r0c0|r0c1", 100056, 200004): "Dach läuft in den groben Siedlungsblock rechts weiter.",
    ("r0c0|r0c1", 100063, 200004): "Graue Hoffläche läuft ohne Kante über die Naht.",
    ("r0c0|r0c1", 100070, 200004): "Dach läuft in den groben Siedlungsblock rechts weiter.",
    ("r0c0|r0c1", 100081, 200004): "Dach läuft in den groben Siedlungsblock rechts weiter.",
    ("r0c0|r0c1", 100092, 200004): "Straßenstreifen läuft weiter; rechts beginnt die Straße einige Bildpunkte tiefer.",
    ("r0c0|r0c1", 100092, 200031): "Straße läuft ohne Kante über die Naht.",
    ("r0c0|r0c1", 100030, 200031): "Straße läuft ohne Kante über die Naht.",
    ("r0c0|r0c1", 100030, 200042): "Straße läuft ohne Kante über die Naht.",
    ("r0c0|r0c1", 100030, 200043): "Straße läuft weiter; 200043 ist ein Splitter in der Straße.",
    ("r0c0|r0c1", 100112, 200047): "Dach bzw. Hof läuft in den groben Siedlungsblock 200047 weiter.",
    ("r0c0|r0c1", 100111, 200047): "Dunkle Hoffläche läuft in den Siedlungsblock 200047 weiter.",
    ("r0c0|r0c1", 100128, 200047): "Dach läuft in den Siedlungsblock 200047 weiter.",
    ("r0c0|r0c1", 100143, 200047): "Dach bzw. Hof läuft in den Siedlungsblock 200047 weiter.",
    ("r0c0|r0c1", 100144, 200047): "Helles Dach läuft in den Siedlungsblock 200047 weiter.",
    ("r0c0|r0c1", 100153, 200047): "Dach läuft in den Siedlungsblock 200047 weiter.",
    ("r0c0|r0c1", 100165, 200047): "Dach bzw. Hof läuft in den Siedlungsblock 200047 weiter.",
    ("r0c0|r0c1", 100176, 200047): "Dächer und Höfe laufen über 170 Bildpunkte in den Siedlungsblock 200047 weiter.",
    ("r0c0|r0c1", 100209, 200047): "Helle Dachfläche läuft weiter (links Gehölz 4.2, rechts Siedlung 1).",
    ("r0c0|r0c1", 100211, 200047): "Dunkle Fläche läuft weiter (links Gehölz 4.2, rechts Siedlung 1).",
    ("r0c0|r0c1", 100215, 200106): "Straße läuft ohne Kante über die Naht.",
    ("r0c0|r0c1", 100198, 200106): "Straße läuft ohne Kante über die Naht.",
    ("r0c0|r0c1", 100198, 200081): "Straße läuft ohne Kante über die Naht.",
    ("r0c0|r0c1", 100218, 200115): "Dunkle Fläche (Baum oder Schatten) läuft weiter (links 4.2, rechts 1.1.1).",
    ("r0c0|r1c0", 100202, 300001): "Helle Grünfläche mit Baumkronen läuft weiter (links 3, rechts 2).",
    ("r0c0|r1c0", 100221, 300001): "Feldrain-Streifen läuft weiter (links 3.4, rechts 2).",
    ("r0c0|r1c0", 100223, 300001): "Feldrain-Streifen läuft weiter (links 3.4, rechts 2).",
    ("r0c0|r1c0", 100154, 300002): "Acker läuft über 251 Bildpunkte ohne Kante über die Naht.",
    ("r0c0|r1c0", 100225, 300080): "Dunkle Fläche läuft einige Bildpunkte über die Naht weiter.",
    ("r0c0|r1c0", 100195, 300006): "Acker läuft ohne Kante über die Naht.",
    ("r0c0|r1c0", 100219, 300004): "Heller Acker läuft ohne Kante über die Naht.",
    ("r0c0|r1c0", 100228, 300004): "Heller Acker läuft ohne Kante über die Naht.",
    ("r0c0|r1c0", 100229, 300079): "Dunkle Gehölzfläche läuft weiter (links 1.2, rechts 4.2).",
    ("r0c0|r1c0", 100218, 300079): "Dunkles Gehölz läuft ohne Kante über die Naht.",
    ("r0c1|r1c1", 200115, 400037): "Dunkle Fläche läuft weiter (oben 1.1.1, unten 4.2).",
    ("r0c1|r1c1", 200081, 400003): "Straße läuft ohne Kante über die Naht.",
    ("r0c1|r1c1", 200081, 400046): "Straße läuft weiter; Grenze 400003/400046 trifft hier die Naht.",
    ("r0c1|r1c1", 200126, 400046): "Straße läuft ohne Kante über die Naht.",
    ("r0c1|r1c1", 200047, 400039): "Graue Hoffläche läuft ohne Kante über die Naht.",
    ("r0c1|r1c1", 200047, 400056): "Graue Hoffläche läuft weiter; 400056 reicht über das helle Dach hinaus bis an die Naht.",
    ("r0c1|r1c1", 200047, 400054): "Dunkles Gebäude läuft ohne Kante über die Naht.",
    ("r0c1|r1c1", 200047, 400006): "Dächer und Höfe laufen in den Gebäudeblock 400006 weiter.",
    ("r0c1|r1c1", 200121, 400047): "Helles Dach reicht über die Naht; 400047 ist sein Randsplitter.",
    ("r0c1|r1c1", 200121, 400048): "Helles Dach reicht 3–5 Bildpunkte über die Naht in 400048.",
    ("r0c1|r1c1", 200113, 400035): "Dunkles Dach läuft ohne Kante über die Naht.",
    ("r0c1|r1c1", 200120, 400009): "Straße läuft ohne Kante über die Naht.",
    ("r0c1|r1c1", 200120, 400051): "Straße läuft ohne Kante über die Naht.",
    ("r0c1|r1c1", 200122, 400051): "Graue Fläche läuft ohne Kante über die Naht.",
    ("r0c1|r1c1", 200122, 400033): "Graue Fläche läuft ohne Kante über die Naht.",
    ("r0c1|r1c1", 200097, 400033): "Dächer und Höfe laufen ohne Kante über die Naht.",
    ("r0c1|r1c1", 200097, 400053): "Dach läuft ohne Kante über die Naht.",
    ("r0c1|r1c1", 200097, 400049): "Dach läuft ohne Kante über die Naht.",
    ("r0c1|r1c1", 200097, 400045): "Dach bzw. Hof läuft ohne Kante über die Naht.",
    ("r0c1|r1c1", 200095, 400011): "Straße läuft ohne Kante über die Naht.",
    ("r0c1|r1c1", 200063, 400050): "Graue Fläche läuft ohne Kante über die Naht.",
    ("r0c1|r1c1", 200112, 400042): "Dach bzw. Hof läuft ohne Kante über die Naht.",
    ("r0c1|r1c1", 200111, 400041): "Helles Dach läuft ohne Kante über die Naht.",
    ("r0c1|r1c1", 200124, 400055): "Dunkler Fleck läuft in den dunklen Streifen weiter; ein Teil der Strecke ist graue Fläche gegen dunkel.",
    ("r0c1|r1c1", 200110, 400029): "Straße läuft ohne Kante über die Naht.",
    ("r0c1|r1c1", 200123, 400029): "Straße läuft ohne Kante über die Naht.",
    ("r0c1|r1c1", 200110, 400057): "Am rechten Rand des Ausschnitts, grau in grau; nicht sicher entscheidbar.",
    ("r0c1|r1c1", 200125, 400057): "Am rechten Rand des Ausschnitts, grau in grau; nicht sicher entscheidbar.",
    ("r1c0|r1c1", 300079, 400037): "Dunkles Gehölz läuft ohne Kante über die Naht.",
    ("r1c0|r1c1", 300079, 400064): "Helle Straße läuft weiter; links liegt sie hier fälschlich in 300079 (Gehölz).",
    ("r1c0|r1c1", 300010, 400064): "Helle Straße läuft ohne Kante über die Naht.",
    ("r1c0|r1c1", 300079, 400072): "Dunkler Streifen unter der Straße läuft ohne Kante über die Naht.",
    ("r1c0|r1c1", 300011, 400078): "Acker läuft über 146 Bildpunkte ohne Kante über die Naht.",
    ("r1c0|r1c1", 300024, 400110): "Helle Straße läuft weiter (rechts als 6.6).",
    ("r1c0|r1c1", 300030, 400110): "Helle Straße läuft weiter (links 1.2, rechts 6.6).",
    ("r1c0|r1c1", 300035, 400137): "Dunkler länglicher Gegenstand läuft weiter (links 1.1.2, rechts 4.2).",
    ("r1c0|r1c1", 300029, 400136): "Graue Fläche unter der Straße läuft ohne Kante über die Naht.",
    ("r1c0|r1c1", 300029, 400118): "Acker läuft über 217 Bildpunkte ohne Kante über die Naht.",
    ("r1c0|r1c1", 300023, 400202): "Feldrain läuft weiter (links 3.4, rechts 2).",
    ("r1c0|r1c1", 300023, 400209): "Feldrain läuft weiter (links 3.4, rechts 2).",
    ("r1c0|r1c1", 300023, 400211): "Feldrain läuft weiter (links 3.4, rechts 2).",
    ("r1c0|r1c1", 300023, 400176): "Feldrain trifft schräg auf 400176, das Feldrain und Acker zugleich umfasst; nicht sicher entscheidbar.",
    ("r1c0|r1c1", 300026, 400176): "Acker läuft ohne Kante über die Naht.",
}

verst = json.load(open(WERK / "streifen" / "verstoesse.json", encoding="utf-8"))
liste, ent, offen, gesehen = [], {}, [], set()
for v in verst:
    key = (v["naht"], *v["ids"])
    if key in BESTAETIGT:
        e, text = "bestaetigt", BESTAETIGT[key]
    elif key in OFFEN:
        e, text = "offen", OFFEN[key]
    else:
        raise SystemExit(f"keine Entscheidung für {key}")
    liste.append({"naht": v["naht"], "ids": v["ids"], "art": v["art"], "entscheidung": e, "teilkachel": None,
                  "text": text})
    ent[v["n"]] = ("bestätigt (echte Grenze)" if e == "bestaetigt" else "offen") + ": " + text
    if e == "offen" and key not in gesehen:
        n = [x["n"] for x in verst if (x["naht"], *x["ids"]) == key]
        offen.append(f"Naht {key[0]}, {key[1]} | {key[2]} (Verstoß {', '.join(map(str, n))}): {text} "
                     f"Gleiche Fläche, aber {GRUND_ID}; braucht globale IDs (Vorstufe mit 'ausgang' bzw. "
                     f"gemeinsamer Nummerierung) oder einen Eingriff, der eine fremde ID übernimmt.")
    gesehen.add(key)

for key in set(BESTAETIGT) | set(OFFEN):
    if key not in gesehen:
        raise SystemExit(f"Entscheidung ohne Verstoß: {key}")

bestaetigt = [{"naht": k[0], "ids": [k[1], k[2]], "grund": g} for k, g in BESTAETIGT.items()]
abgabe = {"runde": 1, "bearbeiter": BEARBEITER, "verstoesse": liste, "naht_bestaetigt": bestaetigt,
          "einheiten": [], "offen": offen,
          "nicht_geprueft": [
              "Klassenkonflikte zwischen gleichen Flächen beiderseits der Naht (z. B. 100202 Grünland | 300001 Acker, "
              "300030 Straße | 400110 offener Boden): Sache der Einigung, hier nicht entschieden.",
              "Lage der Grenzen abseits der Kerngrenzen (nur die gemeldeten Stellen an der Naht angesehen)."]}
json.dump(abgabe, open(ERG / "naht_abgabe.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(ent, open(WERK / "entscheidungen.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)

auftrag = json.load(open(C / "zusammentragen.json", encoding="utf-8"))
rel = "../../../daten/landseg/H0/c-feste-liste/"
probe = dict(auftrag)
probe["manifest"] = "../../../daten/landseg/H0/manifest.json"
probe["einheiten"] = [dict(e, labels=rel + e["labels"], segmente=rel + e["segmente"]) for e in auftrag["einheiten"]]
probe["naht_bestaetigt"] = list(auftrag.get("naht_bestaetigt", [])) + bestaetigt
probe["ziel"] = "probe"
json.dump(probe, open(ERG / "zusammentragen.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("bestätigt Paare", len(bestaetigt), "Verstöße", sum(1 for x in liste if x["entscheidung"] == "bestaetigt"),
      "offen Paare", len(offen), "Verstöße", sum(1 for x in liste if x["entscheidung"] == "offen"))

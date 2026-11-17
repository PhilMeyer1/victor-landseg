"""urteil.json aus einer Datendatei (daten_vN.py) schreiben.
Aufruf: PY schreibe.py <ergebnisordner> <viertel>  (liest <ergebnisordner>/daten.py)"""
import json
import runpy
import sys
from pathlib import Path

out = Path(sys.argv[1])
v = sys.argv[2]
VB = f"C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r0c1/{v}/"
OUT = str(out).replace("\\", "/") + "/"
D = runpy.run_path(str(out / "daten.py"))

MERKMAL = {
    ("Gebäude", "grob"): (None, "Dachfläche mit harten, geraden Kanten und Schattenwurf"),
    ("Befestigte Fläche", "grob"): (None, "glatte graue oder helle Fläche ohne Bewuchs, gerade Ränder"),
    ("Gehölz", "grob"): (None, "Kronen mit Textur aus Licht und Schatten, dunkelgrün"),
    ("Grasland", "grob"): (None, "gleichmäßig grüne, feinkörnige Fläche ohne Kronen"),
    ("Offener Boden", "grob"): (None, "beige bis braune Fläche ohne geschlossenen Bewuchs"),
    ("Wasser", "grob"): (None, "glatte blaue Fläche"),
    ("Schatten", "grob"): (None, "sehr dunkle Fläche, Untergrund nicht erkennbar"),
    ("Wohnhaus", "mittel"): ("Gebäude", "großes Dach mit Schornsteinen, Dachfenstern, Garten rundum"),
    ("Wohnhaus", "fein"): ("Wohnhaus", "wie mittlere Ebene"),
    ("Nebengebäude", "mittel"): ("Gebäude", "kleines Dach, oft Flachdach, neben dem Wohnhaus oder an der Zufahrt"),
    ("Garage", "fein"): ("Nebengebäude", "kleines Flachdach an Zufahrt oder Straße"),
    ("Anbau", "fein"): ("Nebengebäude", "niedrigeres Dach direkt am Wohnhaus, andere Farbe"),
    ("Gartenhütte", "fein"): ("Nebengebäude", "sehr kleines Dach im Garten, wenige Quadratmeter"),
    ("Kleingartenhütte", "fein"): ("Nebengebäude", "kleines Hüttendach in einer Kleingarten-Parzelle"),
    ("Fassade", "fein"): ("Wohnhaus", "schmaler dunkler Streifen an einer Dachkante (Hauswand schräg gesehen oder Schatten)"),
    ("Straße", "mittel"): ("Befestigte Fläche", "langes Band mit gleichmäßigem Belag"),
    ("Asphaltstraße", "fein"): ("Straße", "dunkelgraues Band"),
    ("Betonstraße", "fein"): ("Straße", "helles graues Band (Beton oder heller Belag)"),
    ("Straßenrand", "fein"): ("Straße", "schmaler heller Streifen an der Fahrbahnkante (Randstein, Gehsteig)"),
    ("Hof und Zufahrt", "mittel"): ("Befestigte Fläche", "graue oder helle Fläche zwischen Straße und Gebäude"),
    ("Einfahrt", "fein"): ("Hof und Zufahrt", "befestigte Fläche vor Garage oder Haus"),
    ("Vorplatz im Schatten", "fein"): ("Hof und Zufahrt", "befestigte Fläche im Schlagschatten eines Gebäudes, Fortsetzung erkennbar"),
    ("Weg", "mittel"): ("Befestigte Fläche", "schmales helles Band"),
    ("Gartenweg", "fein"): ("Weg", "schmaler heller Streifen im Garten"),
    ("Feldweg", "fein"): ("Weg", "schmale helle Spur am Feld- oder Wiesenrand"),
    ("Terrasse", "mittel"): ("Befestigte Fläche", "helle Plattenfläche direkt am Haus oder Pool"),
    ("Terrasse", "fein"): ("Terrasse", "wie mittlere Ebene"),
    ("Baum", "mittel"): ("Gehölz", "runde Kronen mit Schatten"),
    ("Einzelbaum", "fein"): ("Baum", "eine einzelne runde Krone"),
    ("Baumgruppe", "fein"): ("Baum", "mehrere ineinander greifende Kronen"),
    ("Gebüsch", "mittel"): ("Gehölz", "niedrigere, kleinteilige Kronen, Hecken und Sträucher"),
    ("Strauch", "fein"): ("Gebüsch", "kleine einzelne Krone, wenige Meter"),
    ("Hecke", "fein"): ("Gebüsch", "schmales, langes Gehölzband an einer Grundstücksgrenze"),
    ("Gartengehölz", "fein"): ("Gebüsch", "Gemenge aus Sträuchern, kleinen Bäumen und Beeten im Garten"),
    ("Gehölzbestand", "mittel"): ("Gehölz", "große geschlossene Fläche aus vielen Kronen"),
    ("Gehölzbestand", "fein"): ("Gehölzbestand", "wie mittlere Ebene"),
    ("Rasen", "mittel"): ("Grasland", "kurzes, gleichmäßiges Grün im Garten"),
    ("Rasen", "fein"): ("Rasen", "wie mittlere Ebene"),
    ("Wiese", "mittel"): ("Grasland", "größere Grasfläche, etwas ungleichmäßiger als Rasen"),
    ("Wiese", "fein"): ("Wiese", "wie mittlere Ebene"),
    ("Randstreifen", "mittel"): ("Grasland", "schmaler bewachsener Streifen an Straße, Weg oder Feld"),
    ("Randstreifen", "fein"): ("Randstreifen", "wie mittlere Ebene"),
    ("Feld", "mittel"): ("Offener Boden", "große beige-braune Fläche mit parallelen Bearbeitungsstreifen"),
    ("Feld gemäht", "fein"): ("Feld", "beige Fläche mit dunkleren Schwaden-Streifen entlang der Hanglinie"),
    ("Gartenboden", "mittel"): ("Offener Boden", "beiger bis grauer Boden, Kies oder Sand im Garten"),
    ("Gartenboden", "fein"): ("Gartenboden", "wie mittlere Ebene"),
    ("Beet", "fein"): ("Gartenboden", "kleine Fläche mit Reihen oder Erde im Garten"),
    ("Schwimmbecken", "mittel"): ("Wasser", "blaue Fläche mit hellem Rand"),
    ("Aufstellpool", "fein"): ("Schwimmbecken", "runde blaue Fläche mit heller Wand"),
    ("Pool", "fein"): ("Schwimmbecken", "rechteckige blaue Fläche mit Rand"),
    ("Poolabdeckung", "fein"): ("Schwimmbecken", "glatte Fläche über einem Becken"),
    ("Schlagschatten", "mittel"): ("Schatten", "dunkle Fläche neben Gebäude oder Baum auf der Nordseite"),
    ("Schlagschatten", "fein"): ("Schlagschatten", "wie mittlere Ebene"),
}

segs, used = [], []
for t in D["SEG"]:
    sid, kh, was, urt, (g, m, f), sicher, punkte, bilder = t
    for name, eb in ((g, "grob"), (m, "mittel"), (f, "fein")):
        if (name, eb) not in used:
            used.append((name, eb))
    segs.append({
        "id": sid, "klasse_heute": kh, "was_ist_es": was, "urteil": urt, "klasse_vorschlag": None,
        "klasse_frei": {"grob": g, "mittel": m, "fein": f}, "sicher": sicher,
        "punkte": [{"nr": k + 1, "art": a, "text": tx, "flaeche_px": fl} for k, (a, tx, fl) in enumerate(punkte)],
        "bilder": [(OUT + b[4:]) if b.startswith("OUT:") else (VB + b) for b in bilder],
    })
kf = []
for name, eb in used:
    if (name, eb) not in MERKMAL:
        raise SystemExit(f"Merkmal fehlt: {name} {eb}")
    el, mk = MERKMAL[(name, eb)]
    kf.append({"name": name, "ebene": eb, "eltern": el, "merkmal": mk})
U = {
    "teilkachel": "r0c1", "viertel": v, "bearbeiter": f"urt-b-r0c1-{v}",
    "bilder_angesehen": {
        "uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/T0.png",
                       "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/ganz/r0c1/ganz_nummern.jpg",
                       "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/ganz/r0c1/ganz_roh.jpg"]
                      + [VB + b for b in D["UEB"]],
        "nah": [VB + b for b in D["NAH"]] + [OUT + b for b in D["EIGEN"]],
    },
    "segmente": segs, "naht": D["NAHT"], "unsicher": D["UNSICHER"], "nicht_geprueft": D["NICHT"],
    "offen": D["OFFEN"], "klassen_frei": kf,
}
(out / "urteil.json").write_text(json.dumps(U, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(segs), "Segmente,", sum(1 for s in segs if s["urteil"] == "nicht_sauber"), "nicht sauber,",
      sum(1 for s in segs if not s["sicher"]), "unsicher,", sum(len(s["punkte"]) for s in segs), "Punkte")

"""Schreibt urteil.json und konfig.json für r1c0/v4 (Fassung B) aus den Urteilen unten."""
import json
from pathlib import Path

V = "v4"
O = Path(f"C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r1c0/{V}")
Q = f"C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r1c0/{V}/"
T0 = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/T0.png"
GZ = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/ganz/r1c0/"
UN, UK = Q + "uebersicht_nummern.jpg", Q + "uebersicht_kontrast.jpg"
N = {k: Q + f"{k}.jpg" for k in ("nah1_nummern", "nah2_nummern", "nah4_nummern", "nah4_roh")}
K1 = str(O / "kontrast_1.jpg")

SCH = {"grob": "Schatten", "mittel": "Schatten auf Gehölz", "fein": "Schatten auf Wald"}
WALD = {"grob": "Gehölz", "mittel": "Wald", "fein": "Wald"}
nr = 0


def p(art, x, y, text, fl=None):
    global nr
    nr += 1
    return {"nr": nr, "art": art, "text": f"{text} ({x}/{y})", "flaeche_px": fl, "_xy": [x, y]}


S = [
    (300048, "0.2", "Dunkle Fläche im Wald oben links mit nur schwacher Kronenstruktur, Grenze auf der Hell-dunkel-Kante: Schatten auf Wald.",
     SCH, False, [],
     [UN, UK, N["nah1_nummern"]]),
    (300059, "0.2", "Kleine dunkle Lücke zwischen beleuchteten Kronen: Schatten im Kronendach.",
     SCH, False, [],
     [UN, UK, N["nah2_nummern"]]),
    (300063, "0.2", "Dunkle, hakenförmige Fläche mitten im Wald, umschließt eine beleuchtete Krone; fast strukturlos: Schatten auf Wald.",
     SCH, False, [],
     [UN, UK, N["nah2_nummern"], N["nah4_nummern"], N["nah4_roh"]]),
    (300076, "0.2", "Dunkle Fläche am Südrand mit zwei beleuchteten Kronen (79, 80) darin; setzt sich ohne Kante in 72 fort.",
     SCH, False,
     [p("verschmelzen", 545, 533, "Grenze zu 72 liegt in durchgehend dunkler Fläche ohne Bildkante; 72 und 76 verschmelzen", None)],
     [UN, UK, N["nah4_nummern"], N["nah4_roh"], K1]),
    (300079, "0.2", "Beleuchtete, gelbgrüne Baumkrone inmitten des Schattens 76, zusammen mit 80 eine Krone.",
     WALD, True,
     [p("klasse", 532, 548, "beleuchtete Krone, kein Schatten", 140),
      p("verschmelzen", 528, 552, "79 und 80 sind eine Krone ohne Kante dazwischen; zusammenlegen, Klasse Wald", 140)],
     [UN, UK, N["nah4_nummern"], N["nah4_roh"], K1]),
    (300072, "0.2", "Dunkle Fläche am rechten Kernrand mit bläulichen Kronenlichtern und einer rötlichen Krone im Nordwestteil; reicht nach rechts aus dem Kern.",
     SCH, False,
     [p("verschmelzen", 548, 528, "mit 76 verschmelzen, Grenze ohne Bildkante", None)],
     [UN, UK, N["nah4_nummern"], N["nah4_roh"], K1]),
    (300077, "0.2", "Dunkle Fläche am unteren Kernrand, fast strukturlos: Schatten auf Wald; reicht nach unten aus dem Kern.",
     SCH, False, [],
     [UN, UK, N["nah4_nummern"], N["nah4_roh"]]),
    (300080, "4.1", "Beleuchtete Krone im Schatten 76, gleiche Krone wie 79.",
     WALD, True,
     [p("verschmelzen", 521, 554, "mit 79 zu einer Krone verschmelzen", 144)],
     [UN, N["nah4_nummern"], N["nah4_roh"], K1]),
]

verschmelzen = {300079: 300080, 300072: 300076}
namen = {300048: "Schatten auf Wald", 300059: "Schatten", 300063: "Schatten auf Wald",
         300076: "Schatten auf Wald", 300077: "Schatten auf Wald", 300080: "Wald"}

segmente, punkte = [], []
for sid, heute, was, kf, sicher, pk, bilder in S:
    for q in pk:
        punkte.append([q["nr"], q["_xy"][0], q["_xy"][1], f"{sid % 100000}: {q['text'].rsplit(' (', 1)[0]}"])
        del q["_xy"]
    segmente.append({"id": sid, "klasse_heute": heute, "was_ist_es": was,
                     "urteil": "nicht_sauber" if pk else "sauber", "klasse_vorschlag": None,
                     "klasse_frei": kf, "sicher": sicher, "punkte": pk, "bilder": bilder})

urteil = {
    "teilkachel": "r1c0", "viertel": V, "bearbeiter": f"urt-b-r1c0-{V}",
    "bilder_angesehen": {
        "uebersicht": [T0, GZ + "ganz_nummern.jpg", GZ + "ganz_roh.jpg", UN, UK],
        "nah": [N["nah1_nummern"], N["nah2_nummern"], N["nah4_nummern"], N["nah4_roh"], K1]},
    "segmente": segmente,
    "naht": [
        {"id": 300072, "seite": "rechts", "text": "Schattenfläche reicht nach r1c1; Klasse dort gleich halten, Verschmelzen mit 76 betrifft nur den Kern hier."}],
    "unsicher": [
        "300008 (Wald, v2): rötliche Krone bei 500–530/500–526 (Blutbuche oder absterbender Baum), halb im Schatten, liegt in 8 und 72.",
        "300060 (v3): dunkle Fläche reicht in den linken Teil von v4; in v3 mit 61 zum Verschmelzen vorgeschlagen.",
        "300042 (v2): Schattenfläche reicht von oben in v4."],
    "nicht_geprueft": [
        "Werkzeug kante nicht benutzt; Grenzen nur nach Sicht beurteilt.",
        "nah1_roh, nah2_roh, nah3_nummern und nah3_roh von v4 nicht angesehen (dort nur Wald 8 und Schatten); 77 nur in Übersicht, Kontrastbild und nah4 beurteilt."],
    "offen": [
        "Alle Schattenflächen (48, 59, 63, 72, 76, 77): Schlagschatten auf dem Kronendach oder dunkle Nadelbäume; eine Höhenkarte oder ein Bild mit anderem Sonnenstand würde es klären.",
        "59: ob so kleine Schattenlücken eigene Segmente bleiben oder zum Wald gehören; einheitlich festlegen."],
    "klassen_frei": [
        {"name": "Gehölz", "ebene": "grob", "eltern": None, "merkmal": "Baum- oder Strauchkronen mit runder Kronenstruktur und Eigenschatten"},
        {"name": "Schatten", "ebene": "grob", "eltern": None, "merkmal": "sehr dunkle Fläche, in der der Grund nicht erkennbar ist"},
        {"name": "Wald", "ebene": "mittel", "eltern": "Gehölz", "merkmal": "geschlossenes Kronendach aus vielen Kronen"},
        {"name": "Schatten auf Gehölz", "ebene": "mittel", "eltern": "Schatten", "merkmal": "dunkle Fläche inmitten von Gehölz"},
        {"name": "Wald", "ebene": "fein", "eltern": "Wald", "merkmal": "Kronendach mit Laubbaumkronen verschiedener Grüntöne, nicht feiner bestimmbar"},
        {"name": "Schatten auf Wald", "ebene": "fein", "eltern": "Schatten auf Gehölz", "merkmal": "fast strukturlos dunkle Fläche, ringsum Wald"}],
}
(O / "urteil.json").write_text(json.dumps(urteil, ensure_ascii=False, indent=1), encoding="utf-8")
konfig = {"viertel": V, "ausgabe": str(O).replace("\\", "/"), "punkte": punkte,
          "verschmelzen": {str(k): v for k, v in verschmelzen.items()}, "namen": {str(k): v for k, v in namen.items()},
          "kontrast": [[1, 470, 460, 100, 110, 5]]}
(O / "konfig.json").write_text(json.dumps(konfig, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(segmente), "Segmente,", sum(1 for s in segmente if s["urteil"] == "nicht_sauber"), "nicht sauber,",
      len(punkte), "Punkte,", sum(1 for s in segmente if not s["sicher"]), "unsicher")

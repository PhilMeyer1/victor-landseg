"""Schreibt urteil.json und konfig.json für r1c0/v3 (Fassung B) aus den Urteilen unten."""
import json
from pathlib import Path

V = "v3"
O = Path(f"C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r1c0/{V}")
Q = f"C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r1c0/{V}/"
T0 = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/T0.png"
GZ = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/ganz/r1c0/"
UN, UR, UK = Q + "uebersicht_nummern.jpg", Q + "uebersicht_roh.jpg", Q + "uebersicht_kontrast.jpg"
N = {k: Q + f"{k}.jpg" for k in ("nah1_nummern", "nah1_roh", "nah2_nummern", "nah2_roh",
                                 "nah3_nummern", "nah3_roh", "nah4_nummern", "nah4_roh")}
E1, E2, K1 = str(O / "nah_1.jpg"), str(O / "nah_2.jpg"), str(O / "kontrast_1.jpg")
V1N4 = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r1c0/v1/nah4_roh.jpg"

SAUM = {"grob": "Grünland", "mittel": "Saum", "fein": "Saum verbuscht"}
GEB = {"grob": "Gehölz", "mittel": "Gebüsch", "fein": "Strauchgruppe"}
SCH = {"grob": "Schatten", "mittel": "Schatten auf Gehölz", "fein": "Schatten auf Wald"}
nr = 0


def p(art, x, y, text, fl=None):
    global nr
    nr += 1
    return {"nr": nr, "art": art, "text": f"{text} ({x}/{y})", "flaeche_px": fl, "_xy": [x, y]}


S = [
    (300038, "1.3.4", "Grobe Kraut- und Hochstaudenfläche zwischen Wiese 19 und Wald mit vielen kleinen Sträuchern und einzelnen hellen Fehlstellen; kein Belag.",
     SAUM, False,
     [p("klasse", 132, 346, "Krautsaum mit Sträuchern, kein Sport- oder Spielplatz", 21077),
      p("fehlt", 300, 351, "heller, gerader Streifen (x 274–330, y 348–356): Pfad oder liegender Stamm, nicht abgetrennt", 200),
      p("sonstiges", 118, 352, "helle Fehlstellen (offener Boden oder Totholz) bei 118/352 und 156/352, je unter der Mindestfläche", 250)],
     [UN, UR, UK, N["nah1_nummern"], N["nah1_roh"], N["nah2_nummern"], N["nah2_roh"], V1N4, E1, K1, E2]),
    (300049, "3.1", "Dunkler, kompakter Strauch oder kleiner Baum mit Eigenschatten im Saum.",
     GEB, True,
     [p("klasse", 197, 330, "Gehölz, keine Wiese", 236)],
     [UN, N["nah2_nummern"], N["nah2_roh"]]),
    (300051, "4.1", "Hufeisenförmige Gruppe dunkler Sträucher im Saum, umschließt die helle Krautfläche 50.",
     GEB, True,
     [p("klasse", 243, 342, "Strauchgruppe, kein geschlossener Wald", 476)],
     [UN, UK, N["nah2_nummern"], N["nah2_roh"]]),
    (300050, "3.1", "Helle Krautfläche innerhalb des Strauchrings 51, gleiche Vegetation wie der Saum 38.",
     SAUM, True,
     [p("verschmelzen", 254, 330, "mit Saum 38 verschmelzen, Grenze zu 38 ohne Bildkante", 147)],
     [N["nah2_nummern"], N["nah2_roh"]]),
    (300043, "4.1", "Nur 25 Bildpunkte am linken Kernrand; im Kern helle Krautvegetation wie 38, der Rest des Segments (Gehölz) liegt im Kontextrand.",
     SAUM, False,
     [p("zu_klein", 66, 362, "Kernteil unter der Mindestfläche; mit Saum 38 verschmelzen", 25)],
     [UN, N["nah1_nummern"], E2]),
    (300058, "2.1", "Kleines, helles Krautstück am Waldrand, kein Acker.",
     SAUM, False,
     [p("klasse", 106, 375, "Krautsaum, kein Acker", 115),
      p("verschmelzen", 108, 378, "mit Saum 38 verschmelzen", 115)],
     [N["nah1_nummern"], N["nah1_roh"], E2]),
    (300056, "3.1", "Krautsaum mit Sträuchern am Waldrand, gleiche Vegetation wie 38; enthält eine bräunliche Fehlstelle am Westende.",
     SAUM, False,
     [p("verschmelzen", 160, 386, "Grenze zu 38 ohne Bildkante; mit 38 verschmelzen", 949)],
     [UN, N["nah1_nummern"], N["nah1_roh"], E2]),
    (300055, "3.1", "Krautsaum am Rand der dunklen Fläche 60/61, gleiche Vegetation wie 38.",
     SAUM, False,
     [p("verschmelzen", 235, 392, "Grenze zu 38 ohne Bildkante; mit 38 verschmelzen", 959)],
     [UN, N["nah2_nummern"], N["nah2_roh"]]),
    (300052, "2.1", "Krautstück am Waldrand mit zwei hellen parallelen Strichen (Hochsitz, Bank oder Holz?) an der Westkante.",
     SAUM, False,
     [p("klasse", 288, 356, "Krautsaum, kein Acker", 165),
      p("verschmelzen", 290, 358, "mit Saum 38 verschmelzen", 165)],
     [N["nah2_nummern"], N["nah2_roh"], E1, K1]),
    (300054, "3.1", "Krautstück mit Sträuchern am rechten Viertelrand, Übergang zum Wald.",
     SAUM, False,
     [p("verschmelzen", 303, 364, "mit Saum 38 verschmelzen, Grenzen ohne Bildkante", 199)],
     [N["nah2_nummern"], N["nah2_roh"], E1]),
    (300053, "0.2", "Dunkler Waldteil am linken Kernrand mit erkennbaren, bläulich beschatteten Kronen.",
     {"grob": "Gehölz", "mittel": "Wald", "fein": "Wald beschattet"}, False,
     [p("klasse", 79, 417, "Kronen erkennbar, kein Schatten ohne Grund", 2132)],
     [UN, UK, N["nah1_nummern"], N["nah1_roh"], E2]),
    (300061, "0.2", "Große, fast strukturlose dunkle Fläche südlich des Saums: Schatten im Wald; Grund nicht erkennbar.",
     SCH, False,
     [p("verschmelzen", 222, 440, "Grenze zu 60 liegt mitten in gleich dunkler Fläche ohne Bildkante; 60 und 61 verschmelzen", None)],
     [UN, UR, UK, N["nah1_nummern"], N["nah2_nummern"], N["nah2_roh"], N["nah3_nummern"]]),
    (300060, "0.2", "Fortsetzung der dunklen Fläche 61 nach Osten bis in v4: Schatten im Wald, nur vereinzelte Kronenlichter.",
     SCH, False,
     [p("verschmelzen", 245, 430, "mit 61 verschmelzen (Grenze ohne Bildkante)", None)],
     [UN, UR, UK, N["nah2_nummern"], N["nah2_roh"], N["nah4_nummern"]]),
    (300073, "0.2", "Kleiner dunkler Zipfel am Südrand von 61, gleich dunkel wie 61.",
     SCH, False,
     [p("verschmelzen", 212, 486, "mit 61 verschmelzen, Grenze ohne Bildkante", 268)],
     [UN, N["nah3_nummern"], N["nah4_nummern"]]),
]

verschmelzen = {300050: 300038, 300043: 300038, 300058: 300038, 300056: 300038, 300055: 300038,
                300052: 300038, 300054: 300038, 300060: 300061, 300073: 300061}
namen = {300038: "Saum verbuscht", 300049: "Strauch", 300051: "Strauchgruppe", 300053: "Wald beschattet",
         300061: "Schatten auf Wald"}

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
        "nah": [N["nah1_nummern"], N["nah1_roh"], N["nah2_nummern"], N["nah2_roh"], V1N4, N["nah3_nummern"], N["nah4_nummern"], E1, E2, K1]},
    "segmente": segmente,
    "naht": [],
    "unsicher": [
        "300008 (Wald, v2): zwischen 53 und 61 ist 8 hier ein heller Streifen aus jungen Bäumen oder Sträuchern; darin eine bräunliche Fehlstelle bei 120–145/382–395 (offener Boden), nicht abgetrennt.",
        "300045 und 300047 (v1): heller Bodenstreifen reicht bis an den oberen Rand von v3.",
        "300048 (v4): dunkle Fläche östlich des hellen Streifens bei 300/351."],
    "nicht_geprueft": [
        "Werkzeug kante nicht benutzt; Grenzen nur nach Sicht beurteilt.",
        "nah3_roh und nah4_roh von v3 (südliche Hälfte, fast nur Wald 8 und Schatten) nicht angesehen; dort nur die Nummernbilder, die Übersicht und das Kontrastbild."],
    "offen": [
        "38 mit 50, 52, 54, 55, 56, 58: ob die Fläche ein Krautsaum mit Sträuchern oder schon junger Gehölzaufwuchs ist; eine Höhenkarte würde es klären.",
        "Heller, gerader Streifen bei 274–330/348–356 mit zwei parallelen Strichen an der Westkante: Pfad, liegender Stamm oder Hochsitz; im Luftbild nicht entscheidbar.",
        "60, 61, 73: Schlagschatten auf Wald oder auf Boden in einer Lücke; Grund nicht erkennbar."],
    "klassen_frei": [
        {"name": "Grünland", "ebene": "grob", "eltern": None, "merkmal": "niedrige, krautige Vegetation ohne Kronen und Schatten von Gehölzen"},
        {"name": "Gehölz", "ebene": "grob", "eltern": None, "merkmal": "Baum- oder Strauchkronen mit runder Kronenstruktur und Eigenschatten"},
        {"name": "Schatten", "ebene": "grob", "eltern": None, "merkmal": "sehr dunkle Fläche, in der der Grund nicht erkennbar ist"},
        {"name": "Saum", "ebene": "mittel", "eltern": "Grünland", "merkmal": "grobe, unruhige Kraut- und Hochstaudenvegetation am Waldrand"},
        {"name": "Gebüsch", "ebene": "mittel", "eltern": "Gehölz", "merkmal": "kleine, dunkle Kronen mit kurzem Schatten, freistehend im Grünland"},
        {"name": "Wald", "ebene": "mittel", "eltern": "Gehölz", "merkmal": "geschlossenes Kronendach aus vielen Kronen"},
        {"name": "Schatten auf Gehölz", "ebene": "mittel", "eltern": "Schatten", "merkmal": "dunkle Fläche inmitten von Gehölz"},
        {"name": "Saum verbuscht", "ebene": "fein", "eltern": "Saum", "merkmal": "Krautsaum mit eingestreuten kleinen dunklen Sträuchern"},
        {"name": "Strauchgruppe", "ebene": "fein", "eltern": "Gebüsch", "merkmal": "mehrere zusammenhängende Strauchkronen"},
        {"name": "Strauch", "ebene": "fein", "eltern": "Gebüsch", "merkmal": "einzelne kompakte Strauch- oder Jungbaumkrone"},
        {"name": "Wald beschattet", "ebene": "fein", "eltern": "Wald", "merkmal": "dunkles Kronendach, einzelne Kronen noch erkennbar"},
        {"name": "Schatten auf Wald", "ebene": "fein", "eltern": "Schatten auf Gehölz", "merkmal": "fast strukturlos dunkle Fläche, ringsum Wald"}],
}
# 49 ist ein einzelner Strauch
urteil["segmente"][1]["klasse_frei"] = {"grob": "Gehölz", "mittel": "Gebüsch", "fein": "Strauch"}
(O / "urteil.json").write_text(json.dumps(urteil, ensure_ascii=False, indent=1), encoding="utf-8")
konfig = {"viertel": V, "ausgabe": str(O).replace("\\", "/"), "punkte": punkte,
          "verschmelzen": {str(k): v for k, v in verschmelzen.items()}, "namen": {str(k): v for k, v in namen.items()},
          "nah": [[1, 262, 326, 90, 80, 6], [2, 60, 340, 100, 80, 6]], "kontrast": [[1, 262, 326, 90, 80, 6]],
          "skizzen": [["Pfad oder Stamm (neu)", [[274, 352], [290, 352], [310, 351], [330, 351]]]],
          "vermerk": "orange: vorgeschlagene neue Grenze"}
(O / "konfig.json").write_text(json.dumps(konfig, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(segmente), "Segmente,", sum(1 for s in segmente if s["urteil"] == "nicht_sauber"), "nicht sauber,",
      len(punkte), "Punkte,", sum(1 for s in segmente if not s["sicher"]), "unsicher")

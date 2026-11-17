"""Schreibt urteil.json und konfig.json für r1c0/v2 (Fassung B) aus den Urteilen unten."""
import json
from pathlib import Path

V = "v2"
O = Path(f"C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r1c0/{V}")
Q = f"C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r1c0/{V}/"
T0 = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/T0.png"
GZ = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/ganz/r1c0/"
UN, UR, UK = Q + "uebersicht_nummern.jpg", Q + "uebersicht_roh.jpg", Q + "uebersicht_kontrast.jpg"
N = {k: Q + f"{k}.jpg" for k in ("nah1_nummern", "nah1_roh", "nah2_nummern", "nah2_roh",
                                 "nah3_nummern", "nah3_roh", "nah4_nummern", "nah4_roh")}
E1, K1 = str(O / "nah_1.jpg"), str(O / "kontrast_1.jpg")
V1E2 = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r1c0/v1/nah_2.jpg"

WALD = {"grob": "Gehölz", "mittel": "Wald", "fein": "Wald"}
WB = {"grob": "Gehölz", "mittel": "Wald", "fein": "Wald beschattet"}
SCH = {"grob": "Schatten", "mittel": "Schatten auf Gehölz", "fein": "Schatten auf Wald"}
nr = 0


def p(art, x, y, text, fl=None):
    global nr
    nr += 1
    return {"nr": nr, "art": art, "text": f"{text} ({x}/{y})", "flaeche_px": fl, "_xy": [x, y]}


S = [
    (300013, "3.1", "Krautige Fläche am Nordostrand des Waldes, der Kernteil nur eine kleine Ecke oben rechts; Grenze zu 17 auf der dunklen Kronenkante.",
     {"grob": "Grünland", "mittel": "Saum", "fein": "Saum"}, True, [],
     [UN, UR, N["nah2_nummern"], N["nah2_roh"]]),
    (300030, "3.1", "Helles, fein strukturiertes Stück am Waldrand rechts vom Wiesenstreifen in v1; setzt wohl die Wiese (24, 21) fort, könnte aber auch eine beleuchtete Randkrone sein.",
     {"grob": "Grünland", "mittel": "Wiese", "fein": "Wiese"}, False,
     [p("verschmelzen", 318, 136, "mit dem Wiesenstreifen 21/24 in v1 verschmelzen, falls Wiese; sonst mit Wald 8", 176)],
     [UN, N["nah1_nummern"], N["nah1_roh"], V1E2]),
    (300022, "0.2", "Dunkle Fläche am Waldrand mit erkennbarer Kronenstruktur: beschattete Kronen oder ein dunkler Nadelbaum.",
     WB, False,
     [p("klasse", 333, 104, "Kronen erkennbar, kein Schatten ohne Grund", 593),
      p("verschmelzen", 336, 112, "eher mit Wald 8 verschmelzen, falls kein eigener Nadelbaum", 593)],
     [UN, UK, N["nah1_nummern"], N["nah1_roh"]]),
    (300031, "3.1", "Hell beleuchtete, runde Baumkrone im Waldrand, keine Wiese.",
     WALD, True,
     [p("klasse", 352, 139, "Baumkrone, keine Wiese", 230),
      p("verschmelzen", 355, 143, "mit Wald 8 verschmelzen", 230)],
     [UN, UK, N["nah1_nummern"], N["nah1_roh"]]),
    (300023, "0.2", "Langes, sehr dunkles Band von Nord nach Süd mitten im Wald, kaum Struktur: Schatten in einer Kronenlücke oder Rinne; Grund nicht erkennbar, Umgebung Wald.",
     SCH, False, [],
     [UN, UR, UK, N["nah1_nummern"], N["nah1_roh"], N["nah3_roh"]]),
    (300017, "0.2", "Dunkler Kronenbereich oben rechts mit gut erkennbaren einzelnen Kronen: beschatteter oder dunkler Waldteil; reicht nach oben aus dem Kern.",
     WB, False,
     [p("klasse", 528, 104, "Kronen erkennbar, kein Schatten ohne Grund", 3902)],
     [UN, UK, N["nah2_nummern"], N["nah2_roh"]]),
    (300029, "6.6", "Schmaler, heller Pfad von Nord nach Süd durch den Wald; das Segment ist breiter als der Pfad und endet, wo der Pfad nach Osten abbiegt.",
     {"grob": "Weg", "mittel": "Pfad", "fein": "Trampelpfad"}, True,
     [p("grenze", 492, 165, "Segment etwa 9 Bildpunkte breit, der Pfad nur 3 bis 4; Säume beidseits gehören zum Nachbarn", None),
      p("fehlt", 540, 194, "Fortsetzung des Pfads nach Osten (x 508–564, y 185–205) liegt in Wald 8", 300)],
     [UN, UK, N["nah2_nummern"], N["nah2_roh"], N["nah4_nummern"], N["nah4_roh"], E1, K1]),
    (300008, "4.1", "Laubreicher Wald mit unterschiedlich hellen Kronen über die ganze Teilkachel; enthält eine krautige Lichtung und Pfadstücke.",
     WALD, True,
     [p("trennen", 528, 165, "krautige Lichtung östlich des Pfads 29 (x 500–555, y 135–200) ohne Kronen, fein strukturiert; eigenes Segment Saum", 3000),
      p("fehlt", 551, 182, "zweiter Pfad in der Lichtung (x 546–551, y 170–190), nur schwach sichtbar, nicht abgetrennt", 80),
      p("sonstiges", 326, 150, "kleiner beiger Fleck (Totholz oder offener Boden) am Waldrand, unter der Mindestfläche", 100)],
     [UN, UR, UK, N["nah1_roh"], N["nah2_nummern"], N["nah2_roh"], N["nah3_roh"], N["nah4_nummern"], N["nah4_roh"], E1, K1]),
    (300042, "0.2", "Große, sehr dunkle Fläche unten rechts mit nur schwacher Kronenstruktur: Schatten auf dem Wald; reicht nach rechts aus dem Kern und nach v4.",
     SCH, False, [],
     [UN, UR, UK, N["nah4_nummern"], N["nah4_roh"]]),
]

verschmelzen = {300030: 300021, 300022: 300008, 300031: 300008}
namen = {300013: "Saum", 300023: "Schatten auf Wald", 300017: "Wald beschattet", 300029: "Trampelpfad",
         300008: "Wald", 300042: "Schatten auf Wald"}

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
        "nah": [N["nah1_nummern"], N["nah1_roh"], N["nah2_nummern"], N["nah2_roh"], N["nah3_roh"],
                N["nah4_nummern"], N["nah4_roh"], E1, K1, V1E2]},
    "segmente": segmente,
    "naht": [
        {"id": 300013, "seite": "oben", "text": "Segment liegt größtenteils in r0c1/r1c1 außerhalb des Kerns; Klasse Saum/Grünland auf beiden Seiten gleich halten."},
        {"id": 300017, "seite": "oben", "text": "Dunkler Waldteil reicht nach r0c0; dort gleiche Klasse (Wald, beschattet)."},
        {"id": 300042, "seite": "rechts", "text": "Schattenfläche reicht nach r1c1; Klasse auf beiden Seiten gleich, Grenze dort auf der Dunkelkante."},
        {"id": 300008, "seite": "rechts", "text": "Lichtung und Pfad östlich von 29 setzen sich nach r1c1 fort; der Schnitt muss dort an derselben Stelle ankommen."}],
    "unsicher": [
        "300027 (v1): dunkles Band am linken Viertelrand, Krone oder Schlagschatten; in v1 geurteilt.",
        "300048 (v4): dunkle Fläche unten am Viertelrand, Schatten auf Wald wie 42.",
        "Heller, gelbgrüner Streifen in Wald 8 bei x 437–445, y 145–200: zugewachsener Pfad oder helle Kronen, nicht entscheidbar."],
    "nicht_geprueft": [
        "Werkzeug kante nicht benutzt; Grenzen nur nach Sicht beurteilt.",
        "Teile von 8 in v3 und v4 nur in der Teilkachel-Übersicht angesehen, nicht in den Nahansichten dieser Viertel (dort in den Aufträgen v3 und v4 angesehen)."],
    "offen": [
        "23, 42 und 17: ob die dunklen Flächen Schlagschatten auf dem Wald oder dunkle Nadelbäume sind; eine Höhenkarte oder ein zweites Luftbild mit anderem Sonnenstand würde es klären.",
        "30: Wiese oder beleuchtete Randkrone; Grenze zur Wiese in v1 ohne Bildkante.",
        "Lichtung östlich von 29: ob krautige Fläche (Saum) oder junger, niedriger Aufwuchs; Höhenkarte würde es klären."],
    "klassen_frei": [
        {"name": "Grünland", "ebene": "grob", "eltern": None, "merkmal": "niedrige, krautige Vegetation ohne Kronen und Schatten von Gehölzen"},
        {"name": "Gehölz", "ebene": "grob", "eltern": None, "merkmal": "Baum- oder Strauchkronen mit runder Kronenstruktur und Eigenschatten"},
        {"name": "Weg", "ebene": "grob", "eltern": None, "merkmal": "schmale, helle, linienhafte Fläche ohne Bewuchs"},
        {"name": "Schatten", "ebene": "grob", "eltern": None, "merkmal": "sehr dunkle Fläche, in der der Grund nicht erkennbar ist"},
        {"name": "Saum", "ebene": "mittel", "eltern": "Grünland", "merkmal": "grobe, unruhige Kraut- und Hochstaudenvegetation am Waldrand"},
        {"name": "Wiese", "ebene": "mittel", "eltern": "Grünland", "merkmal": "gleichmäßig feine, hellgrüne Grasstruktur"},
        {"name": "Wald", "ebene": "mittel", "eltern": "Gehölz", "merkmal": "geschlossenes Kronendach aus vielen Kronen"},
        {"name": "Pfad", "ebene": "mittel", "eltern": "Weg", "merkmal": "unbefestigter Weg unter 2 m Breite"},
        {"name": "Schatten auf Gehölz", "ebene": "mittel", "eltern": "Schatten", "merkmal": "dunkle Fläche inmitten von Gehölz"},
        {"name": "Saum", "ebene": "fein", "eltern": "Saum", "merkmal": "wie mittlere Ebene"},
        {"name": "Wiese", "ebene": "fein", "eltern": "Wiese", "merkmal": "wie mittlere Ebene"},
        {"name": "Wald", "ebene": "fein", "eltern": "Wald", "merkmal": "Kronendach mit Laubbaumkronen verschiedener Grüntöne, nicht feiner bestimmbar"},
        {"name": "Wald beschattet", "ebene": "fein", "eltern": "Wald", "merkmal": "dunkles Kronendach, einzelne Kronen noch erkennbar"},
        {"name": "Trampelpfad", "ebene": "fein", "eltern": "Pfad", "merkmal": "heller, gewundener Streifen von 3 bis 4 Bildpunkten Breite"},
        {"name": "Schatten auf Wald", "ebene": "fein", "eltern": "Schatten auf Gehölz", "merkmal": "fast strukturlos dunkle Fläche, ringsum Wald"}],
}
(O / "urteil.json").write_text(json.dumps(urteil, ensure_ascii=False, indent=1), encoding="utf-8")
konfig = {"viertel": V, "ausgabe": str(O).replace("\\", "/"), "punkte": punkte,
          "verschmelzen": {str(k): v for k, v in verschmelzen.items()}, "namen": {str(k): v for k, v in namen.items()},
          "nah": [[1, 476, 118, 100, 100, 6]], "kontrast": [[1, 476, 118, 100, 100, 6]], "skizzen": [["Lichtung (neu, Saum)", [[500, 135], [515, 128], [540, 133], [552, 140], [556, 160], [556, 185], [548, 190], [525, 197], [508, 200], [503, 180], [500, 160], [500, 135]]], ["Pfad (neu)", [[508, 201], [530, 196], [548, 190], [564, 186]]]], "vermerk": "orange: vorgeschlagene neue Grenze"}
(O / "konfig.json").write_text(json.dumps(konfig, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(segmente), "Segmente,", sum(1 for s in segmente if s["urteil"] == "nicht_sauber"), "nicht sauber,",
      len(punkte), "Punkte,", sum(1 for s in segmente if not s["sicher"]), "unsicher")

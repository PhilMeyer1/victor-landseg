"""Schreibt urteil.json und konfig.json für r1c0/v1 (Fassung B) aus den Urteilen unten."""
import json
from pathlib import Path

V = "v1"
O = Path(f"C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r1c0/{V}")
Q = f"C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r1c0/{V}/"
T0 = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/T0.png"
GZ = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/ganz/r1c0/"
UN, UR, UK = Q + "uebersicht_nummern.jpg", Q + "uebersicht_roh.jpg", Q + "uebersicht_kontrast.jpg"
N = {k: Q + f"{k}.jpg" for k in ("nah1_nummern", "nah1_roh", "nah2_nummern", "nah2_roh",
                                 "nah3_nummern", "nah3_roh", "nah4_nummern", "nah4_roh")}
E1, E2, K1 = str(O / "nah_1.jpg"), str(O / "nah_2.jpg"), str(O / "kontrast_1.jpg")

WIESE = {"grob": "Grünland", "mittel": "Wiese", "fein": "Wiese"}
nr = 0


def p(art, x, y, text, fl=None):
    global nr
    nr += 1
    return {"nr": nr, "art": art, "text": f"{text} ({x}/{y})", "flaeche_px": fl, "_xy": [x, y]}


S = [
    (300016, "0.2", "Kernteil (6 Zeilen am oberen Kernrand) ist Wiese wie 1; der dunklere Fleck des Segments liegt oberhalb in r0c0.",
     WIESE, False,
     [p("klasse", 140, 67, "Kernteil ist Wiese, kein Schatten ohne Grund", 77),
      p("verschmelzen", 150, 68, "Kernteil mit 1 verschmelzen, Grenze ohne Bildkante", 77)],
     [UN, N["nah1_nummern"], N["nah1_roh"], E1]),
    (300001, "1.3.4", "Oberer Teil der großen Wiese; gleiche feine Grasstruktur wie 19, kein Belag.",
     WIESE, True,
     [p("klasse", 186, 91, "Wiese, kein Sport- oder Spielplatz mit Kunstbelag", 7060),
      p("verschmelzen", 160, 108, "Treppengrenze zu 19 ohne Bildkante, beide eine Wiese", None),
      p("grenze", 253, 100, "senkrechte Gerade zu 21 ohne Bildkante", None)],
     [UN, UR, N["nah1_nummern"], N["nah1_roh"], N["nah2_nummern"], E1]),
    (300018, "2.1", "Schmales Stück am oberen Kernrand; im Kern Wiese, oben in r0c0 ein kleiner Strauch.",
     WIESE, False,
     [p("verschmelzen", 221, 68, "Kernteil ist Wiese, mit der Wiese (15/1) verschmelzen", 88)],
     [UN, N["nah2_nummern"], E1]),
    (300021, "2.1", "Teil des Wiesenstreifens zwischen Baum 26 und Waldrand 27, etwas gröber als 1, mit einzelnen kleinen Sträuchern.",
     WIESE, True,
     [p("klasse", 265, 95, "Wiese, keine Acker- oder Reihenstruktur", 1427),
      p("verschmelzen", 262, 122, "mit 15, 24, 25, 28, 32, 33, 36, 37, 39 eine Fläche, Teilgrenzen ohne Bildkante", None)],
     [UN, N["nah2_nummern"], N["nah2_roh"], E2]),
    (300015, "3.1", "Wiese am oberen Rand rechts, mit einem kleinen dunklen Strauch bei 281/93; reicht nach r0c0 und v2.",
     WIESE, True,
     [p("verschmelzen", 300, 80, "Grenzen zu 21, 24 und 18 ohne Bildkante; mit der Wiese verschmelzen", None)],
     [UN, N["nah2_nummern"], N["nah2_roh"], E1, E2]),
    (300026, "0.2", "Dunkle, dichte Krone eines großen Einzelbaums (etwa 13 m) am Wiesenrand, samt Schlagschatten nach Nordwesten; Krone im Kontrastbild klar strukturiert.",
     {"grob": "Gehölz", "mittel": "Einzelbaum", "fein": "Einzelbaum"}, True,
     [p("klasse", 215, 135, "Baumkrone mit erkennbarem Grund, kein Schatten ohne Grund", 2470)],
     [UN, UR, UK, N["nah2_nummern"], N["nah2_roh"], E2]),
    (300028, "4.1", "Wiesenstück zwischen Baumkrone 26 und 21; kein Gehölz.",
     WIESE, True,
     [p("klasse", 247, 128, "Wiese, kein Wald", 257),
      p("verschmelzen", 249, 135, "mit dem Wiesenstreifen 21 verschmelzen", 257)],
     [N["nah2_nummern"], N["nah2_roh"], E2]),
    (300032, "3.1", "Kleines Wiesenstück im Streifen; Klasse stimmt, Grenzen ohne Bildkante.",
     WIESE, True,
     [p("verschmelzen", 269, 138, "mit 21 verschmelzen, Grenzen ohne Bildkante", 173)],
     [N["nah2_nummern"], N["nah2_roh"], E2]),
    (300025, "1.3.4", "Kleines Wiesenstück im Streifen, kein Belag.",
     WIESE, True,
     [p("klasse", 271, 113, "Wiese, kein Sportplatz", 156),
      p("verschmelzen", 272, 117, "mit 21 verschmelzen", 156)],
     [N["nah2_nummern"], N["nah2_roh"], E2]),
    (300033, "4.1", "Helles Wiesenstück am Rand der dunklen Fläche 27, kein Wald.",
     WIESE, True,
     [p("klasse", 282, 146, "Wiese, kein Wald", 129),
      p("verschmelzen", 284, 145, "mit 21 verschmelzen", 129)],
     [N["nah2_nummern"], N["nah2_roh"], E2]),
    (300024, "2.1", "Kleines Wiesenstück am rechten Viertelrand.",
     WIESE, True,
     [p("klasse", 306, 103, "Wiese, kein Acker", 132),
      p("verschmelzen", 308, 101, "mit 15 und 21 verschmelzen", 132)],
     [N["nah2_nummern"], E2]),
    (300019, "2.2", "Große Wiese mit hellen, schräg verlaufenden Streifen und hellen Fehlstellen; feine Grasstruktur, keine Furchen.",
     WIESE, True,
     [p("klasse", 121, 162, "Wiese, kein gepflügter Acker", 25781),
      p("fehlt", 130, 285, "helle lückige Stellen wie in 41 (x 95–170, y 255–312) nicht abgetrennt", 1800),
      p("grenze", 105, 300, "Grenze zum Saum 38 unten links nur ungefähr auf dem Helligkeitswechsel", None)],
     [UN, UR, UK, N["nah1_nummern"], N["nah1_roh"], N["nah3_nummern"], N["nah3_roh"]]),
    (300036, "3.1", "Kleines Wiesenstück unten im Streifen.",
     WIESE, True,
     [p("verschmelzen", 257, 151, "mit 21 verschmelzen, Grenzen ohne Bildkante", 145)],
     [N["nah2_nummern"], N["nah2_roh"], E2]),
    (300039, "3.1", "Kleines Wiesenstück am unteren Ende des Streifens, grenzt an den Wald 8.",
     WIESE, True,
     [p("verschmelzen", 270, 172, "mit 21 verschmelzen, Grenzen ohne Bildkante", 136)],
     [N["nah2_nummern"], N["nah2_roh"], E2]),
    (300037, "2.1", "Wiesenstück im unteren Streifen, keine Ackerstruktur.",
     WIESE, True,
     [p("klasse", 271, 158, "Wiese, kein Acker", 596),
      p("verschmelzen", 274, 162, "mit 21 verschmelzen", 596)],
     [N["nah2_nummern"], N["nah2_roh"], E2]),
    (300027, "0.2", "Langes dunkles Band am Waldrand: dunkle Kronen der Randbäume oder deren Schlagschatten nach Nordwesten auf den Saum; Gehölz in jedem Fall erkennbar.",
     {"grob": "Gehölz", "mittel": "Wald", "fein": "Wald beschattet"}, False,
     [p("klasse", 300, 164, "Kronenstruktur erkennbar, kein Schatten ohne Grund", 2040),
      p("grenze", 318, 182, "rechte Grenze zum Wald 8 ohne klare Kante; eher mit 8 verschmelzen", None)],
     [UN, UR, UK, N["nah2_nummern"], N["nah2_roh"], N["nah4_nummern"], E2]),
    (300041, "6.1", "Helle, beige Ringe und Flecken in der Wiese mit grünen Inseln: lückige, trockene Grasnarbe oder aufgewühlter Boden.",
     {"grob": "Grünland", "mittel": "Wiese", "fein": "Wiese lückig"}, False,
     [p("klasse", 191, 222, "überwiegend lückige Grasnarbe, kein offener Sand oder Lehm; Ursache unklar", 1662)],
     [UN, UR, UK, N["nah3_nummern"], N["nah3_roh"], N["nah4_nummern"], K1]),
    (300044, "3.1", "Grobe Krautvegetation unter dem Waldrand, wie der Saum 38.",
     {"grob": "Grünland", "mittel": "Saum", "fein": "Saum verbuscht"}, True,
     [p("verschmelzen", 258, 232, "gleiche Krautvegetation wie 38, Grenze unten ohne Bildkante; mit 38 verschmelzen", 298)],
     [N["nah4_nummern"], N["nah4_roh"]]),
    (300047, "1.3.4", "Kleines Stück am Südende des hellen Streifens 45: heller Boden mit etwas Wiese.",
     {"grob": "Offenboden", "mittel": "Rohboden", "fein": "Erdstreifen"}, False,
     [p("verschmelzen", 184, 296, "heller Teil gehört zu 45, Wiesenrand zu 19; kein Sportplatz", 134)],
     [N["nah3_nummern"], N["nah3_roh"], N["nah4_nummern"]]),
    (300046, "1.3.4", "Wiesenstück zwischen 41, 45 und 19, gleiche Grasnarbe wie 19.",
     WIESE, True,
     [p("klasse", 209, 256, "Wiese, kein Sportplatz", 132),
      p("verschmelzen", 207, 262, "mit 19 verschmelzen", 132)],
     [N["nah4_nummern"], N["nah4_roh"], K1]),
    (300045, "6.1", "Heller, rötlich-beiger Streifen von Nordost nach Südwest mit kleinen dunklen Sträuchern: offener oder vertrockneter Boden, vielleicht eine Rinne oder Aufschüttung.",
     {"grob": "Offenboden", "mittel": "Rohboden", "fein": "Erdstreifen"}, False,
     [p("klasse", 220, 268, "offener Boden wahrscheinlich, Art (Rinne, Aufschüttung, Streu) nicht erkennbar", 2046)],
     [UN, UR, UK, N["nah4_nummern"], N["nah4_roh"], N["nah3_nummern"], K1]),
]

verschmelzen = {300016: 300001, 300001: 300019, 300018: 300015, 300015: 300021, 300025: 300021,
                300028: 300021, 300032: 300021, 300033: 300021, 300036: 300021, 300037: 300021,
                300039: 300021, 300024: 300021, 300021: 300019, 300044: 300038, 300046: 300019,
                300047: 300045}
namen = {300019: "Wiese", 300041: "Wiese lückig", 300026: "Einzelbaum", 300027: "Wald beschattet?",
         300045: "Erdstreifen?"}

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
        "uebersicht": [T0, GZ + "ganz_nummern.jpg", GZ + "ganz_roh.jpg", UN, UR, UK],
        "nah": [N["nah1_nummern"], N["nah1_roh"], N["nah2_nummern"], N["nah2_roh"], N["nah3_nummern"], N["nah3_roh"],
                N["nah4_nummern"], N["nah4_roh"], E1, E2, K1]},
    "segmente": segmente,
    "naht": [
        {"id": 300016, "seite": "oben", "text": "Kernteil ist Wiese (mit 1 verschmelzen); der dunklere Teil oberhalb in r0c0 ist dort zu entscheiden, die Klasse 0.2 trifft auch dort nicht sicher zu."},
        {"id": 300018, "seite": "oben", "text": "Kernteil Wiese; das Segment reicht nach r0c0, dort mit kleinem Strauch."},
        {"id": 300015, "seite": "oben", "text": "Wiese reicht nach r0c0; Klasse Wiese auf beiden Seiten gleich halten."},
        {"id": 300001, "seite": "oben", "text": "Wiese reicht nach r0c0; Vorschlag Klasse Wiese gilt für das ganze Segment."}],
    "unsicher": [
        "300008 (Wald, Viertel v2): am Rand zu v1 bei 243/202 ein heller Fleck im Kronendach (Lücke oder abgestorbener Baum), im Segment 8 enthalten.",
        "300038 (Saum, Viertel v3): grenzt mit grober Krautvegetation an 19; die Klasse Sportplatz der Vorstufe trifft nicht zu.",
        "300030 (Viertel v2): kleines helles Stück am Waldrand rechts von 24, Wiese oder Lichtung."],
    "nicht_geprueft": [
        "Werkzeug kante nicht benutzt; Grenzen nur nach Sicht in den Übersichts- und Nahansichten beurteilt.",
        "Teile von 16, 18, 15 und 1 außerhalb des Kerns (r0c0) nur in der Übersicht angesehen."],
    "offen": [
        "Ob der Wiesenstreifen rechts von x 253 (21, 15, 25, 28, 32, 33, 36, 37, 39, 24) eine eigene, ungemähte oder verbrachte Fläche ist oder zur Wiese 1/19 gehört: Bild zeigt keine Kante, nur gröbere Struktur; ein Bild aus anderem Jahr oder Begehung würde es klären.",
        "26 und 27: wie viel der dunklen Fläche Krone und wie viel Schlagschatten (nach Nordwesten) ist; eine Höhenkarte (Oberflächenmodell) würde die Grenze klären.",
        "41 und 45: helle Stellen trockene Grasnarbe, Wühlstellen von Wildschweinen oder offener Boden; im Luftbild nicht unterscheidbar.",
        "19: ob die übrigen hellen Fehlstellen (x 95–170, y 255–312) wie 41 abgetrennt werden sollen oder 41 in 19 aufgehen soll; einheitlich entscheiden."],
    "klassen_frei": [
        {"name": "Grünland", "ebene": "grob", "eltern": None, "merkmal": "niedrige, krautige Vegetation ohne Kronen und Schatten von Gehölzen"},
        {"name": "Gehölz", "ebene": "grob", "eltern": None, "merkmal": "Baum- oder Strauchkronen mit runder Kronenstruktur und Eigenschatten"},
        {"name": "Offenboden", "ebene": "grob", "eltern": None, "merkmal": "helle, beige bis rötliche Fläche mit wenig oder keinem Grün"},
        {"name": "Wiese", "ebene": "mittel", "eltern": "Grünland", "merkmal": "gleichmäßig feine, hellgrüne Grasstruktur"},
        {"name": "Saum", "ebene": "mittel", "eltern": "Grünland", "merkmal": "grobe, unruhige Kraut- und Hochstaudenvegetation am Waldrand"},
        {"name": "Einzelbaum", "ebene": "mittel", "eltern": "Gehölz", "merkmal": "einzelne freistehende Krone mit eigenem Schlagschatten"},
        {"name": "Wald", "ebene": "mittel", "eltern": "Gehölz", "merkmal": "geschlossenes Kronendach aus vielen Kronen"},
        {"name": "Rohboden", "ebene": "mittel", "eltern": "Offenboden", "merkmal": "offener, heller Boden mit einzelnen Pflanzen"},
        {"name": "Wiese", "ebene": "fein", "eltern": "Wiese", "merkmal": "wie mittlere Ebene, nicht feiner unterscheidbar"},
        {"name": "Wiese lückig", "ebene": "fein", "eltern": "Wiese", "merkmal": "Wiese mit hellen beigen Ringen und Fehlstellen in der Grasnarbe"},
        {"name": "Saum verbuscht", "ebene": "fein", "eltern": "Saum", "merkmal": "Krautsaum mit eingestreuten kleinen dunklen Sträuchern"},
        {"name": "Einzelbaum", "ebene": "fein", "eltern": "Einzelbaum", "merkmal": "wie mittlere Ebene"},
        {"name": "Wald beschattet", "ebene": "fein", "eltern": "Wald", "merkmal": "sehr dunkles Kronendach oder Schlagschatten hoher Bäume auf dem Wald"},
        {"name": "Erdstreifen", "ebene": "fein", "eltern": "Rohboden", "merkmal": "schmaler, länglicher Streifen offenen Bodens"}],
}
(O / "urteil.json").write_text(json.dumps(urteil, ensure_ascii=False, indent=1), encoding="utf-8")
konfig = {"viertel": V, "ausgabe": str(O).replace("\\", "/"), "punkte": punkte,
          "verschmelzen": {str(k): v for k, v in verschmelzen.items()}, "namen": {str(k): v for k, v in namen.items()},
          "nah": [[1, 110, 36, 130, 96, 6], [2, 228, 86, 104, 112, 6]],
          "kontrast": [[1, 150, 180, 100, 130, 5]], "skizzen": [["helle Fehlstellen (neu, Wiese lückig)", [[95, 255], [130, 250], [170, 280], [172, 310], [130, 312], [100, 290], [95, 255]]]], "vermerk": "orange: vorgeschlagene neue Grenze"}
(O / "konfig.json").write_text(json.dumps(konfig, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(segmente), "Segmente,", sum(1 for s in segmente if s["urteil"] == "nicht_sauber"), "nicht sauber,",
      len(punkte), "Punkte,", sum(1 for s in segmente if not s["sicher"]), "unsicher")

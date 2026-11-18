import json
from pathlib import Path

VIERTEL = "v3"
H0 = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
UEBERSICHT = [H0 + "H0.png", H0 + "ganz/H0_raster.jpg", H0 + "ganz/r0c0/ganz_nummern.jpg", H0 + "ganz/r0c0/ganz_roh.jpg",
              "uebersicht_nummern.jpg", "uebersicht_roh.jpg"]
NAH = ["nah1_nummern.jpg", "nah1_roh.jpg", "nah3_nummern.jpg", "nah3_roh.jpg", "nah_1.jpg", "nah_1_roh.jpg"]
UN = "uebersicht_nummern.jpg"
SEGMENTE = [
 (100173, "Helle, fleckige Fläche am linken Kernrand südlich der Gartenparzelle 100160 (71/340), großteils im Kontextrand.", "n", "3.3", False,
  [("klasse", "Kein Hauptgebäude erkennbar: Anger/Fahrweg-Zone wie 100114 (Ruderalflur mit Fahrspur).", None)],
  [UN, "nah_1.jpg", "nah1_roh.jpg"]),
 (100174, "Nach Verschmelzen: dunklerer Rain mit Büschen am Nordwestrand des Ackers 100154 (162/320).", "n", "3.4", False,
  [("verschmelzen", "100175 und 100177 ohne Bildkante angefügt.", 302),
   ("klasse", "Linearer Rain zwischen Anger und Acker; einzelne dunkle Büsche (150/330) zu klein zum Teilen.", None)],
  [UN, "nah_1.jpg", "nah1_roh.jpg"]),
 (100184, "Heller Fleck auf dem Fahrweg am linken Kernrand (68/353).", "n", "6.6", False,
  [("klasse", "Kein Gebäude: liegt auf der hellen Fahrspur von 100114 nach Südwesten; unbefestigter Weg wahrscheinlich.", None)],
  [UN, "nah_1.jpg"]),
 (100181, "Nach Verschmelzen: gekörnte, fleckige Grasfläche westlich der Hecke 100188 (87/424).", "n", None, False,
  [("verschmelzen", "Helle bzw. graue Flecken 100204 und 100208 ohne klare Kante angefügt.", 439),
   ("sonstiges", "Wiese/Weide plausibel (heller und fleckiger als der Acker); Acker nicht ganz ausgeschlossen.", None)],
  [UN, "nah_1.jpg", "nah_1_roh.jpg"]),
 (100154, "Großer Acker mit feinen hellen Längsstreifen (Streifenflur), von v1 bis v4 (226/401).", "n", "2", False,
  [("klasse", "Acker sicher nach Form und Streifen; ob gepflügt (2.2) oder bewachsen (2.1) ist bei Grauwert 77 ohne Furchen nicht zu entscheiden, daher Elternklasse.", None),
   ("sonstiges", "Hellere Längsstreifen (z. B. 300/350 nach 450/290) könnten eigene Streifenparzellen sein; Kanten zu schwach zum Teilen (G4).", None)],
  [UN, "uebersicht_roh.jpg", "nah_1_roh.jpg"]),
 (100188, "Dunkle, hakenförmige Linie am Westrand des Ackers (136/451): Hecke bzw. Baumreihe mit Schatten.", "n", "4.2.3", False,
  [("klasse", "Nicht 0.2: klar erkennbare lineare Struktur; Hecke wahrscheinlich, Graben oder Hohlweg möglich.", None),
   ("grenze", "Segment schließt einen Streifen Gras östlich der Linie ein (140/430); Grenze zur Wiese ohne Bildkante.", None)],
  [UN, "nah_1.jpg", "nah_1_roh.jpg"]),
 (100202, "Helle Fläche mit verstreuten dunklen Flecken im Südwesten (76/537), großteils im Kontextrand.", "n", "3.5", False,
  [("klasse", "Keine Baustelle erkennbar (keine Maschinen, keine Erdbewegung): helles Gras mit verstreuten Büschen; Grube oder Ruderalfläche möglich.", None)],
  [UN, "nah_1.jpg", "uebersicht_roh.jpg"]),
 (100213, "Dunkler Streifen am Westrand des Ackers (88/519).", "n", "3.4", False,
  [("klasse", "Feldrain mit dunkler Kante zwischen Acker und Gebüschfläche; Hecke (4.2.3) möglich.", None)],
  [UN, "nah_1.jpg"]),
 (100221, "Randstück am Westrand des Ackers (97/547).", "n", "3.4", False,
  [("klasse", "Rain zwischen Acker 100154 und Fläche 100202, kein eigener Acker.", None)],
  [UN, "nah_1.jpg"]),
 (100223, "Randstück am Westrand des Ackers am unteren Kernrand (99/558).", "n", "3.4", False,
  [("klasse", "Rain, Fortsetzung von 100221; Grenze zu 100221 ohne Bildkante.", None),
   ("verschmelzen", "Gehört zu 100221; nicht verschmolzen, weil beide in den Kontextrand reichen.", None)],
  [UN, "nah_1.jpg"]),
]
NAHT = [
 {"id": 100154, "seite": "unten", "text": "Acker reicht über die Teilkachelgrenze nach r1c0; Klasse 2 (Acker) dort gleich halten."},
 {"id": 100202, "seite": "unten", "text": "Gebüschfläche reicht nach r1c0; Klasse 3.5 dort prüfen."},
]
UNSICHER = ["100160 und 100114 (v1): Anger und Gartenparzelle oberhalb, Fahrweg läuft durch 100173 und 100184 weiter nach Südwesten."]
NICHT_GEPRUEFT = ["Kontextrand-Anteile von 100173, 100202, 100221 nur als Umgebung gesehen; 100154 im Viertel v4 nur in der Übersicht."]
OFFEN = [
 "Acker 100154: gepflügt oder bewachsen im Farbbild entscheidbar.",
 "100188: Hecke oder Graben im Farbbild (Grün gegen Wasser/Erde) entscheidbar.",
 "100202: Gebüschfläche, Grube oder Ruderalfläche im Farbbild prüfen.",
]
import importlib.util as _iu
_s = _iu.spec_from_file_location("en", Path(__file__).resolve().parent / "eingriffe_netto.py"); _m = _iu.module_from_spec(_s); _s.loader.exec_module(_m)
EINGRIFFE = _m.netto(Path(__file__).resolve().parent / "protokoll.json")

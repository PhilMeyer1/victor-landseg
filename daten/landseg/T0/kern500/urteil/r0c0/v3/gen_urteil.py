import sys
sys.path.insert(0, "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil/r0c0/v1")
from schreibe import schreibe

K = "klasse"; V = "verschmelzen"; F = "fehlt"; G = "grenze"; T = "trennen"; S = "sonstiges"
KR = "Dunkle Krone mit bläulichen Lichtpunkten (Textur im Kontrastbild sichtbar)"
segs = [
 (100140, "0.2", "Dunkle, große Baumkrone (etwa 10 × 9 m) im verbuschten Hang; Kronentextur sichtbar, kein Schatten ohne Grund.", "4.2", True,
  [(K, f"{KR} bei (135/340); nach U2 Gehölz statt 0.2; Einzelbaum oder Gruppe offen, daher Elternklasse.", 1503),
   (G, "Dunkler Kronenteil zwischen 140 und 151 (121/356) liegt in 56 und gehört zur Krone.", 480)], ["e:kontrast_1.jpg", "n1", "u"]),
 (100151, "0.2", "Kleinere dunkle Krone südlich von 140 mit schmalem Ausläufer nach Nordwesten.", "4.2", True,
  [(K, "Kronentextur (130/380); Gehölz statt 0.2.", 630)], ["n1", "e:kontrast_1.jpg"]),
 (100145, "0.2", "Herzförmige dunkle Krone, wohl zwei zusammenstehende Bäume (etwa 10 × 12 m).", "4.2", True,
  [(K, "Zwei Kronenlappen mit Textur (279/353); Gehölz statt 0.2.", 1935)], ["n2", "u"]),
 (100165, "0.2", "Größte dunkle Krone am linken Kernrand (etwa 14 × 15 m), bildet mit 171 und 178 eine Baumgruppe.", "4.2", True,
  [(K, "Kronentextur (85/436); Gehölz statt 0.2.", 2706)], ["n1", "n3", "u"]),
 (100168, "4.2.1", "Kleines, etwas helleres Stück zwischen den Kronen 165 und 171: Kronenrand.", "4.2", False,
  [(V, "Mit 100165 verschmelzen (100/416); keine eigene Krone.", 74)], ["n1"]),
 (100157, "0.2", "Längliche dunkle Krone mitten im Hang.", "4.2", True,
  [(K, "Kronentextur (174/421); Gehölz statt 0.2.", 1396)], ["n1", "n2"]),
 (100161, "0.2", "Kleine, etwas hellere Krone aus zwei Lappen am rechten Rand des Viertels: Strauch oder kleiner Baum.", "4.2", True,
  [(K, "Gehölz mit Textur (291/409) statt 0.2.", 645)], ["n2"]),
 (100182, "3.1", "Wiesenstück zwischen Krone 165/178 und der Wiese 166.", None, True,
  [(V, "Mit 100166 verschmelzen, keine Bildkante (88/480).", 189)], ["n3"]),
 (100178, "4.2.1", "Hellere, bläulich-grüne Krone am Südrand der Gruppe 165, eigener Baum.", None, False,
  [(G, "Kronentextur setzt sich nach Osten in 56 fort (122/486); dort fehlen etwa 100 Bildpunkte.", 100)], ["n3", "u"]),
 (100171, "0.2", "Dunkle Krone östlich von 165, Teil der Baumgruppe.", "4.2", True,
  [(K, "Kronentextur (135/461); Gehölz statt 0.2.", 1344)], ["n1", "n3"]),
 (100180, "0.2", "Kompakte dunkle Krone im Südosten des Viertels.", "4.2", True,
  [(K, "Kronentextur (264/497); Gehölz statt 0.2.", 1537)], ["n4", "u"]),
 (100186, "3.1", "Kleiner dunkler Busch neben dem hellen Trampelpfad.", "4.2", False,
  [(K, "Dunkler, runder Fleck (295/488), eher Busch als Wiese.", 176)], ["n4"]),
 (100166, "3.1", "Gleichmäßige, glattere Wiese links und unten im Viertel, deutlich anders als die raue Fläche 56.", None, True, [], ["n3", "n4", "u", "ur"]),
 (100188, "3.1", "Dunkler Saum am Westrand der Krone 184.", "4.2", False,
  [(V, "Mit 100184 verschmelzen (103/500); Kronenrand bzw. Schatten der Krone.", 131)], ["n3"]),
 (100184, "0.2", "Längliche dunkle Krone am Westrand des Viertels.", "4.2", True,
  [(K, "Kronentextur (115/513); Gehölz statt 0.2.", 879)], ["n3"]),
 (100181, "4.2.4", "Große, dunkle Gehölzfläche aus mehreren Kronen (etwa 10 × 14 m), eher Baumgruppe als niedriges Gebüsch.", "4.2", True,
  [(K, "Hohe Kronen mit Lichtpunkten (178/510); Unterklasse Gebüsch zu fein, Elternklasse.", 2179)], ["n3", "n4"]),
 (100193, "3.1", "Wiesenstück unter der Gehölzfläche 181.", None, False,
  [(V, "Mit 100166 verschmelzen, keine Bildkante (197/545); Zuordnung zu 56 auch möglich.", 451)], ["n3", "n4"]),
 (100192, "4.2.1", "Kleiner dunkler Lappen am Südostrand der Krone 180.", "4.2", False,
  [(V, "Mit 100180 verschmelzen (280/515).", 110)], ["n4"]),
 (100195, "0.2", "Mittelgrüne, glatte Wiesenfläche am unteren Kernrand, kaum dunkler als 166; kein Schatten ohne Grund.", "3.1", False,
  [(K, "Wiese (143/551), nach U2 keine 0.2.", 747), (V, "Mit 100166 verschmelzen (143/551).", 747)], ["n3"]),
]
naht = [
 {"id": 100195, "seite": "unten", "text": "Vorschlag 3.1 und Verschmelzen mit 166; ein kleiner Teil liegt jenseits des Kerns in r1c0 und muss dort gleich behandelt werden."},
]
unsicher = [
 "100056 (v1): enthält in v3 weitere dunkle Gehölzflecken ohne eigenes Segment (163/336, 205/358, 230/499, 249/368, 293/552) und helle Trampelpfade (260/420, 280/500); im Urteil von v1 bei 56 nachgetragen.",
 "100138 und 100125 (v1): dunkle Kronen wie die Kronen hier; in v1 als Gehölz vorgeschlagen.",
 "100176 und 100177 (v4): Rand der großen Krone 177 am rechten Rand des Viertels.",
]
nicht_geprueft = [
 "Rohbilder nah1_roh bis nah4_roh, uebersicht_kontrast.jpg und uebersicht_gitter.jpg nicht eigens angesehen; eigenes Kontrastbild für die Kronen 125 bis 151.",
 "Werkzeug kante (W4) nicht benutzt; Grenzen nach Augenschein.",
 "Gegenseite der Naht in r1c0 nicht angesehen.",
]
offen = [
 "Alle dunklen Kronen: Einzelbaum (4.2.1), Baumgruppe (4.2.2) oder Gebüsch (4.2.4) ist ohne Höhe nicht sicher; deshalb Elternklasse 4.2.",
 "100193: gehört zur glatten Wiese 166 oder zur rauen Fläche 56?",
]
schreibe("v3", ["x:T0.png", "x:ganz/r0c0/ganz_nummern.jpg", "x:ganz/r0c0/ganz_roh.jpg", "u", "ur", "uv"],
         ["n1", "n2", "n3", "n4", "e:kontrast_1.jpg"], segs, naht, unsicher, nicht_geprueft, offen)

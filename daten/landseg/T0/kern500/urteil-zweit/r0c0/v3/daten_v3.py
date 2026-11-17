# Urteil Zweitagent Fassung A, r0c0 v3. Zeile: (id, klasse_heute, was_ist_es, urteil, klasse_vorschlag, sicher, punkte, bilder)
S, N = "sauber", "nicht_sauber"
UEBERSICHT = ["T0", "G", "GR", "U", "R", "K", "V"]
NAH = ["n1", "n2", "n3", "n4", "r1", "k1"]

KRONE = "Dunkle Krone mit Blattstruktur und Lichtpunkten"

SEG = [
 (100140, "0.2", f"{KRONE} (etwa 10 m) in der verbuschten Wiese, Baum oder Strauchgruppe.", N, "4.2", True,
  [("klasse", "Kronenstruktur sichtbar (135/335), kein strukturloser Schatten (U2); Baum oder Strauch offen, daher 4.2.", 1503)], ["n1", "U", "R"]),
 (100151, "0.2", "Etwas hellere, strukturierte Strauchkrone südlich von 140.", N, "4.2", False,
  [("klasse", "Strauchstruktur (130/378), Gehölz statt 0.2; Rand zur Wiese unscharf, evtl. beschattete Hochstauden.", 630)], ["n1", "K"]),
 (100145, "0.2", f"{KRONE}, zwei zusammengewachsene Kronen im Nordosten des Viertels.", N, "4.2", True,
  [("klasse", "Zwei Kronenlappen (279/350), Gehölz statt 0.2; Baumgruppe 4.2.2 möglich.", 1935)], ["n2", "U", "R"]),
 (100165, "0.2", f"{KRONE}, größte Krone der Baumgruppe am linken Kernrand (etwa 12 m).", N, "4.2", True,
  [("klasse", "Kronenstruktur (85/436), Gehölz statt 0.2; mit 171, 178, 184 eine Baumgruppe (4.2.2 möglich).", 2706)], ["n1", "n3", "k1"]),
 (100168, "4.2.1", "Kleines helleres Randstück zwischen Krone 165 und Wiese.", N, "4.2", False,
  [("verschmelzen", "Randstück (99/414) ohne Kante zu 165, mit 165 verschmelzen; als Einzelbaum zu klein.", 74)], ["n1", "k1"]),
 (100157, "0.2", f"{KRONE} in der Mitte des Viertels.", N, "4.2", True,
  [("klasse", "Kronenstruktur (174/421), Gehölz statt 0.2.", 1396)], ["n1", "k1"]),
 (100161, "0.2", "Zwei kleine dunkle Kronen südlich von 145, oben links etwas Gras eingeschlossen.", N, "4.2", True,
  [("klasse", "Kronenstruktur (291/412), Gehölz statt 0.2.", 645),
   ("grenze", "Helleres Gras im Nordwestzipfel (283/398) gehört zu 56.", 60)], ["n2"]),
 (100182, "3.1", "Wiesenrand zwischen Krone 165 und der offenen Wiese 166.", N, None, True,
  [("verschmelzen", "Gleiche Wiese ohne Kante zu 166 (89/482), mit 166 verschmelzen.", 189)], ["n3", "k1"]),
 (100178, "4.2.1", "Besonnter, heller Kronenteil in der Baumgruppe 165/171/184.", N, "4.2", False,
  [("grenze", "Hell besonnte Seite (108/469); ob eigene Krone oder Südostseite von 165/171, ist offen.", None)], ["n3", "k1"]),
 (100171, "0.2", f"{KRONE} in der Baumgruppe östlich von 165.", N, "4.2", True,
  [("klasse", "Kronenstruktur (135/455), Gehölz statt 0.2.", 1344)], ["n1", "n3", "k1"]),
 (100180, "0.2", f"{KRONE} im Südosten des Viertels am Trampelpfad.", N, "4.2", True,
  [("klasse", "Kronenstruktur (264/497), Gehölz statt 0.2.", 1537)], ["n4"]),
 (100186, "3.1", "Kleiner, etwas dunklerer Fleck in der verbuschten Wiese östlich von 180.", N, None, False,
  [("verschmelzen", "Keine Kante zur Umgebung (296/489), mit 56 verschmelzen; kleiner Strauch nicht ausgeschlossen.", 176)], ["n4"]),
 (100166, "3.1", "Gleichmäßige, offene Wiese im Südwesten und am Südrand, glatter als die verbuschte Fläche 56.", N, None, True,
  [("trennen", "Im Kern vier Teile (4200, 2142, 1105, 5 px), z. B. (88/539) und Südrand in v4: nicht zusammenhängend.", 7452),
   ("grenze", "Grenze zu 56 an der Südkante (250/560) ohne deutliche Bildkante, geschätzt.", None),
   ("verschmelzen", "Randstücke 182, 188, 193, 195 gehören zu dieser Wiese.", 1518)], ["n3", "n4", "K", "U"]),
 (100188, "3.1", "Wiesenstück zwischen Kronen 178/184 und Wiese 166.", N, None, True,
  [("verschmelzen", "Gleiche Wiese (103/500) ohne Kante, mit 166 verschmelzen.", 131)], ["n3", "k1"]),
 (100184, "0.2", f"{KRONE}, länglich, im Südteil der Baumgruppe.", N, "4.2", True,
  [("klasse", "Kronenstruktur (115/513), Gehölz statt 0.2.", 879)], ["n3", "k1"]),
 (100181, "4.2.4", f"{KRONE}, etwa 10 × 14 m, eher Baum oder Baumgruppe als niedriges Gebüsch.", N, "4.2", True,
  [("klasse", "Große Krone (178/505) mit Lichtpunkten, Strauchfläche nicht sicher; Gehölz 4.2.", 2179)], ["n3", "k1"]),
 (100193, "3.1", "Wiesenstück südlich der Krone 181.", N, None, True,
  [("verschmelzen", "Wiese ohne Kante zu 166 (190/545), mit 166 verschmelzen.", 451)], ["n3", "n4"]),
 (100192, "4.2.1", "Kleines Kronenstück am Südrand der Krone 180.", N, "4.2", False,
  [("verschmelzen", "Gehört zur Krone 180 (280/515), verschmelzen.", 110)], ["n4"]),
 (100195, "0.2", "Wiesenfläche am Südrand, kaum dunkler als die Umgebung; kein Schatten.", N, "3.1", True,
  [("klasse", "Farbe wie Wiese (140/550), keine Schattenfläche: 3.1, mit 166 verschmelzen.", 747)], ["n3", "k1"]),
]

NAHT = [
 (100166, "unten", "Wiese reicht über den unteren Kernrand; Teile im Kern nicht zusammenhängend."),
 (100195, "unten", "Klassenwechsel 0.2 zu 3.1 reicht bis an den unteren Kernrand."),
 (100165, "links", "Krone reicht über den linken Kernrand; Klasse Gehölz statt 0.2 auch dort."),
]
UNSICHER = [
 "100056 (v1): im Viertel v3 fehlen eigene Segmente für beschattete Kronen, z. B. (140/480) östlich von 171/178 und (285/360) zwischen 145 und 161.",
 "100056 (v1): heller Trampelpfad quer durch das Viertel (240/440) bis (310/520), 3–4 px breit, ohne eigenes Segment (6.6).",
 "100056 (v1): in v3 deutlich verbuscht (Hochstauden, kleine Sträucher); 3.5 oder 3.3 passender als 3.1.",
 "100138 (v1): Krone an der Grenze zu v3, wie 140 Gehölz.",
 "100172, 100176, 100177 (v4): am rechten Rand sichtbar, dunkle Kronen bzw. Wiesenrand.",
]
NICHT_GEPRUEFT = ["Werkzeug kante nicht benutzt; Grenzen nur am Bild beurteilt."]
OFFEN = [
 "Feinklasse der Kronen (Einzelbaum, Baumgruppe oder Gebüsch) bleibt offen; einheitlich 4.2 vorgeschlagen.",
 "100178: eigene Krone oder besonnte Seite der Nachbarkronen.",
]

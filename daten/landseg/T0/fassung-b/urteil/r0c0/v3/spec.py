VIERTEL = "v3"
UEBERSICHT = ["u", "ur"]
NAH = ["n1", "n2", "n3", "r3", "n4", "r4"]
EB = ("Gehölz", "Einzelbaum", "Einzelbaum")
BG = ("Gehölz", "Baumgruppe", "Baumgruppe")
GB = ("Gehölz", "Gebüsch", "Gebüsch oder kleiner Baum")
WI = ("Grünland", "Wiese", "Wiese")
SEG = [
 (100140, "0.2", "Dunkle Baumkrone mit Eigenschatten im Gebüsch am oberen Rand von v3.", "n",
  EB, True, [("klasse", "Kronenstruktur und Lichtpunkte erkennbar, Baum statt Schatten; Vorstufe hielt das für sicher (140/340).", 1503)], ["n1", "u"]),
 (100151, "0.2", "Etwas hellere, dunkle Krone unterhalb von 100140, Strauch oder Teil desselben Baums.", "n",
  GB, False, [("klasse", "Gehölz statt Schatten (130/375).", 630)], ["n1"]),
 (100145, "0.2", "Zwei ineinander greifende dunkle Kronen (Herzform) im Gebüsch.", "n",
  BG, True, [("klasse", "Kronen statt Schatten; Vorstufe hielt das für sicher (279/353).", 1935)], ["n2", "u"]),
 (100165, "0.2", "Große dunkle Krone am Westrand des Gebüschs mit Lichtpunkten, wohl ein bis zwei Bäume.", "n",
  BG, False, [("klasse", "Kronen statt Schatten; Vorstufe hielt das für sicher (85/436).", 2706),
              ("verschmelzen", "Der Splitter 100168 am Nordrand gehört zur Krone (99/414).", 74)], ["n1", "n3", "r3"]),
 (100168, "4.2.1", "Splitter am Nordrand der Krone 100165.", "n",
  BG, False, [("verschmelzen", "Splitter von 74 Bildpunkten, mit 100165 verschmelzen (99/414).", 74)], ["n1"]),
 (100157, "0.2", "Länglich-dunkle Krone eines Einzelbaums im Gebüsch.", "n",
  EB, True, [("klasse", "Baum statt Schatten; Vorstufe hielt das für sicher (174/421).", 1396)], ["n1", "u"]),
 (100161, "0.2", "Zwei kleine dunkle Kronen nahe dem Ostrand von v3.", "n",
  GB, False, [("klasse", "Gehölz statt Schatten (291/409).", 645)], ["n2"]),
 (100182, "3.1", "Grau-bläulicher Kronensaum zwischen Krone 100165 und Wiese, wie 100178.", "n",
  BG, False, [("verschmelzen", "Kronensaum statt Wiese; mit 100178 verschmelzen (89/481).", 189)], ["n3", "r3"]),
 (100178, "4.2.1", "Hellere, grau-bläuliche Krone zwischen 100165 und 100171.", "s",
  BG, False, [], ["n3", "r3"]),
 (100171, "0.2", "Dunkle Krone mit Lichtpunkten südöstlich von 100165.", "n",
  EB, False, [("klasse", "Baum statt Schatten (135/461).", 1344)], ["n1", "n3", "r3"]),
 (100180, "0.2", "Dunkle, große Baumkrone mit Eigenschatten am Trampelpfad.", "n",
  EB, True, [("klasse", "Baum statt Schatten; Vorstufe hielt das für sicher (264/497).", 1537),
             ("verschmelzen", "Der Kronenrand 100192 am Südrand gehört dazu (280/515).", 110)], ["n4", "r4"]),
 (100186, "3.1", "Kleiner hellerer Strauch im Gebüsch direkt am Trampelpfad, keine Wiese.", "n",
  ("Gehölz", "Gebüschfläche", "Gebüschfläche"), False,
  [("verschmelzen", "Ohne Bildkante im Gebüsch; mit der Gebüschfläche (heute 100056) verschmelzen (295/488).", 176)], ["n4", "r4"]),
 (100166, "3.1", "Glatte, gleichmäßige Wiese am Südwestrand des Gebüschs, Fortsetzung der großen Hangwiese.", "s",
  WI, False, [], ["n3", "r3", "n4", "u"]),
 (100188, "3.1", "Wiesenzipfel zwischen den Kronen 100178 und 100184, Teil der Wiese 100166.", "n",
  WI, True, [("verschmelzen", "Abgetrenntes Stück derselben Wiese; mit 100166 verschmelzen (103/501).", 131)], ["n3", "r3"]),
 (100184, "0.2", "Dunkle, längliche Krone am Wiesenrand.", "n",
  EB, False, [("klasse", "Baum statt Schatten (115/513).", 879)], ["n3", "r3"]),
 (100181, "4.2.4", "Mehrere dunkle Kronen mit Lichtpunkten im Süden des Gebüschs.", "s",
  BG, False, [], ["n3", "r3", "n4"]),
 (100193, "3.1", "Hellgrüner Grassaum zwischen der Krone 100181 und der Wiese.", "n",
  WI, False, [("verschmelzen", "Ohne Bildkante zur Wiese; mit 100166 verschmelzen (197/545).", 451)], ["n3", "r3", "n4", "r4"]),
 (100192, "4.2.1", "Südrand der Krone 100180.", "n",
  EB, False, [("verschmelzen", "Kronenrand, mit 100180 verschmelzen (280/515).", 110)], ["n4", "r4"]),
 (100195, "0.2", "Dunklere, glatte Grasstelle in der Wiese am Südrand von v3, keine Struktur von Gehölz.", "n",
  ("Grünland", "Wiese ungemäht", "Wiese ungemäht"), False,
  [("klasse", "Schatten ist keine Klasse und kein Baum steht südlich davon; dunkleres Gras, wohl höher oder feuchter (143/551).", 747)], ["n3", "r3"]),
]
NAHT = [
 {"id": 100166, "seite": "unten", "text": "Die Wiese läuft über die untere Kerngrenze nach r1c0 weiter; dort dieselbe Klasse."},
 {"id": 100195, "seite": "unten", "text": "Dunklere Grasstelle berührt die untere Kerngrenze; Grünland statt Schatten auch in r1c0."},
]
UNSICHER = [
 "100056 (v1): Der Teil in v3 ist dichtes Gebüsch mit Jungwuchs, keine Wiese; Trampelpfad schräg durch das Gebüsch nicht abgegrenzt (im Urteil v1 eingetragen).",
 "100172, 100176, 100177 (v4): Kronen und Saum am Ostrand von v3 gehören zum Gehölz 100177.",
]
NICHT_GEPRUEFT = ["nah1_roh.jpg, nah2_roh.jpg, uebersicht_kontrast.jpg, uebersicht_gitter.jpg, uebersicht_vorschlag.jpg und uebersicht_maengel.jpg nicht angesehen; Grenzen nicht mit dem Werkzeug kante nachgemessen."]
OFFEN = [
 "100165, 100145: ein oder zwei Bäume nicht sicher zu trennen.",
 "100195: höheres Gras, Feuchtstelle oder Schatten eines Geländeknicks nicht zu entscheiden.",
 "100151, 100161: Strauch oder kleiner Baum nicht zu entscheiden.",
]

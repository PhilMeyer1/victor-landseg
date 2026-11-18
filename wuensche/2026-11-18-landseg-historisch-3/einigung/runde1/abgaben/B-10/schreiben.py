import json
P=[
("r0c1:200363|r1c1:400011","gleich","3.1","Beide Seiten zeigen dieselbe glatte hell- bis mittelgraue Fläche ohne Kante (um 140–165 Grauwert), das Stück 363 liegt im Band der Straße, die vom Dreieck nach Südost zur Gabel mit der Bogenstraße läuft; der dunkle Punkt darin ist ein kleiner Gegenstand, keine eigene Fläche."),
("r0c1:200363|r1c1:400050","gleich","3.1","400050 ist dasselbe ursprüngliche Segment wie 200363 (gleiche Bildpunkte, nur an der Naht geteilt), gleiche graue Fläche ohne Kante; Kettenglied zu 400011, daher dieselbe Klasse Straße."),
("r0c1:200112|r1c1:400042","gleich","2.1.1","Gleichmäßig mittelgraue, glatte offene Fläche vor den Giebelenden der Häuser, die über die Naht ohne jede Kante weiterläuft; die dunkle Schräglinie liegt erst unterhalb in 400042 und gehört zur selben offenen Fläche (Hof offen, wie im Viertel benannt)."),
("r0c1:200350|r1c1:400042","grenze",None,"Nur ein Randpunkt: die schmale dunkle Schattenzunge (Schatten zwischen den Häusern, Grauwert um 50) endet an der Naht, darunter beginnt die mittelgraue offene Hoffläche; zwei verschiedene Flächen."),
("r0c1:200111|r1c1:400042","grenze",None,"Nur ein Randpunkt an der linken unteren Ecke des hellen Rechtecks 200111 (Grauwert um 175) gegen die dunklere mittelgraue offene Fläche 400042 (um 125); verschiedene Flächen."),
("r0c1:200111|r1c1:400041","gleich","1.1","Dasselbe helle, rechteckige Feld mit geraden Kanten, dünner dunkler Trennlinie zum Nachbarfeld und Schatten an der Westseite läuft ohne Kante über die Naht; Form und Schatten sprechen für eine Dachfläche, daher Gebäude statt Hof."),
("r0c1:200124|r1c1:400055","gleich","0","Dasselbe dunkle, fleckige Band unter dem Südrand der hellen Felder läuft ohne Kante über die Naht; ob Schlagschatten oder Gebüsch, ist im Schwarz-Weiß nicht zu trennen, daher die Elternklasse nicht bestimmbar."),
("r0c1:200124|r1c1:400029","grenze",None,"Nur ein Randpunkt: oben der dunkle Fleck 200124 (Grauwert um 65), darunter die mittelgraue, fleckige Fläche 400029 neben der Bogenstraße (um 110); verschiedene Flächen."),
("r0c1:200123|r1c1:400029","grenze",None,"Der kleine dunkle Fleck 200123 (Grauwert 50–75) endet mit weichem Übergang knapp über der Naht, darunter liegt die hellere mittelgraue Fläche 400029 (um 130–150); verschiedene Flächen."),
("r0c1:200110|r1c1:400057","grenze",None,"Nur ein Randpunkt am Ausschnittrand: oben das helle Band der nach Nordost abzweigenden Straße 200110, darunter beginnt die große dunkle, fleckige Fläche 400057 (Grauwert fällt von 120 auf 45); verschiedene Flächen."),
("r0c1:200125|r1c1:400057","gleich","0","200125 (2 Bildpunkte im Kern) und 400057 sind dieselbe große dunkle, fleckige Fläche südöstlich der Straße (im Kontextrand beider Teilkacheln deckungsgleich); Schatten der Häuser oder Gehölz ist im Schwarz-Weiß nicht zu trennen, daher die Elternklasse nicht bestimmbar."),
]
d={"schema":"landseg-einigung-abgabe/1","fassung":"B","buendel":"B-10","bearbeiter":"agent:einigung-B-10:20261118i-r1",
 "paare":[{"paar":p,"entscheidung":e,"klasse":k,"grund":g} for p,e,k,g in P],
 "offen":[
  "Paare 1-3: Straße (400011, 200363, 400050) und offene Fläche (200112, 400042) gehen an der Straßengabel ohne sichtbare Kante ineinander über; ob 200112/400042 Hof (2.1.1) oder Platz/Vorplatz (3.4) ist, ist im Schwarz-Weiß nicht sicher; gewählt wurde die Benennung des Viertels.",
  "400042 enthält unten eine dunkle Schräglinie mit hellem Fleck darunter (x 880-905, y 503-522), womöglich ein kleiner Bau mit Schatten; Grenzen wurden nicht geändert.",
  "Paar 6: 200111/400041 als Gebäude (1.1) nach Form und Schatten; Hof nicht ganz ausgeschlossen.",
  "Paare 7 und 11: dunkle Flächen als 0 (nicht bestimmbar), weil Schatten und Gehölz nicht zu trennen sind.",
  "400057 hat an der Naht (x 997-1005, y 500-505) eine helle Zunge, die eher zur Straße gehört; nur Grenzfrage, nicht geändert."],
 "nicht_geprueft":[]}
json.dump(d,open("einigung_abgabe.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)

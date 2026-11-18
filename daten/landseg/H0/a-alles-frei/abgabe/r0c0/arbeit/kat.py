import json
K = [
 ('1', 'Siedlung / Hofstellen', None, '#c0392b', 'Häuser, Höfe und Gärten im Ort: kleinteilige Wechsel von hell und dunkel, gerade Kanten'),
 ('1.1', 'Gebäude', '1', '#e74c3c', 'Dachfläche mit geraden Kanten; Satteldach als heller und dunkler Streifen nebeneinander, Schlagschatten an der Nordostseite'),
 ('1.1.1', 'Hauptgebäude (langes Haus eines Streckhofs)', '1.1', '#ff6f61', 'langer, schmaler Baukörper quer zur Straße oder entlang der Parzelle, durchgehende Dachkante'),
 ('1.1.2', 'Nebengebäude / Schuppen', '1.1', '#ff9e80', 'kleiner, freistehender heller Baukörper mit Schatten'),
 ('1.2', 'Hofraum', '1', '#f5b7b1', 'offene, mittelgraue Fläche zwischen Gebäuden einer Hofstelle'),
 ('1.3', 'Hofstelle ungetrennt (Dach oder Hof)', '1', '#d98880', 'Parzellenstreifen zwischen dunklen Grenzlinien, Dach und Hof auf dem Scan nicht trennbar'),
 ('1.4', 'Garten / Grünfläche im Ort', '1', '#a9cce3', 'gleichmäßig dunkelgraue, feinkörnige Fläche zwischen Straßen, ohne Bauten'),
 ('1.5', 'Mauer / Einfriedung', '1', '#7b241c', 'schmale, durchgehende dunkle Linie an Parzellengrenzen (Mauer, Zaun oder Hecke samt Schatten)'),
 ('2', 'Verkehrsfläche', None, '#7f8c8d', 'helle, lange Bänder mit parallelen Kanten'),
 ('2.1', 'Straße (Fahrbahn)', '2', '#bdc3c7', 'breites, sehr helles Band mit gleichbleibender Breite'),
 ('2.2', 'Weg / Gasse', '2', '#d5dbdb', 'schmales helles Band, oft weicher Rand'),
 ('2.3', 'Straßenrand (Bankett, Gehweg, Vorplatz)', '2', '#aab7b8', 'schmaler mittelgrauer Streifen parallel zur Fahrbahn'),
 ('3', 'Landwirtschaftliche Fläche', None, '#b7950b', 'große gleichmäßige Flächen außerhalb des Orts, mit Bearbeitungsstreifen'),
 ('3.1', 'Acker (Streifenparzelle)', '3', '#f4d03f', 'lange, parallele Streifen gleicher Richtung, feine Längsstruktur; Grenzen als hellere Raine'),
 ('4', 'Gehölz', None, '#1e8449', 'dunkle, runde oder gereihte Flecken mit weichem Rand und Schatten'),
 ('4.1', 'Einzelbaum / Busch', '4', '#27ae60', 'einzelner dunkler runder Fleck, Schatten daneben'),
 ('4.2', 'Baumreihe / Hecke', '4', '#52be80', 'Reihe dunkler Flecken entlang einer Straße oder Feldgrenze'),
 ('5', 'Offene Fläche (unbebaut, nicht Acker)', None, '#8e44ad', 'unregelmäßig helle Flächen ohne Streifen und ohne Bauten'),
 ('5.1', 'Anger / Dorfplatz / Freifläche', '5', '#c39bd3', 'offene, fleckig helle Fläche im Ort mit Trittspuren und Wegen'),
 ('5.2', 'Brache / Weide am Ortsrand', '5', '#d7bde2', 'helle, fleckige Fläche mit einzelnen Büschen am Ortsrand'),
 ('9', 'Unklar', None, '#2c3e50', 'Fläche, deren Art auf dem Scan nicht erkennbar ist'),
 ('9.1', 'Schatten (Untergrund nicht erkennbar)', '9', '#34495e', 'tiefschwarze Fläche an der Nordostseite eines Baukörpers oder Baums'),
 ('9.2', 'dunkle Fläche unklar (Baumgruppe oder dunkles Dach)', '9', '#566573', 'dunkler Block ohne erkennbare Dach- oder Kronenform'),
 ('9.3', 'helles Kleinobjekt unklar (Schuppen, Haufen)', '9', '#f7dc6f', 'kleiner sehr heller Fleck ohne erkennbare Form'),
]
classes = []
for code, name, parent, color, cue in K:
    classes.append(dict(code=code, name=name, parent=parent, level=code.count('.') + 1, color=color, image_cue=cue))
json.dump({'schema': 'landseg-kategorien/1', 'teilkachel': 'r0c0', 'fassung': 'A (Alles frei)',
           'hinweis': 'Eigene Liste für den Schwarz-Weiß-Scan von 1968; Farben nur für die Darstellung.',
           'classes': classes},
          open('C:/Users/Phil/Developement/Victor/daten/landseg/H0/a-alles-frei/abgabe/r0c0/kategorien-teil.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print(len(classes))

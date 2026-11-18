# Neuschrift des Urteils r0c0 v2 (Fassung B) durch urt-b-r0c0-v2 (Nachholauftrag).
# Liest die aktuelle Karte, schreibt urteil.json und die Bilder roh/umriss/maengel/vorschlag.
import json
import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi

D = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
OUT = D + "b-kategorien-frei/urteil/r0c0/v2/"
VB = D + "viertel/r0c0/v2/"
SEGJ = D + "b-kategorien-frei/r0c0/segmente.json"
LAB = D + "b-kategorien-frei/r0c0/labels.tif"
BILD = D + "teilkacheln/r0c0.png"

U, R = VB + "uebersicht_nummern.jpg", VB + "uebersicht_roh.jpg"
N1, N2, N3, N4 = (VB + f"nah{i}_nummern.jpg" for i in range(1, 5))
R1, R3 = VB + "nah1_roh.jpg", VB + "nah3_roh.jpg"
A = OUT + "nah_2.jpg"
V = 100000

# Klassen: (grob, mittel, fein)
K = {
    "HOF": ("Hof und Garten", "Hof", "Hof"),
    "HOFSCH": ("Hof und Garten", "Hof", "Hof im Schatten"),
    "GARTEN": ("Hof und Garten", "Garten", "Garten"),
    "LAENGSBAU": ("Gebäude", "Dach", "Längsbau"),
    "NEBENGEB": ("Gebäude", "Dach", "Nebengebäude"),
    "DACH": ("Gebäude", "Dach", "Dach"),
    "FAHRWEG": ("Verkehrsfläche", "Straße/Weg", "Fahrbahn"),
    "STRASSENRAND": ("Verkehrsfläche", "Straße/Weg", "Straßenrand"),
    "FELDWEG": ("Verkehrsfläche", "Straße/Weg", "Hinterweg"),
    "FELD": ("Landwirtschaft", "Feld", "Feld"),
    "ANGER": ("Grünfläche", "Anger", "Anger"),
    "WEGRAIN": ("Grünfläche", "Saum", "Wegrain"),
    "FELDRAIN": ("Grünfläche", "Saum", "Feldrain"),
    "BAUM": ("Gehölz", "Gebüsch/Baum", "Baum"),
    "GEBUESCH": ("Gehölz", "Gebüsch/Baum", "Gebüsch"),
    "SCHATTEN": ("Unklar", "Schatten", "Schlagschatten"),
    "DUNKEL": ("Unklar", "Dunkle Fläche", "Dunkle Fläche"),
}
KLASSEN_FREI = [
    ("Gebäude", "grob", None, "scharf begrenzte Fläche mit geraden Kanten und Schlagschatten daneben"),
    ("Dach", "mittel", "Gebäude", "Dachfläche, hell bis mittelgrau, gerade Kanten; Wohn- oder Wirtschaftsbau im Schwarz-Weiß-Bild nicht zu trennen"),
    ("Längsbau", "fein", "Dach", "langes schmales helles Dach längs des Grundstücks, quer zur Straße (Streckhof)"),
    ("Nebengebäude", "fein", "Dach", "kleiner, scharf begrenzter heller Bau im Hof oder am Hofende"),
    ("Hof und Garten", "grob", None, "Flächen innerhalb der Grundstücke zwischen den Gebäuden"),
    ("Hof", "mittel", "Hof und Garten", "mittelgraue offene Fläche zwischen den Längsbauten, ohne Gartenkorn"),
    ("Hof im Schatten", "fein", "Hof", "fast schwarze Hoffläche im Schlagschatten des Nachbarbaus, Untergrund nicht sichtbar"),
    ("Garten", "mittel", "Hof und Garten", "von dunklen Mauer- oder Zaunlinien umrahmtes Rechteck mit fleckigem Grau"),
    ("Verkehrsfläche", "grob", None, "lange, gleichmäßig breite, helle Bänder"),
    ("Straße/Weg", "mittel", "Verkehrsfläche", "helles Band mit parallelen Rändern; Belag im Schwarz-Weiß-Bild nicht bestimmbar"),
    ("Fahrbahn", "fein", "Straße/Weg", "durchgehend sehr helles Band von etwa 10 Bildpunkten Breite"),
    ("Straßenrand", "fein", "Straße/Weg", "mittelgrauer, gleichmäßiger Streifen zwischen Fahrbahn und Hof oder Feld"),
    ("Hinterweg", "fein", "Straße/Weg", "schmaler heller Weg oder Fahrspur hinter den Höfen"),
    ("Landwirtschaft", "grob", None, "große gleichmäßige Flächen außerhalb der Höfe"),
    ("Feld", "mittel", "Landwirtschaft", "große, gleichmäßig dunkelgraue Fläche mit feinem Korn; Acker oder Grünland nicht zu trennen"),
    ("Grünfläche", "grob", None, "unbebaute, unversiegelte Flächen mit fleckiger Textur ohne Feldstruktur"),
    ("Anger", "mittel", "Grünfläche", "offene, fleckig mittelgraue Fläche hinter den Höfen mit hellen Fahrspuren"),
    ("Saum", "mittel", "Grünfläche", "schmaler Streifen zwischen Weg oder Hof und Feld"),
    ("Wegrain", "fein", "Saum", "Streifen neben einer Fahrbahn, dunkler als der Weg, heller oder fleckiger als das Feld"),
    ("Feldrain", "fein", "Saum", "fleckiger Randstreifen am Feldrand"),
    ("Gehölz", "grob", None, "dunkle, rundliche, unscharf begrenzte Flecken"),
    ("Gebüsch/Baum", "mittel", "Gehölz", "dunkle Flecken oder Ketten von Flecken am Weg- oder Feldrand"),
    ("Baum", "fein", "Gebüsch/Baum", "einzelne runde dunkle Krone mit Schatten"),
    ("Gebüsch", "fein", "Gebüsch/Baum", "kleiner, weniger dunkler Fleck am Rand"),
    ("Unklar", "grob", None, "Fläche, deren Oberfläche im Bild nicht zu sehen ist"),
    ("Schatten", "mittel", "Unklar", "fast schwarzer Streifen unmittelbar neben einem Gebäude"),
    ("Schlagschatten", "fein", "Schatten", "fast schwarzer Streifen an der Seite eines Gebäudes, abgewandt vom Licht"),
    ("Dunkle Fläche", "mittel", "Unklar", "fast schwarze, eckige Fläche ohne Textur: Schatten, dunkles Dach oder Gehölz"),
]

# (id, klasse, sicher, urteil, was_ist_es, punkte[(art, text, (x,y), flaeche)], bilder)
S = [
 (V+45, "HOFSCH", False, "nicht_sauber", "Hof im Schlagschatten zwischen den Längsbauten 264 und 265; den hellen Längsbau am linken Rand abgetrennt.", [
     ("trennen", "Heller Längsbau 312–332/75–105 steckte im Hof; abgetrennt als 100264.", (322, 90), 272)], [U, N1, R1, A]),
 (V+264, "LAENGSBAU", True, "sauber", "Helles schmales Dach eines Längsbaus (neu aus 45), Schattenhof 45 daneben.", [], [N1, A]),
 (V+41, "HOFSCH", False, "sauber", "Schmaler Hofstreifen am oberen Kernrand im Schatten, Untergrund kaum sichtbar.", [], [U, N1, R1]),
 (V+37, "HOFSCH", False, "nicht_sauber", "Hof im Schatten des Nachbarbaus; den hellen Längsbau 265 abgetrennt.", [
     ("trennen", "Heller Längsbau 395–428/78–114 steckte im Hof; abgetrennt als 100265.", (410, 95), 282)], [U, N1, R1, A]),
 (V+265, "LAENGSBAU", True, "sauber", "Langes helles Dach eines Längsbaus (neu aus 37), Schattenhof 37 daneben.", [], [N1, A]),
 (V+28, "HOFSCH", False, "nicht_sauber", "Hof im Schatten zwischen zwei Längsbauten am oberen Kernrand; Dachstück 266 abgetrennt.", [
     ("trennen", "Helles Dachstück 418–432/65–80 im Kern abgetrennt als 100266; der Rest des Dachs liegt im Kontextrand.", (425, 72), 166)], [U, N1, N2, A]),
 (V+266, "LAENGSBAU", False, "sauber", "Kernstück eines hellen Längsbaudachs am oberen Kernrand (neu aus 28); nur ein kurzes Stück im Kern.", [], [N2, A]),
 (V+50, "GARTEN", False, "sauber", "Kleine graue Fläche nördlich der Straße am oberen Kernrand, Garten oder Hof.", [], [U, N2]),
 (V+12, "GARTEN", False, "sauber", "Kernstück einer großen fleckig grauen Fläche im Kontextrand nördlich der Kreuzung, Garten oder Feld.", [], [U, N2]),
 (V+53, "GARTEN", False, "sauber", "Fleckige graue Fläche nördlich der Kreuzung, Garten oder Hof.", [], [U, N2]),
 (V+54, "HOF", False, "sauber", "Gleichmäßig mittelgraue kleine Hoffläche nördlich der Kreuzung.", [], [U, N2]),
 (V+60, "STRASSENRAND", False, "sauber", "Hellgrauer offener Platz an der Nordseite der Kreuzung, ohne Dach und Schatten.", [], [U, N2]),
 (V+49, "HOFSCH", False, "sauber", "Dunkle, beschattete kleine Fläche am oberen Kernrand.", [], [U, N2]),
 (V+20, "HOF", False, "sauber", "Nur 7 Bildpunkte im Kern am oberen Kernrand, Hauptteil im Kontextrand.", [], [U, N2]),
 (V+46, "HOF", False, "sauber", "Mittelgrauer Hofstreifen zwischen den Längsbauten 42 und 56.", [], [U, N2]),
 (V+56, "HOFSCH", False, "nicht_sauber", "Hof im Schatten des Längsbaus 42; den hellen Dachstreifen 269 abgetrennt.", [
     ("trennen", "Heller Dachstreifen 525–546/80–95 steckte im Hof; abgetrennt als 100269.", (535, 87), 101)], [U, N2, A]),
 (V+269, "LAENGSBAU", False, "sauber", "Schmaler heller Dachstreifen (neu aus 56), kurz und unscharf.", [], [N2, A]),
 (V+42, "LAENGSBAU", True, "sauber", "Sehr helles, scharf begrenztes Dach am oberen rechten Kernrand mit dunklem Schatten daneben.", [], [U, N2]),
 (V+73, "FELDWEG", False, "sauber", "Heller Hinterweg vom Weg 64 zur Einmündung 109, mit hellen Flecken.", [], [U, N1, R1]),
 (V+89, "NEBENGEB", False, "sauber", "Sehr heller kleiner Fleck 332–342/133–144 am Hinterweg: kleiner heller Bau oder heller Haufen.", [], [U, N1, R1]),
 (V+71, "HOFSCH", False, "sauber", "Dunkle, beschattete Fläche am hinteren Ende des Hofs 45 am Hinterweg.", [], [U, N1, R1]),
 (V+82, "HOF", False, "sauber", "Kleine graue Fläche zwischen Hinterweg 73 und Garten 66.", [], [U, N1, R1]),
 (V+66, "GARTEN", False, "nicht_sauber", "Ummauertes Rechteck mit fleckigem Dunkelgrau, links beschattet; den hellen Bau 268 am unteren Ende abgetrennt.", [
     ("trennen", "Heller schmaler Bau 388–403/131–155 steckte im Garten; abgetrennt als 100268.", (395, 143), 162)], [U, N1, R1, A]),
 (V+268, "NEBENGEB", False, "sauber", "Heller schmaler Bau am hinteren Ende des Gartens 66 (neu aus 66).", [], [N1, A]),
 (V+62, "GARTEN", False, "sauber", "Großes ummauertes Rechteck mit gleichmäßig mittelgrauem Korn zwischen 66, 37 und der Straße.", [], [U, N1, R1]),
 (V+84, "STRASSENRAND", False, "sauber", "Heller Streifen am Nordrand der Straße 30.", [], [U, N1, N2]),
 (V+86, "STRASSENRAND", False, "sauber", "Heller Streifen am Südrand der Straße 30.", [], [U, N2]),
 (V+69, "STRASSENRAND", False, "sauber", "Mittelgrauer Streifen zwischen Straße 30 und Garten 62 mit dunklem Fleck bei 477/113.", [], [U, N2]),
 (V+87, "BAUM", False, "sauber", "Dunkler runder Fleck am Südrand der Straße: Baum oder Busch mit Schatten.", [], [U, N2]),
 (V+30, "FAHRWEG", False, "sauber", "Helle Straßenkreuzung mit drei Ästen (nach Nordwest, Südost und zur Einmündung 109).", [], [U, N2, A]),
 (V+79, "STRASSENRAND", False, "sauber", "Schmaler mittelgrauer Streifen zwischen Straße und Hof 63.", [], [U, N2]),
 (V+63, "HOFSCH", False, "sauber", "Hof im Schatten zwischen Längsbau 56 und der Straße.", [], [U, N2]),
 (V+32, "HOFSCH", False, "sauber", "Kernstück eines beschatteten Hofs am rechten Kernrand, Hauptteil in r0c1.", [], [U, N2]),
 (V+81, "LAENGSBAU", False, "sauber", "Kernstück eines hellen Dachs am rechten Kernrand (547–563/122–145).", [], [U, N2]),
 (V+70, "DACH", False, "sauber", "Nur 45 Bildpunkte im Kern am rechten Kernrand; heller Teil eines Baus in r0c1.", [], [U, N2]),
 (V+94, "ANGER", False, "sauber", "Gleichmäßig graue offene Fläche zwischen Hinterweg 73 und 100, wie Anger 77.", [], [U, N1, N3]),
 (V+100, "DUNKEL", False, "nicht_sauber", "Fast schwarze Fläche neben dem hellen Bau 271: Schatten, dunkles Dach oder Gehölz; den hellen Bau 271 abgetrennt.", [
     ("trennen", "Heller Bau 333–347/161–186 steckte in der dunklen Fläche; abgetrennt als 100271.", (340, 173), 175)], [U, N1, N3, A]),
 (V+271, "NEBENGEB", False, "sauber", "Heller schmaler Bau (neu aus 100).", [], [N1, A]),
 (V+110, "HOF", False, "sauber", "Kleine graue Fläche zwischen 100 und der Einmündung 109.", [], [U, N1, N3]),
 (V+109, "FAHRWEG", False, "sauber", "Helle Einmündung von Hinterweg 73 und Straße 30 in die Straße nach Süden.", [], [U, N1, N3]),
 (V+96, "WEGRAIN", False, "sauber", "Mittelgrauer Streifen am Südrand der Straße mit dunklen Flecken (Büsche).", [], [U, N2, N3]),
 (V+95, "GEBUESCH", False, "sauber", "Dunklerer Fleck am Straßenrand, Busch.", [], [U, N2]),
 (V+125, "HOF", False, "sauber", "Kleine hellere Fläche zwischen Feld 83 und dem Längsbau 127.", [], [U, N4]),
 (V+83, "FELD", False, "sauber", "Große, gleichmäßig dunkelgraue Fläche zwischen den Straßen; eine schwache Tonstufe ohne Kante, nicht geteilt.", [], [U, N2, N4, A]),
 (V+111, "HOF", False, "nicht_sauber", "Beschatteter Hof am rechten Kernrand mit schmalem hellem Bau 534–547/183–210.", [
     ("trennen", "Schmaler heller Bau 534–547/183–210 steckt im Hof; nicht geteilt, weil der Schnitt das Segment über den Kernrand zerlegt hätte.", (540, 196), 167)], [U, N2, N4]),
 (V+107, "WEGRAIN", False, "sauber", "Mittelgraues Eckstück zwischen Straße 30, Feld 83 und Hof 111.", [], [U, N2]),
 (V+92, "STRASSENRAND", False, "sauber", "Mittelgrauer Streifen an der Straße am rechten Kernrand.", [], [U, N2]),
 (V+112, "SCHATTEN", False, "sauber", "Fast schwarzer Fleck am rechten Kernrand neben einem Bau in r0c1.", [], [U, N2]),
 (V+104, "ANGER", False, "nicht_sauber", "Offene, fleckige Fläche zwischen Hinterweg, Straße und Feld 154; die helle Fahrspur 272 abgetrennt.", [
     ("trennen", "Helle Fahrspur 318–386/213–244 (Fortsetzung der Spur im Anger 114) abgetrennt als 100272.", (350, 228), 792),
     ("sonstiges", "Dunkler Fleck 354–366/250–264 und dunkle Fläche 361–396/185–224 bleiben im Segment: Busch oder Schatten, Kante zu unscharf zum Teilen.", (360, 257), None)], [U, N3, R3, A]),
 (V+272, "FELDWEG", False, "sauber", "Hellste, gerade Spur über den Anger zur Einmündung 109 (neu aus 104), ohne Schlagschatten daneben; ein flacher heller Bau wäre auch möglich.", [], [N3, R3, A]),
 (V+137, "BAUM", False, "sauber", "Dunkler Fleck am Westrand der Straße nach Süden.", [], [U, N3, R3]),
 (V+117, "FAHRWEG", False, "sauber", "Westliches helles Band der Straße nach Süden.", [], [U, N3, R3]),
 (V+126, "WEGRAIN", False, "sauber", "Schmaler Streifen zwischen Straße 117 und Feld 83.", [], [U, N3]),
 (V+145, "DUNKEL", False, "sauber", "Fast schwarze Fläche mit geraden Rändern östlich der Straße am Westende des Baus 142: Schatten, dunkles Dach oder Baumgruppe.", [], [U, N3, N4, A]),
 (V+141, "DUNKEL", False, "sauber", "Dunkle Fläche neben 145, gleiche Art.", [], [U, N4]),
 (V+139, "SCHATTEN", False, "sauber", "Dunkle kleine Fläche am Westende des Hofs 128 neben dem Längsbau 127.", [], [U, N4]),
 (V+130, "HOF", False, "sauber", "Hellere fleckige Fläche vor dem Längsbau 127 mit zwei hellen Punkten.", [], [U, N4]),
 (V+127, "LAENGSBAU", True, "sauber", "Langes helles Dach, scharf begrenzt, dunkler Streifen daneben.", [], [U, N4]),
 (V+128, "HOF", False, "nicht_sauber", "Hofstreifen zwischen den Längsbauten 127 und 142 und Hof rechts davon; das helle Dachstück dem Bau 142 zugeschlagen.", [
     ("trennen", "Helles Dachstück 472–518/226–254 steckte im Hof; abgetrennt und mit dem Dach 142 verschmolzen.", (478, 248), 421)], [U, N4, A]),
 (V+148, "DUNKEL", False, "sauber", "Fast schwarze, eckige Fläche 305–337/240–270: Schatten, dunkles Dach oder Gehölz.", [], [U, N3, R3]),
 (V+156, "NEBENGEB", False, "sauber", "Hellgraue rechteckige Fläche mit Schattenstreifen 164 daneben: Bau mit hellem Dach.", [], [U, N3, R3]),
 (V+164, "SCHATTEN", False, "sauber", "Dunkler Streifen an der Unterseite von 156.", [], [U, N3, R3]),
 (V+151, "NEBENGEB", False, "nicht_sauber", "Heller Fleck zwischen 148 und 156, gleicher Grauton wie 156.", [
     ("verschmelzen", "Wahrscheinlich Teil des Baus 156 (341/251), Grenze ohne klare Bildkante; nicht verschmolzen, weil die Zugehörigkeit nicht sicher ist.", (341, 251), 128)], [U, N3, R3]),
 (V+155, "FELDRAIN", False, "sauber", "Schmaler Randstreifen zwischen Anger 104 und Feld 154.", [], [U, N3, R3]),
 (V+150, "WEGRAIN", False, "sauber", "Kleines Stück am Westrand der Straße nach Süden.", [], [U, N3, R3]),
 (V+161, "GEBUESCH", False, "sauber", "Dunklerer Fleck am Westrand der Straße, Busch.", [], [U, N3, R3]),
 (V+166, "BAUM", False, "sauber", "Dunkler Fleck am Westrand der Straße, Baum oder Busch.", [], [U, N3, R3]),
 (V+149, "FAHRWEG", False, "sauber", "Östliches helles Band der Straße nach Süden, reicht in v4.", [], [U, N3, R3]),
 (V+158, "BAUM", False, "sauber", "Kleine dunkle Fläche zwischen 145 und Straße, Busch oder Schatten.", [], [U, N3, N4]),
 (V+142, "LAENGSBAU", True, "nicht_sauber", "Großes helles Dach eines Längsbaus; um das abgetrennte Dachstück aus 128 ergänzt.", [
     ("verschmelzen", "Dachstück aus 128 (472–518/226–254) zugeschlagen, gleiche Dachfläche in einer Flucht.", (495, 240), 421)], [U, N4, A]),
 (V+167, "LAENGSBAU", False, "sauber", "Langes mittelgraues Dach mit hellerem Teil zwischen dunklen Streifen.", [], [U, N4]),
 (V+144, "LAENGSBAU", True, "sauber", "Langes helles Dach am rechten Kernrand.", [], [U, N4]),
 (V+169, "BAUM", False, "sauber", "Fast schwarzer länglicher Fleck an der Straße: Baum mit Schatten.", [], [U, N3, R3]),
 (V+153, "HOF", False, "nicht_sauber", "Hof mit dunklem Fleck am rechten unteren Rand; das helle Dachstück 274 abgetrennt.", [
     ("trennen", "Helles Dachstück 532–555/289–313 steckte im Hof; abgetrennt als 100274.", (543, 300), 255)], [U, N4, A]),
 (V+274, "LAENGSBAU", False, "sauber", "Helles Dachstück (neu aus 153).", [], [N4, A]),
]

EINGRIFFE = [
 {"schritt": "teilen", "vorher": [V+45], "nachher": [V+45, V+264], "grund": "Heller Längsbau 312–332/75–105 steckte im Schattenhof 45; Splitter beim Schnitt wieder dem Bau zugeschlagen."},
 {"schritt": "teilen", "vorher": [V+37], "nachher": [V+37, V+265], "grund": "Heller Längsbau 395–428/78–114 steckte im Hof 37; Splitter wieder dem Bau zugeschlagen."},
 {"schritt": "teilen", "vorher": [V+28], "nachher": [V+28, V+266], "grund": "Helles Dachstück im Kern 418–432/65–80 steckte im Schattenhof 28."},
 {"schritt": "teilen", "vorher": [V+66], "nachher": [V+66, V+268], "grund": "Heller Bau 388–403/131–155 steckte im Garten 66; Splitter wieder dem Bau zugeschlagen."},
 {"schritt": "teilen", "vorher": [V+56], "nachher": [V+56, V+269], "grund": "Heller Dachstreifen 525–546/80–95 steckte im Schattenhof 56."},
 {"schritt": "teilen", "vorher": [V+100], "nachher": [V+100, V+271], "grund": "Heller Bau 333–347/161–186 steckte in der dunklen Fläche 100."},
 {"schritt": "teilen", "vorher": [V+104], "nachher": [V+104, V+272], "grund": "Helle Fahrspur 318–386/213–244 steckte im Anger 104."},
 {"schritt": "teilen", "vorher": [V+128], "nachher": [V+128, V+142], "grund": "Helles Dachstück 472–518/226–254 im Hof 128 abgetrennt und mit dem Dach 142 verschmolzen (gleiche Dachfläche)."},
 {"schritt": "teilen", "vorher": [V+153], "nachher": [V+153, V+274], "grund": "Helles Dachstück 532–555/289–313 steckte im Hof 153."},
]
UNSICHER = [
 "100143 (v4): große Fläche südlich der Längsbauten 142/167; Hof oder Straße, in v4 zu urteilen; das Stück 100276 (aus 143 geteilt, bei 443/285) liegt im Bild dieses Viertels, gehört aber v4.",
 "100154 (v3/v4): Feld; die Randstreifen 155/164 grenzen ohne klare Bildkante daran.",
 "100077, 100115 (v1): Anger und heller Bau neben dem Anger 104.",
]
NICHT_GEPRUEFT = [
 "Naht zu r0c1 (rechter Kernrand x 563): Segmente und Urteile auf der anderen Seite nicht angesehen; 32, 70, 81, 92, 111, 112, 128, 144, 153 reichen dorthin.",
 "Eigene Bilder des ersten Durchgangs nah_1.jpg, nah_3.jpg, kontrast_1.jpg nicht angesehen; geurteilt auf den vorbereiteten Bildern und nah_2.jpg.",
 "uebersicht_kontrast.jpg, uebersicht_vorschlag.jpg, uebersicht_maengel.jpg, uebersicht_gitter.jpg, nah2_roh.jpg, nah4_roh.jpg nicht angesehen.",
]
OFFEN = [
 "Feld 83 und Gärten 12/50/53/62/66: Acker, Grünland oder Gemüsegarten im Schwarz-Weiß-Bild nicht zu trennen; im Farbbild Grün gegen Braun und Reihen.",
 "83: schwache Tonstufe von etwa 480/130 nach 505/200 (rechts heller) deutet zwei Parzellen an; keine Kante, nicht geteilt; im Farbbild prüfen.",
 "Straßen 30, 109, 117, 149 und Ränder 60/69/79/84/86/92: Belag nicht bestimmbar; im Farbbild Asphalt (dunkelgrau) gegen Schotter oder Erde.",
 "272: helle gerade Spur in Verlängerung der Fahrspur des Angers 114 ohne Schlagschatten, darum als Weg geurteilt; ein flacher heller Bau wäre möglich (im Farbbild Dachfarbe).",
 "100, 145, 141, 148: fast schwarze, eckige Flächen; Schatten, dunkles Dach oder Gehölz; im Farbbild Grün (Gehölz) gegen Dachfarbe, sonst Schattenrichtung aus der Aufnahmezeit.",
 "151: wahrscheinlich Teil des Baus 156; im Farbbild gleiche Dachfarbe würde das Verschmelzen tragen.",
 "111: schmaler heller Bau 534–547/183–210 im Hof nicht abgetrennt (Schnitt hätte das Segment über den Kernrand zerlegt); bei der Naht mit r0c1 klären.",
 "Höfe im Schatten (41, 45, 28, 37, 49, 56, 63, 71, 32): Untergrund unter dem Schlagschatten nicht sichtbar.",
]


def main():
    seg = json.load(open(SEGJ, encoding="utf-8"))
    heute = {s["id"]: s["klasse"] for s in seg["segmente"]}
    L = tifffile.imread(LAB)
    segmente = []
    alle_bilder = set()
    for sid, k, sicher, urt, was, punkte, bilder in S:
        assert sid in heute, sid
        g, m, f = K[k]
        pp = []
        for i, (art, text, xy, fl) in enumerate(punkte, 1):
            pp.append({"nr": i, "art": art, "text": text, "flaeche_px": fl})
        b = list(dict.fromkeys(bilder))
        alle_bilder.update(b)
        segmente.append({"id": sid, "klasse_heute": heute[sid], "was_ist_es": was, "urteil": urt,
                         "klasse_vorschlag": None, "klasse_frei": {"grob": g, "mittel": m, "fein": f},
                         "sicher": sicher, "punkte": pp, "bilder": b})
    benutzt = set()
    for k in {x[1] for x in S}:
        benutzt.update(K[k])
    kf = [{"name": n, "ebene": e, "eltern": p, "merkmal": mk} for n, e, p, mk in KLASSEN_FREI if n in benutzt]
    namen = {x["name"] for x in kf}
    assert benutzt <= namen, benutzt - namen
    eigene = [OUT + n for n in ("roh.jpg", "umriss.jpg", "maengel.jpg", "vorschlag.jpg")]
    urteil = {
        "teilkachel": "r0c0", "viertel": "v2", "bearbeiter": "urt-b-r0c0-v2",
        "bilder_angesehen": {
            "uebersicht": [D + "H0.png", D + "ganz/r0c0/ganz_nummern.jpg", U, R] + eigene,
            "nah": [N1, R1, N2, N3, R3, N4, A],
        },
        "segmente": segmente, "naht": [], "unsicher": UNSICHER, "nicht_geprueft": NICHT_GEPRUEFT,
        "offen": OFFEN, "eingriffe": EINGRIFFE, "klassen_frei": kf,
    }
    gesehen = set(urteil["bilder_angesehen"]["uebersicht"]) | set(urteil["bilder_angesehen"]["nah"])
    assert alle_bilder <= gesehen, alle_bilder - gesehen
    with open(OUT + "urteil.json", "w", encoding="utf-8") as fh:
        json.dump(urteil, fh, ensure_ascii=False, indent=1)
    zeichne(L, segmente)
    print("segmente", len(segmente), "nicht_sauber", sum(s["urteil"] == "nicht_sauber" for s in segmente),
          "punkte", sum(len(s["punkte"]) for s in segmente), "unsicher", sum(not s["sicher"] for s in segmente))


FX, FY, FW, F = 282, 32, 314, 3
FARBEN = {
    "Hof": (230, 150, 60), "Hof im Schatten": (160, 95, 40), "Garten": (60, 160, 60),
    "Längsbau": (220, 60, 60), "Nebengebäude": (240, 110, 160), "Dach": (200, 40, 40),
    "Fahrbahn": (245, 235, 80), "Straßenrand": (190, 160, 230), "Hinterweg": (225, 205, 160),
    "Feld": (140, 180, 60), "Anger": (190, 220, 110), "Wegrain": (110, 220, 160), "Feldrain": (80, 190, 190),
    "Baum": (20, 90, 40), "Gebüsch": (50, 130, 60), "Schlagschatten": (60, 60, 170), "Dunkle Fläche": (110, 40, 150),
}


def schrift(n):
    return ImageFont.truetype("C:/Windows/Fonts/arial.ttf", n)


def grundbild():
    im = np.array(Image.open(BILD).convert("RGB"))
    return im[FY:FY + FW, FX:FX + FW]


def gross(a):
    return np.repeat(np.repeat(a, F, 0), F, 1)


def rahmen(d):
    x0, y0 = (314 - FX) * F, (64 - FY) * F
    d.rectangle([x0, y0, x0 + 250 * F, y0 + 250 * F], outline=(0, 255, 255), width=2)


def grenzen(Lw):
    g = np.zeros(Lw.shape, bool)
    g[:, 1:] |= Lw[:, 1:] != Lw[:, :-1]
    g[1:, :] |= Lw[1:, :] != Lw[:-1, :]
    return g


def ankerpunkt(maske):
    dt = ndi.distance_transform_edt(np.pad(maske, 1))[1:-1, 1:-1]
    y, x = np.unravel_index(np.argmax(dt), dt.shape)
    return x, y


def text_mit_rand(d, xy, t, fnt, fill):
    x, y = xy
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            d.text((x + dx, y + dy), t, font=fnt, fill=(0, 0, 0), anchor="mm")
    d.text((x, y), t, font=fnt, fill=fill, anchor="mm")


def speichern(img, name, titel, legende=None):
    if legende:
        zeilen = (len(legende) + 2) // 3
        neu = Image.new("RGB", (img.width, img.height + 22 * zeilen + 10), (20, 20, 20))
        neu.paste(img, (0, 0))
        d = ImageDraw.Draw(neu)
        fnt = schrift(15)
        for i, (t, c) in enumerate(legende):
            x = 8 + (i % 3) * (img.width // 3)
            y = img.height + 6 + (i // 3) * 22
            d.rectangle([x, y + 2, x + 14, y + 16], fill=c)
            d.text((x + 20, y), t, font=fnt, fill=(235, 235, 235))
        img = neu
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, img.width, 22], fill=(20, 20, 20))
    d.text((6, 3), titel, font=schrift(15), fill=(255, 255, 120))
    img.save(OUT + name, quality=90)


def zeichne(L, segmente):
    Lw = L[FY:FY + FW, FX:FX + FW]
    base = grundbild()
    # roh
    img = Image.fromarray(gross(base))
    rahmen(ImageDraw.Draw(img))
    speichern(img, "roh.jpg", "r0c0 v2: Luftbild 1968 (Schwarz-Weiß), Viertel cyan umrandet")
    eigen = {s["id"] for s in segmente}
    g = gross(grenzen(Lw))
    fnt = schrift(14)
    # umriss
    a = gross(base).copy()
    a[g] = (255, 230, 0)
    img = Image.fromarray(a)
    d = ImageDraw.Draw(img)
    rahmen(d)
    for sid in np.unique(Lw):
        x, y = ankerpunkt(Lw == sid)
        text_mit_rand(d, (x * F + 1, y * F + 1), str(int(sid) % 100000), fnt,
                      (255, 255, 255) if sid in eigen else (170, 170, 170))
    speichern(img, "umriss.jpg", "r0c0 v2: Grenzen nach dem Nachsegmentieren, weiß = Segmente dieses Viertels")
    # vorschlag
    a = gross(base).astype(float)
    fein = {s["id"]: s["klasse_frei"]["fein"] for s in segmente}
    farbe = np.zeros(Lw.shape + (3,))
    hat = np.zeros(Lw.shape, bool)
    for sid, fn in fein.items():
        m = Lw == sid
        farbe[m] = FARBEN[fn]
        hat |= m
    fg, hg = gross(farbe), gross(hat)
    a[hg] = a[hg] * 0.5 + fg[hg] * 0.5
    a = a.astype(np.uint8)
    a[g] = (255, 255, 255)
    img = Image.fromarray(a)
    d = ImageDraw.Draw(img)
    rahmen(d)
    for sid in fein:
        m = Lw == sid
        if m.sum() < 15:
            continue
        x, y = ankerpunkt(m)
        text_mit_rand(d, (x * F + 1, y * F + 1), str(int(sid) % 100000), schrift(12), (255, 255, 255))
    leg = [(n, c) for n, c in FARBEN.items() if n in set(fein.values())]
    speichern(img, "vorschlag.jpg", "r0c0 v2: Klassen (fein) wie vorgeschlagen; ungefärbt = Nachbarviertel", leg)
    # maengel
    a = gross(base).copy()
    a[g] = (200, 200, 120)
    img = Image.fromarray(a)
    d = ImageDraw.Draw(img)
    rahmen(d)
    legende = []
    n = 0
    for sid, k, sicher, urt, was, punkte, _ in S:
        for art, text, (x, y), fl in punkte:
            n += 1
            px, py = (x - FX) * F, (y - FY) * F
            d.ellipse([px - 11, py - 11, px + 11, py + 11], fill=(220, 30, 30), outline=(255, 255, 255), width=2)
            d.text((px, py), str(n), font=schrift(13), fill=(255, 255, 255), anchor="mm")
            getan = any(sid in e["vorher"] or sid in e["nachher"] for e in EINGRIFFE)
            kurz = {"trennen": "geteilt" if getan else "teilen? (nicht getan)",
                    "verschmelzen": "zugeschlagen" if getan else "verschmelzen? (nicht getan)",
                    "sonstiges": "Hinweis"}.get(art, art)
            legende.append((f"{n}: {int(sid) % 100000} {kurz}", (220, 30, 30)))
        if not sicher:
            m = Lw == sid
            if m.any():
                x, y = ankerpunkt(m)
                d.ellipse([x * F - 3, y * F - 3, x * F + 3, y * F + 3], fill=(255, 160, 0))
    legende.append(("orange Punkt: sicher nein", (255, 160, 0)))
    speichern(img, "maengel.jpg", "r0c0 v2: Mängel und Eingriffe (rote Nummern), orange = unsicher", legende)


if __name__ == "__main__":
    main()

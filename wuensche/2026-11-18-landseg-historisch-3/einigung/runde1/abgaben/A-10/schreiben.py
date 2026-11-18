import json
P=[
("r0c1:201233|r1c1:400138","gleich","1.1","Der helle Dachstreifen läuft über die Naht weiter; 400138 ist sein etwas dunklerer Südwestrand (Grau 105 gegen 157, Unschärfe der Traufe), den 201233 oberhalb der Naht in derselben Breite mit umfasst; Haupt- oder Nebengebäude ist am schmalen Streifen nicht sicher, darum Elternklasse Gebäude wie für 400141."),
("r0c1:201233|r1c1:400141","gleich","1.1","Derselbe helle, lange Dachstreifen (Grau 157 und 162) setzt sich ohne Kante über die Naht nach Südost fort, mit dunklem Schattenband an der Nordostseite; ein Gebäude ist sicher, ob Hauptbau oder schmales Nebengebäude nicht, darum 1.1."),
("r0c1:201236|r1c1:400144","gleich","0.1","Beide liegen im selben fast schwarzen Band nordöstlich des hellen Dachstreifens (Grau 41 und 61), das unterhalb der Naht als Schlagschatten 400143 weiterläuft; beschattete Dachhälfte und Boden im Schatten sind auf dem Scan nicht zu trennen."),
("r0c1:201241|r1c1:400146","unklar",None,"Beide sind schmale mittelgraue Säume am Nordostrand des Schattenbands zur hellen Straße hin (Grau 141 und 112) und zeigen dieselbe Übergangszone; ob dort Straßenrand, Boden im Halbschatten oder eine Traufe liegt, gibt das Schwarz-Weiß-Bild nicht her."),
("r0c1:201120|r1c1:400146","grenze",None,"Die helle Fahrbahn (Grau 174) setzt sich unterhalb der Naht als 400149 fort, nicht als 400146; dieses ist nur der dunklere Saum am Rand des Schattenbands (Grau 112), Berührung nur an einem Eckpunkt."),
("r0c1:201120|r1c1:400149","gleich","3.1.1","Das breite helle Straßenband zwischen den Streckhöfen läuft ohne Kante über die Naht und mündet in die Bogenstraße nach Osten; es liegt mitten im Ort, darum Straße im Ort."),
("r0c1:201120|r1c1:400152","gleich","3.1.1","Das Stück 400152 (7 Bildpunkte, Grau 109) ist der untere Ausläufer des dunklen Flecks auf der Fahrbahn, den 201120 als Teil der Straße führt, und liegt rundum in der Straße 400149; eine Schattenfuge zwischen Gebäuden gibt es dort nicht."),
("r0c1:201128|r1c1:400149","unklar",None,"Die mittelgraue Fläche vor dem Giebel des hellen Dachstreifens (Grau 140) läuft ohne Kante über die Naht in den oberen rechten Teil von 400149, ist aber von der hellen Bogenstraße durch eine dunkle Linie getrennt; ob sie Straßeneinmündung oder Vorplatz/Hof ist, lässt sich am Bild nicht entscheiden, und 400149 umfasst beides."),
("r0c1:201128|r1c1:400156","grenze",None,"400156 (2 Bildpunkte im Kern, Grau 100) ist die Spitze des dunklen Schattenstreifens am Nordostrand der mittelgrauen Fläche 201128 (Grau 140); der Grauwertsprung zeigt dort den Rand zweier verschiedener Flächen."),
]
a=json.load(open("C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde1/auftraege-A/A-10/auftrag.json",encoding='utf-8'))
soll=[p['paar'] for p in a['abgabe_muster']['paare']]
assert soll==[p[0] for p in P], soll
out={"schema":"landseg-einigung-abgabe/1","fassung":"A","buendel":"A-10","bearbeiter":"agent:einigung-A-10:20261118i-r1",
 "paare":[{"paar":p,"entscheidung":e,"klasse":k,"grund":g} for p,e,k,g in P],
 "offen":["r0c1:201241|r1c1:400146: schmaler Saum zwischen Schattenband und Straße, Straßenrand oder Traufe; das Farbbild oder eine höhere Auflösung würde es klären.",
          "r0c1:201128|r1c1:400149: mittelgraue Fläche vor dem Giebel, Straßeneinmündung oder Vorplatz/Hof; 400149 reicht über beide Flächen, eine Grenze an der dunklen Linie zur Bogenstraße würde es klären (Grenzänderung, nicht Teil der Einigung)."],
 "nicht_geprueft":[]}
json.dump(out,open("einigung_abgabe.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("ok",len(P))

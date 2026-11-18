import json
OUT='C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde1/abgaben/B-12/einigung_abgabe.json'
P=[
("r1c0:300035|r1c1:400137","gleich","0.3","Beide Seiten zeigen denselben fast schwarzen, länglichen Fleck (etwa 6 × 2 m) am Südrand des hellen Wegs ohne Textur und ohne hohen Körper daneben; ob Hütte, Wagen oder Schatten, ist bei 0,45 m nicht zu sehen, daher Dunkle Fläche statt Nebengebäude oder Schlagschatten."),
("r1c0:300029|r1c1:400136","gleich","6.1","Die 13 Kernpunkte von 400136 sind dasselbe gleichmäßig mittelgraue, feinkörnige Feld wie 300029 westlich der Naht, das bis an den Wegrand reicht; ein eigener Rainstreifen ist am Bild nicht abgesetzt."),
("r1c1:400171|r1c1:400244","grenze",None,"Die Segmente berühren sich nur an einer Ecke: 400171 ist ein eigenes mittelgraues Dach mit Schlagschatten an der Ostseite, 400244 der nördliche Nachbarstreifen mit hellem Dach, getrennt durch die Schattenlinie, die genau an der Berührstelle endet."),
("r1c1:400171|r1c1:400266","grenze",None,"Die Berührstelle liegt an der Südostecke des Dachs 400171, wo dessen dunkler Schatten an der Ostseite ausläuft; südlich davon beginnt mit 400266 der fleckig graue Nachbarstreifen, also zwei verschiedene Flächen."),
("r1c1:400188|r1c1:400239","unklar",None,"Das kleine mittelgraue Stück 400188 an der Einmündung stößt an der Berührstelle an den dunklen Fleck im Streifen 400239; ob es Straßenrand (unbefestigter Rand der Straße) oder die Vorfläche dieses Hofstreifens ist, zeigt der Grauton nicht."),
("r1c1:400188|r1c1:400192","grenze",None,"Die Quergasse 400192 ist ein sehr helles glattes Band, das Stück 400188 nördlich davon deutlich dunkler mittelgrau; das Band endet sichtbar an seinem Rand, also zwei verschiedene Flächen."),
("r1c1:400303|r1c1:400304","grenze",None,"Die Segmente berühren sich nur mit einer Ecke im dunklen Bereich westlich des Gebäudes: 400303 ist der Streifen mit dem hellen Dach im Norden (nur ein schmaler Ausläufer reicht am Straßenrand nach Süden), 400304 die dunkle fleckige Gartenfläche, also verschiedene Flächen."),
("r1c1:400207|r1c1:400216","grenze",None,"400207 ist das sehr helle Straßenband, 400216 die dunkler graue Fläche westlich und südlich davon am Bildrand; an der Strecke liegt der Hell-Dunkel-Übergang des Straßenrands, nur einzelne Randpunkte des hellen Bands gehören zu 400216."),
("r1c1:400148|r1c1:400264","grenze",None,"400148 ist die helle glatte Dorfstraße, 400264 der grau gefleckte Hofstreifen östlich davon mit dunklen Ringen und hellen Flecken; die Berührstelle liegt am Ostrand der Straße."),
("r1c1:400130|r1c1:400283","grenze",None,"400130 ist das lange gleichmäßig mittelgraue Dachband zwischen zwei Schattenlinien; 400283 liegt nördlich vom Westende dieses Bands an der Straße, und die nördliche Schattenlinie des Bands endet genau an der Berührstelle, also gehört 400283 zur nächsten Zeile."),
("r1c1:400130|r1c1:400292","grenze",None,"Die drei Berührpunkte liegen am Südrand des langen gleichmäßigen Dachbands 400130, wo eine dunkle fleckige Schattenlinie den südlich anschließenden Hofstreifen 400292 mit eigenen Dächern und Schatten abtrennt."),
]
d={"schema":"landseg-einigung-abgabe/1","fassung":"B","buendel":"B-12","bearbeiter":"agent:einigung-B-12:20261118i-r1",
 "paare":[{"paar":p,"entscheidung":e,"klasse":k,"grund":g} for p,e,k,g in P],
 "offen":["r1c1:400188|r1c1:400239: ob 400188 Straßenrand oder Vorfläche des Hofstreifens 400239 ist, klärt nur ein schärferes Bild oder eine Ortskarte (Hofeinfahrt)."],
 "nicht_geprueft":[]}
json.dump(d,open(OUT,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(P))

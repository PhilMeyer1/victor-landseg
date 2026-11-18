import json
B='agent:einigung-A-07:20261118i-r1'
P=[
("r0c1:200433|r0c1:200525","grenze",None,"Fast schwarzer Schattenstreifen (Grau etwa 37) neben einer mittelhellen offenen Fläche (etwa 135): deutlicher Helligkeitsunterschied, zwei verschiedene Flächen, die sich nur an einem Punkt der Viertelgrenze berühren."),
("r0c1:200535|r0c1:200637","grenze",None,"Kleine dunkelgraue, weiche Fläche (etwa 74) neben einem fast schwarzen Schatten (etwa 32): der Grauton springt sichtbar, die Fläche ist kein Teil des Schattens."),
("r0c1:200539|r0c1:200544","grenze",None,"Breiter fast schwarzer Schatten (etwa 38) und ein schmaler mittelheller Streifen (etwa 130) an seinem Ende: klar getrennte Helligkeiten, zwei verschiedene Flächen."),
("r0c1:200547|r0c1:200548","grenze",None,"Zwei parallele Längsstreifen, der eine mittelhell (etwa 126), der andere deutlich dunkler (etwa 78), mit sichtbarem Helligkeitssprung entlang der ganzen Längsseite; sie berühren sich an der Viertelgrenze nur an der Spitze."),
("r0c1:200548|r0c1:200550","grenze",None,"Schmaler dunkelgrauer Streifen (etwa 78) als eigene Linie neben einer helleren mittelgrauen Fläche (etwa 107); der Streifen hebt sich auf seiner ganzen Länge ab, Berührung nur an seinem Fußende."),
("r0c1:200552|r0c1:200651","unklar",None,"Zwischen Fahrbahn und dem hellen Streifen an ihrem Südostrand ist keine Kante zu sehen (Grau 156 gegen 168), der helle Streifen gehört aber zu einem Segment, das auch einen quer zur Straße liegenden Dachstreifen enthält; weder Straße noch Gebäude passt für beide Teile."),
("r0c1:200553|r0c1:200556","grenze",None,"Mittelheller Dachstreifen (etwa 148) direkt neben einem fast schwarzen Schatten (etwa 49): typische besonnte Dachseite gegen Schatten, klarer Helligkeitssprung."),
("r0c1:201169|r1c1:400188","gleich","2.1","Über die Naht läuft ohne Kante dieselbe mittelhelle, gleichmäßige Fläche (Grau 154 gegen 157) ohne Dachform oder Schlagschatten weiter; offene befestigte Hof- oder Platzfläche."),
]
d={"schema":"landseg-einigung-abgabe/1","fassung":"A","buendel":"A-07","bearbeiter":B,
 "paare":[{"paar":p,"entscheidung":e,"klasse":k,"grund":g} for p,e,k,g in P],
 "offen":["r0c1:200552|r0c1:200651: Segment r0c1:200552 vereint einen hellen Randstreifen längs der Straße mit einem quer liegenden Dachstreifen; klären würde eine Teilung des Segments (Grenzänderung, nicht Teil der Einigung) oder ein Farbbild, ob der Randstreifen Fahrbahn, Straßenrand oder Hausfront ist."],
 "nicht_geprueft":[]}
json.dump(d,open('einigung_abgabe.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)

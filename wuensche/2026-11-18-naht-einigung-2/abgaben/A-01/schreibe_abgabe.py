"""Schreibt einigung_abgabe.json fuer Buendel A-01 (Fassung A)."""
import json

AUFTRAG = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-naht-einigung-2/auftraege-A/A-01/auftrag.json"
OUT = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-naht-einigung-2/abgaben/A-01/einigung_abgabe.json"

E = {
    1: ("grenze", None, "Offene ungemähte Wiese im Norden und Wiese mit vielen dunklen Kronen im Süden; der Übergang ist ohne Kante von Hand gezogen, aber die Dichte der Sträucher unterscheidet zwei Zonen."),
    2: ("grenze", None, "Dunkle große Baumkrone gegen helle Wiese mit deutlichem Helligkeitswechsel am Kronenrand."),
    3: ("gleich", "4.1", "Beidseits der Naht dieselbe hellere, glatte Wiese; das Segment unten reicht auch in raueres Gras, daher die Klasse Wiese / Grünland."),
    4: ("unklar", None, "An der Naht liegt beidseits dieselbe raue Wiese mit verstreuten Sträuchern, aber das Segment unten umfasst auch die glatte Wiese im Westen, sodass weder Verbuschte Wiese noch Wiese für beide ganzen Segmente sicher passt."),
    5: ("gleich", "4.3", "Der kleine Fleck unten zeigt keine abgrenzbare Strauchkrone, sondern dieselbe raue Wiese mit Gebüschflecken wie die Fläche darüber."),
    6: ("gleich", "6.1", "Geschlossenes Kronendach desselben Gehölzbestands läuft ohne Kante über die Naht."),
    7: ("grenze", None, "Oben Kronen des Gehölzbestands, unten eine helle Wiesenzunge zwischen den Kronen; sie berühren sich nur an einer Ecke."),
    8: ("gleich", "6.1", "Die dunklen Kronen am Rand des Bestands setzen sich ohne Kante über die Naht in den Wald fort; dunkel, aber derselbe Bestand."),
    9: ("grenze", None, "Waldrand gegen ungemähte Wiese; das Waldsegment reicht an der Naht wenige Bildpunkte in die Wiese, die Flächen sind aber verschieden."),
    10: ("gleich", "4.1.1", "Dieselbe raue, ungemähte Wiese beidseits der Naht ohne Kante."),
    11: ("grenze", None, "Heller schmaler Trampelpfad gegen Wiese, der Pfad ist als helle Spur sichtbar."),
    12: ("grenze", None, "Unten das Segment des schwachen hellen Pfads, der nach Süden weiterläuft, oben die offene Wiese; Pfad und Wiese sind verschiedene Flächen, auch wenn das Pfadsegment breit ist."),
    13: ("grenze", None, "Dunkle Krone der Baumgruppe gegen Wiese, Berührung nur an der Ecke am Kronenrand."),
    14: ("grenze", None, "Wiese gegen dunkle Baumgruppe, Berührung nur an einer Ecke am Kronenrand."),
    15: ("grenze", None, "Wiese gegen dunkles Gehölzband, Berührung nur an einer Ecke am Rand des Bandes."),
    16: ("gleich", "6.2", "Dasselbe dunkle Gehölzband aus Kronen und Schlagschatten läuft ohne Kante über die Naht; zusammen mehrere Kronen, daher Baumgruppe."),
    17: ("gleich", "6.2", "Glied derselben Baumgruppe wie Paar 16 und 18: das dunkle Band oben geht in die grünen Kronen unten über."),
    18: ("gleich", "6.2", "Grüne Kronen am Feldrand setzen sich ohne Kante unter der Naht in derselben Baumgruppe fort."),
    19: ("unklar", None, "Am Ostende der Kronen am Feldrand ist nicht zu erkennen, ob dort noch Krone oder schon Wiese liegt; beide Seiten sehen gleich mittelgrün aus."),
    20: ("grenze", None, "Dunkle Kronengruppe gegen helle Wiese mit deutlichem Helligkeitswechsel."),
    21: ("grenze", None, "Großflächig dunkle Stelle im Wald gegen besonntes Kronendach; die Helligkeit unterscheidet sich deutlich."),
    22: ("grenze", None, "Beiger, vegetationsarmer Fleck gegen grünen Saum, sichtbarer Farbwechsel."),
    23: ("grenze", None, "Glattere Wiese gegen rauen, verbuschenden Saum; fließender Übergang, aber zwei verschiedene Zonen."),
    24: ("grenze", None, "Dunkle Einzelkrone im helleren Saum, Rand sichtbar."),
    25: ("unklar", None, "Länglicher, etwas dunklerer und glatterer Fleck am Schattenrand; ob Krone oder dichtere Krautflur, ist am Bild nicht sicher."),
    26: ("gleich", "6.1", "Die helle Fläche zeigt dieselbe klumpige Kronenstruktur mit Schattenlücken wie das umgebende besonnte Kronendach, keine glatte Krautfläche."),
    27: ("grenze", None, "Dunkle, beschattete Stelle zwischen hellen besonnten Kronen, deutlicher Helligkeitswechsel."),
    28: ("grenze", None, "Die helle Pfadspur kreuzt hier die Naht und läuft im Pfadsegment unten weiter; daneben Wiese."),
    29: ("gleich", "4.1.1", "Dieselbe raue Hangwiese beidseits der Naht ohne Kante."),
    30: ("gleich", "4.1.1", "Die wenigen Kernbildpunkte des kleinen Flecks zeigen keine Strauchkrone, sondern dieselbe Wiese wie daneben."),
    31: ("unklar", None, "Der Teil des Waldsegments an der Naht zeigt dieselbe raue Grünfläche mit einzelnen dunklen Flecken wie die Wiese daneben; ob das Krautflur oder niedrige Kronen sind, ist nicht sicher zu sagen."),
    32: ("grenze", None, "Lichtung im Gehölz gegen offene Hangwiese, getrennt durch Kronen; Berührung nur an einer Ecke."),
    33: ("gleich", "6.1", "Geschlossenes Kronendach desselben Waldes läuft ohne Kante über die Naht."),
    34: ("grenze", None, "Helle Lichtung mit Pfad gegen geschlossenen Wald; die Lichtung reicht etwa 10 Bildpunkte über die Naht in das Waldsegment, die Flächen sind aber verschieden."),
    35: ("grenze", None, "Heller Trampelpfad gegen Wald; der Pfad läuft jenseits der Naht im Waldsegment weiter."),
    36: ("gleich", "6.1", "Geschlossenes Kronendach desselben Waldes beidseits der Naht."),
    37: ("grenze", None, "Dunkle, beschattete Stelle gegen helle besonnte Kronen; die dunkle Stelle reicht wenige Bildpunkte über die Naht, die Flächen sind aber verschieden."),
    38: ("grenze", None, "Wiese gegen dunkle Krone der Baumgruppe am Kronenrand."),
}

OFFEN = [
    "Paar 4 (r0c0:100103|r1c0:300016): gemeinsame Klasse nicht entscheidbar, weil r1c0:300016 glatte und raue Wiese zusammenfasst; klären würde eine Teilung von 300016 entlang des Übergangs glatt/rau (etwa x 100 bis 140), dann raue Hälfte mit 100103.",
    "Paar 19 (r0c1:200175|r1c1:400002): Ostende der Kronen am Feldrand (x 773 bis 783) nicht von Wiese zu trennen.",
    "Paar 25 (r1c0:300041|r1c0:300045): Krone oder dichtere Krautflur nicht entscheidbar.",
    "Paar 31 (r1c0:300051|r1c1:400002): der Streifen von 300051 an der Naht (etwa x 465 bis 500, y 500 bis 580) sieht wie die Wiese 400002 aus; das ist eine Grenzfrage, die mit Klassen allein nicht zu lösen ist.",
    "Grenzlage, nicht Klasse: r1c1:400034 enthält an der Naht (x 500 bis etwa 512, y 610 bis 640) noch Lichtung und Pfad aus r1c0 (Paare 34, 35); r1c0:300051 reicht an der Naht wenige Bildpunkte in die Wiese 100120 (Paar 9); die dunkle Stelle r1c0:300042 reicht wenige Bildpunkte in r1c1:400052 (Paar 37).",
    "Ketten: Wald {r1c0:300051, r0c0:100122, r0c0:100123, r1c0:300034, r1c1:400034, r1c1:400052} auf 6.1 (statt 6.1.1, weil 100123 und Teile von 300051 dunkel sind); Wiese {r0c0:100120, r1c0:300009, r1c0:300014, r1c1:400002} auf 4.1.1; Baumgruppe {r0c1:200170, r0c1:200175, r1c1:400011, r1c1:400019} auf 6.2.",
]


def main():
    a = json.load(open(AUFTRAG, encoding="utf-8"))
    paare = []
    for p in a["paare"]:
        ent, kl, grund = E[p["nr"]]
        paare.append({"paar": p["paar"], "entscheidung": ent, "klasse": kl, "grund": grund})
    out = {
        "schema": "landseg-einigung-abgabe/1",
        "fassung": "A",
        "buendel": "A-01",
        "bearbeiter": "agent:einigung-A-01:20261118e",
        "paare": paare,
        "offen": OFFEN,
        "nicht_geprueft": [],
    }
    assert len(paare) == len(a["paare"]) == 38
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    from collections import Counter
    print(Counter(x["entscheidung"] for x in paare))


if __name__ == "__main__":
    main()

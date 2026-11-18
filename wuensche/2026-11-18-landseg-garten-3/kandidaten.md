# Garten-Kandidaten (landseg-garten-3)

Gesamt: **495** Kandidaten in **26** Einheiten (Skript `skripte/kandidaten_garten.py`, Regeln im Kopf des Skripts).

| Bild | Fassung | Garten-Code | Kandidaten | Einheiten | davon Grünland / Acker klein / offener Boden |
|---|---|---|---|---|---|
| T0 | A | 4.4 | 108 | 5 | 108 / 0 / 0 |
| T0 | B | 2.4 | 132 | 5 | 129 / 3 / 0 |
| T0 | C | 3.6 | 136 | 5 | 132 / 4 / 0 |
| H0 | A | 4.4 | 58 | 4 | 56 / 2 / 0 |
| H0 | B | 5.3 | 34 | 4 | 31 / 3 / 0 |
| H0 | C | 3.6 | 27 | 3 | 19 / 6 / 2 |

## Einheiten

| Einheit | Kandidaten | Viertel |
|---|---|---|
| T0-A-r0c0-1 | 13 | v1, v2, v4 |
| T0-A-r0c1-1 | 17 | v1, v2, v3 |
| T0-A-r1c1-1 | 23 | v1, v2 |
| T0-A-r1c1-2 | 27 | v3 |
| T0-A-r1c1-3 | 28 | v4 |
| T0-B-r0c0-1 | 25 | v1, v2, v4 |
| T0-B-r0c1-1 | 16 | v1, v2, v3 |
| T0-B-r1c1-1 | 29 | v1, v2 |
| T0-B-r1c1-2 | 31 | v3 |
| T0-B-r1c1-3 | 31 | v4 |
| T0-C-r0c0-1 | 22 | v1, v2, v4 |
| T0-C-r0c1-1 | 15 | v1, v2, v3 |
| T0-C-r1c1-1 | 26 | v1, v2 |
| T0-C-r1c1-2 | 33 | v3 |
| T0-C-r1c1-3 | 40 | v4 |
| H0-A-r0c0-1 | 4 | v1, v2, v3 |
| H0-A-r0c1-1 | 19 | v1, v2 |
| H0-A-r0c1-2 | 26 | v3, v4 |
| H0-A-r1c1-1 | 9 | v1, v2, v3, v4 |
| H0-B-r0c0-1 | 18 | v1, v2, v4 |
| H0-B-r0c1-1 | 10 | v1, v2, v4 |
| H0-B-r1c0-1 | 2 | v3 |
| H0-B-r1c1-1 | 4 | v1, v3, v4 |
| H0-C-r0c0-1 | 23 | v1, v2, v3, v4 |
| H0-C-r1c0-1 | 2 | v3 |
| H0-C-r1c1-1 | 2 | v1, v3 |

## Hinweise

- Ein Segment, dessen Kern über mehrere Teilkacheln reicht (gleiche ID), ist nur einmal Kandidat: in der Teilkachel mit den meisten Kernbildpunkten (`auch_in` nennt die anderen); das Urteil gilt für alle (L6).
- Fassung A trägt kein Merkmal `im_siedlung`; es kommt aus der Karte der Fassung C (Mehrheit der Bildpunkte).
- Freie Listen: die eigene Grünland-Klasse heißt jetzt „Dauergrünland (…)“, darunter die neue Klasse Garten; H0 B: alte Klasse 2.2 „Garten“ unter „Hof und Garten“ heißt jetzt „Gartenfläche am Hof (bisher „Garten“)“ (Code unverändert) und ist Kandidat. Vorher-Stand der Listen unter `listen-vorher/`.
- Offen: T0-B-r1c1-2: 31 Kandidaten in einem Viertel (über 30, Viertel nicht geteilt)
- Offen: T0-B-r1c1-3: 31 Kandidaten in einem Viertel (über 30, Viertel nicht geteilt)
- Offen: T0-C-r1c1-2: 33 Kandidaten in einem Viertel (über 30, Viertel nicht geteilt)
- Offen: T0-C-r1c1-3: 40 Kandidaten in einem Viertel (über 30, Viertel nicht geteilt)

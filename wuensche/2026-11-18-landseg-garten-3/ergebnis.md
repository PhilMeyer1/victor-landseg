# Garten eintragen (garten-3), Ergebnis

Bearbeiter wf:garten:20261118n. Sicherung vorher: `sicherung-vor-garten/<bild>/<ordner>/<teilkachel>` (und `zusammen`, soweit vorhanden). Skripte: `skripte/eintragen.py`, `skripte/auswerten.py`; Logs: `anwenden/`.

| Bild | Fassung | Garten-Klasse | ja (eingetragen) | nein | unklar | Garten-Segmente im Kern | Anteil Fläche | offene Einigungspaare | zusammentragen |
|---|---|---|---|---|---|---|---|---|---|
| T0 | A | 4.4 | 101 | 4 | 3 | 101 | 12,15 % | 0 | FEHLER (309 Nahtverstöße, 247 Mängel) |
| T0 | B | 2.4 | 115 | 8 | 9 | 115 | 13,56 % | 1 | FEHLER (312 Nahtverstöße, 130 Mängel) |
| T0 | C | 3.6 | 118 | 11 | 7 | 118 | 11,67 % | 1 | FEHLER (312 Nahtverstöße, 20 Mängel) |
| H0 | A | 4.4 | 1 | 22 | 35 | 1 | 0,32 % | 0 | FEHLER (163 Nahtverstöße, 33 Mängel) |
| H0 | B | 5.3 | 3 | 14 | 17 | 3 | 0,72 % | 0 | FEHLER (141 Nahtverstöße, 178 Mängel) |
| H0 | C | 3.6 | 0 | 14 | 13 | 0 | 0,00 % | 0 | Nähte: FEHLER (105), pruefen ok |

Anteil = Bildpunkte der Garten-Segmente im zusammengetragenen Ausschnitt (1000 x 1000) durch alle Bildpunkte.

- `pruefen` aller 24 Teilkacheln nach dem Eintragen: 24 mal ok.
- `zusammentragen` 6 mal gelaufen. Die Fehler sind Nahtverstöße (Grenzen ohne Bildkante) und Teile eines Segments über die Kerne hinweg, keine Lücken; sie kommen nicht von den Klassenänderungen (nur Klassen gesetzt). Für T0 B und C gab es keine `zusammentragen.json`; ich habe sie nach dem Muster von T0 A in den Fassungsordnern angelegt.
- Offene Einigungspaare (nur gezählt, nicht geklärt): T0 B 1, T0 C 1, sonst 0.
- „unklar“ und „nein“ bleiben unverändert (Zahlen in der Tabelle).

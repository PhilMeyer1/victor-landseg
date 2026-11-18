# Messung H0

USD: Rechenwert nach Listenpreis (Stand 2026-10-08), keine Abo-Kosten. Gelesen = Cache-Lesen, neu = Eingabe + Cache-Schreiben; Runden = API-Antworten (2026-11-18T12:12:10Z bis 2026-11-18T13:56:35Z).

| Phase | Modell | Agents | Wand (min) | Agent-min | Runden | gelesen (Mio.) | neu (Mio.) | Ausgabe (Mio.) | USD | Bilder gelesen | .py geschrieben |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Vorbereitung | opus | 1 | 7,7 | 7,7 | 38 | 4,75 | 0,17 | 0,040 | 2,62 | 3 | 3 |
| Urteile | opus | 13 | 33,6 | 332,4 | 1283 | 250,32 | 3,66 | 1,608 | 100,52 | 699 | 78 |
| Nachholen | opus | 8 | 9,8 | 58,7 | 242 | 27,60 | 1,08 | 0,310 | 17,13 | 162 | 18 |
| Vereinheitlichen | sonnet | 1 | 4,9 | 4,9 | 29 | 2,63 | 0,13 | 0,036 | 0,94 | 0 | 3 |
| Zusammenführen | opus | 1 | 6,8 | 6,8 | 33 | 3,58 | 0,17 | 0,036 | 2,28 | 0 | 1 |
| Nähte | opus | 3 | 13,3 | 27,8 | 150 | 19,21 | 0,51 | 0,134 | 9,10 | 96 | 7 |
| Einigung | opus | 41 | 27,7 | 202,3 | 976 | 94,18 | 4,04 | 0,975 | 58,52 | 675 | 55 |
| Anwenden | sonnet | 3 | 11,9 | 2,1 | 18 | 0,97 | 0,17 | 0,007 | 0,60 | 0 | 0 |
| zusammen |  | 71 | 104,4 | 642,6 | 2769 | 403,24 | 9,93 | 3,147 | 191,70 | 1635 | 165 |

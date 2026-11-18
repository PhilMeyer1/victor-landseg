# Bericht landseg
Status: bereit-zur-pruefung
Für den Nutzer: Der historische Ausschnitt H0 (Luftbild 1968) ist fertig geprüft und steht zusammen mit T0 in
  einer Prüfseite: `C:/Users/Phil/Developement/Victor/daten/landseg/seiten/T0-H0.html` (14,4 MB, oben Bildwahl
  T0/H0, daneben A/B/C). Vorher repariert: Flächen, die nur über den Rand der Teilkachel zusammenhingen,
  wurden getrennt (A 20, B 28, C 32 Stücke) bzw. dem gleichartigen Nachbarn zugeschlagen. Die „falschen
  Klassen" in A und B waren keine: Sie wurden gegen die feste Liste geprüft statt gegen die eigene Liste der
  Fassung, gegen die eigene sind alle gültig. Was ich nicht konnte: die Seite selbst ansehen (keine
  Browser-Erweiterung in diesem Lauf). Was fehlt: Ihr Urteil je Klasse (Durchsicht). Danach baut Teil 5 die
  Seite ins Gesamtprojekt. Kurz zum Ergebnis: Auf Schwarz-Weiß sind 84–90 % der Flächen „unsicher" (T0 51–76 %),
  in C fallen 97 % der Flächen auf eine gröbere Stufe zurück (T0 52 %); Gebäude, Straßen und Äcker als
  Ganzes lassen sich erkennen, feinere Unterscheidungen (Acker oder Wiese, Belag, Gehölzart) kaum.
Commit: keiner (Ergebnis: ohne Commit)
Nachweis: Karten H0 aller drei Fassungen repariert und geprüft (`pruefen` ok je Teilkachel und auf der
  zusammengetragenen Karte, 0 zerfallene Segmente: A 1833, B 728, C 470 Segmente), Einigung nachgezogen (offen 0),
  Prüfseite T0+H0 gebaut, Messzahlen T0/H0 und PQ der Gegenprobe gemessen. Belege: `pruefen-h0.log`,
  `zerfall.log`/`zerfall.json`, `einigung-nachziehen.log`, `einigung-messen.txt`, `naht-h0.log`, `seite.json`,
  `messung.json`/`messung.log`, `pq-gegenprobe.json` (alle in diesem Ordner); Skripte unter `skripte/`;
  Sicherung der geänderten Teilkachelkarten unter `sicherung/`.
Abnahmekriterien:
AK5: nicht erfüllt (teilweise) — Messbericht unten mit allen Zahlen außer dem Nutzerurteil je Klasse (folgt in der Durchsicht, F3); Tokens/Kosten nur je Phase, nicht je Fassung trennbar
AK7: nicht prüfbar — Seite gebaut (`seite.json`: Bilder T0 und H0 je „vorhanden", Fassungen A/B/C je „vorhanden", Nähte- und Einigungszahlen je Bild); Ansicht im Gesamtprojekt erst nach Teil 5, Fotos ohne Browser-Erweiterung nicht möglich
Prüfungen:
zerfall_beheben.py (Probe, dann echt) → A 20 Teile (10 neu, 10 an Nachbarn), B 28 (20/8), C 32 (13/19), Fehler 0
landseg pruefen je Teilkachel, eigene Liste der Fassung → 12 × ok
landseg zusammentragen + pruefen zusammen (eigene Liste) → A 1833, B 728, C 470 Segmente, nicht zusammenhängend 0, ok
landseg pruefen zusammen gegen Liste des Repos → A 136, B 294 Mängel (nur Klassen der freien Listen), C ok
landseg einigung messen (nach Zerfall-Behebung, vor Nachziehen) → offen A 4, B 3, C 5 (neue Paare an den getrennten Stücken)
einigung_nachziehen.py → 12 Paare: 9 Beschlüsse des alten Paars übernommen, 3 als „unklar" belegt
landseg einigung messen → offen 0/0/0; unsicher belegt A 35, B 17, C 13; geklärt 178/136/88; Exit 0
landseg naht → Verstöße A 187, B 152 (11 bestätigt), C 119 (29 bestätigt); Exit 1 = Befund (wie T0 offen, eigener Wunsch „Grenzlinien an den Nähten nachziehen")
landseg seite --daten … --einstellungen seite-einstellungen.json → Exit 0, 14 398 921 Bytes, T0 und H0 je A/B/C mit Daten
messen_h0.py → Zahlen unten; pq_gegenprobe.py → PQ 0,845, Boundary-PQ 0,818
Aufruf-Budget: 50, ausgeschöpft bis zum Abschluss (keine weitere Ansicht/Probe möglich)
Nicht geprüft: Ansicht der Seite (Bildwahl, Schrittleiste, Klick auf Einigungsgrund) — keine Browser-Erweiterung;
  Seite im Gesamtprojekt (Teil 5); Nutzerurteil je Klasse; klassengleiche PQ (Hilfsrechnung im Skript lieferte
  0 Treffer, nicht verlässlich, nicht gewertet); Kosten von Teil 2 (Vorbereitung H0) nicht erfasst.
Technische Entscheidungen:
- Zerfall an der Quelle behoben (Teilkachelkarten), nicht nur in `zusammen/`: Seite und Gesamtprojekt lesen die
  Teilkachelkarten. Größter Kernteil behält die ID; weitere Kernteile gehen an den angrenzenden Nachbarn gleicher
  Klasse im Kern (längste Grenze), sonst neue ID mit gleicher Klasse (`zerfall_teil_von`). Die Randpixel des
  Segments wachsen geodätisch zum nächsten Kernteil (euklidisch zerriss es Segmente im Rand, Probe zeigte 22 Fehler).
- Neue Nahtpaare erben den Einigungsbeschluss des alten Paars (Hinweis im Grund, Bearbeiter
  `umsetzer:landseg-historisch-4`); 3 Paare, deren altes Paar „unklar" war, bleiben „unklar".
- „Ungültige Klassen": nichts umcodiert, weil alle Codes in der Liste der Fassung stehen (Beleg `pruefen-h0.log`).
- Seite: T0 aus dem Gesamtprojekt (`daten/gesamt/victor-landseg/ergebnisse/manifest.json`, neue Ordnernamen),
  H0 aus `daten/landseg/H0` über `--einstellungen` mit absoluten Manifesten; Ziel `daten/landseg/seiten/T0-H0.html`.
- Gegenprobe: liegt für H0 unter `c-feste-liste/gegenprobe/r0c0` (Fassung C), nicht in A (`a-alles-frei/abgabe-gegenprobe/r0c0` ist leer). Erst-Urteil = C r0c0 vor dem Beheben (Sicherung).
Nacharbeit im Hauptordner: keine aus diesem Teil; Teil 5 übernimmt Ergebnisse und Seite ins Gesamtprojekt (Nacharbeit des Mutterwunschs: Profil, Lagebild, KATEGORIEN.md-Befund).
Abräumen: WEG (keine Arbeitskopie angelegt); keine Prozesse gestartet.
Lagebild: unberührt: kein Code geändert, Datenlauf ohne Commit.
Erkenntnisse fürs Profil:
- `pruefen` ohne `--kategorien` prüft gegen die feste Liste: bei A/B immer die Liste der Fassung (`kategorien-a.json`, `kategorien-b.json`) angeben, sonst Scheinfehler „ungültige Klasse".
- `pruefen` je Teilkachel ist ok, obwohl die zusammengetragene Karte zerfallene Segmente hat: ein Segment kann nur über den Kontextrand zusammenhängen. Nach jedem Nachsegmentieren die Kernkarte prüfen (`zusammentragen` meldet es); Behebung `wuensche/2026-11-18-landseg-historisch-4/skripte/zerfall_beheben.py`.
- Teilen/Zusammenlegen von Segmenten nach der Einigung erzeugt neue offene Nahtpaare; `einigung messen` danach erneut fahren.
- Eine Seite mit T0 und H0 geht mit `seite --daten <beliebig> --einstellungen <json mit bilder[].manifest absolut>`; T0 unter `daten/landseg/T0` hat die alten Ordnernamen, T0 aus dem Gesamtprojekt die neuen.
Abweichungen vom Zielbild:
- `landseg/landseg/pruefen.py:77` — Zusammenhang wird über die ganze Teilkachel (Kern + Rand) geprüft, maßgeblich ist aber der Kern — darum fiel der Zerfall erst nach dem Zusammentragen auf und musste nachträglich behoben werden — sauber wäre eine Kernprüfung in `pruefen` (mit Manifest) bzw. in `eingriff`, damit Agents es beim Nachsegmentieren sehen.

## Messbericht H0 gegen T0

Kosten (Teil 3, Workflow wf_62f47ff3-c51, Auswertung `2026-11-18-landseg-effiz/bericht.md`): 71 Agents,
11,41 Mio. Tokens laut Workflow (gelesen 403 Mio. inkl. Wiederlesen, neu 9,9, Ausgabe 3,15), rund 221 USD,
104 min Wand, 643 Agent-min. Je Phase: Urteile 13 Agents (A 4, B 4, C 4, Gegenprobe 1; 33,6 min, 111,5 USD),
Nachholen 8 (unnötig, Skriptfehler; 20,4 USD), Vereinheitlichen B 1, Zusammenführen 1, Nähte 3 (je Fassung 1),
Einigung 41 in 3 Runden (27,7 min, 70,7 USD), Anwenden 3. Je Fassung nicht getrennt ausgewiesen.
T0 zum Vergleich: Urteile 15 Agents, 3,30 Mio. Tokens, 25 min; Einigung 15 Agents, 1,89 Mio., 13,5 min.
Läufe: Vorstufe 1 (grob, 4 Teilkacheln, 27 s ohne Laden), Urteile 1 + Nachholen, Einigung 3 Runden, dieser Teil 0 Agents.

| | A Alles frei | B Kategorien frei | C Feste Liste |
|---|---|---|---|
| Vorstufe (Teilkachelbild / Kern) | 705 / 465 | 705 / 465 | 705 / 465 |
| Segmente im Kern H0 (T0) | 1833 (607) | 728 (641) | 470 (641) |
| Eingriffe im Urteil H0 | eigene Karten | 137 | 110 |
| Klassen benutzt H0 (T0) | 33 (35) | 31 (38) | 14 (28) |
| Liste der Fassung H0 | 7/18/24 | 7/19/26 | 7/25/43 |
| `sicher: nein` Segmente H0 (T0) | 83,8 % (51,1 %) | 85,9 % (62,1 %) | 89,8 % (75,7 %) |
| `sicher: nein` Fläche H0 (T0) | 82,4 % (54,9 %) | 87,0 % (68,2 %) | 95,5 % (73,0 %) |
| gröbere Stufe (Code < 3 Stufen), Fläche H0 (T0) | 71 % (69 %) | 58 % (58 %) | 98 % (70 %) |
| Einigung: unsicher / geklärt / offen | 35 / 178 / 0 | 17 / 136 / 0 | 13 / 88 / 0 |
| Nahtverstöße (ID-Teil, offen) | 187 | 152 | 119 |

Je Teilkachel (Segmente/unsicher) H0: A r0c0 93/82, r0c1 876/836, r1c0 44/41, r1c1 820/577; B 191/178, 282/227,
22/19, 233/201; C 158/144, 138/104, 29/29, 145/145. A hat in r0c1 und r1c1 sehr fein selbst segmentiert.
Annahme aus `landseg-methode` (H0 etwa 200–300 Segmente): C 470, B 728, A 1833 — alle darüber.

Gegenprobe (C, r0c0, Kern 500 × 500, klassenunabhängig): Erst 155, Gegenprobe 158 Segmente, 138 Treffer
(IoU > 0,5), SQ 0,958, RQ 0,882, **PQ 0,845**, **Boundary-PQ 0,818** (Rand 2 px; 0,824 bei 5 px). Beide
starten von derselben Vorstufe, die hohe Übereinstimmung misst darum vor allem, wie wenig beide daran ändern.

Was auf Schwarz-Weiß trägt (C, Fläche): Gebäude 1.1 (100 Segmente, 45 sicher, die meisten sicheren), Verkehrsflächen
1.2 (74), Acker als Ganzes 2 (38 % der Fläche, Streifenflur an der Textur). Was nicht trägt: Acker gegen Grünland
und Wiese/Weide (T0 C: 3.1 Wiese/Weide 18 %, H0 nur Ebene 1 „3" 5,6 %), Belag (versiegelt/unversiegelt: 34 % als
Ebene 1 „1 Versiegelt/bebaut"), Gehölzarten (4.2 nur grob, Einzelbaum 2), Dach gegen Hof; alle Klassen außer 1.1
sind zu 90–100 % „unsicher". Die SW-Spalte von `kategorien.json` bleibt Vermutung.

Nutzerurteil je Klasse (F3): offen — folgt in der Durchsicht der Seite.

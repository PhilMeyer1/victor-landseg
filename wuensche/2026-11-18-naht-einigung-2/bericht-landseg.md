# Bericht naht-einigung-2: Einigung auf T0 für A, B, C (Hauptsession, Workflow)

Für den Nutzer: An allen Grenzen und Ecken der vier Teilkacheln und an den Viertelgrenzen haben KI-Helfer je Stelle beide Seiten angesehen und entschieden: gleiche Fläche (gemeinsame Klasse), echte Grenze oder unklar (als unsicher markiert, mit Grund). Danach ist in allen drei Fassungen keine Stelle mehr offen, an der dieselbe Fläche ohne Kante zwei Klassen hat. Karten und Segmentnummern sind unverändert.

Ergebnis: ohne Commit im Repo landseg; geändert wurden nur die Daten der Übergabe (`daten/landseg/uebergabe/landseg-t0/T0/<fassung>/<teilkachel>/segmente.json`, Klassen und Vermerk `einigung`), dort lokal committet.

## Zahlen (`landseg einigung messen`, Segment-Paare gleicher Fläche mit verschiedener Klasse)

| Fassung | vorher offen | nachher offen | unsicher belegt | geklärt | Schnittlinien ohne Bildkante (unverändert) |
|---|---|---|---|---|---|
| A Alles frei | 68 (896 Randpunkte) | 0 | 9 (193) | 59 (703) | 83 |
| B Kategorien frei | 59 (592) | 0 | 6 (102) | 58 (731) | 84 |
| C Feste Kategorienliste | 52 (625) | 0 | 9 (145) | 49 (593) | 84 |

Endstand wörtlich: `messen-nachher.txt`. `landseg pruefen` auf allen 12 Teilkacheln: ok.

## Läufe

| Runde | Lauf | Bündel/Agents | Modell | Tokens | Dauer | Entscheidungen |
|---|---|---|---|---|---|---|
| 1 | wf_4ce0fe3b-082 (20261118e) | 12 (je Fassung 4) | Opus, effort high | 1 590 179 | 9,5 min | A 21/38/9, B 26/28/5, C 18/26/8 (gleich/grenze/unklar) |
| 2 | wf_b53fdcd2-937 (20261118e-r2) | 2 (B, C) | Opus, high | 218 861 | 3,4 min | B 4/0/1, C 4/1/1 |
| 3 | wf_ba51a992-5f2 (20261118e-r3) | 1 (B) | Opus, high | 77 085 | 0,6 min | B 1/0/0 |
| zusammen | | 15 Agents | | 1 886 125 | 13,5 min | |

Warum Runden 2 und 3: Eine gemeinsame Klasse für eine Kette erzeugt an deren anderem Rand neue Widersprüche zu Nachbarn (B 5, C 6 nach Runde 1; B 1 nach Runde 2). Deckel: höchstens 3 Runden; nach Runde 3 offen 0.

Schätzung der Klärung: etwa 10 Agents, 1 Mio. Tokens, 10 Minuten; tatsächlich 15 Agents, 1,9 Mio. Tokens, 13,5 Minuten.

## Offen (aus den Abgaben, als unsicher belegt oder als Grenze belassen)

- Mehrere Stellen sind Fragen der Grenzlage, nicht der Klasse (Waldzipfel in Wiese, Lichtung über die Naht, Splitter eines Segments in der Nachbarkrone). Nach F1 nur Klassen: als unsicher bzw. Grenze mit Grund belassen. Lösung wäre ein eigener Wunsch „Grenzen an den Nähten nachziehen/zusammenfügen“.
- Ketten bekamen teils die Elternklasse (z. B. „Gehölz“, „Wald“, „Dauergrünland“), wenn die Feinklasse nicht für alle Glieder sicher war.

Ablage: Aufträge `auftraege-<F>/`, `runde2/`, `runde3/`; Abgaben samt eigener Lupenbilder `abgaben/<bündel>/`; Skript `workflow.js`, Selbstprüfung `review.md`.

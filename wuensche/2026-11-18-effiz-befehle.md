# K2: Fertige `landseg`-Befehle für die wiederkehrenden Agent-Skripte: urteil.json aus einer Liste bauen und prüfen, Einig

Kurzname: effiz-befehle | Datum: 2026-11-18 | Größe: mittel | Bereich: victor | Repos: landseg | Status: eingereiht | Herkunft: Ermittlung landseg-effiz K2

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

K2: Fertige `landseg`-Befehle für die wiederkehrenden Agent-Skripte: urteil.json aus einer Liste bauen und prüfen, Einigungs-Abgabe bauen, Ausschnitt/Zoom einer Stelle mit Umriss und Nummern; die Aufträge nennen sie statt „Eigene Skripte als Datei" — Gewinn geschätzt 20–35 % der Runden in Urteil und Einigung, rund 35–60 USD und 5–10 min Wand je Lauf (Stitcher-Vorbild: 31 % der Kosten) — Aufwand mittel — Risiko mittel (Agents müssen bei Sonderfällen weiter frei arbeiten dürfen, sonst leidet die Genauigkeit) — Repo landseg — empfohlen

Belege: wuensche/2026-11-18-landseg-effiz/bericht.md, K2.

Empfehlung der Deutung (wuensche/2026-11-18-landseg-effiz.md, Abschnitt Empfehlung):
- K2: trägt — genau der Hauptansatz des Stitchers (runden-straffen) gegen den größten Fokusverlust bei uns: 180 eigene .py und 1.112 Python-Aufrufe stehen gegen 189 Aufrufe von `-m landseg`.
- Nächster Schritt: K2 als Folge-Wunsch — er bringt den größten Gewinn (geschätzt 35–60 USD und 5–10 min je Lauf) und ist genau der Schritt, der im Stitcher gewirkt hat. Für die Läufe auf dem ganzen Orthofoto zählt jede gesparte Runde, weil sie das Wiederlesen des ganzen Kontexts spart.
- Gegenargument: Der Gewinn von K2 ist nur geschätzt. Im Stitcher ließen sich die fünf Maßnahmen von runden-straffen nicht trennen, und selbst danach schrieb ein Agent weiter eigene Skripte für Ansichtsbilder, das Zeitziel wurde verfehlt (bericht.md S1). Ein Teil unserer Skripte ist echte Fachhilfe (`wscheide.py`, B2). — Der Schritt gilt trotzdem: Die mechanischen Wiederholungen (urteil.json und Abgabe bauen, Zoombilder) schreibt jeder Agent neu, und der Gewinn lässt sich am nächsten Lauf mit derselben Transkript-Auswertung gegen H0 nachmessen.

## Fragen

Keine. Ob Agents bei Sonderfällen weiter eigene Skripte schreiben dürfen, ist entschieden (siehe Bausteine und Fallen): ja, die Befehle sind der Standardweg, kein Verbot.

## Entscheidungen

- Landschafts-Segmente: Effizienz der Agents, ein Agent je Viertel — Nutzer am 18.11.2026 nach der Ermittlung landseg-effiz (H0-Lauf 71 Agents, rund 221 USD Rechenwert, Kostentreiber Wiederlesen des Verlaufs, 180 eigene Agent-Skripte): alle Kandidaten K1–K6 bauen (Nachhol-Prüfung reparieren, fertige landseg-Befehle statt eigener Skripte, Kostenmessung je Phase, Bilder nur einmal verlangen, Vorbereitung und Zusammenführen als feste Befehle, kleine Einigungsbündel zusammenlegen) und K7: künftig ein Urteils-Agent je Viertel statt je Teilkachel, um den Kontext kurz zu halten. Ersetzt für die Urteile „ein Agent je Teilkachel, arbeitet die vier Viertel nacheinander ab“ (2026-11-17); jeder Agent sieht weiter zuerst den ganzen Ausschnitt und seine ganze Teilkachel, dann sein Viertel. (aus entscheidungen.md, 2026-11-18)
- Landschafts-Segmente: Vorstufe eher grob, Agents segmentieren selbst nach — Nutzer am 18.11.2026 zum historischen Ausschnitt H0: „Es soll eher gröber sein aber die Agents sollen die Möglichkeit haben Objekte sauber selbständig nachsegmentieren zu können. Möglichst direkt, einfach und Tokengünstig ohne große Umwege aber trotzdem maximal effektiv und präzise.“ Daraus: Verschmolzene Objekte teilen die Urteils-Agents selbst sauber nach, direkt im Urteilsschritt, mit möglichst wenig Aufwand an Tokens, aber präzise an der Bildkante. (aus entscheidungen.md, 2026-11-18)
- Landschafts-Segmente: Einigung an den Übergängen der Teilkacheln — Nutzer am 18.11.2026: „Bei den Tiles am Ende sollen sich dann alle Agents bei den Übergängen mit den Klassifikationen einigen. So, dass nicht gleiche Flächen unterschiedliche Labels bekommen, weil sich die Agenten nicht abgesprochen haben.“ Daraus: fester Einigungsschritt an allen Übergängen in jedem Lauf; unaufgelöste Widersprüche werden als unsicher markiert und belegt. Gilt für jede Fassung (A, B, C) und alle künftigen Läufe. (aus entscheidungen.md, 2026-11-18)
- 2026-11-18: Landschafts-Segmente: gröbere Flächen auf alten Schwarz-Weiß-Bildern: Nutzer am 18.11.2026: „außerdem solle die Flächen in den schwarz weiß, niedrig aufgelösten Landschaftsbildern nicht ganz so fein sein. Die wirklich feine Untersuchung funktioniert gut auf hochaufgelösten Bildern aber nicht auf den alte[n]“. Daraus: Auf alten, niedrig aufgelösten Schwarz-Weiß-Bildern (heute H0, Luftbild 1968) werden Flächen deutlich gröber gezogen als auf Farb-Orthofotos (T0); feines Nachsegmentieren gilt dort nur für klar erkennbare Objekte. Verschärft für SW-Bilder die Neuklärung „eher gröber, Agents dürfen nachsegmentieren“ (landseg-historisch); im H0-Lauf kam Fassung A auf 1833 Segmente (T0 607). Wie grob genau und ob H0 neu läuft, klärt der Wunsch landseg-sw-grob. (aus entscheidungen.md, 2026-11-18)

## Arbeitsauftrag

### Abnahmekriterien

AK1: Ein Urteils-Agent gibt für seine Teilkachel (oder sein Viertel) nur eine kurze Liste ab (je Segment: Nummer, Urteil, Vorschlag, Punkte, Bilder), und ein Befehl baut daraus die vollständige `urteil.json` im Format der Vorlage; was der Befehl aus den Daten kennt (Teilkachel, Bearbeiter, heutige Klasse, Schema), muss der Agent nicht schreiben — prüfbar: `"$PY" -B -m unittest tests.test_urteil` (neu; baut aus Wegwerf-Daten eine `urteil.json` und vergleicht Feld für Feld)
AK2: Ein zweiter Befehl prüft eine `urteil.json` und nennt jeden Fehler in Klartext (Segment im Kern ohne Eintrag oder doppelt, unbekannte Klasse, unbekannte Punktart, fehlende Bilddatei, Segment außerhalb des Kerns); Exit 0 bei ok, 1 bei Fehlern — prüfbar: `"$PY" -B -m unittest tests.test_urteil` (je Fehlerart ein Fall)
AK3: Die Einigungs-Abgabe baut ein Befehl aus einer kurzen Liste (Paar, Entscheidung, Klasse, Grund): Schema, Fassung, Bündel und Bearbeiter kommen aus dem Auftrag des Bündels, fehlende oder fremde Paare meldet er, und das Ergebnis besteht `einigung anwenden --probe` — prüfbar: `"$PY" -B -m unittest tests.test_einigung` (erweitert um den Abgabe-Befehl)
AK4: Ein Zoom-Befehl zeichnet den Ausschnitt einer Stelle (Punkt mit Radius, Rechteck oder Segmentnummern) vergrößert, mit Segmentumriss und Nummern, auf Wunsch neben dem rohen Luftbild; Bild höchstens 2000 Bildpunkte an der langen Seite, JPEG, Beschriftung deutsch — prüfbar: `"$PY" -B -m unittest tests.test_ansicht` (erweitert; Größe, Format, Nummern an der richtigen Stelle) und Ansicht des erzeugten Bildes an Teilkachel r0c0 aus `BASIS/daten/landseg/T0` (Umriss und Nummern lesbar, nichts verdeckt)
AK5: Die Auftragsvorlagen `urteil.md` und `einigung.md` nennen die neuen Befehle als Standardweg mit Aufruf und lassen eigene Skripte nur für Sonderfälle zu (statt „Eigene Skripte als Datei“ als Regelfall); der Skill `landseg-agent` (L10, L12) widerspricht dem nicht und `vorlagen/README.md` kennt jeden neuen Platzhalter — prüfbar: `"$PY" -B -m unittest tests.test_vorlagen` und Lesen `vorlagen/urteil.md`, `vorlagen/einigung.md`
AK6: `README.md` beschreibt die drei neuen Befehle (Aufruf, Eingabeliste, Ausgabe, Exit-Codes) und `--help` jedes Befehls läuft — prüfbar: `"$PY" -B -m landseg <befehl> --help` je Befehl und Lesen `README.md`
AK7: Weg des Nutzers bis zum Ergebnis, am laufenden Stand: Aus der vorhandenen `urteil.json` einer fertigen Teilkachel (`BASIS/daten/landseg/T0/fassung-b/urteil/r0c0/urteil.json`) wird die kurze Liste gezogen, der Bau-Befehl baut daraus eine `urteil.json`, die der Prüf-Befehl mit Exit 0 annimmt und die inhaltlich der Vorlage entspricht; ebenso eine Einigungs-Abgabe aus einem vorhandenen Bündel (`einigung anwenden --probe` ohne „Abgelehnt“) — prüfbar: Befehle der Reihe nach an diesen T0-Daten (offline, ohne GPU, unter einer Minute), Ergebnisse nur in einem Wegwerfordner unter `BASIS/daten/landseg/`
AK8: Die ganze Testreihe des Pakets bleibt grün — prüfbar: nachts: voll (Befehl unter `## Testreihen`)

Nacharbeit: Profil `landseg` (Abschnitt „Routinen“) um die drei Befehle ergänzen; `landseg/betrieb.md` und das Lagebild nachziehen (Pflege nach dem Einreihen, nicht Teil der Arbeitskopie).
Nacharbeit: Den Gewinn (Runden, Kosten, Wand je Lauf) misst der nächste Produktionslauf mit derselben Transkript-Auswertung gegen H0 (siehe `effiz-kosten`, K3); kein Kriterium dieses Wunschs.

### Einstieg

- landseg: `landseg/__main__.py:318` — Befehlsbaum (`add_subparsers`); hier kommen drei Befehle dazu: Bau und Prüfung von `urteil.json` (etwa `urteil bauen|pruefen`), der Zoom, und unter `einigung` (`__main__.py:452`) der Schritt `abgabe` neben `finden|anwenden|messen`.
- landseg: `landseg/einigung.py:343` — `_abgabe_pruefen` kennt schon alle Regeln der Abgabe (Schema `ABGABE_SCHEMA`, Entscheidungen, Klasse nur bei `gleich`, Segmente im Kern, jedes Paar genau einmal); der Abgabe-Bau ruft sie auf, statt sie nachzubauen.
- landseg: `landseg/ansicht.py:133` — Klasse `Ansicht` (Fenster `segment_fenster` Zeile 239, Umriss `_segment_umriss` 267, Beschriftung `_beschriften` 281, `zeichnen` 334): der Zoom baut auf ihnen auf; heute gibt es nur Fenster je Segment (`ansicht()` Zeile 369), kein freies Rechteck oder Punkt mit Radius.
- landseg: `landseg/__main__.py:250` — `befehl_ansicht` liest Manifest, Teilkachelbild, Kern, Labels und Segmente; der Zoom nutzt dieselbe Ladeart (Zeile 204 `_rgb_bild`, Altlast A5: lieber `naht.lese_bild` Zeile 75 nehmen).
- landseg: `vorlagen/urteil.md:23` — „Eigene Skripte als Datei in `{{ERGEBNIS}}`“ und das Format von `urteil.json` (Zeilen 38–50); `vorlagen/einigung.md` — Abschnitt „Wie“ und „Ergebnis“ (`einigung_abgabe.json`); `vorlagen/README.md` (Platzhalter), `.claude/skills/landseg-agent/SKILL.md:52` (L10) und `:59` (L12).
- landseg: `tests/test_vorlagen.py:10` — prüft Platzhalter und „keine absoluten Pfade“ in den Vorlagen; `tests/test_einigung.py`, `tests/test_ansicht.py` — Vorbild und Ort für die neuen Fälle.

### Bausteine und Fallen

- Benutzen statt nachbauen: `einigung._abgabe_pruefen` und `ABGABE_SCHEMA` (Abgabe), `ansicht.Ansicht` mit `Fenster` (Zoom, Umriss, Nummern, Kernrahmen), `dateien.lese_json`/`schreibe_json`, `kategorien` (gültige Klassen), `naht.lese_bild` (Bildleser), `pruefen` (Zusammenhang/Lücken, nicht neu schreiben), `einstellungen/*.json` für Größen und Farben (neue Schlüssel dorthin, nicht in den Code).
- Der Agent schreibt nur, was nur er wissen kann (Urteil, Vorschlag, Punkte, Grund); alles andere füllt der Befehl aus den Daten (`manifest.json`, `labels.tif`, `segmente.json`, `auftrag.json`) — das ist der Kern der Ersparnis. Ein Segment, das der Agent ausließ, ergänzt der Befehl nicht stillschweigend als „sauber“, sondern meldet es (Lückenlosigkeit der Urteile ist Regel L1/L2).
- Freiheit bleibt: Nachsegmentieren und fachliche Hilfen (z. B. Wasserscheide) sind weiter eigene Arbeit der Agents (Entscheidung 18.11., Vorstufe eher grob); die Vorlagen sagen „Befehl zuerst, eigenes Skript nur, wenn der Befehl den Fall nicht deckt“, kein Verbot. L12 „Skripte als Datei“ bleibt gültig.
- Auch eine Teilkachel mit nachträglich geänderter Segmentzahl (Nachsegmentieren) muss der Prüf-Befehl richtig behandeln: Soll-Segmente aus der aktuellen Label-Karte lesen, nicht aus der ursprünglichen Planzahl (Berührung mit `effiz-nachholen`, K1).
- Parallele Geschwister-Wünsche ändern dieselben Vorlagen: `effiz-bilder` (K4: Bildpflicht, Nahbilder roh und nummeriert nebeneinander, wird den Zoom nutzen), `effiz-viertel` (K7: ein Agent je Viertel, `urteil.json` dann je Viertel; Bau und Prüfung dürfen nicht auf „eine Datei je Teilkachel“ festgelegt sein, besser Eingabe: Teilkachel plus optional Viertel), `effiz-bau-befehle` (K5). Vorlagen und Befehlsbaum mit kleinen, getrennten Änderungen halten, damit das Einreihen ohne Konflikt geht.
- Fallen: Windows-Pfade `C:/Users/...` an Python; Interpreter nur aus dem Profil; keine absoluten Pfade in den Vorlagen (Test in `test_vorlagen.py`); JPEG-Ausgabe der Bilder (nicht PNG wie `ansicht`) und höchstens 2000 Bildpunkte (L11); UTF-8 mit Umlauten; Ausgabe der Agents darf nie in Eingabedaten schreiben (L10).

### Bauweise

Richtung: ohne Zielbild (landseg hat kein `zielbild.md`; Maßstab ist ein sauberer Aufbau: neue Befehle als eigene kleine Module nach dem Muster der vorhandenen Werkzeuge, ohne Kopie der Regeln aus `einigung.py`). Repo ohne Zielbild: Bauzustand ermitteln.
Berührt: landseg: A5 — der Zoom braucht einen Bildleser; `__main__.py:204` `_rgb_bild` ist der Zweitleser, der Zoom nimmt `naht.lese_bild` und fügt keinen dritten hinzu
Tilgt: keine
Flick-Signale: keine — kein Vorgänger (Herkunft ist die Ermittlung landseg-effiz, kein Glied; die Geschwister `effiz-*` sind parallele Wünsche zu anderen Kandidaten, nicht dieselbe Stelle)
Anbau: drei neue Befehle samt Tests neben den vorhandenen, Vorlagen und README ziehen nach — Dauer kurz — Risiko gering bis mittel (zu enges Format nimmt den Agents die Freiheit bei Sonderfällen) — danach bleibt der Zweitleser `_rgb_bild` (A5)
Umbau: Bildleser und Fensterlogik von `ansicht`/`kante` zuerst vereinheitlichen, dann die Befehle — Dauer mittel — Risiko mittel — Netz vorhanden (`tests/test_ansicht.py`, `tests/test_kante.py`) — danach entfällt A5
Belege: `landseg/__main__.py:204` (`_rgb_bild`), `landseg/naht.py:75` (`lese_bild`)
Empfehlung: Anbau — A5 ist eine eigene kleine Altlast und kein Hindernis; der Zoom nutzt den vorhandenen gemeinsamen Leser, der Umbau würde den Wunsch verzögern, ohne ihn zu verbessern

Reihenfolge der Repos: landseg · Risiken: zu starres Format kostet Genauigkeit bei Sonderfällen (Befehl nur Standardweg); Vorlagen werden von Geschwister-Wünschen (K4, K5, K7) gleichzeitig geändert; keine Daten-, Login-, Zahlungs- oder Löschlogik · Vorbedingungen: keine

## Teile

Entfällt (Größe mittel).

## Varianten

Entfällt.

## Entwurf

Stufe: nein — Kommandozeilenbefehle und Auftragsvorlagen, keine Oberfläche für den Nutzer (das Zoombild ist ein Arbeitsbild für Agents).

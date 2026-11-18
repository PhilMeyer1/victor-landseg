# Auftragsvorlagen für Agents

Vorlagen für die Agent-Schritte der Landschafts-Segmentierung (fünf Aufträge, zwei Prompts der Urteils-Agents, vier Aufträge, die `landseg vorbereiten` füllt), je eine Datei mit Platzhaltern
`{{NAME}}`. Die Hauptsession kopiert die Vorlage, setzt alle Platzhalter ein (es darf keiner übrig
bleiben) und gibt den Text als Auftrag weiter. Die Regeln, die für alle Schritte gelten, stehen im
Agent-Skill `landseg-agent` (`.claude/skills/landseg-agent/SKILL.md`); die Vorlagen verweisen darauf
und wiederholen sie nicht.

| Vorlage | Schritt | Abgabe |
|---|---|---|
| `urteil.md` | ein Agent je Teilkachel urteilt über alle Segmente darin | Bilder + `urteil.json` |
| `umsetzen.md` | ein Agent je Teilkachel setzt das bestätigte Urteil auf der Label-Karte um | `labels.tif`, `segmente.json`, `abgabe.json`, Bilder |
| `korrektur.md` | ein Agent je Teilkachel setzt genau die Kommentare des Nutzers um (Runde n) | wie `umsetzen.md` |
| `naht.md` | ein Agent klärt die Nahtverstöße aus `zusammentragen` | geänderte Teilkacheln (neue Runde), `naht_abgabe.json` |
| `agent-urteil-viertel.md` | Prompt eines Urteils-Agents für genau ein Viertel (Fassungen B, C, Gegenprobe): zuerst der ganze Ausschnitt, dann die ganze Teilkachel, dann nur sein Viertel-Auftrag; die Karte zum Nachsegmentieren teilen sich die vier Agents einer Teilkachel | Quittung mit einem Eintrag unter `teile` |
| `agent-urteil-teilkachel.md` | Prompt eines Urteils-Agents für eine ganze Teilkachel (Fassung A „Alles frei“, ohne Viertel) | Quittung mit einem Eintrag unter `teile` (v 0) |
| `urteil-viertel.md` | ein Agent je Viertel urteilt über die Segmente seines Viertels und teilt grob zusammengefasste nach (Fassungen mit Urteil und Gegenprobe; gefüllt von `landseg vorbereiten`) | Bilder + `urteil.json` mit `eingriffe` |
| `frei.md` | ein Agent je Teilkachel segmentiert und klassifiziert frei (Fassung „Alles frei“; gefüllt von `landseg vorbereiten`) | `labels.tif`, `segmente.json`, `kategorien-teil.json` |
| `vereinheitlichen-urteil.md`, `vereinheitlichen-frei.md` | ein Agent legt die freien Klassen einer Fassung zu einer Liste zusammen (Viertel-Urteile bzw. Listen je Teilkachel; gefüllt von `landseg vorbereiten`) | `kategorien-entwurf.json` (+ `codes.json` bzw. `abbildung_teilkacheln`) |
| `abschnitte.md` | Bausteine je Fassung und Bildart, die `landseg vorbereiten` in die Aufträge einsetzt (`{{KATEGORIEN}}`, `{{FASSUNG_ABSCHNITT}}`, `{{GEGENPROBE}}`, `{{FEINHEIT}}`) | – |
| `einigung.md` | ein Agent je Bündel aus `einigung finden` einigt die Klassen an den Übergängen der Teilkacheln (Urteil im Verbund: Bilder beider Seiten, ein Urteil je Stelle für alle Beteiligten, nur Klassen im Kern) | `einigung_abgabe.json` |

Die beiden `agent-urteil-*.md` füllt nicht die Hauptsession, sondern `python -m landseg plan` (README, „plan“):
er bildet aus der Auftragsliste der Vorbereitung einen Agent je Viertel (B, C, Gegenprobe) bzw. je Teilkachel (A)
und setzt den Auftrag des Agents ein, der seinerseits nach `urteil.md` gebaut ist.

Die Vorlagen enthalten keine Pfade dieses Rechners und keinen Einzelfall: Alles Fallbezogene kommt
über die Platzhalter. Für wiederkehrende Schritte nennen sie fertige Befehle als Standardweg
(`urteil bauen`/`urteil pruefen`, `zoom`, `einigung abgabe`; README des Repos); eigene Skripte der
Agents nur für Fälle, die kein Befehl deckt.

## Platzhalter

| Platzhalter | Bedeutung | Beispiel |
|---|---|---|
| `{{PY}}` | Python-Interpreter mit numpy, Pillow, OpenCV, scipy, tifffile (README, „Umgebung“) | Python des venv |
| `{{REPO}}` | Ordner des Repos landseg; Befehle `{{PY}} -m landseg …` laufen dort | Ordner des Repos |
| `{{DATEN}}` | Ordner des Ausschnitts mit `manifest.json` (eingefrorener Stand, nur lesen) | `…/daten/landseg/T0/<lauf>` |
| `{{TEILKACHEL}}` | Kennung der Teilkachel aus dem Manifest | `r0c1` |
| `{{LABELS}}` | Label-Karte, von der der Agent ausgeht (relativ zu `{{DATEN}}`) | `vorstufe/r0c1/labels.tif` |
| `{{SEGMENTE}}` | `segmente.json` dazu (relativ zu `{{DATEN}}`) | `vorstufe/r0c1/segmente.json` |
| `{{URTEIL}}` | bestätigtes `urteil.json` der Teilkachel (relativ zu `{{DATEN}}`) | `urteil/r0c1/urteil.json` |
| `{{ABWEICHUNGEN}}` | was der Nutzer an den Vorlagen anders will, wörtlich, sonst „keine“ | „Segment 17 ist Rain, nicht Weg“ |
| `{{ERGEBNIS}}` | eigener Ergebnisordner des Agents (leer, nur er schreibt dort) | `…/T0/<lauf>/umsetzen/r0c1` |
| `{{BEARBEITER}}` | Name des Agents im Verlauf der Eingriffe | `ums-r0c1` |
| `{{RUNDE}}` | Nummer der Runde, die der Agent abgibt (Umsetzen 0, Korrektur und Naht ab 1) | `1` |
| `{{KOMMENTARE}}` | Kommentare des Nutzers für diesen Agent, wörtlich mit Kennung | `K3: „Hecke reicht bis zum Weg“` |
| `{{AUFTRAG_ZUSAMMEN}}` | `zusammentragen.json` des Ausschnitts (relativ zu `{{DATEN}}`) | `zusammentragen.json` |
| `{{FASSUNG}}` | Kennung der Fassung aus `einstellungen/seite.json` | `A` |
| `{{AUFTRAEGE}}` | Ordner, in den `einigung finden` die Bündel-Aufträge geschrieben hat | `…/T0/<lauf>/einigung-a` |
| `{{BUENDEL}}` | Name des Bündels (Unterordner von `{{AUFTRAEGE}}`) | `A-02` |
| `{{URTEILE}}` | Ordner mit `<teilkachel>/urteil.json` der Fassung (relativ zu `{{DATEN}}`) | `urteil` |
| `{{FASSUNG_NAME}}` | Name der Fassung im Prompt eines Urteils-Agents (`plan`) | `Fassung C „Feste Kategorienliste“` |
| `{{AUSSCHNITT}}` | Name des Ausschnitts | `H0` |
| `{{AUSSCHNITT_BILD}}` | Übersichtsbild des ganzen Ausschnitts (mit Teilkachelgitter, sonst ohne) | `…/H0/ganz/H0_raster.jpg` |
| `{{TEILKACHEL_BILD}}` | Übersichtsbild der ganzen Teilkachel mit Grenzen, Nummern und Vierteln | `…/H0/ganz/r0c0/ganz_nummern.jpg` |
| `{{AUFTRAG}}` | der eine Auftrag des Agents (nach `urteil.md` gebaut) | `…/auftraege/c/r0c0/v2/auftrag.md` |
| `{{VIERTEL}}`, `{{VIERTEL_LAGE}}`, `{{V}}` | Viertel des Agents, seine Lage im Kern, Nummer in der Quittung (A: `{{V}}` 0) | `v2`, `oben rechts`, `2` |
| `{{SEGMENTZAHL}}` | Zahl der Segmente im Viertel-Auftrag | `67` |
| `{{HINWEIS}}` | Satz zum Bild für alle Agents des Laufs, sonst „keiner“ | „Schwarz-Weiß-Scan von 1968“ |
| `{{TEILKACHEL_ROH}}` | Gesamtbild der Teilkachel ohne Grenzen | `…/H0/ganz/r0c0/ganz_roh.jpg` |
| `{{TEILKACHEL_DATEI}}` | Bild der Teilkachel aus dem Manifest (relativ zu `{{DATEN}}`) | `teilkacheln/r0c0.png` |
| `{{VIERTEL_RECHTECK}}` | Lage des Viertels im Teilkachelbild | `x 44–63, y 8–27 im Teilkachelbild (20 × 20 Bildpunkte)` |
| `{{KERNZAHL}}`, `{{JE_VIERTEL}}` | Kernsegmente der Teilkachel, Zahl je Viertel | `130`, `v1 31, v2 40, v3 28, v4 31` |
| `{{BILDER}}` | Ordner der vorbereiteten Bilder (Viertel, Ansicht der Teilkachel bzw. alle Viertel) | `…/H0/viertel/r0c0/v2` |
| `{{NUMMER_MODULO}}` | Nummer im Bild = ID mod diese Zahl (`paar.nummer_modulo` in `einstellungen/ansicht.json`) | `100000` |
| `{{LISTE}}` | Tabelle der Segmente des Viertels (Markdown) | – |
| `{{KATEGORIEN}}`, `{{FASSUNG_ABSCHNITT}}`, `{{GEGENPROBE}}` | Abschnitte aus `abschnitte.md` je Fassung | – |
| `{{ID_GRENZE}}` | IDs der freien Abgabe bleiben darunter (`id_versatz` in `einstellungen/lauf.json`) | `100000` |
| `{{ABGABEN}}` | Tabelle der Abgaben, die eine Vereinheitlichung liest (Markdown) | – |
| `{{FEINHEIT}}` | Feinheit der Bildart: Abschnitt `feinheit-<bildart>` aus `abschnitte.md` mit Richtwert und Mindestfläche aus `einstellungen/bildarten.json`, für Farbbilder leer; Text: `landseg bildart --manifest … --teilkachel … --auftrag` | Absatz „Feinheit auf diesem Schwarz-Weiß-Scan …“ oder leer |
| `{{RICHTWERT}}`, `{{MINDESTFLAECHE_QM}}`, `{{MINDESTFLAECHE_PX}}` | Richtwert der Segmente im Kern und Mindestfläche der Bildart (nur in `abschnitte.md`, `feinheit-<bildart>`) | `150`, `100`, `494` |
| `{{ZUSAMMEN}}` | Ordner des zusammengetragenen Stands mit `labels.tif`, `segmente.json`, `naht.json` (relativ zu `{{DATEN}}`) | `zusammen` |

Nach dem Rücklauf trägt die Hauptsession jede Abgabe als Einheit in `zusammentragen.json` ein
(`teilkachel`, `labels`, `segmente`, `runde`, `name`), bei `naht.md` auch dessen `naht_bestaetigt`,
und ruft `python -m landseg zusammentragen --datei zusammentragen.json` (README, „zusammentragen“). Bei
`einigung.md` ruft sie nach dem Rücklauf aller Bündel einer Fassung einmal `python -m landseg einigung anwenden`
mit allen Abgaben und danach `einigung messen` (README, „einigung“).

Nach jedem Lauf mit diesen Vorlagen misst die Hauptsession die Kosten und übernimmt die Tabelle in den
Bericht des Laufs:
`python -m landseg messung --transkripte <Protokollordner des Laufs> --lauf <Name> --ziel <Berichtsordner>`
(schreibt `messung.md` und `messung.json`; README, „messung“).

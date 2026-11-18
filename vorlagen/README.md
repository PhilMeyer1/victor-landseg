# Auftragsvorlagen für Agents

Vorlagen für die Agent-Schritte der Landschafts-Segmentierung (fünf Aufträge, zwei Prompts der Urteils-Agents), je eine Datei mit Platzhaltern
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

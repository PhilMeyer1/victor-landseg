# landseg

Werkzeuge für die Landschafts-Segmentierung von Luftbildern: Jedes Luftbild wird lückenlos in
Segmente zerlegt, und jedes Segment bekommt eine Kategorie aus einer festen, gestuften Liste.
Grundlage ist die Ermittlung `landseg-methode` im Wunsch-System (Basisordner, `wuensche/`).

## Inhalt

| Pfad | Was |
|---|---|
| `kategorien.json` | Kategorienliste, maschinenlesbar: 7 grobe Klassen (Codes 0 bis 6), 25 auf Ebene 2, 43 feinste Klassen; je Klasse Code, Name, Elternklasse, Ebene, Farbe, SW-Kennzeichen und Abbildungen auf CORINE, CLC+, FLAIR, DKM und Bericht 48; dazu die Regeln G1–G5 und U1–U5 und die Abweichungen A1–A4 |
| `KATEGORIEN.md` | Erklärung der Kategorienliste in Alltagssprache: Aufbau, Klassentabelle, Regeln, Abweichungen von Bericht 48, was noch ungesichert ist |
| `tools/pruefe_kategorien.py` | Prüfskript für `kategorien.json` (nur Python-Standardbibliothek) |
| `tools/gesamt_projekt.py`, `einstellungen/gesamt_projekt.json`, `gesamt/` | Gesamtprojekt für Victor (nur Standardbibliothek): `bauen` legt es aus dem Basisordner an oder frischt es auf (Programm und Unterlagen mit Verlauf per `git subtree`, Wünsche und Arbeitsdaten als Kopie, ohne Original-Luftbilder; committet nur bei Änderungen), `pruefen` (Vollständigkeit, Größen ab 50/100 MB, Pfade in README, ANLEITUNG und CLAUDE.md, `--luftbilder` mit SHA-256), `durchsicht` (Vertrauliches; jede Fundstelle braucht eine Regel in den Einstellungen); `gesamt/` enthält README, Anleitung, `CLAUDE.md` (Anweisung an Claude Code: zu Beginn jeder Session `ergebnisse/T0.html` im Browser öffnen) und Luftbild-Beschreibung des Gesamtprojekts |
| `landseg/` | Python-Paket mit den Werkzeugen, ein Modul je Werkzeug; Befehlszeile `python -m landseg <befehl>` |
| `landseg/kacheln.py` | W1 `kacheln`: Arbeitsausschnitt aus einem Luftbild, Teilkacheln (Kern + Kontextrand), Manifest mit Georeferenz |
| `landseg/vorstufe.py`, `landseg/sam3.py` | W2 `vorstufe`: lückenlose Vorbelegung einer Teilkachel (Superpixel, SAM 3 mit Text je Kategorie, Semantik-argmax), mit Sicherheit je Segment und Kandidatenliste |
| `vorstufe.json` | Einstellungen der Vorstufe: Superpixel-Größe, SAM-3-Modell und -Schwellen, Texte je Kategorie, Schwellen für `sicher` und die Kandidaten, Siedlungszone für `im_siedlung` (Abschnitt `siedlung`) |
| `landseg/ansicht.py` | W3 `ansicht`: Standardbilder je Teilkachel und je Segment (roh, umriss, maengel, vorschlag, nah, kontrast, gitter) mit Verzeichnis `ansicht.json` |
| `landseg/kante.py` | W4 `kante`: Grenze zweier Nachbarsegmente im engen Band auf die Bildkante einrasten; Strecken ohne Bildkante bleiben stehen und werden als „geschätzt“ gemeldet |
| `einstellungen/` | Einstellungen der Werkzeuge als JSON (`ansicht.json`, `kante.json`, `seite.json`, `einigung.json`): Schwellen, Größen, Farben; `--einstellungen <datei>` überschreibt einzelne Schlüssel |
| `landseg/eingriff.py` | W5 `eingriff`: Bearbeiten der Label-Karte (verschmelzen, teilen, Grenze verschieben, Klasse setzen, Polygon zuweisen), immer lückenlos, mit Verlauf |
| `landseg/pruefen.py` | W6 `pruefen`: Wächter der Lückenlosigkeit (H × W ohne 0, Zusammenhang je Segment, gültige Klassen) |
| `landseg/zusammentragen.py` | W7 `zusammentragen`: Abgaben der Teilkacheln (je Teilkachel die letzte Runde, nur der Kern) zur Label-Karte des Ausschnitts; Einheiten, Klassen des Nutzers und offene Fragen aus einem JSON-Auftrag |
| `landseg/seite.py`, `landseg/seite_vorlage/` | W8 `seite`: Übersichtsseite als eine HTML-Datei (je Bild das Ergebnis, Umschalter zwischen den Fassungen A/B/C mit je eigener Kategorienliste, Ebenen grob/mittel/fein, Lücken, Nähte, Kategorienliste, Kommentare mit Export); Vorlage aus HTML, CSS und JavaScript |
| `landseg/naht.py` | Nahtregel: an jeder Kerngrenze gleiche ID oder echte Bildkante, gleiche Klasse |
| `landseg/einigung.py` | `einigung`: Klassen an den Übergängen der Teilkacheln abgleichen (`finden`: offene Stellen bündeln, je Bündel Agent-Auftrag mit Bildern beider Seiten; `anwenden`: Abgaben umsetzen, nur Klassen und Vermerke; `messen`: Stellen gleicher Fläche mit verschiedener Klasse, offen/unsicher/geklärt); Einstellungen `einstellungen/einigung.json` |
| `vorlagen/` | Auftragsvorlagen für Agents (Urteil, Umsetzen, Korrektur, Naht, Einigung) mit Platzhaltern, erklärt in `vorlagen/README.md` |
| `.claude/skills/landseg-agent/SKILL.md` | Agent-Skill mit den Arbeitsregeln für diese Aufträge |
| `landseg/kategorien.py`, `landseg/dateien.py` | Kategorienliste laden; Lesen und Schreiben von Label-Karte, `segmente.json`, Manifest |
| `tests/` | Tests (Python-Standardmodul `unittest`, synthetische Bilder und Label-Karten) |


## Umgebung

Das Repo hat noch keine eigene Python-Umgebung. Alle Befehle laufen mit dem Python des Stitcher-venv
(dort nichts installieren): `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe`,
unten kurz `PY`. Aufruf immer im Repo-Ordner, damit Python das Paket `landseg` findet.

## Begriffe und Dateien

- **Label-Karte** (`labels.tif`): für jeden Bildpunkt die Nummer (ID) seines Segments, 32 Bit ohne
  Vorzeichen; 0 heißt „kein Segment“ und darf in einer fertigen Karte nicht vorkommen. Gespeichert als
  einkanaliges TIFF, weil PNG nur bis 16 Bit reicht.
- **`segmente.json`**: je Segment `id`, `klasse` (Code aus `kategorien.json`, feinste sichere Ebene),
  `grob` (Ebene-1-Klasse), dazu Felder wie `herkunft`; unter `verlauf` jeder Eingriff mit Zeit und
  Bearbeiter.
- **Sicherheit** (`sicher: ja | nein` in `segmente.json`, von der Vorstufe): ob der Klassenvorschlag
  die Schwellen aus `vorstufe.json` erreicht; `nein` heißt „Klasse prüfen“, nicht „falsch“.
- **Im Siedlungsgebiet** (`im_siedlung: ja | nein` in `segmente.json`, von der Vorstufe): ob ein
  Segment aus Acker, Grünland oder Gehölz außerhalb Wald überwiegend nahe an Gebäuden und befestigten
  Flächen liegt (Abschnitt `siedlung` in `vorstufe.json`). Merkmal, keine Klasse; ein Klassenwechsel
  ändert es nicht. Für Auswertungen nach Bericht 48 macht `bericht48_klasse` in
  `landseg/kategorien.py` daraus „1 Versiegelt / bebaut“ (`KATEGORIEN.md`, „Siedlungsgebiet und Bericht 48“).
- **Kandidatenliste** (`kandidaten.json`, von der Vorstufe): Stellen, die das Urteil zuerst ansehen
  soll: `klasse_unsicher`, `grenze_ohne_bildkante` (zwei Segmente grenzen dort aneinander, wo das
  Bild kaum eine Kante zeigt), `nicht_zusammenhaengend` (ein Fund von SAM 3 zerfiel in mehrere
  Segmente), `zu_klein`.
- **Manifest** (`manifest.json`, von `kacheln`): Quelle, Ausschnitt, Raster und je Teilkachel Bild,
  Kern, Kontext und Lage. Alle Pfade relativ zum Ordner des Manifests. Koordinaten in Bildpunkten:
  `kern` und `kontext` relativ zum Ausschnitt, `kern_im_bild` relativ zum Bild der Teilkachel;
  `transform` rechnet die Ecke oben links eines Bildpunkts in Landeskoordinaten um (EPSG aus der
  `.prj`). Neben jedem PNG liegt eine Weltdatei `.pgw` für GIS-Programme.
- **Zusammenhang** heißt: Bildpunkte eines Segments hängen über gemeinsame Kanten zusammen (nur über
  eine Ecke reicht nicht).

## Erster Durchgang: von T0 bis zur Übersichtsseite

Im Repo-Ordner, `PY` wie unter „Umgebung“. `<ausschnitt>` steht für den Ergebnisordner des
Ausschnitts außerhalb des Repos (hier `../daten/landseg/T0/<lauf>`); alle Ergebnisse landen dort.

```
PY -m landseg kacheln --bild ../daten/luftbilder/orthofoto-aktuell/0009626524_100_Orthophoto_aktuell_5236-56.tif    --x 2000 --y 2400 --breite 1000 --hoehe 1000 --kern 500 --rand 64 --name T0 --ziel <ausschnitt>
PY -B -m landseg vorstufe --manifest <ausschnitt>/manifest.json --teilkachel r0c0
PY -m landseg pruefen --labels <ausschnitt>/vorstufe/r0c0/labels.tif    --segmente <ausschnitt>/vorstufe/r0c0/segmente.json --bild <ausschnitt>/teilkacheln/r0c0.png
PY -B -m landseg seite --manifest <ausschnitt>/manifest.json --ziel <ausschnitt>/seite/T0.html --oeffnen
```

1. `kacheln` schneidet das Testfenster in vier Teilkacheln (siehe unten).
2. `vorstufe` belegt eine Teilkachel lückenlos vor (GPU, rund eine halbe Minute; ohne `--teilkachel`
   alle vier). Die Messzeile nennt Segmente, Anteil „unsicher“ und Kandidaten.
3. `pruefen` muss mit `ok` enden.
4. `seite` schreibt die Übersichtsseite und öffnet sie im Browser (ohne `--oeffnen` die Datei
   `T0.html` selbst doppelklicken). Teilkacheln ohne Daten erscheinen leer, Fassungen ohne Daten
   ausgegraut.

Die Seite zeigt je Fassung ein Ergebnis. Welche Fassungen es gibt, in welcher Reihenfolge und wo
ihre Daten liegen, steht unter `fassungen` in `einstellungen/seite.json`; die Seite öffnet mit der
ersten Fassung mit Daten:

| Kennung | Name | Ordner neben dem Manifest | Kategorienliste |
|---|---|---|---|
| A | Alles frei | `a-alles-frei/` | eigene, `a-alles-frei/kategorien-a.json` |
| B | Kategorien frei | `b-kategorien-frei/` | eigene, `b-kategorien-frei/kategorien-b.json` |
| C | Feste Kategorienliste | `c-feste-liste/` | die Liste des Aufrufs (`--kategorien`, Standard `kategorien.json` des Repos) |

In jedem Ordner liegt je Teilkachel `<teilkachel>/labels.tif` und `segmente.json`. Nach der
Vorstufe hat noch keine Fassung Daten: Die Vorstufe ist der Ausgang von B und C (Kopie von
`vorstufe/<teilkachel>/` nach `c-feste-liste/<teilkachel>/`, dann das Urteil), oder man zeigt sie
mit einer eigenen Fassungsliste. Liegt ein Ergebnis woanders, nennt eine eigene Datei mit dem
Schlüssel `fassungen` die Ordner: `seite … --einstellungen <datei.json>`.

## Befehle

Abgeleitete Daten gehören nach `daten/landseg/` im Basisordner, nie ins Repo und nie zu den
Originalen. Exit-Code 0 = in Ordnung, 1 = Befund bzw. Eingriff abgelehnt, 2 = Aufruf- oder Lesefehler.

### kacheln

Testfenster T0 (Blatt 5236-56, x 2000, y 2400, 1000 × 1000 Bildpunkte) in vier Teilkacheln mit
Kern 500 und Kontextrand 64:

```
PY -m landseg kacheln --bild ../daten/luftbilder/orthofoto-aktuell/0009626524_100_Orthophoto_aktuell_5236-56.tif \
   --x 2000 --y 2400 --breite 1000 --hoehe 1000 --kern 500 --rand 64 --name T0 --ziel <ausschnitt>
```

Ergebnis: `T0.png` (ganzer Ausschnitt), `teilkacheln/r<zeile>c<spalte>.png` (Kern plus Rand, Rand
aus dem Originalbild, nur am Bildrand abgeschnitten) und `manifest.json`. Die Kerngröße ist frei
(`--kern 250` ergibt 16 Teilkacheln); geht sie nicht auf, sind die letzten Kerne kleiner. Ein
vorhandenes Manifest wird nur mit `--ueberschreiben` ersetzt.

### vorstufe

Braucht die GPU (SAM 3, Modell `facebook/sam3` aus dem Zwischenspeicher von Hugging Face). Ist sie
belegt, den Befehl später wiederholen; auf der CPU rechnet die Vorstufe nicht.

```
PY -m landseg vorstufe --manifest <ausschnitt>/manifest.json --teilkachel r0c0
```

Ohne `--teilkachel` laufen alle Teilkacheln des Manifests: SAM 3 Teilkachel nach Teilkachel auf der
GPU, die übrigen Schritte gleichzeitig. Ablauf je Teilkachel: (a) Superpixel (SLIC), (b) SAM 3 mit
den Texten je Kategorie aus `vorstufe.json` liefert Funde (Instanzen), (c) dazu je Bildpunkt einen
Wert je Kategorie (Semantikkopf mal „Presence“), (d) Funde rasten auf Superpixel ein (kleinste
zuerst), übrige Superpixel bekommen die Kategorie mit dem höchsten Wert und verbinden sich mit
gleichartigen Nachbarn, (e) `pruefen`. Jede Stelle gehört so zu genau einem zusammenhängenden
Segment.

Ausgabe unter `vorstufe/<teilkachel>/` neben dem Manifest: `labels.tif`, `segmente.json` (je
Segment `id`, `klasse`, `grob`, `herkunft` `sam3-instanz` oder `semantik`, `sicher`, `sicherheit`,
`flaeche`, `im_kern`, `im_siedlung`; unter `vorstufe` die Messung), `kandidaten.json` und `sam3_roh.npz` (Rohwerte
von SAM 3). Je Teilkachel eine Messzeile: Segmente (davon im Kern), Anteil `sicher: nein` nach Zahl
und Fläche, Kandidaten, Befund von `pruefen`, Laufzeit. Die Segment-IDs sind im ganzen Ausschnitt
eindeutig (Nummer der Teilkachel × `id_block` + laufende Nummer).

Eine fertige Teilkachel mit denselben Einstellungen wird übersprungen; `--neu` rechnet sie neu und
nimmt dabei die gespeicherten Rohwerte, solange die SAM-3-Einstellungen und Texte gleich sind (dann
ohne GPU). `--bild <png> --ziel <ordner>` rechnet ein einzelnes Bild, `--konfig` nimmt andere
Einstellungen.

### ansicht

```
PY -m landseg ansicht --manifest <ausschnitt>/manifest.json --teilkachel r0c0    --labels <labels.tif> --segmente <segmente.json> --ziel <ausschnitt>/ansicht/r0c0
```

Schreibt `teilkachel/<art>.png` (roh, umriss, maengel, vorschlag, kontrast, gitter) und je Segment
`segmente/<id>/<art>.png` (dieselben plus `nah`), dazu `ansicht.json` mit Fenster und
Vergrößerungsfaktor je Segment: `x_teilkachel = fenster.x + x_bild // faktor` (`roh` je Segment im
Maßstab 1; im Gitterbild vorher 40 px links und 16 px oben abziehen). Das Gitter ist in Bildpunkten
der Teilkachel beschriftet, `vorschlag` färbt nach der Klassenfarbe aus `kategorien.json`,
`maengel` zeigt Lücken, nicht zusammenhängende Segmente, fehlende Einträge, `sicher: nein`,
`--mindestflaeche`, `--kandidaten <json>` und mit `--kante <bericht.json>` die geschätzten Strecken.
Ohne `--labels` entstehen nur roh, kontrast und gitter; `--ids 3,5` und `--nur-teilkachel` begrenzen.

### kante

```
PY -m landseg kante --labels <labels.tif> --segmente <segmente.json> --bild <teilkachel.png>    --bearbeiter <name> --a 12 --b 17 [--band 4] [--bereich x,y;x,y;...] [--bericht kante.json]
```

Rastet die Grenze zwischen Segment `a` und `b` im Band (Standard ±4 Bildpunkte) auf die Bildkante
ein (Wasserscheide mit Marken); nur Bildpunkte von `a` und `b` im Band wechseln, die Karte bleibt
lückenlos, beide Segmente bleiben zusammenhängend (sonst abgelehnt, Exit 1). Wo die Grenze auf
keiner Bildkante liegt (Kantenstärke unter `kante_min`), bleibt sie unverändert und wird als
„geschätzt“ gemeldet, mit Anfang, Ende, Länge und Kantenstärke. `--trocken` meldet nur,
`--bericht` schreibt die Meldung mit allen Punkten (für `ansicht --kante`). Der Eingriff steht im
Verlauf von `segmente.json`.

### seite

```
PY -B -m landseg seite --manifest <manifest.json> --ziel <seite.html> [--einstellungen <datei.json>] [--kategorien <kategorien.json>] [--kommentare <kommentare.json>]... [--oeffnen]
PY -B -m landseg seite --daten <ordner> --ziel <seite.html> [dieselben Schalter]
```

Mehrere Bilder auf einer Seite: Mit `--daten <ordner>` nimmt die Seite alle Bilder unter `bilder` in
`einstellungen/seite.json` (je Bild `kennung`, `name`, `beschreibung`, `manifest` relativ zu `--daten` oder
absolut, wahlweise `ordner` = Kennung der Fassung -> eigener Ordner für dieses Bild). Voreingestellt sind
`T0/manifest.json` (Orthofoto T0) und `H0/manifest.json` (historischer Ausschnitt H0, Scan 1968). Oben neben den
Fassungen steht dann die Bildwahl; sie wechselt Bild, Teilkacheln, Nähte-Zahlen, Einigung und Kategorienliste
ohne Neuladen und behält Fassung, Ansicht und Teilkachel, soweit es sie im anderen Bild gibt. Ein Bild ohne
Manifest oder ohne Daten erscheint ausgegraut; erst wenn kein Bild Daten hat, bricht `seite` ab. Lage
(Georeferenz) braucht die Seite nicht; ein Scan ohne Weltdatei (Manifest `georeferenz: null`) und Graustufen
gehen wie ein Orthofoto. Links der Seite: `#/<Bild>/<Fassung>/kachel/<tk>` (alte Links ohne Bild gelten dem
ersten Bild). Kommentare stehen je Bild getrennt im Browser; der Export nennt `bild`, `ausschnitt` und
`manifest`, danach ordnet `--kommentare` (mehrfach möglich) jede Datei ihrem Bild zu. Mit `--manifest` entsteht
eine Seite mit genau diesem Bild, ohne Bildwahl.

`kacheln` liest Graustufen-Scans einkanalig (`kanaele: 1`) und übersetzt Palettenbilder über ihre Farbtafel
(nur Grautöne: Graustufen), statt die Indizes zu schreiben.

Schreibt eine HTML-Datei, die ohne Server im Browser aufgeht (Bilder und Daten stecken darin, für
vier Teilkacheln und eine Fassung rund 7 MB). Sie zeigt je Teilkachel ein großes Bild mit dem
Ergebnis einer Fassung (Mausrad vergrößert, Ziehen verschiebt). Oben schaltet man zwischen den
Fassungen um (Name und Kurzbeschreibung stehen darunter); eine Fassung ohne Daten ist ausgegraut.
Jede Fassung bringt ihre eigene Kategorienliste im Format von `kategorien.json` mit (Code, Name,
Eltern, Ebene, Farbe); Klassen, Namen, Farben und die Ebenen-Knöpfe kommen nur daraus. Welche
Fassungen es gibt, steht unter `fassungen` in `einstellungen/seite.json` (`kennung`, `name`,
`beschreibung`, `ordner` relativ zum Ordner des Manifests, `kategorien` relativ zum Ordner der
Fassung; ohne `kategorien` gilt `--kategorien`, Standard die Liste des Repos); `--einstellungen`
ersetzt die Liste. Liegt im Ordner einer Fassung keine Teilkachel, ist sie ausgegraut; fehlt bei
vorhandenen Daten die eigene Kategorienliste, bricht der Befehl mit Exit 2 ab.

Die Maus nennt für die Stelle unter ihr das Segment mit allen Ebenen
(`1 Versiegelt / bebaut … › 1.1 Gebäude › 1.1.1 Hauptgebäude …`) und „sicher“ oder „unsicher“; ein Klick wählt ein
Segment („Gewählt“), die Leiste zeigt es im selben Format samt aller Felder aus `segmente.json`.
Schalter: Ebene (grob/mittel/fein, soweit die Fassung sie hat), Flächen (mit Deckkraft), Umriss,
Lücken (Bildpunkte ohne Segment rot), Nähte (Verstöße der Nahtregel an den Kerngrenzen, auf den
zusammengesetzten Kernen geprüft, sobald alle Teilkacheln einer Fassung vorliegen; dazu zwei getrennte Zahlen
je Teilkachel und für den ganzen Ausschnitt: „Schnittlinien an Nähten ohne Bildkante“ wie `naht` und „Stellen, an
denen gleiche Flächen verschiedene Klassen haben (davon unsicher belegt)“ wie `einigung messen`, ein Segment-Paar
je Stelle, Nähte und Viertelgrenzen; das Luftbild liest die Seite mit `naht.lese_bild`), Nur unsicher,
Gitter (alle `gitter_abstand` Bildpunkte), Kategorien (Liste mit Segmentzahl und Flächenanteil;
Klick hebt eine Kategorie hervor). Unter dem Kopf liegt die Kachel-Wahl in fester Höhe: „vorige“,
„Ganzer Ausschnitt“, je Teilkachel ein Reiter mit Nummer, Miniatur des Kerns, Raster-Symbol und Lage in
Worten („oben links“ …, aus `zeile`/`spalte`; die Kennung `r0c0` klein dabei), „nächste“; die Pfeiltasten
← → gehen dieselben Schritte (nicht in Eingabefeldern). Im Bild steht „Teilkachel n von N“ mit dem
nächsten Schritt. „Ganzer Ausschnitt“ zeigt den Ausschnitt mit Kerngrenzen, Nummer und Lage je Kern und
Nahtverstößen. Auf schmalen Bildschirmen (bis 760 px) entfallen die Leisten links und rechts. Kommentare zum gewählten Segment werden im Browser vorgemerkt und unter
„Export (JSON)“ als `kommentare-<name>.json` (`schema` `landseg-kommentare/1`, je Kommentar mit
`fassung`) gespeichert; `--kommentare` zeigt eine solche Datei wieder an. Farben und
Voreinstellungen der Seite stehen in `einstellungen/seite.json`.

### pruefen

```
PY -m landseg pruefen --labels <labels.tif> --segmente <segmente.json> --bild <teilkachel.png>
```

Meldet `H × W`, die Zahl der Bildpunkte ohne Segment, die Zahl der Segmente und endet mit `ok` oder
`FEHLER` samt Liste der Mängel (Lücke, nicht zusammenhängend, Segment ohne Eintrag oder ohne
Bildpunkte, ungültige Klasse). `--form HxW` statt `--bild` gibt die erwartete Größe direkt an,
`--kategorien` eine andere Kategorienliste, `--mindestflaeche N` meldet kleinere Segmente, `--json`
gibt den Befund maschinenlesbar aus.

### eingriff

```
PY -m landseg eingriff --labels <labels.tif> --segmente <segmente.json> --bearbeiter <name> <operation> ...
```

| Operation | Wirkung |
|---|---|
| `verschmelzen --ids 3,5 [--ziel 3]` | benachbarte Segmente zu einem; das Ziel (Standard: erste ID) behält ID und Klasse |
| `teilen --id 4 --linie "x,y;x,y;..."` | teilt ein Segment entlang eines Linienzugs; das größte Teil behält die ID |
| `verschieben --von 5 --nach 3 --flaeche "x,y;..."` | Bildpunkte von 5 im Polygon gehen an den Nachbarn 3 (Grenze verschieben) |
| `klasse --id 4 --klasse 3.1` | setzt die Klasse (und die grobe Klasse) |
| `polygon --flaeche "x,y;..." (--id N \| --klasse C)` | alles im Polygon an ein angrenzendes Segment oder an ein neues mit Klasse; dadurch zerteilte Nachbarn bekommen eigene IDs |
| `stapel --datei schritte.json` | mehrere Schritte `{"schritte": [{"op": "teilen", "id": 4, "linie": [[0, 5], [9, 5]]}, ...]}`, alle oder keiner |

Koordinaten sind Bildpunkte der Label-Karte (`x` Spalte, `y` Zeile). Ein Eingriff schreibt nur
Segment-Nummern auf vorhandene Bildpunkte um, Lücken entstehen also nie. Ist er nicht ausführbar
(Segmente nicht benachbart, Linie trennt nicht, Klasse unbekannt), bleibt alles unverändert. Danach
läuft `pruefen` von selbst und meldet den Befund.

### zusammentragen

```
PY -m landseg zusammentragen --datei <ordner>/zusammentragen.json
```

Der Auftrag `zusammentragen.json` (Pfade relativ zu seinem Ordner) nennt alles Fallbezogene:

```
{"schema": "landseg-zusammentragen/1",
 "manifest": "manifest.json",
 "ausgang": "vorstufe/segmente.json",
 "einheiten": [{"teilkachel": "r0c0", "labels": "umsetzen/r0c0/labels.tif",
                "segmente": "umsetzen/r0c0/segmente.json", "runde": 0, "name": "ums-r0c0"}],
 "nutzerklassen": [{"id": 17, "klasse": "3.1.1", "kommentar": "Einzelbaum"}],
 "fragen": [{"id": "F1", "text": "Weg oder Feldrain?", "segmente": [17]}],
 "naht": {"kante_schwelle": 25, "kante_band": 1, "mindestlaenge": 1},
 "naht_bestaetigt": [{"naht": "r0c0|r0c1", "ids": [3, 7], "grund": "Feldgrenze, kaum Farbsprung"}],
 "ziel": "zusammen"}
```

- `einheiten`: je Teilkachel eine Abgabe; gibt es mehrere, gilt die mit der höchsten `runde`
  (Korrekturrunden). Die Label-Karte hat die Größe des Teilkachelbilds (dann zählt nur der Kern)
  oder nur des Kerns. Eine Teilkachel ohne Einheit bleibt leer und fällt in `pruefen` als Lücke auf.
- `ausgang` (wahlweise): `segmente.json` der Vorstufe; deren IDs gelten als global. Eine andere ID,
  die mehrere Teilkacheln neu vergeben haben, bekommt außer in der ersten eine neue Nummer
  (`umbenannt`). Ohne `ausgang` gelten alle IDs als global.
- `nutzerklassen`: Klassen, die der Nutzer festgelegt hat; sie gehen allem vor und entscheiden
  auch einen Klassenkonflikt an der Naht. `fragen`: offene Fragen für die Prüfseite; das Ergebnis
  ergänzt je Frage die Lage (`bbox` [x0, y0, x1, y1] im Ausschnitt).
- `naht`, `naht_bestaetigt` (wahlweise): Einstellungen der Nahtregel und Grenzen, die ein
  Bearbeiter am Bild als echt bestätigt hat.

Ergebnis im Ordner `ziel`: `labels.tif` (ganzer Ausschnitt), `segmente.json` (je Segment mit
`teilkacheln`, dazu `fragen` und `verlauf`) und `naht.json` (Nahtbefund, Klassenkonflikte,
Umbenennungen, Mängel, Befund von `pruefen`). Die Ausgabe endet mit `Zusammentragen ok` oder
`Zusammentragen FEHLER`; dann Exit-Code 1, die Dateien werden trotzdem geschrieben (der Naht-Agent
braucht sie). `--ziel` schreibt woandershin, `--json` gibt das Ergebnis maschinenlesbar aus.

**Nahtregel.** An jeder Kerngrenze zweier Nachbarkacheln stehen sich je Position zwei Bildpunkte
gegenüber. Sie tragen dieselbe ID, oder zwischen ihnen liegt eine echte Bildkante (Farbsprung von
mindestens `kante_schwelle`, gesucht bis `kante_band` Bildpunkte neben der Grenze). Sonst ist es ein
Verstoß `ohne_kante` (zwei Bearbeiter haben dieselbe Fläche verschieden zugeordnet, oder die Grenze
ist nur die Gerade der Kachelung). Eine ID, die in zwei Teilkacheln vorkommt, muss dort dieselbe
Klasse haben, sonst Verstoß `klasse`. Strecken kürzer als `mindestlaenge` zählen nicht.

### naht

```
PY -m landseg naht --manifest <manifest.json> --labels <labels.tif des Ausschnitts> [--datei zusammentragen.json]
```

Prüft nur den ID-Teil der Nahtregel auf einer schon zusammengetragenen Label-Karte, etwa nach einem
Eingriff des Naht-Agents; `--datei` liefert Einstellungen und bestätigte Grenzen.

### einigung

```
PY -B -m landseg einigung finden   --manifest <manifest.json> --fassung <A|B|C> --ziel <neuer Ordner>
PY -B -m landseg einigung anwenden --manifest <manifest.json> --fassung <A|B|C> --auftraege <Ordner von finden> --abgabe <einigung_abgabe.json> [--abgabe …] [--ziel <neuer Ordner>] [--probe]
PY -B -m landseg einigung messen   --manifest <manifest.json> [--fassung <A|B|C>]
```

Fester Schritt nach dem Zusammentragen der Urteile, vor dem Erzeugen der Seite: An den Kerngrenzen
(Nähte samt Ecken) und an den Viertelgrenzen (Mitte jedes Kerns) sucht `finden` die Segment-Paare, die
ohne Bildkante aneinandergrenzen (Bildkanten-Regel und Bildleser wie `naht`) und verschiedene Klassen
tragen. Ein Segment heißt `<teilkachel>:<id>`, ein Paar `<segment>|<segment>`. Paare, die ein Segment
teilen, bleiben in einem Bündel (eine Ecke also auch); jede kleine Gruppe kommt in das erste Bündel,
das noch Platz bis `buendel_paare` Paare hat, eine größere bleibt allein (`uebergross`). Je Bündel entsteht `<ziel>/<fassung>-<nr>/auftrag.json` mit `paar_<nr>.jpg` (Luftbild
beider Seiten, rechts mit beiden Segmenten und der Grenze), dazu `<ziel>/einigung.json` (Zahlen,
Bündel). Ein Agent je Bündel urteilt nach `vorlagen/einigung.md` und gibt `einigung_abgabe.json` ab;
`anwenden` setzt je Paar `gleich` (gemeinsame Klasse der Kategorienliste der Fassung, per `eingriff`),
`grenze` (nichts ändert sich) oder `unklar` (beide `sicher: nein`) um und vermerkt bei jedem beteiligten
Segment unter `einigung` Entscheidung, Grund, Bearbeiter und Bündel, mit Verlaufseintrag. Label-Karten
bleiben unberührt; nur Segmente im Kern; alles oder nichts (Exit 1 bei abgelehnter Abgabe). `messen`
zählt je Fassung die Stellen (Paare, Strecken, Randpunkte): offen, unsicher belegt, geklärt, dazu alle
Schnittlinien ohne Bildkante; Exit 1, solange etwas offen ist. Die Fassungen (Ordner, Kategorienliste)
kommen aus `einstellungen/seite.json`, wahlweise `--ordner`.

## Auftragsvorlagen

`vorlagen/urteil.md`, `umsetzen.md`, `korrektur.md`, `naht.md`, `einigung.md`: Aufträge für Agents mit Platzhaltern
`{{NAME}}` (Liste in `vorlagen/README.md`), ohne Pfade dieses Rechners. Die Regeln, die für alle
gelten, stehen im Skill `.claude/skills/landseg-agent/SKILL.md`.

## Tests

```
PY -B -m unittest discover -s tests -t .
```

## Kategorienliste prüfen

Im Repo-Ordner, mit dem Python des Stitcher-venv (dort nichts installieren) oder jedem Python 3:

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I tools/pruefe_kategorien.py kategorien.json
```

Ausgabe: die Zahlen je Ebene (`7/25/43`), die Zahl der Regeln (`5 G, 5 U`), der kleinste
Farbabstand und am Ende `ok`. Bei einem Fehler nennt das Skript die Stelle und endet mit Code 1.

## Daten

Originalbilder und abgeleitete Daten (Kacheln, Label-Karten) liegen nie im Repo: Originale unter
`daten/luftbilder/` des Basisordners (nur lesen), Abgeleitetes unter `daten/landseg/`.

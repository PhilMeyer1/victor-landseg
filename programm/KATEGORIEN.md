# Kategorien der Landschafts-Segmente

Diese Liste legt fest, welche Kategorie ein Stück Luftbild bekommen kann. Jeder Bildpunkt gehört zu
genau einem Segment, und jedes Segment bekommt genau eine Kategorie aus dieser Liste — die Karte hat
also keine Lücken. Die Liste steht maschinenlesbar in `kategorien.json`; dieses Dokument erklärt sie.

Herkunft: Ermittlung `landseg-methode`, Teil e02 (Vorschlag einer gestuften Liste) mit Gegenprüfung,
und die Entscheidungen des Nutzers vom 17.11.2026 (F1 bis F7 in `wuensche/entscheidungen.md` des
Basisordners). Seit dem 17.11.2026 gilt dazu die Entscheidung „Bedeckung statt Nutzung“: Rasen
und unbefestigte Wege werden nach dem eingeordnet, was im Bild liegt; ob ein Segment im
Siedlungsgebiet liegt, ist ein eigenes Merkmal (siehe „Siedlungsgebiet und Bericht 48“). Seit dem
18.11.2026 haben Haus- und Hofgärten eine eigene Unterklasse „Garten“ (3.6) im Dauergrünland
(Entscheidung „Gärten als Dauergrünland mit Unterklasse Garten“, siehe „Garten“ unter der Tabelle).

## Aufbau: drei Ebenen

Die Kategorien sind wie ein Baum gestuft:

- **Ebene 1 (7 Klassen, Codes 0 bis 6):** die groben Klassen. Das sind die sechs Klassen aus
  Bericht 48 (Versiegelt/bebaut, Acker, Dauergrünland, Wald, Gewässer, Offener Boden) und dazu
  „Nicht bestimmbar“ für Bildfehler und Wolken.
- **Ebene 2 (26 Klassen, z. B. 1.2 Verkehrsfläche):** eine feinere Unterteilung jeder groben Klasse.
- **Ebene 3 (z. B. 1.2.1 Straße):** die feinsten Klassen, wo das Bild sie hergibt.

Der Code verrät die Ebene: Ein Code ohne Punkt ist Ebene 1, mit einem Punkt Ebene 2, mit zwei Punkten
Ebene 3. Nicht jede Klasse der Ebene 2 ist weiter unterteilt; „Ackerbrache“ (2.3) zum Beispiel ist
schon die feinste Stufe. Klassen ohne Unterklassen heißen Blätter; es gibt 44 davon (über alle
Ebenen gezählt). Insgesamt hat die Liste 59 Klassen.

Wichtig: Auch eine grobe Klasse ist eine gültige Antwort (Regel G5). Wer nicht sicher sagen kann, ob
ein Weg befestigt ist, nimmt „Verkehrsfläche“ (1.2) statt zu raten (Regel U1).

## Was noch nicht gesichert ist

- **Spalte SW ist eine Vermutung bis zum Test.** Sie sagt, ob eine Klasse auch auf alten
  Schwarz-Weiß-Luftbildern (0,5 bis 1 m je Bildpunkt) sicher erkennbar ist: `ja` = sicher,
  `eing.` = eingeschränkt, dann wird oft die Elternklasse genommen, `nein` = nur auf Farbbildern.
  Die Werte stammen aus Bericht 48 oder sind geschätzt; erst der Test am Ausschnitt T0 zeigt, ob sie
  stimmen.
- **Die Abbildungen auf CORINE, CLC+, FLAIR und DKM sind eine eigene Zuordnung, nicht gegen
  amtliche Tabellen geprüft.** Sie sagen, welcher Klasse in diesen bekannten Verzeichnissen eine
  Kategorie ungefähr entspricht. Die CORINE-Codes sind aus dem Gedächtnis zugeordnet. Mehrere
  Werte bedeuten „eine von diesen, je nach Fall“. Die Abbildungen stehen nur in `kategorien.json`.
- **Die Farben** hat der Umsetzer festgelegt: jede grobe Klasse eine Farbfamilie (Nicht bestimmbar
  grau, Bebaut rot bis violett, Acker gelb, Grünland hellgrün, Wald dunkelgrün, Gewässer blau,
  Offener Boden braun). Das Prüfskript sorgt dafür, dass alle 59 Farben deutlich verschieden sind.
  Garten (3.6) ist ein helles Mintgrün, das sich von allen anderen Grüntönen am weitesten abhebt.

## Die Klassen

| Code | Klasse | Woran man sie im Bild erkennt | SW (Vermutung) | Farbe |
|---|---|---|---|---|
| 0 | **Nicht bestimmbar (technisch)** (Abweichung A1) | Bildfehler, Scanrand, Rahmenmarke, Wolke | ja | `#808080` |
| 0.1 | › Bildfehler / Scanrand / Rahmenmarke / Kratzer | außerhalb Bildinhalt, Linien, Flecken | ja | `#383838` |
| 0.2 | › Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | weiß bzw. völlig schwarz, keine Struktur | ja | `#d9d9d9` |
| 1 | **Versiegelt / bebaut (Siedlung und Verkehr)** | Form, harte Kanten | ja | `#bd2835` |
| 1.1 | › Gebäude | Dach, Schlagschatten, rechteckig | ja | `#eb21ed` |
| 1.1.1 | › › Hauptgebäude (Wohn-, Betriebsgebäude) | groß, mit Zufahrt | eing. | `#e61382` |
| 1.1.2 | › › Nebengebäude / Schuppen / Stadel | klein, oft im Garten oder Feld | eing. | `#d370f3` |
| 1.1.3 | › › Gewächshaus / Folientunnel | hell, glänzend, Bögen | eing. | `#e63d13` |
| 1.2 | › Verkehrsfläche | lang, gleich breit, verbunden | ja | `#f584cd` |
| 1.2.1 | › › Straße (versiegelt) | glatt, Markierung | ja | `#f19daa` |
| 1.2.2 | › › Weg, befestigt (Asphalt, Pflaster) | schmal, glatt | eing. | `#d4aee0` |
| 1.2.4 | › › Platz / Parkplatz / Hoffläche versiegelt | flächig, glatt | ja | `#ce5678` |
| 1.2.5 | › › Bahnkörper | Gleise, Schotterbett | ja | `#930fbf` |
| 1.3 | › Sonstige künstliche Fläche | – | eing. | `#740b84` |
| 1.3.1 | › › Lager-, Schotter-, Kiesfläche (künstlich, unversiegelt) (Abweichung A3) | hell, körnig, ohne Bewuchs | eing. | `#a21771` |
| 1.3.2 | › › Baustelle | Erdbewegung, Maschinen | eing. | `#572768` |
| 1.3.3 | › › Schwimmbecken | türkis bzw. glatt, scharfe Form | nein | `#840b2d` |
| 1.3.4 | › › Sport-, Spielplatz (künstlicher Belag) | Linien, Form | eing. | `#b370c9` |
| 2 | **Acker (und Dauerkulturen)** | Parzellen, Bearbeitungsspuren | ja | `#eec72b` |
| 2.1 | › Acker mit Bewuchs | gleichmäßige Fläche, Fahrgassen | ja | `#a4771e` |
| 2.2 | › Acker ohne Bewuchs (gepflügt, Saatbett) | Furchen, hell bzw. dunkel | ja | `#fdf8a5` |
| 2.3 | › Ackerbrache | unregelmäßiger Bewuchs auf Ackerschlag | eing. | `#f9f914` |
| 2.4 | › Dauerkultur (Abweichung A4) | regelmäßige Zeilen/Raster | ja | `#9b9b27` |
| 2.4.1 | › › Weingarten | Zeilentextur | ja | `#fbfb6f` |
| 2.4.2 | › › Obstanlage (intensiv, Reihen) | Bäume in dichtem Raster | ja | `#e19806` |
| 2.4.3 | › › Sonstige Dauerkultur (Beeren, Hopfen, Baumschule) | Reihen, gemischt | eing. | `#e2cd63` |
| 3 | **Dauergrünland (krautig, nicht Acker)** | gleichmäßige, feine Textur | ja | `#9dd161` |
| 3.1 | › Wiese / Weide (gemeinsam) | gleichmäßig, Mahdspuren bzw. Trittpfade | ja | `#3de723` |
| 3.1.1 | › › Wiese (Mahdspuren sichtbar) | Schwaden, Mähstreifen | eing. | `#80ef6f` |
| 3.1.2 | › › Weide (Trittpfade, Zäune, Tiere) | Pfade, Geilstellen | eing. | `#4d9d3a` |
| 3.2 | › Trocken-/Magerrasen | fleckig, helle Stellen, lückig | eing. | `#a1df19` |
| 3.3 | › Grünlandbrache / Ruderalflur | ungleichmäßig, hochwüchsig | eing. | `#a5d19f` |
| 3.4 | › Krautsaum linear (Feldrain, Wegrand, Böschung) | schmaler Streifen zwischen Nutzungen | ja | `#47b521` |
| 3.5 | › Verbuschende Fläche (Grünland mit Gehölzanflug) | Gras mit verstreuten Büschen | eing. | `#749146` |
| 3.6 | › Garten (Haus- und Hofgarten: Grünfläche, Beet) | kleinteiliges Grün und Beete am Haus oder Hof, von Gebäude, Zaun oder Hecke eingefasst | eing. | `#a6ffaf` |
| 4 | **Wald und Gehölze** (Abweichung A2) | grobe Kronentextur, dunkel | ja | `#1d7239` |
| 4.1 | › Wald (geschlossener Bestand) | durchgehendes Kronendach | ja | `#19e697` |
| 4.1.1 | › › Laubwald | runde Kronen | eing. | `#103714` |
| 4.1.2 | › › Nadelwald | spitze Kronen, dunkler | eing. | `#1e675b` |
| 4.1.3 | › › Mischwald | beides | eing. | `#22af6f` |
| 4.1.4 | › › Kahlschlag / Jungwuchs / Schlagflur | Lichtung im Wald, Stümpfe | eing. | `#19e6c4` |
| 4.2 | › Gehölz außerhalb Wald | Krone(n) einzeln oder linear | ja | `#13ae95` |
| 4.2.1 | › › Einzelbaum | eine Krone mit Schatten | ja | `#15bc58` |
| 4.2.2 | › › Baumgruppe / Feldgehölz | wenige Kronen, flächig | ja | `#4f926e` |
| 4.2.3 | › › Hecke / Baumreihe / Ufergehölz (linear) | Kronenband | ja | `#19e65c` |
| 4.2.4 | › › Gebüsch / Strauchfläche | niedrig, kleinkronig | eing. | `#0c3c34` |
| 5 | **Gewässer / Feuchtgebiet** | sehr dunkel bzw. glatt | ja | `#1d64c9` |
| 5.1 | › Fließgewässer | lang, gewunden | ja | `#0c0ced` |
| 5.1.1 | › › Fluss / Bach | natürlich gewunden | ja | `#1b5b89` |
| 5.1.2 | › › Graben / Kanal | gerade | eing. | `#80eef8` |
| 5.2 | › Stillgewässer (See, Teich, Weiher) | glatt, Ufer | ja | `#0cb5ed` |
| 5.3 | › Feuchtgebiet / Röhricht / Ufervegetation | dunkel, strukturiert, am Wasser | eing. | `#6558f6` |
| 6 | **Offener Boden / Fels** | sehr hell | ja | `#d8b897` |
| 6.1 | › Offene Sand-, Löss-, Lehmstelle (Abbruch, Hohlweg, Grube) | sehr hell, klein, Kante | eing. | `#763c23` |
| 6.2 | › Abbau, Halde, Deponie | großflächig, Terrassen | ja | `#db7a57` |
| 6.3 | › Fels / Geröll | hell, grob strukturiert | ja | `#97784f` |
| 6.4 | › Kies-/Sandbank (Gewässerufer, unbewachsen) | hell, am Wasser | ja | `#e0b16c` |
| 6.5 | › Schnee / Eis / Gletscher | weiß, glatt | eing. (Verwechslung mit Überstrahlung) | `#6b5747` |
| 6.6 | › Weg, unbefestigt (Feld-, Wald-, Schotterweg) | Fahrspuren, Mittelstreifen | eing. | `#a0522d` |

### Garten

Gärten spielen in der Landschaft eine nennenswerte Rolle und tragen deshalb eine eigene Unterklasse
im Dauergrünland: **3.6 Garten**. Grobe Klasse bleibt „3 Dauergrünland“.

- **Dazu gehört:** jede krautige Grünfläche und jedes Beet in einem Haus- oder Hofgarten, auch
  Vorgarten, Obstgarten und Gemüsegarten am Haus. Ein gepflegter Rasen ist kein Kennzeichen: Auch
  verwilderte, gemähte oder brachliegende Gartenfläche ist Garten. Erkennbar ist ein Garten vor
  allem an der Lage: am Wohnhaus oder Hof, oft von Zaun, Hecke oder Gebäuden eingefasst.
- **Nicht dazu gehört:** Gartenbaum, Strauch und Hecke im Garten bleiben Gehölz (4.2.1 bis 4.2.4),
  weil man von oben die Krone sieht (G2); ein Gartenhaus ist Nebengebäude (1.1.2), ein befestigter Gartenweg
  oder eine Terrasse Weg bzw. Platz (1.2.2, 1.2.4), ein Gartenteich Stillgewässer (5.2), ein Pool
  Schwimmbecken (1.3.3). Rasen in Parks, auf Friedhöfen und Sportanlagen ist kein Garten, sondern
  Wiese/Weide (3.1); eine Obstanlage in Reihen ist Dauerkultur (2.4.2); Wiese oder Acker am
  Ortsrand, die nicht zu einem Haus oder Hof gehört, bleibt Wiese/Weide bzw. Acker.
- **Im Zweifel:** Lässt sich nicht sicher sagen, ob eine Grünfläche am Haus zum Garten gehört,
  gilt die Elternklasse „3 Dauergrünland“ (U1); die Lage ist Nutzung und allein kein Grund für
  `sicher: nein` (U5).

Eine eigene grobe Klasse „Siedlungsgrün“ gibt es nicht. Unbefestigte Wege stehen unter Offener
Boden (6.6).

## Grundsätze G1 bis G5

Sie sagen, was ein Segment überhaupt beschreibt. Wortlaut und Herkunft stehen auch in
`kategorien.json` unter `rules`.

- **G1 Bedeckung vor Nutzung:** Das Segment-Label beschreibt, was in der Draufsicht zu sehen ist (CLC+, FLAIR, LUCAS LC, EAGLE LCC). Nutzung, die das Bild nicht zeigt (Wiese vs. Weide, Kulturart, Brache-Status, Widmung), kommt in eine getrennte Attributschicht aus Fremddaten (INVEKOS, DKM) — EAGLE LUA, LUCAS LU, LISA LN (B6, B7, B11). Siedlungsgrün ist keine eigene grobe Klasse: Haus- und Hofgärten (jede krautige Grünfläche und jedes Beet darin, gepflegt oder nicht, auch Vor-, Obst- und Gemüsegarten) tragen die Unterklasse Garten (3.6) im Dauergrünland; Gartenbaum, Strauch und Hecke bleiben Gehölz (4.2, G2); Rasen in Park, Friedhof und Sportanlage bleibt Wiese/Weide (3.1). Ob ein Segment im Siedlungsgebiet liegt, trägt es als Merkmal `im_siedlung: ja|nein`; für Auswertungen nach Bericht 48 gilt die Regel im nächsten Abschnitt.
- **G2 Sichtbare oberste Schicht:** Baumkrone über Straße ist Baum; Verdecktes wird nicht geraten (wie Draufsicht-Schemata CLC+, FLAIR; vermutet für FLAIR, nicht in deren Regeln nachgelesen).
- **G3 Keine harte Mindestfläche beim Segmentieren:** Keine harte Mindestfläche beim Segmentieren (CLC+: „no MMU“); untere Grenze ist die Erkennbarkeit, Richtwert 3 Bildpunkte Breite (0,6 m bei 0,2 m; 1,5–3 m bei historischen 0,5–1 m) — Vorschlag, vermutet. Die Mindestgrößen aus Bericht 48 (100–400 m², Linien ≥ 2 m) und DKM (200 m²) sind Auswertungsebenen, die aus den feinen Segmenten aggregiert werden (deckt F1 „empfohlen“).
  Berichtigung: DKM-Mindestflächen nach § 4 BANU-V (Gegenprüfung B10, wuensche/2026-11-17-landseg-methode/gegenpruefung/e02.md:23): Gebäude ab 20 m², streifenförmige Elemente ab 4 m Breite (befestigte Verkehrswege und fließende Gewässer auch darunter), Wald ab 10 m Breite und 1 000 m², Alpen/Fels/Geröll/vegetationsarme Flächen/Gletscher ab 2 000 m², übrige Nutzungen ab 200 m². „DKM 200 m²“ gilt nur für die übrigen Nutzungen.
- **G4 Texturflächen statt Einzelreihen:** Weingarten, Obstanlage, Acker mit Fahrspuren sind je eine Fläche (Zeilen nicht einzeln); Streuobst dagegen = Einzelbäume als eigene Segmente in Grünland, zusammengefasst über ein Verbund-Attribut „Streuobstbestand“ (Vorschlag).
- **G5 Jede Klasse ist ein gültiges Label:** Jede Klasse ist ein gültiges Label auf jeder Ebene (HILUCS-Prinzip „most appropriate and detailed level“, B13); das Trainingsziel kann so hierarchisch rechnen.

## Siedlungsgebiet und Bericht 48

Die grobe Klasse eines Segments (`grob`, Ebene 1) richtet sich nur nach der Bedeckung: Ein Garten
(3.6) ist „3 Dauergrünland“ wie jede Wiese. Verwechselt die Vorstufe Garten und Wiese, ist das
deshalb nur ein feiner Fehler.

Ob ein Segment im Siedlungsgebiet liegt, steht als eigenes Merkmal `im_siedlung: ja | nein` je
Segment in `segmente.json` (wie `sicher`), nicht als Klasse. Die Vorstufe setzt es aus der fertigen
Karte: Gebäude und befestigte Straßen, Wege und Hofflächen bilden die Siedlungszone, aufgeweitet um
einen Abstand in Metern; ein Segment aus Acker, Grünland oder Gehölz außerhalb Wald, das überwiegend
in dieser Zone liegt, bekommt `ja`, alle anderen `nein` (Einstellungen in `vorstufe.json`, Abschnitt
`siedlung`, am Test T0 noch nicht abgestimmt).

**Abbildung auf Bericht 48:** Bericht 48 führt Hausgärten „als Teil der Siedlung“. Für Auswertungen
nach Bericht 48 zählt deshalb ein Segment der Klassen 2, 3 und 4.2 (samt Unterklassen, also auch
Garten 3.6) mit `im_siedlung: ja` als „1 Versiegelt / bebaut“; alle anderen Segmente zählen nach
ihrer Ebene-1-Klasse, ein Garten ohne `im_siedlung: ja` also als „3 Dauergrünland“.
Die Klassenliste dazu steht in `kategorien.json` bei Regel G1 (Feld `bericht48`), die Funktion ist
`bericht48_klasse(klasse, im_siedlung)` in `landseg/kategorien.py`.

Wo das nicht ganz trägt: Parks und Friedhöfe ohne Gebäude oder befestigte Fläche in der Nähe zählen
nach dieser Regel als Grünland bzw. Gehölz, nicht als Siedlung; umgekehrt kann ein schmaler Acker-
oder Wiesenstreifen direkt an einer Straße oder einem Hof `ja` bekommen. Ob der Abstand passt, zeigt
erst der Test T0.

## Regeln für Unklares U1 bis U5

Sie sagen, was zu tun ist, wenn man nicht sicher ist. Jeder Bildpunkt bekommt trotzdem genau eine
Klasse.

- **U1 Feinste sichere Klasse, sonst Elternklasse:** Feinste sicher entscheidbare Klasse; im Zweifel die Elternklasse (Ebene 2, notfalls Ebene 1) — Elternklassen sind gültige Labels (G5). Jedes Segment trägt dazu `sicher: ja|nein`.
- **U2 Schatten ist keine Klasse:** Was im Schatten liegt, bekommt die Klasse der erkennbaren Fortsetzung (Straße läuft durch, Wiese setzt sich fort); geht das nicht, Elternklasse der Umgebung mit `sicher: nein`; Klasse 0.2 nur, wenn gar nichts erkennbar ist.
- **U3 Mischpixel an Kanten:** Grenze auf den Farb-/Helligkeitsumschlag (Stitcher-Einrasten, e05); ein Bildpunkt gehört der Klasse mit Mehrheit (CLC+: 50 %-Schwelle, B5).
  Anmerkung: CLC+ nutzt keine schlichte Mehrheit, sondern eine 50 %-Schwelle mit Entscheidungsbaum und relativer Mehrheit; als Vorbild taugt es nur sinngemäß (Gegenprüfung B5, wuensche/2026-11-17-landseg-methode/gegenpruefung/e02.md:13).
- **U4 Unter der Erkennbarkeitsgrenze:** Unter Erkennbarkeitsgrenze (G3): Das Objekt fällt der umgebenden Klasse zu, nicht Klasse 0.
- **U5 Nutzung ist kein Grund für Unsicherheit:** Ist nur die Nutzung unklar (Wiese oder Weide, Acker- oder Grünlandbrache), wird die Bedeckungsklasse der Ebene darüber genommen (3.1, 3.3) und die Nutzung bleibt Attribut `nutzung: unbekannt`, später aus INVEKOS/DKM füllbar.

## Abweichungen von Bericht 48

Die grobe Ebene folgt Bericht 48, an vier Stellen aber bewusst nicht. Die Entscheidungen F1 (so fein
segmentieren, wie im Bild erkennbar; Mindestgrößen nur bei der Auswertung), F2 (Kategorien allgemein
und gestuft, lückenlos) und F5 (Weingärten und Obstanlagen zu Acker) liegen ihnen zugrunde; die
Zuordnung unbefestigter Wege zur Verkehrsfläche aus F5 ist durch „Bedeckung statt Nutzung“ ersetzt.

- **A1** (Klassen 0, 0.1, 0.2; Entscheidung F2, F5): Klasse 0 „Nicht bestimmbar“ kommt hinzu, nur für Bildfehler, Scanrand, Wolke; Lückenlosigkeit verlangt ein Label auch dort. In Auswertungen nach Bericht 48 wird 0 ausgeblendet (no data wie CLC+ 255).
- **A2** (Klassen 4, 4.2; Entscheidung F1, F2): Ebene 1 „Wald“ wird „Wald und Gehölze“: Hecken, Einzelbäume, Feldgehölze brauchen bei Lückenlosigkeit einen Platz in Ebene 1; ihr Bedeckungsbild ist das des Waldes (Krone). Für Bericht-48-Auswertungen gilt Wald = 4.1, Gehölze außerhalb Wald = 4.2 getrennt.
- **A3** (Klasse 1.3.1; Entscheidung F5): Künstliche Schotterflächen (1.3.1) stehen unter „Versiegelt/bebaut“, obwohl nicht versiegelt (Nutzung Verkehr/Lager dominiert). Unbefestigte Wege stehen dagegen nach Bedeckung unter Offener Boden (6.6); das ersetzt für sie die Zuordnung „Verkehrsfläche“ aus F5.
- **A4** (Klassen 2.4, 2.4.1, 2.4.2, 2.4.3; Entscheidung F5): Dauerkulturen (Weingarten, Obstanlage) stehen unter „Acker“ als 2.4; Bericht 48 führt Weingarten nur in Ebene 2. Streuobst ist keine eigene Fläche, sondern Einzelbäume (4.2.1) in Grünland (3.1) mit Verbund-Attribut (G4). Entschieden: Weingärten und Obstanlagen zählen zu Acker (F5).

## Prüfen

```
python -I tools/pruefe_kategorien.py kategorien.json
```

Das Skript braucht nur Python selbst. Es zählt die Klassen je Ebene (7/26/44) und die Regeln (5 G,
5 U), prüft eindeutige Codes, vorhandene Elternklassen, Pflichtfelder, gültige und deutlich
verschiedene Farben und die Regel zu Bericht 48 (Feld `bericht48` bei G1: Klassen vorhanden, Ziel
auf Ebene 1) und meldet am Ende `ok`. Bei einem Fehler nennt es die Stelle und endet mit
Fehlercode 1.

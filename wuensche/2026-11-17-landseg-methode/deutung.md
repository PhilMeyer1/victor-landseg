# Deutung: landseg-methode (Recherche, Stufe M)

## Ausgangsfrage und Vermutung

Frage (Nutzer): Wie kann man die Landschaftsbilder mit Claude Code vollständig und lückenlos, so fein
wie möglich in Segmente mit Kategorien zerlegen? Die Grundlage ist das Bild im Repo, der Lauf ist als
Test gedacht, und die Methode soll ganzheitlich vorgeschlagen werden.
Vermutung: Die Vorgehensweise der Stitcher-Session (Insekten) lässt sich etwa so auf Landschaftsbilder
übertragen, wie sie ist.

## Gelesene Quellen

- `C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-methode.md` (Wunsch, Fragen F1–F7, Befund, Abdeckung, Kandidaten)
- `C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-methode/bericht.md` (1–2.5, 3–6)
- `C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-methode/plan.md` (Kopf)
- `C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-methode/einheiten/e05.md` (Werkzeuge W1–W10, Kostenrechnung, Empfehlung Z. 153)
- `C:/Users/Phil/Developement/Victor/wuensche/entscheidungen.md` (nur Push-Regel, nicht einschlägig)
- Profil `C:/Users/Phil/Developement/Victor/.claude/repos/unterlagen.md` (Kopf: nur Dokumente, keine Prüfungen)

## Kette

Es gibt keine Herkunft und keine Vergleichsmessung; das ist die erste Ermittlung zum Thema.

## Trägt die Vermutung?

Nur teilweise. Übertragbar sind der Ablauf (Urteil mit Mängelbild, Bestätigung durch den Nutzer,
direkte Maske per Python mit Kante im engen Band, Zusammentragen, Prüfseite, Korrekturrunden) sowie
die Regeln „nicht raten" und „geschätzte Kanten melden" (`bericht.md` 2.2, e05 B6/B9, bestätigt).
Umgekehrt liegt der Hebel bei der Einheit und beim Abgabeformat. Im Stitcher wurden 19 von 333
Segmenten (5,7 %) einzeln bearbeitet, und am Ende waren 14,6 % der Bildpunkte belegt. Die Zählprobe
prüfte dort nur das Belegte (e05 B3–B5). Lückenlos wird das Ergebnis also durch die Datenform
(Label-Karte, 0 verboten) und durch Teilkacheln als Einheit, nicht durch mehr Agents je Objekt. Auch
kein Modell schafft es allein: SAM 2.1 „segment everything" erreicht 91–98 % (e03 B8).

## Abwägung je Kandidat (gegen die Frage)

- K1 trägt: Die Kategorien sind Teil der Frage, und der Aufwand ist klein. Die Liste hängt an F2/F5
  und wird für K2 gebraucht, deshalb wird sie im nächsten Schritt mitgenommen.
- K2 trägt: Er ist die Voraussetzung jedes Tests und macht die Lückenlosigkeit prüfbar. Die
  Empfehlung von e05 (Z. 153) lautet „W1–W8 + W10 vor dem Test", W9 (Export) braucht der Test nicht.
- K3 trägt: Das ist der eigentliche Wunsch des Nutzers („soll erst mal ein Test werden"). Er setzt
  aber K2 voraus und ist deshalb nicht der nächste Schritt.
- K4 trägt teilweise: Er dient der Robustheit, zeigt aber ein anderes Gebiet und kommt nach K3.
- K5 trägt teilweise: Er ist für die Lückenlosigkeit nicht nötig und steht im Spannungsfeld zur
  Unabhängigkeit von Zusatzdaten (F6).
- K6 und K8 tragen teilweise: Sie liefern Mehrjahrgang erst nach dem Test. Bei K6 ist das Gebiet nur
  nach Augenschein bestimmt, K8 kostet Geld.
- K7 trägt teilweise: Er ist das Endziel, aber erst ab einigen hundert Teilkacheln sinnvoll.

## Nächster Schritt

K2 als Folge-Wunsch, zugeschnitten auf T0 (W1–W8, W10, `kategorien.json` aus K1; W9 später). Er
braucht vorher die Entscheidung F4 (Ort, im Profil unterlagen gibt es keine Prüfungen). Abgenommen
wird an einer T0-Teilkachel: Die Vorstufe läuft, `pruefen` meldet H × W ohne 0, und die Zahl der
Segmente je Teilkachel ist gemessen.

## Beleg des Gegenarguments

- Die Dichte je Agent ist ungeprüft. Im Stitcher war es ein Segment je Urteils-Agent (4–8 min), in
  T0 wären es 40–60 Segmente je 500er-Teilkachel (vermutet). Das ist laut `bericht.md` 3.6 das
  „größte Risiko".
- Die Vorstufe erreicht 43–60 % mIoU (SegEarth-OV3 auf OpenEarthMap, LoveDA, Potsdam, Vaihingen) und
  ist schwach bei dünnen Linien und Kleinobjekten (`bericht.md` 2.1, e03 L6/B3). Genau das ist die
  geforderte Feinheit.
- Es gab keinen Probelauf (Eingriff keiner), und die Aufwandszahlen sind reine Schätzung (3.5).

Der Schritt gilt trotzdem: Die Größe der Teilkacheln ist ein Parameter von W1 (250 px als
Gegenmittel, 3.6), und die Abnahme misst die Dichte, bevor K3 Läufe kostet.

# Deutung landseg-effiz (Untersuchung, Stufe S)

## Ausgangsfrage und Vermutung

Frage: Wie hat die Stitcher-Session Tokens, Effizienz und Dauer verbessert, lässt sich das bei uns
anwenden, und machen unsere Agents noch unnötige Schritte oder sind sie maximal fokussiert?
Vermutung: Die Stitcher-Ansätze lassen sich übertragen, und unsere Agents machen noch unnötige Schritte.
Ergebnis: Die Vermutung trägt, in beiden Teilen.

## Gelesene Quellen

- `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-effiz.md` (Wunsch, Fragen, Entscheidungen, Befund, Abdeckung, Kandidaten)
- `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-effiz/bericht.md` (S1–S6, Tabelle H0, B1–B8, Übertragbarkeit)
- `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-effiz/bericht-landseg.md`
- `C:/Users/Phil/Developement/Victor/wuensche/entscheidungen.md` (Zeilen alle und landseg, 10–19)
- Kopf von `C:/Users/Phil/Developement/Victor/.claude/repos/landseg.md`
- Gezielter grep: `segmente !== ` in den Workflows unter `wuensche/` (Treffer: historisch-3 `workflow.js:404`
  und `workflow-fein.js:340` mit derselben Prüfung; test-t0-2 `workflow.js:245` mit einer ähnlichen Prüfung)
- Kein `auswertung.md` und kein `plan.md` (Stufe S); `roh/` nicht geöffnet

## Kette

Keine Herkunft und kein Vergleich in der Kopfzeile. Die Kette besteht hier aus dem Stitcher-Vorbild
(runden-straffen: Runde 10,43 auf 3,20 USD, 20,8 auf 12,4 min, IoU 0,994–1,000 außer Borste) und dem
gleichen Muster in H0: eigene Skripte und Wiederlesen als Kostentreiber. Kein Widerspruch zwischen
den Gliedern. Es gibt keine Kette ab drei Gliedern an derselben Stelle, also keinen Anlass für einen Neubau.

## Abwägung je Kandidat (gegen die Ausgangsfrage)

- K1 trägt: Das ist der sicherste unnötige Schritt, im Code belegt, mit 8 Agents, 20,4 USD und 9,8 min (rund 9 % von H0).
  Die Prüfung steht auch in `workflow-fein.js:340`. Schwäche: Ob alle 8 unnötig waren, ist nur
  „wahrscheinlich“, weil `kontrolle_ok` nicht je Viertel geprüft wurde.
- K2 trägt: Er ist der Hauptansatz des Stitchers und trifft den größten Fokusverlust bei uns (180 .py, 679 Läufe
  und 433 Inline-Aufrufe gegen 189 Aufrufe von `-m landseg`). Gewinn geschätzt 35–60 USD.
- K3 trägt teilweise: Er ist Voraussetzung, um Gewinne zu belegen, beantwortet die Frage aber nicht selbst. Die Auswertung
  gibt es schon als einmaliges Skript (roh/).
- K4 trägt teilweise: 66 doppelte von 1.635 Bildlesungen sind rund 4 %. Die Schätzung von 10–20 % stützt sich auf
  die nicht gemessene Zusammenlegung der Nahbilder. Bei a:r1c0 gab es nur eine Doppelung.
- K5 trägt teilweise: Er entspricht S2, spart aber nur 5,9 USD (2,6 %); der Gewinn liegt in Wandzeit und Fehlerrisiko.
- K6 trägt teilweise: Er entspricht S1(3), spart rund 5 von 70,7 USD; die Paarzahl je Bündel ist nicht geprüft.
- K7 trägt nicht: Er ist kein Stitcher-Ansatz, der Gewinn ist nur vermutet, und er steht gegen `entscheidungen.md:17`.

## Nächster Schritt

K2 als Folge-Wunsch. Er bringt den größten Gewinn, ist genau der Hebel, der im Stitcher gewirkt hat,
und skaliert mit den künftigen Läufen auf dem ganzen Orthofoto (`entscheidungen.md:18`). K1 ist kleiner
und sicherer, spart aber weniger als die Hälfte.

## Beleg des Gegenarguments

- bericht.md S1 (Zeilen 44–51): Das Zeitziel von 5–7 min wurde verfehlt, weil ein Agent „weiter eigene
  Skripte für Ansichtsbilder schreibt“. Gewinn und Ursachen lassen sich nicht einzeln trennen.
- bericht.md B2 (Gegenprobe): `wscheide.py` ist echte Fachhilfe beim Nachsegmentieren.
- bericht.md „Nicht geprüft“: Die Qualität bei weniger Runden ist ungemessen (Eingriff keiner).
- Warum der Schritt trotzdem gilt: Wiederkehrend und mechanisch sind urteil.json und Abgabe bauen sowie
  Ausschnitt- und Zoombilder, und jede gesparte Runde spart das Wiederlesen (B3). Der Gewinn lässt
  sich nach dem nächsten Lauf mit derselben Transkript-Auswertung gegen H0 messen.

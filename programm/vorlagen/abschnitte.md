# Abschnitte der Urteils-Aufträge

Bausteine, die `landseg vorbereiten` je nach Fassung in `urteil-viertel.md` und `frei.md` einsetzt (Platzhalter
`{{KATEGORIEN}}`, `{{FASSUNG_ABSCHNITT}}`, `{{GEGENPROBE}}`). Ein Abschnitt reicht bis zum nächsten Kopf
`<!-- abschnitt: … -->`. `feinheit-<bildart>` setzt `{{FEINHEIT}}` je Bildart (`einstellungen/bildarten.json`; Farbe:
leer, der Auftrag bleibt wie bisher), mit `{{RICHTWERT}}`, `{{MINDESTFLAECHE_QM}}`, `{{MINDESTFLAECHE_PX}}`.

<!-- abschnitt: feinheit-farbe -->
<!-- abschnitt: feinheit-sw -->
**Feinheit auf diesem Schwarz-Weiß-Scan (Regel L15):** Das Bild ist alt und niedrig aufgelöst; Korn und Rauschen
sind keine Flächen. Richtwert für die Teilkachel: höchstens rund {{RICHTWERT}} Segmente im Kern. Kleiner als
{{MINDESTFLAECHE_QM}} m² ({{MINDESTFLAECHE_PX}} Bildpunkte) bleibt eine Fläche nur, wenn sie ein klar erkennbares
Objekt ist (Haus, Einzelbaum, schmaler Weg, Garten am Haus) und du sie mit `sicher: ja` urteilst; ein klar
erkennbarer Garten am Haus bleibt eigene Fläche „Garten“ (L14), ein unklarer geht in die Nachbarfläche. Jede
andere kleinere Fläche legst du mit dem passenden Nachbarn zusammen (`eingriff verschmelzen`, Klasse der größeren
Fläche). Nachsegmentieren nur für klar erkennbare Objekte, nie für Helligkeitsflecken. `pruefen --manifest …
--teilkachel …` meldet ein Überschreiten des Richtwerts als Hinweis.

<!-- abschnitt: kategorien-fest -->
`{{REPO}}/kategorien.json` und `{{REPO}}/KATEGORIEN.md`: die gültigen Klassen und Regeln. Gärten nach Regel L14 des Skills: krautige Grünfläche und Beet im Haus- oder Hofgarten = 3.6 Garten;
  Wiese/Weide oder Acker mit `im_siedlung: ja` ist nur ein Kandidat, entschieden wird am Bild.
<!-- abschnitt: kategorien-frei -->
`{{REPO}}/kategorien.json` und `{{REPO}}/KATEGORIEN.md`: nur Anregung; in dieser Fassung benennst du die Klassen
  selbst (Abschnitt „Klassen frei“).
<!-- abschnitt: fassung-fest -->

<!-- abschnitt: fassung-frei -->

## Klassen frei

Diese Fassung ist ein Vergleichsmuster ohne feste Kategorienliste. Abweichend von Regel L3 des Skills wählst du
die Klassen nicht aus `kategorien.json`, sondern benennst jede Fläche selbst, gestuft in drei Ebenen unter
`klasse_frei`: `grob` (wenige Oberklassen für die ganze Landschaft), `mittel` und `fein` (so fein, wie im Bild
sicher erkennbar; sonst wiederholt `fein` die mittlere Ebene). Kurze deutsche Namen, gleiche Dinge gleich benannt.
`klasse_heute` ist der Code der Vorstufe und nur ein Hinweis; `klasse_vorschlag` bleibt `null`; braucht ein
Eingriff eine Klasse, nimm den Code des geteilten Segments. Unter `klassen_frei` stehen alle Namen, die du benutzt
hast, je mit `name`, `ebene` (grob, mittel, fein), `eltern` und `merkmal` (woran im Bild erkennbar). Gärten
(Regel L14 des Skills: krautige Grünfläche und Beet im Haus- oder Hofgarten) benennst du immer gleich: `grob`
„Dauergrünland“, `mittel` und `fein` „Garten“; Wiese oder Acker mit `im_siedlung: ja` ist nur ein Kandidat. Nach allen
Vierteln gleicht ein eigener Agent die Namen zu einer Liste an. Alle übrigen Regeln gelten wie in der festen Liste.
<!-- abschnitt: gegenprobe -->

## Unabhängig urteilen

Du bist die Gegenprobe: Ein anderer Agent bearbeitet dieselbe Stelle auf einer eigenen Karte. Sein Ergebnis siehst
du nicht an, auch nicht, wenn es schon da ist. Deine Abgabe geht in keine Karte ein; aus beiden wird die
Übereinstimmung gemessen.
<!-- abschnitt: keine-gegenprobe -->

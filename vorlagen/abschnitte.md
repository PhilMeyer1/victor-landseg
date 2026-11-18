# Abschnitte der Urteils-Aufträge

Bausteine, die `landseg vorbereiten` je nach Fassung in `urteil-viertel.md` und `frei.md` einsetzt (Platzhalter
`{{KATEGORIEN}}`, `{{FASSUNG_ABSCHNITT}}`, `{{GEGENPROBE}}`). Ein Abschnitt reicht bis zum nächsten Kopf
`<!-- abschnitt: … -->`.

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

# Teil 1 von landseg-garten: Kategorienliste, Prüfskript und Bericht-48-Abbildung

Kurzname: landseg-garten-1 | Datum: 2026-11-18 | Größe: mittel | Bereich: victor | Repos: landseg | Status: eingereiht | Mutterwunsch: landseg-garten

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

Teil 1 des Mutterwunschs `landseg-garten` (`wuensche/2026-11-18-landseg-garten.md`), Zeile aus dessen Teile-Liste:

1. Kategorienliste, Prüfskript und Bericht-48-Abbildung — Umsetzer — Repo: landseg — Vorbedingungen: keine — nach: – — AK 1, 2, 3 — Garten steht als Klasse 3.6 in `kategorien.json` und `KATEGORIEN.md`, Prüfskript und Zähltests grün

## Fragen

keine (siehe Mutterwunsch)

## Entscheidungen

siehe Mutterwunsch

## Arbeitsauftrag

### Abnahmekriterien

AK1: In der Kategorienliste steht unter „3 Dauergrünland“ eine neue Unterklasse „Garten“ (Code 3.6, eigene, von allen anderen deutlich verschiedene Farbe, SW-Spalte, Bildmerkmal, Zuordnung zu Bericht 48), und das Prüfskript meldet die neuen Zahlen mit „ok“ — prüfbar: `"$PY" -I tools/pruefe_kategorien.py kategorien.json` (nach F1, F2, F4)
AK2: `KATEGORIEN.md` nennt Garten als Klasse und sagt, was dazugehört und was nicht; der Absatz „keine Klasse Siedlungsgrün“ und Grundsatz G1 sind angepasst, Gesamtzahl und Zählung stimmen in `KATEGORIEN.md`, `README.md`, `gesamt/ANLEITUNG.md`, `gesamt/CLAUDE.md` und im Test `tests/test_kategorien.py` — prüfbar: Lesen `KATEGORIEN.md`; `"$PY" -B -m unittest tests.test_kategorien`
AK3: Die Bericht-48-Abbildung zählt „Garten“ im Siedlungsgebiet weiter als „1 Versiegelt / bebaut“, außerhalb als Dauergrünland — prüfbar: `"$PY" -B -m unittest tests.test_kategorien` (neuer Fall)

Einstieg, Bausteine, Entscheidungen: siehe Mutterwunsch

Vorbedingungen: keine

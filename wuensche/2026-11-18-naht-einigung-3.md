# Teil 3 von naht-einigung: Ergebnis-Ansicht: neue Zahl und gemeinsamer Bildleser

Kurzname: naht-einigung-3 | Datum: 2026-11-18 | Größe: mittel | Bereich: victor | Repos: landseg | Status: bereit | Mutterwunsch: naht-einigung

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

Teil 3 des Mutterwunschs `naht-einigung` (`wuensche/2026-11-18-naht-einigung.md`), Zeile aus dessen Teile-Liste:

3. Ergebnis-Ansicht: neue Zahl und gemeinsamer Bildleser — Umsetzer — Repo: landseg — Vorbedingungen: keine — nach: 1 — AK 5 — Seite zeigt die Zahl „gleiche Fläche, verschiedene Klasse“ (davon unsicher) neben der Zahl der Schnittlinien, Nähte-Schalter nutzt `naht.lese_bild`; Wortlaut und Zahl in der bestehenden Ansicht; kein Entwurf. Erst nach dem Einreihen von seite-kachelwahl.

## Fragen

keine (siehe Mutterwunsch)

## Entscheidungen

siehe Mutterwunsch

## Arbeitsauftrag

### Abnahmekriterien

AK5: Die Ergebnis-Ansicht zeigt je Fassung und im Schalter „Nähte“ die neue Zahl „Stellen, an denen gleiche Flächen verschiedene Klassen haben“ (davon unsicher belegt), getrennt von der bisherigen Zahl der Schnittlinien ohne Bildkante; beide Zahlen stimmen mit `einigung messen` bzw. `naht` überein (der Nähte-Schalter benutzt den gemeinsamen Bildleser, Altlast A2 erledigt) (nach F1) — prüfbar: Ansicht Ganzer Ausschnitt, Fassung C, Schalter Nähte an, Desktop; `PY -B -m unittest tests.test_seite`

Einstieg, Bausteine, Entscheidungen: siehe Mutterwunsch

Vorbedingungen: keine

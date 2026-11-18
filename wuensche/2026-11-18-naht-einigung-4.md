# Teil 4 von naht-einigung: Seiten neu erzeugen und ANLEITUNG

Kurzname: naht-einigung-4 | Datum: 2026-11-18 | Größe: mittel | Bereich: victor | Repos: landseg | Status: bereit | Mutterwunsch: naht-einigung

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

Teil 4 des Mutterwunschs `naht-einigung` (`wuensche/2026-11-18-naht-einigung.md`), Zeile aus dessen Teile-Liste:

4. Seiten neu erzeugen und ANLEITUNG — Umsetzer — Repo: landseg — Vorbedingungen: keine — nach: 2, 3 — AK 7, 8 — Ergebnis-Seiten für T0 mit dem einigten Stand neu erzeugt (Prüfseiten in `daten/landseg`, `T0.html` für das Gesamtprojekt), `gesamt/ANLEITUNG.md` und `gesamt/README.md` um den Schritt ergänzt; Bau und Upload des Gesamtprojekts bleibt bei der Hauptsession. Erst nach dem Einreihen von seite-kachelwahl.

## Fragen

keine (siehe Mutterwunsch)

## Entscheidungen

siehe Mutterwunsch

## Arbeitsauftrag

### Abnahmekriterien

AK7: Der Weg des Nutzers: Die neu erzeugte Seite `T0.html` öffnet, jede Fassung A/B/C zeigt den einigten Stand und die neue Zahl, ein Klick auf ein Segment an einer Naht zeigt Klasse und (falls unsicher) den Grund der Einigung — prüfbar: Ansicht `T0.html` (neu erzeugt), Fassung A, Teilkachel r0c1, Nähte an, Desktop
AK8: `gesamt/ANLEITUNG.md` (und, wo es den Aufbau nennt, `gesamt/README.md`) beschreibt den Einigungsschritt: warum, wie die Agents zugeschnitten sind, wie die Zahl gezählt wird, vorher/nachher je Fassung, Kosten; „Bekannte Schwächen“ und „Zahlen“ sind nachgezogen; `gesamt_projekt.py pruefen` bleibt `ok` — prüfbar: Lesen `gesamt/ANLEITUNG.md`; `PY -B tools/gesamt_projekt.py pruefen --basis <BASIS> --ziel <Test-Ziel>` (wie in den Tests des Repos)

Einstieg, Bausteine, Entscheidungen: siehe Mutterwunsch

Vorbedingungen: keine

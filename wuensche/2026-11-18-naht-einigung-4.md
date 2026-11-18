# Teil 4 von naht-einigung: Seiten neu erzeugen und ANLEITUNG

Kurzname: naht-einigung-4 | Datum: 2026-11-18 | Größe: mittel | Bereich: victor | Repos: landseg | Status: eingereiht | Mutterwunsch: naht-einigung

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

- Beleg-Freigabe (Nutzer 2026-11-18): ohne Beleg des Prüfers für AK7 einreihen; der Beleg ist von der Hauptsession über die Browser-Erweiterung nachgeholt (Eintrag „Beleg AK7 nachgeholt“).
- 2026-11-18 Beleg AK7 nachgeholt (Hauptsession, Browser-Erweiterung, Seite `wuensche/2026-11-18-naht-einigung-4/T0.html` über 127.0.0.1): Seite öffnet ohne Konsolenfehler; Fassung A, Teilkachel r0c1, Nähte an: Kopfzeile „143 Schnittlinien an Nähten ohne Bildkante · 5 Stellen, an denen gleiche Flächen verschiedene Klassen haben (davon unsicher …)“; Klick auf Segment 200100 an der Naht zeigt „6 Gehölz · unsicher“ und je Paar die Einigung mit Grund (echte Grenze mit r0c0:100049, unklar mit r0c0:100067). Fassung B zeigt auf r0c1 1 Stelle, C 2 Stellen; Umschalten ohne Fehler.
- 2026-11-18 (Hauptsession): Teil 2 ist gefahren; die geeinigten Daten liegen in der Übergabe-Grundlage `daten/landseg/uebergabe/landseg-t0/T0/` (Commit 3988411, lokal, nicht gepusht), Endstand `wuensche/2026-11-18-naht-einigung-2/messen-nachher.txt` (offen A/B/C 0, unsicher 9/6/9), Bericht daneben. Die Ergebnis-Seite `T0/T0.html` der Grundlage wird aus diesem Stand neu erzeugt; die ANLEITUNG nennt die Zahlen und Kosten aus dem Bericht. Die alten Arbeitsdaten unter `daten/landseg/T0/` (alte Benennung) bekommen die Einigung nicht.
- Neubau abgelehnt: README.md#Inhalt, 2026-11-18 (Nutzer auf die Frage des Beobachters B-584eb3: „Weiter anbauen“; die Lücke im Bauwerkzeug wird in diesem Teil nachgezogen).
- 2026-11-18 (Hauptsession, Befund beim Nachziehen von seite-kachelwahl): `gesamt_projekt.py bauen` übernimmt neue Ergebnisse aus der Übergabe-Grundlage (`daten/landseg/uebergabe/landseg-t0/T0/`) nicht; `pruefen` vergleicht mit deren HEAD. Die Hauptsession hat T0.html deshalb von Hand in der Grundlage committet (mit `core.autocrlf=false`, sonst weichen die Prüfsummen ab) und ins Gesamtprojekt kopiert. Dieser Teil soll das im Werkzeug lösen: `bauen` zieht `ergebnisse/` aus dem HEAD der Grundlage nach (Byte für Byte), statt dass jemand von Hand kopiert.
siehe Mutterwunsch

## Arbeitsauftrag

### Abnahmekriterien

AK7: Der Weg des Nutzers: Die neu erzeugte Seite `T0.html` öffnet, jede Fassung A/B/C zeigt den einigten Stand und die neue Zahl, ein Klick auf ein Segment an einer Naht zeigt Klasse und (falls unsicher) den Grund der Einigung — prüfbar: Ansicht `T0.html` (neu erzeugt), Fassung A, Teilkachel r0c1, Nähte an, Desktop
AK8: `gesamt/ANLEITUNG.md` (und, wo es den Aufbau nennt, `gesamt/README.md`) beschreibt den Einigungsschritt: warum, wie die Agents zugeschnitten sind, wie die Zahl gezählt wird, vorher/nachher je Fassung, Kosten; „Bekannte Schwächen“ und „Zahlen“ sind nachgezogen; `gesamt_projekt.py pruefen` bleibt `ok` — prüfbar: Lesen `gesamt/ANLEITUNG.md`; `PY -B tools/gesamt_projekt.py pruefen --basis <BASIS> --ziel <Test-Ziel>` (wie in den Tests des Repos)

Einstieg, Bausteine, Entscheidungen: siehe Mutterwunsch

Vorbedingungen: keine

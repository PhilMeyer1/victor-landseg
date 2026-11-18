# Teil 1 von landseg-historisch: Seite mit Bildwahl und Graustufen-Eingang

Kurzname: landseg-historisch-1 | Datum: 2026-11-18 | Größe: mittel | Bereich: victor | Repos: landseg | Status: eingereiht | Mutterwunsch: landseg-historisch

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

Teil 1 des Mutterwunschs `landseg-historisch` (`wuensche/2026-11-18-landseg-historisch.md`), Zeile aus dessen Teile-Liste:

1. Seite mit Bildwahl und Graustufen-Eingang — Umsetzer — Repo: landseg — Vorbedingungen: keine — nach: – — AK 1 — Die Seite trägt mehrere Bilder in einer Datei mit Bildwahl (Schrittleiste, Nähte-Zahlen, Einigungsgrund je Bild), kommt ohne Weltdatei aus, T0 unverändert; Graustufenbilder lesen Kacheln, Ansicht und Seite; Tests dazu; Einstellungen und README.

## Fragen

keine (siehe Mutterwunsch)

## Entscheidungen

siehe Mutterwunsch

## Arbeitsauftrag

### Abnahmekriterien

AK1: Die Prüfseite zeigt neben Fassung und Teilkachel auch das Bild (Orthofoto T0 / historischer Ausschnitt H0) zur Wahl; die Wahl wechselt Bild, Teilkachel-Schrittleiste, Nähte-Zahlen, Einigungsgrund beim Klick und Kategorienliste ohne Neuladen, T0 verhält sich wie vorher, ein Bild ohne Georeferenz oder ohne Daten bricht die Seite nicht ab — prüfbar: `PY -B -m unittest discover -s tests -t .` (neue Tests für mehrere Bilder in einer Seite, ohne Weltdatei, T0 unverändert) und Ansicht Prüfseite mit T0 und H0, Desktop

Einstieg, Bausteine, Entscheidungen: siehe Mutterwunsch

Vorbedingungen: keine

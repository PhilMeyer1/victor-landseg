# Teil 3 von landseg-garten: Umstellen der Ergebnisse T0 und H0 in allen drei Fassungen (ohne Commit)

Kurzname: landseg-garten-3 | Datum: 2026-11-18 | Größe: mittel | Bereich: victor | Repos: landseg | Status: eingereiht (ohne Commit) | Mutterwunsch: landseg-garten | Ergebnis: ohne Commit

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

Teil 3 des Mutterwunschs `landseg-garten` (`wuensche/2026-11-18-landseg-garten.md`), Zeile aus dessen Teile-Liste:

3. Umstellen der Ergebnisse T0 und H0 in allen drei Fassungen (ohne Commit) — Workflow — Repo: landseg — Vorbedingungen: keine — Aufruf-Budget: 120 — nach: 1, 2 — AK 6 — je Viertel und Fassung ein Agent bestätigt die Garten-Kandidaten, Karten geprüft, Zahl je Fassung im Bericht

## Fragen

keine (siehe Mutterwunsch)

## Entscheidungen

siehe Mutterwunsch

## Arbeitsauftrag

### Abnahmekriterien

AK6: In den Ergebnissen T0 und H0 aller drei Fassungen tragen die als Garten bestätigten Segmente die Klasse „Garten“; `pruefen` meldet für jede der sechs Karten keinen Fehler, die Zahl der Garten-Segmente je Fassung steht im Bericht — prüfbar: `pruefen` je Fassung für T0 und H0 (Datenlauf unter `BASIS/daten/landseg/`, ohne Commit)

Einstieg, Bausteine, Entscheidungen: siehe Mutterwunsch

Vorbedingungen: keine

Aufruf-Budget: 120

## Nachweis

- 2026-11-18: Workflow wf_230c0b9f-a95 (29 Agents, 2,39 Mio. Tokens, 22 min): H0 vergröbert A 1833→566, B 728→468, C 470→297 (pruefen ok, Einigung offen 0); 495 Garten-Kandidaten in 26 Einheiten am Bild geprüft (ja 339, nein 72, unklar 84); eingetragen T0 A 101, B 115, C 118, H0 A 1, B 3, C 0 Garten-Segmente; pruefen 24× ok (AK6); Tabelle ergebnis.md, Sicherungen sicherung-vor-vergroebern und sicherung-vor-garten. Offen als Nacharbeit in Teil 4: freie Listen A/B (pruefen --frei), Zusammenhang nach dem Vergröbern, 2 Einigungspaare T0 B/C.

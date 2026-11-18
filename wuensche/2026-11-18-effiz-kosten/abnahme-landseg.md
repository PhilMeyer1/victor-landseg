abgenommen
Wunschtext und Verhalten (Bestätigung am Diff 53afff0, Bericht und vorhandenen Prüfergebnissen): kein Mangel am Code; AK1 bis AK3 erfüllt, AK4 in Agents, gelesenen und neuen Tokens erfüllt, AK6 nachts.

Verworfen:
- Kandidat 1 und 2 (zusammengefasst, AK4, USD 191,70 statt ~221): kein Mangel des Codes. `messung.py` Zeile 64-73 bepreist 5-min- und 1-h-Cache-Schreiben getrennt, genau wie das Vorbild `PREIS` des Plugins (Stand 2026-10-08); am Lauf H0 ist `ephemeral_1h_input_tokens` in allen Antworten 0, also gilt der 5-min-Preis (5 statt 8 USD je Mio.). Die Bezugszahl 221 USD stammt aus der Ermittlung, die alle Schreibvorgänge zum 1-h-Preis rechnete; mit dem 1-h-Preis liefert der Befehl laut Bericht 221,06 USD und je Phase die Zahlen der Ermittlung. Den Code auf 221 zu zwingen wäre falsch. Zu berichtigen ist nur die Bezugszahl (Nacharbeit unten), nicht der Umsetzer.

Nicht geprüft:
- AK6 (ganze Testreihe): Nachts-Kriterium, Übergabe an die Nachtprüfung.
- Tests und Lauf am Protokollordner H0 in dieser Bestätigung nicht neu ausgeführt (Bestätiger startet nichts); Belege aus dem Bericht und `messung-h0-landseg.md`.
- `landseg/betrieb.md` (Themen-Datei des Profils, außerhalb der Arbeitskopie): Nacharbeit, kein Mangel; trägt den Hinweis noch nicht.

Nacharbeit (kein Mangel, vor oder nach dem Einreihen von Hand/Profilpflege):
- `BASIS/.claude/repos/landseg/betrieb.md` um den Befehl ergänzen (AK5) und Profil `landseg.md`, Abschnitt Routinen.
- `wuensche/2026-11-18-landseg-effiz/bericht.md` und AK4 dieses Wunsches: H0 kostet 191,70 USD (5-min-Cache-Schreiben), nicht ~221; Folgeschätzungen (K2) darauf prüfen.

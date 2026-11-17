# Gemeinsames Gesamtprojekt für Victor: Programm mit Verlauf, alle Wünsche und Berichte, alle T0-Daten (ohne Original-Luftbilder) in einem privaten GitHub-Projekt

Kurzname: landseg-gesamt | Datum: 2026-11-17 | Größe: mittel | Bereich: victor | Repos: landseg | Status: bereit

## Wunsch

„ahhh das sollte schon alles in ein gemeinsames projekt damit Victor auf alles Zugriff hat und nachvollziehen kann"

Präzisierung (Antworten des Nutzers 2026-11-17, nach landseg-uebergabe):
- Umfang: alles aus C:/Users/Phil/Developement/Victor AUSSER den Original-Luftbildern (daten/luftbilder, 582 MB, Einzeldateien über 100 MB): Programm landseg mit seinem Git-Verlauf, wuensche/ (alle Wünsche, Berichte, Methoden-Ermittlung, Abnahmen, Aufträge der Agents, entscheidungen.md), unterlagen/, daten/landseg/ samt Zwischenbildern (rund 361 MB), das Übergabe-Material aus landseg-t0 (ANLEITUNG.md, Ergebnisse je Fassung A/B/C neu benannt, Prüfseite). Ohne Git-Zusatzspeicher für große Dateien; jede Datei unter 100 MB (GitHub-Grenze), Warnungen ab 50 MB nennen.
- Die Original-Luftbilder bekommt Victor getrennt (z. B. Google-Drive-Link, macht die Hauptsession später); die Anleitung sagt, welche Dateien es sind (Namen, Größen, Prüfsummen) und wohin er sie legt, damit alle Befehle laufen.
- GitHub: das bestehende private Projekt PhilMeyer1/landseg-t0 wird umbenannt (z. B. victor-landseg) und zum Gesamtprojekt ausgebaut; nichts wird gelöscht. Push ausdrücklich gewünscht (macht die Hauptsession nach dem Einreihen, ebenso Umbenennen auf GitHub und Einladen von Victor, sobald sein Kontoname da ist).
- Vor dem Hochladen: Durchsicht auf Vertrauliches, weil Victor eine externe Person ist — keine Zugangsdaten, Schlüssel, E-Mail-Adressen, Inhalte anderer Bereiche (nai, privat, marlene, eventmanagement) oder des Wunsch-Systems selbst über das hinaus, was zum Nachvollziehen nötig ist; Fundstellen im Bericht nennen.
- Eine Einstiegsseite (README) erklärt den Aufbau des Gesamtprojekts: wo Programm, Wünsche/Berichte (Wie ist es entstanden?), Daten und Ergebnisse liegen, in welcher Reihenfolge man liest; verweist auf ANLEITUNG.md. Die Benennung A = Alles frei, B = Kategorien frei, C = Feste Kategorienliste gilt; ältere Berichte mit alter Benennung bleiben unverändert, die Übersetzungstabelle steht im README.
- Der Klärer entscheidet den Aufbau (eigenes Gesamt-Repo oder der Basisordner Victor selbst, Umgang mit dem Verlauf von landseg und mit der Hoheitstabelle .claude/hoheit.md).

## Fragen

Keine offenen Fragen: Der Aufbau ist technisch entschieden (siehe Arbeitsauftrag, „Aufbau-Entscheidung"). Ein Hinweis zur Durchsicht steht in „Risiken".

## Entscheidungen

- Push zu GitHub: Nur auf ausdrückliche Ansage, nie automatisch nach einem Wunsch. (aus entscheidungen.md, 2026-11-17) — Hier ausdrücklich angesagt, aber erst durch die Hauptsession nach dem Einreihen.
- Landschafts-Segmente: drei Fassungen als Übersicht für Victor, Ergebnis ohne Vorher/Nachher: Nutzer am 17.11.2026: „Es soll nur eine Version geben mit allen Stufen und Klassifikationen" und „erstelle dafür 2 zusätzliche Versionen. Das soll jetzt alles nur als Übersicht für Victor dienen, der sich dann raussuchen kann, was er am besten findet. Eine Version der Ergebnisse ohne Vorher nachher". (aus entscheidungen.md, 2026-11-17; Kurzfassung, gilt hier für die Benennung A/B/C der Fassungen)
- Übrige Zeilen der entscheidungen.md (Grundsätze, Kategorien, Urteil im Verbund) betreffen die Methode, nicht diesen Wunsch; sie liegen im Gesamtprojekt als `wuensche/entscheidungen.md` zum Nachlesen.

## Arbeitsauftrag

### Aufbau-Entscheidung (Klärer)

- **Eigenes Gesamt-Repo, nicht der Basisordner Victor.** Der Basisordner hat eine `.gitignore`, die fast alles ausschließt (nur Zustand, ohne `daten/`), enthält die Wunsch-System-Profile (`.claude/repos/`), `CLAUDE.md` und `.stand.json` (Wunsch-System-intern, für Victor ohne Wert) und die zwei eingebetteten Repos `landseg` und `unterlagen`. Ihn hochzuladen würde das alles öffnen oder umbauen.
- **Basis ist das schon vorhandene Gesamt-Repo `PhilMeyer1/landseg-t0`** (lokal `BASIS/daten/landseg/uebergabe/landseg-t0`, ein Commit `f0a0198`, `origin` zeigt auf GitHub). Der neue Arbeitsordner `BASIS/daten/gesamt/victor-landseg` ist ein `git clone` davon; die Kopie wird nur lokal gebaut, die bestehende Übergabe-Kopie bleibt unverändert liegen (nichts wird gelöscht; der Alt-Stand bleibt im Verlauf). Das Umbenennen auf GitHub ändert die Adresse nicht für den Verlauf; `origin` bleibt vorerst auf der alten Adresse, die Hauptsession stellt sie nach dem Umbenennen um.
- **Verlauf von landseg bleibt erhalten:** `git subtree add --prefix=programm <Pfad zum Repo landseg> main` (ohne `--squash`), danach `git subtree pull` für spätere Stände. Der Ordner heißt `programm/`, nicht `landseg/`: im alten Stand von landseg-t0 liegt das Python-Paket `landseg/` im Wurzelordner. Vorher werden die alten Wurzeldateien dieser Kopie mit `git rm` aus dem neuen Stand genommen (bleiben im Verlauf); ihr Inhalt kommt aus dem Verlauf von landseg zurück bzw. in `ergebnisse/`. Dasselbe für `unterlagen` (Prefix `unterlagen`, zwei Commits, eigene `.gitattributes` mit `berichte/** -text` bleibt wirksam).
- **Zielaufbau:** `README.md` (Einstieg), `ANLEITUNG.md` (Anleitung zum T0-Test, aus der Übergabe, Pfade für das Gesamtprojekt angepasst), `programm/` (Repo landseg mit Verlauf), `unterlagen/` (Repo unterlagen mit Verlauf), `wuensche/` (Wunsch-Dateien, Berichtsordner, `entscheidungen.md`, `uebersicht.md`; ohne `roh/` und ohne `.stand.json`), `daten/landseg/` (die Arbeitsdaten T0 mit den alten Ordnernamen `kern500`, `fassung-b`, `fassung-c`; ohne `uebergabe/`, das ist nur die alte Kopie), `ergebnisse/` (die Übergabe-Ergebnisse mit neuer Benennung a-alles-frei, b-kategorien-frei, c-feste-liste, Prüfseite, Gesamtbilder; Inhalt aus `uebergabe/landseg-t0/T0/`), `daten/luftbilder/README.md` (Platzhalter mit Namen, Größen, SHA-256 der Originale und dem Hinweis, wohin sie gehören; die Bilder selbst fehlen bewusst).
- **Hoheitstabelle:** `.claude/hoheit.md` liegt außerhalb von Victor (Bereich-übergreifend) und kommt nicht in das Gesamtprojekt. Das Gesamtprojekt ist eine abgeleitete Kopie ohne eigene Hoheit; die Tabelle bekommt nur eine Zeile, siehe Nacharbeit.
- **Werkzeug:** `tools/gesamt_projekt.py` im Repo landseg (Standardbibliothek, mit Tests), Befehle `bauen` (Gesamt-Ordner anlegen oder aktualisieren, idempotent, committet im Gesamt-Ordner), `pruefen` (Vollständigkeit, Größen, Pfade im README, Luftbild-Prüfsummen) und `durchsicht` (Suche nach Vertraulichem, schreibt den Bericht). Quelle `--basis <Victor>`, Ziel `--ziel <Ordner>`.
- **Größen heute:** größte Datei 17,8 MB (`sam3_roh.npz`), also nichts über 50 MB und nichts über 100 MB; die 361 MB von `daten/landseg` enthalten die 45 MB der alten Kopie `uebergabe/` (nicht mitgenommen), im Ziel bleiben rund 320 MB Daten plus Verlauf. Das Werkzeug meldet trotzdem jede Datei ab 50 MB als Warnung und bricht ab 100 MB ab.

Nacharbeit: `.claude/hoheit.md` (Abschnitt „Victor"): Zeile „Gesamtprojekt victor-landseg (GitHub, Kopie)" — Hoheit: Bereich victor, abgeleitet aus `programm/`, `unterlagen/`, `wuensche/`, `daten/landseg/`; keine eigenen Daten. · `BASIS/daten/README.md`: Hinweis auf `BASIS/daten/gesamt/`. · Hauptsession nach dem Einreihen: auf GitHub umbenennen, `origin` umstellen, pushen (wegen rund 320 MB in Etappen und ohne Force), Victor einladen.

### Abnahmekriterien

AK1: Im Gesamt-Ordner liegen `README.md`, `ANLEITUNG.md`, `programm/`, `unterlagen/`, `wuensche/`, `daten/landseg/`, `ergebnisse/`, `daten/luftbilder/README.md`; der Verlauf von landseg ist erhalten (alle Commits aus `git -C landseg log` stehen im Gesamt-Repo, auch `git log -- programm` zeigt sie) und der alte Commit `f0a0198` von landseg-t0 steht weiter im Verlauf — prüfbar: `git -C <Ziel> log --oneline`, `git -C <Ziel> log --oneline -- programm`, `git -C <Ziel> cat-file -t f0a0198`, `ls <Ziel>`
AK2: Alles Genannte ist vollständig und unverändert da: jede Datei aus `wuensche/` (ohne `roh/`, `.stand.json`), `unterlagen/` und `daten/landseg/` (ohne `uebergabe/`) steht mit gleicher Prüfsumme im Ziel; kein Original-Luftbild (`daten/luftbilder/**`) und nichts aus `.claude/`, `CLAUDE.md` des Basisordners ist darin — prüfbar: `"$PY" -B tools/gesamt_projekt.py pruefen --basis <Victor> --ziel <Ziel>` (erwartet „fehlend 0, abweichend 0, fremd 0", Exit 0)
AK3: Jede Datei ist kleiner als 100 MB, es gibt keinen Git-Zusatzspeicher (kein `lfs` in `.gitattributes`), und jede Datei ab 50 MB steht als Warnung in der Ausgabe (heute keine; größte Datei 17,8 MB) — prüfbar: `… pruefen` meldet „größte Datei … MB; Warnungen: 0", dazu Unittest mit einer künstlichen 60-MB-Datei (Warnung) und einer 101-MB-Datei (Fehler, Exit 1)
AK4: Die Durchsicht auf Vertrauliches ist gelaufen und im Bericht `wuensche/2026-11-17-landseg-gesamt/bericht-landseg.md` ausgewiesen: je Fundstelle Datei, Zeile, Art (Zugangsdaten/Schlüssel, E-Mail-Adresse, Inhalt eines anderen Bereichs nai/privat/marlene/eventmanagement, Wunsch-System-Innenleben, Pfad mit Kontoname) und Behandlung (behalten mit Grund | in der Kopie entfernt); keine Zugangsdaten und keine Schlüssel im Ziel; bekannte Funde (öffentliche Behörden-Adressen in `wuensche/2026-11-17-landseg-methode/`) sind eingeordnet; Quellordner bleiben unverändert — prüfbar: `"$PY" -B tools/gesamt_projekt.py durchsicht --ziel <Ziel>` (Exit 1 bei ungeordnetem Fund, 0 sonst), Lesen `bericht-landseg.md`
AK5: Das README erklärt Aufbau und Lesereihenfolge (Programm, Wie ist es entstanden = Wünsche/Berichte, Daten, Ergebnisse), verweist auf `ANLEITUNG.md`, führt die Benennung A = Alles frei, B = Kategorien frei, C = Feste Kategorienliste und die Übersetzungstabelle zu den alten Namen in den älteren Berichten (`fassung-c`, `fassung-b`, `kern500`/`urteil-stand`) auf und erklärt, dass `ergebnisse/` die Übergabe-Auswahl und `daten/landseg/` die vollen Arbeitsdaten mit alten Ordnernamen sind; jeder im README genannte Pfad existiert — prüfbar: Lesen `README.md`; `… pruefen` meldet „README-Pfade: alle vorhanden"
AK6: Die Anleitung nennt die acht Original-Dateien (Namen, Größen in Bytes, SHA-256, aus `BASIS/daten/README.md`) und sagt, in welchen Ordner Victor sie legt, damit alle Befehle der Anleitung laufen; fehlen sie, meldet das Werkzeug das mit Namen, statt zu scheitern — prüfbar: Lesen `ANLEITUNG.md` und `daten/luftbilder/README.md`; `… pruefen --luftbilder <Victor>/daten/luftbilder` meldet „8 von 8 passen"; ohne die Option „Luftbilder nicht geprüft", Exit 0
AK7: Der Weg des Nutzers am laufenden Stand: In einem frischen `git clone` des Ziels (neuer Ordner) mit hineinkopierten Originalen laufen die Tests des Programms und der erste Befehl der Anleitung ohne Fehler — prüfbar: `git clone <Ziel> <Neuordner>`, dort in `programm/` die Testreihe aus dem Profil (`"$PY" -B -m unittest discover -s tests -t .`, grün) und der Prüfbefehl für T0 aus `ANLEITUNG.md` (Exit 0), die Texte der Anleitung stimmen mit den gelaufenen Befehlen überein
AK8: `bauen` ist wiederholbar: ein zweiter Lauf ohne Änderung erzeugt keinen neuen Commit, nach einem neuen Commit in landseg bringt ein Lauf ihn mit Verlauf nach `programm/`, und im Ziel bleibt `core.autocrlf` aus (Dateien Byte für Byte wie in der Quelle) — prüfbar: Unittest mit Wegwerf-Repos (zwei Läufe, ein neuer Commit), `git -C <Ziel> config core.autocrlf` meldet `false`

### Einstieg

- landseg: `tools/pruefe_kategorien.py` — Muster für ein eigenständiges Werkzeug in `tools/` (Standardbibliothek, Aufruf mit `-I`-tauglichem Skript); das neue `tools/gesamt_projekt.py` daneben anlegen, Tests in `tests/` (Muster: bestehende Tests, `unittest`).
- landseg: `README.md` (Tabelle „Inhalt") — neue Zeile für `tools/gesamt_projekt.py`; `.claude/repos/landseg.md` (Profil, „Routinen") nennt es die Hauptsession später per Profilpflege.
- landseg: `BASIS/daten/landseg/uebergabe/landseg-t0/ANLEITUNG.md` (303 Zeilen, Abschnitt Benennung ab Zeile 49, Dateitabelle Zeilen 30–40) — Quelle der neuen `ANLEITUNG.md`; Pfade `T0/…` werden zu `ergebnisse/…`, Programm-Befehle laufen in `programm/`, Daten unter `daten/`.
- Quelle der Daten: `BASIS/wuensche/`, `BASIS/unterlagen/` (Repo, `.git` mit 2 Commits), `BASIS/daten/landseg/T0/` (kern500, fassung-b, fassung-c), `BASIS/daten/README.md` (Tabelle der Originale mit Prüfsummen).

### Bausteine und Fallen

- Verlauf übernehmen mit `git subtree add --prefix=programm "<Pfad>" main` (ist in Git for Windows vorhanden, `git subtree` meldet Aufruf). `--squash` nicht verwenden. Der Zielstand darf bei `subtree add` keine Änderungen haben; erst `git rm` der alten Wurzeldateien committen.
- Der Prefix darf nicht `landseg` heißen (Kollision mit dem Paket-Ordner im alten Stand von landseg-t0).
- `core.autocrlf=true` steht in der alten Kopie: im Ziel `git config core.autocrlf false` und im Wurzel-`.gitattributes` `* -text`, sonst werden Berichte (CRLF) und Prüfsummen beim Auschecken verändert. Prüfsummen immer Quelle gegen Ziel vergleichen.
- Nicht mitnehmen: `wuensche/**/roh/` (Roh-Läufe der Agents, auch im Basisordner unversioniert), `wuensche/.stand.json`, `.claude/` und `CLAUDE.md` des Basisordners, `daten/luftbilder/`, `daten/landseg/uebergabe/` (alte Kopie, würde den Verlauf doppeln). Das `.gitignore` des Ziels darf `.npz`, `.tif`, `.html` nicht ausschließen.
- Das Durchsuchen deckt Quellen ab, nicht nur das Ziel: Funde in Berichten werden nur in der Kopie behandelt (Berichte „bleiben unverändert" gilt für die Quelle). Schon bekannt: `kundenservice@bev.gv.at` und `doris.geol.post@ooe.gv.at` in `wuensche/2026-11-17-landseg-methode/` (öffentliche Behörden-Adressen, Bezugsquellen der Luftbilder, zum Nachvollziehen nötig — behalten, im Bericht einordnen); 121 Dateien enthalten Pfade `C:/Users/Phil/…`, Wörter wie `wunsch-system`, `marlene` oder `eventmanagement` (Ursache je Treffer ansehen: bloße Erwähnung des Systems oder echter Inhalt eines anderen Bereichs). Echte Inhalte anderer Bereiche in der Kopie entfernen und im Bericht nennen, Erwähnungen des Wunsch-Systems als Herkunft behalten. Kein Zugriff auf `BASIS/daten/zugaenge/` o. Ä. (Geheimnisschutz): Ordner nie öffnen, nur im Ausschluss nennen.
- Benennung: In den Quell-Berichten und in `daten/landseg/` gilt die alte (`kern500` = C, `fassung-b` = B, `fassung-c` = A); die Anleitung aus der Übergabe hat die Übersetzungstabelle schon (Zeilen 49–60), ins README übernehmen, nicht neu erfinden.
- Größe der ersten Übertragung rund 320 MB plus 45 MB Alt-Verlauf; Push in Etappen ist Sache der Hauptsession (nicht hier pushen).
- Geschützt: Zielordner `BASIS/daten/gesamt/` liegt im unversionierten Datenraum (Basis-`.gitignore` schließt `daten/*` aus); nie unter `daten/landseg/` anlegen (würde sich selbst einschließen).
- Python: Interpreter aus dem Profil; Hilfsskripte außerhalb des Repos mit `-I`, Pfade in Windows-Form.

### Bauweise

Richtung: neutral
Berührt: landseg: keine
Tilgt: keine
Flick-Signale: keine — kein Vorgänger (neues, eigenständiges Werkzeug; A1 und A2 aus `altlasten.md` liegen in anderen Dateien)
Anbau: neues Skript `tools/gesamt_projekt.py` mit Tests neben den vorhandenen Werkzeugen — Dauer mittel — Risiko gering (nur Lesen der Quellen, Schreiben im neuen Ordner) — danach bleibt ein wiederholbarer Weg, das Gesamtprojekt aufzufrischen
Belege: –
Empfehlung: Anbau — kein Muster und keine Altlast betroffen, Umbau nicht angezeigt

Reihenfolge der Repos: landseg · Risiken: Vertrauliches in Berichten (Durchsicht), Windows-Zeilenenden (Prüfsummen), Größe des ersten Push, Verlauf-Kollision `landseg/` · Vorbedingungen: keine

## Entwurf

Stufe: nein — keine Oberfläche; Ergebnis sind Ordner, ein Werkzeug und zwei Textdateien (README, Anleitung).

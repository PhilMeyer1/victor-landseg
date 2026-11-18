# Urteils-Agent: {{FASSUNG_NAME}}, Teilkachel {{TEILKACHEL}}, Viertel {{VIERTEL}}

Du beurteilst als einziger Agent das Viertel {{VIERTEL}} ({{VIERTEL_LAGE}}, {{SEGMENTZAHL}} Segmente) der
Teilkachel {{TEILKACHEL}} in {{FASSUNG_NAME}} des Ausschnitts {{AUSSCHNITT}}. Die anderen Viertel dieser
Teilkachel urteilen andere Agents, gleichzeitig mit dir.
Lies zuerst den Skill `landseg-agent` (`{{REPO}}/.claude/skills/landseg-agent/SKILL.md`); seine Regeln gelten hier.
Du schreibst nur in deinen Ergebnisordner und, nur über `eingriff` und `kante`, auf die Karte, die dein Auftrag
unter „Nachsegmentieren“ nennt. Alle anderen Eingaben liest du nur.

## Reihenfolge (Vorgabe des Nutzers)

1. Zuerst den ganzen Ausschnitt {{AUSSCHNITT}}: `{{AUSSCHNITT_BILD}}` (Teilkachel rXcY = Zeile X, Spalte Y,
   gezählt von oben links ab 0).
2. Dann die ganze Teilkachel {{TEILKACHEL}}: `{{TEILKACHEL_BILD}}` (Grenzen, Nummern, Viertel).
3. Dann nur dein Viertel {{VIERTEL}}, wie es dein Auftrag beschreibt. Ausschnitt und Teilkachel sind nur
   Zusammenhang: Du urteilst nur über die Segmente in der Liste deines Auftrags, auch über ihre Teilstücke nach
   einer Teilung; ein Segment an der Viertelgrenze, das nicht in deiner Liste steht, gehört einem anderen Agent.
   Die Nachbar-Viertel siehst du nur auf den beiden Bildern aus Schritt 1 und 2.

Sieh jedes Bild nur einmal an. Nennt der Auftrag dieselben Übersichtsbilder noch einmal, sind es diese; weitere
Übersichtsbilder des Ausschnitts und der Teilkachel nur, wenn du eine Stelle sonst nicht beurteilen kannst. Trage
die Bilder aus Schritt 1 und 2 in `urteil.json` unter "bilder_angesehen" → "uebersicht" vor den Viertelbildern ein.

## Auftrag (maßgeblich)

`{{AUFTRAG}}` → Ergebnis in `{{ERGEBNIS}}`

## Gemeinsame Karte

Die Karte zum Nachsegmentieren teilen sich die Agents der vier Viertel. `eingriff` und `kante` warten, bis kein
anderer Agent gerade auf ihr schreibt, und lesen sie dann frisch; schreib alle Eingriffe deines Viertels in einen
Stapel und teile nur Segmente deiner Liste. Lehnt `pruefen` danach eine Stelle außerhalb deiner Liste ab, nenne sie
unter "offen", statt sie zu ändern.

## Hinweis des Laufs

{{HINWEIS}}

Im Zweifel `sicher: false` und eine Notiz unter "offen": eine ehrlich als unsicher markierte Fläche wird
nachgeprüft, eine falsch als sicher markierte geht unbemerkt in die Trainingsdaten. Arbeite jedes Segment deiner
Liste ab; überfliege nichts gegen Ende. Wird dir Platz knapp, schreib ehrlich unter "nicht_geprueft", was fehlt,
statt zu raten. Führe zum Schluss die Kontrolle aus dem Auftrag aus.

## Grenzen

Kein Subagent, kein ToolSearch, keine Fenster, keine Dauerprozesse, nichts installieren, kein git. Python nur
`{{PY}}` (Skripte als Datei, ausführen mit `-B`); Befehle `{{PY}} -B -m landseg …` im Ordner `{{REPO}}`. Am Repo
und an den Originalbildern änderst du nichts.

RÜCKGABE: ausschließlich das JSON nach Schema — unter "teile" genau ein Eintrag (v = {{V}}), nie den Inhalt
deiner Dateien.

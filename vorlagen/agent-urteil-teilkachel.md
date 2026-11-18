# Urteils-Agent: {{FASSUNG_NAME}}, Teilkachel {{TEILKACHEL}}

Du bearbeitest als einziger Agent {{FASSUNG_NAME}} für die ganze Teilkachel {{TEILKACHEL}} des Ausschnitts
{{AUSSCHNITT}}; diese Fassung hat keine Viertel-Aufträge.
Lies zuerst den Skill `landseg-agent` (`{{REPO}}/.claude/skills/landseg-agent/SKILL.md`); seine Regeln gelten hier.
Du schreibst nur in die Ordner, die dein Auftrag nennt. Alle anderen Eingaben liest du nur.

## Reihenfolge (Vorgabe des Nutzers)

1. Zuerst den ganzen Ausschnitt {{AUSSCHNITT}}: `{{AUSSCHNITT_BILD}}` (Teilkachel rXcY = Zeile X, Spalte Y,
   gezählt von oben links ab 0).
2. Dann die ganze Teilkachel {{TEILKACHEL}}: `{{TEILKACHEL_BILD}}`.
3. Dann segmentierst und klassifizierst du die Teilkachel nach deinem eigenen Vorgehen, wie im Auftrag beschrieben.

Sieh jedes Bild nur einmal an. Trage die Bilder aus Schritt 1 und 2 in `arbeitsweise.md` ein.

## Auftrag (maßgeblich)

`{{AUFTRAG}}` → Ergebnis in `{{ERGEBNIS}}`

## Hinweis des Laufs

{{HINWEIS}}

Im Zweifel `sicher: false` und eine Notiz unter "offen": eine ehrlich als unsicher markierte Fläche wird
nachgeprüft, eine falsch als sicher markierte geht unbemerkt in die Trainingsdaten. Arbeite die ganze Teilkachel
ab; überfliege nichts gegen Ende. Führe zum Schluss die Kontrolle aus dem Auftrag aus.

## Grenzen

Kein Subagent, kein ToolSearch, keine Fenster, keine Dauerprozesse, nichts installieren, kein git. Python nur
`{{PY}}` (Skripte als Datei, ausführen mit `-B`); Befehle `{{PY}} -B -m landseg …` im Ordner `{{REPO}}`. Am Repo
und an den Originalbildern änderst du nichts.

RÜCKGABE: ausschließlich das JSON nach Schema — unter "teile" genau ein Eintrag (v = {{V}}), nie den Inhalt
deiner Dateien.

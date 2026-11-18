"""Einmalige Anpassung der Kopie baue_auftraege_h0.py für Teil 3 (Karte je Auftrag, Nachsegmentieren)."""
from pathlib import Path

p = Path("C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/skripte/baue_auftraege_h0.py")
t = p.read_text(encoding="utf-8")


def r(alt, neu, anzahl=1):
    global t
    n = t.count(alt)
    assert n == anzahl, (n, alt[:80])
    t = t.replace(alt, neu)


r('def viertel_auftrag(fassung, tk, n, ein, bilder: Path, ergebnis: Path, daten: Path, bearbeiter, ganz: dict) -> str:\n'
  '    """fassung c = feste Liste, b = Kategorien frei; daten = Ordner der Fassung (Vorstufen-Kopie je Teilkachel)."""\n',
  'def viertel_auftrag(fassung, tk, n, ein, bilder: Path, ergebnis: Path, karte: Path, bearbeiter, ganz: dict) -> str:\n'
  '    """fassung c = feste Liste, b = Kategorien frei; karte = Ordner der Kartenkopie (labels.tif, segmente.json,\n'
  '    kandidaten.json), auf der der Agent nachsegmentiert."""\n')
# Vorlage: Karte darf nach dem Abschnitt Nachsegmentieren geändert werden
r('    t = ersetze(t, "Du urteilst über jedes\\nSegment, das im Kern dieser Teilkachel liegt,",\n',
  '    t = ersetze(t, "zeichnest ein, was\\ndu ändern würdest. Die Label-Karte änderst du nicht.",\n'
  '                "zeichnest ein, was\\ndu ändern würdest. Die Label-Karte änderst du nur nach dem Abschnitt "\n'
  '                "„Nachsegmentieren“\\n(grob zusammengefasste Segmente teilen, bevor du sie urteilst).")\n'
  '    t = ersetze(t, "## Daten (eingefrorener Stand, nur lesen)",\n'
  '                "## Daten (nur lesen; Ausnahme: Karte und `segmente.json` aus „Karte zum Nachsegmentieren“, "\n'
  '                "nur über `eingriff` und `kante`)")\n'
  '    t = ersetze(t, "Du urteilst über jedes\\nSegment, das im Kern dieser Teilkachel liegt,",\n')
r('Für fragliche Grenzen `kante` (W4, hier nur "\n                "zum Ansehen\\nder Bildkante), zur Kontrolle `pruefen`.")',
  'Für fragliche Grenzen `kante` (W4: "\n                "ansehen; einrasten\\nnur an Linien aus deinem Nachsegmentieren), zur Kontrolle `pruefen`.")')
r('''        t = ersetze(t, '"unsicher": ["..."], "nicht_geprueft": ["..."]}',
                    '"unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."],\\n'
''', '''        t = ersetze(t, '"unsicher": ["..."], "nicht_geprueft": ["..."]}',
                    '"unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."],\\n'
                    ' "eingriffe": [{"schritt": "teilen", "vorher": [ID], "nachher": [ID, ID], "grund": "ein Satz"}],\\n'
''')
r('''                    '"unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."]}')''',
  '''                    '"unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."],\\n'
                    ' "eingriffe": [{"schritt": "teilen", "vorher": [ID], "nachher": [ID, ID], "grund": "ein Satz"}]}')''')
r("Kandidaten aus `{p(daten)}/{tk}/kandidaten.json`", "Kandidaten aus `{p(karte)}/kandidaten.json`")
r("--segmente {p(daten)}/{tk}/segmente.json --fassung", "--segmente {p(karte)}/segmente.json --fassung")
r('    if fassung == "b":\n        abschnitt += """',
  '    abschnitt += "\\n" + nachseg_abschnitt(fassung, tk, karte, ergebnis, bearbeiter)\n'
  '    if fassung == "b":\n        abschnitt += """')
r('"LABELS": f"{daten.name}/{tk}/labels.tif", "SEGMENTE": f"{daten.name}/{tk}/segmente.json",',
  '"LABELS": (karte / "labels.tif").relative_to(H0).as_posix(),\n'
  '                      "SEGMENTE": (karte / "segmente.json").relative_to(H0).as_posix(),')
r('viertel_auftrag(fassung, tk, n, ein, bilder, ergebnis, daten, bearbeiter, erg[tk]["ganz"])',
  'viertel_auftrag(fassung, tk, n, ein, bilder, ergebnis, daten / tk, bearbeiter, erg[tk]["ganz"])')
r('viertel_auftrag("c", GEGEN_TK, n, ein, bilder, ergebnis, daten_c, f"gegen-c-{GEGEN_TK}-v{n}", erg[GEGEN_TK]["ganz"])',
  'viertel_auftrag("c", GEGEN_TK, n, ein, bilder, ergebnis, daten_c / "gegenprobe" / GEGEN_TK, f"gegen-c-{GEGEN_TK}-v{n}", erg[GEGEN_TK]["ganz"])')
# Gegenprobe: eigene Karte nennen, fremde Karte und fremdes Urteil nicht ansehen
r('''"Viertel. Sein Ergebnis (`{p(daten_c)}/urteil/`) siehst du nicht an, auch nicht, wenn es "
                       "schon da ist. Aus beiden Urteilen wird die Übereinstimmung gemessen.\\n\\n## Werkzeuge")''',
  '''"Viertel. Sein Ergebnis (`{p(daten_c)}/urteil/`) und seine Karte (`{p(daten_c)}/{GEGEN_TK}/`) siehst du "
                       "nicht an, auch nicht, wenn sie schon da sind. Du teilst nur auf deiner eigenen Kopie "
                       f"(`{p(daten_c)}/gegenprobe/{GEGEN_TK}/`). Aus beiden Urteilen wird die Übereinstimmung gemessen.\\n\\n## Werkzeuge")''')
r('''                                   "bearbeiter": f"gegen-c-{GEGEN_TK}-v{n}", "modell": "opus", "effort": "hoch"})''',
  '''                                   "karte": p(daten_c / "gegenprobe" / GEGEN_TK),
                                   "bearbeiter": f"gegen-c-{GEGEN_TK}-v{n}", "modell": "opus", "effort": "hoch"})''')
r('''                                        "auftrag": p(ordner / "auftrag.md"), "ergebnis": p(ergebnis), "bilder": p(bilder),
                                        "bearbeiter": bearbeiter, "modell": "opus", "effort": "hoch"})''',
  '''                                        "auftrag": p(ordner / "auftrag.md"), "ergebnis": p(ergebnis), "bilder": p(bilder),
                                        "karte": p(daten / tk), "bearbeiter": bearbeiter, "modell": "opus", "effort": "hoch"})''')
r('plan = {"schema": "landseg-h0-auftraege/1",', 'plan = {"schema": "landseg-h0-auftraege/1", "vorstufe": "grob", "konfig": p(KONFIG),')
p.write_text(t, encoding="utf-8", newline="\n")
print("ok")

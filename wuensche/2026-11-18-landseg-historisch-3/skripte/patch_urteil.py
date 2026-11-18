"""Einmalige Anpassung der Kopie pruefe_urteil.py für Teil 3: Feld "eingriffe" (Nachsegmentieren)."""
from pathlib import Path

p = Path("C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/skripte/pruefe_urteil.py")
t = p.read_text(encoding="utf-8")


def r(alt, neu):
    global t
    assert t.count(alt) == 1, alt[:80]
    t = t.replace(alt, neu)


r('Ausgabe: Befund, letzte Zeile `ok` oder `FEHLER`; Exit 0 / 1, Aufruf- oder Lesefehler 2.\n"""',
  'Teil 3 (grobe Vorstufe, Nachsegmentieren): --segmente ist die bearbeitete Kartenkopie. Liste `eingriffe`\n'
  '(je Eintrag `vorher`, `nachher` als ID-Listen, `grund` als Text) ist Pflicht, wenn --viertel gesetzt ist oder\n'
  'neben urteil.json eine eingriffe.json liegt (dann nicht leer). Verlangt sind die IDs aus --ids, die noch auf\n'
  'der Karte stehen, plus jede neue ID (in `nachher`, nicht in `vorher`) im Kern; eine ID aus --ids, die nicht\n'
  'mehr auf der Karte steht, muss unter `vorher` stehen. IDs aus `nachher` dürfen geurteilt werden.\n'
  'Ausgabe: Befund, letzte Zeile `ok` oder `FEHLER`; Exit 0 / 1, Aufruf- oder Lesefehler 2.\n"""')
r('''    soll = {int(x) for x in a.ids.split(",")} if a.ids else kern
    maengel = []
''', '''    soll = {int(x) for x in a.ids.split(",")} if a.ids else kern
    maengel = []
    vorhanden = kern | rand
    eingriffe = urteil.get("eingriffe")
    stapel = Path(a.urteil).parent / "eingriffe.json"
    vorher_alle, nachher_alle, neu_alle = set(), set(), set()
    if eingriffe is None:
        if a.viertel is not None or stapel.is_file():
            maengel.append("Liste `eingriffe` fehlt (ohne Eingriff: leere Liste)")
        eingriffe = []
    if not isinstance(eingriffe, list):
        maengel.append("`eingriffe` ist keine Liste")
        eingriffe = []
    for i, g in enumerate(eingriffe, 1):
        vorher = g.get("vorher") if isinstance(g, dict) else None
        nachher = g.get("nachher") if isinstance(g, dict) else None
        if not (isinstance(vorher, list) and vorher and all(isinstance(x, int) for x in vorher)):
            maengel.append(f"Eingriff {i}: `vorher` keine nicht leere ID-Liste")
            vorher = []
        if not (isinstance(nachher, list) and all(isinstance(x, int) for x in nachher)):
            maengel.append(f"Eingriff {i}: `nachher` keine ID-Liste")
            nachher = []
        if not (isinstance(g, dict) and isinstance(g.get("grund"), str) and g["grund"].strip()):
            maengel.append(f"Eingriff {i}: `grund` fehlt")
        vorher_alle |= set(vorher)
        nachher_alle |= set(nachher)
        neu_alle |= set(nachher) - set(vorher)
    try:
        schritte = json.loads(stapel.read_text(encoding="utf-8")).get("schritte") if stapel.is_file() else None
    except (OSError, ValueError, AttributeError):
        schritte = None
        maengel.append("eingriffe.json nicht lesbar")
    if schritte and not eingriffe:
        maengel.append(f"eingriffe.json hat {len(schritte)} Schritte, `eingriffe` im Urteil ist leer")
    weg = sorted(i for i in soll if i not in vorhanden)
    ohne_eingriff = [i for i in weg if i not in vorher_alle]
    if ohne_eingriff:
        maengel.append(f"nicht mehr auf der Karte, aber in keinem Eingriff unter `vorher`: {ohne_eingriff}")
    soll = (soll & vorhanden) | (neu_alle & kern)
    erlaubt = soll | (nachher_alle & vorhanden)
''')
r('''    fremd_rand = sorted(i for i in gesehen if i in rand)
    fremd = sorted(i for i in gesehen if i not in soll and i not in rand)''',
  '''    fremd_rand = sorted(i for i in gesehen if i in rand and i not in erlaubt)
    fremd = sorted(i for i in gesehen if i not in erlaubt and i not in rand)''')
r('''          f"sicher false: {sum(1 for e in eintraege if e.get('sicher') is False)}")''',
  '''          f"sicher false: {sum(1 for e in eintraege if e.get('sicher') is False)}, "
          f"Eingriffe: {len(eingriffe)}, neue IDs im Kern: {len(neu_alle & kern)}")''')
p.write_text(t, encoding="utf-8", newline="\n")
print("ok")

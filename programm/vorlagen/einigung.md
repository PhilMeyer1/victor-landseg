# Auftrag: Einigung an den Übergängen, Fassung {{FASSUNG}}, Bündel {{BUENDEL}}

Lies zuerst den Skill `landseg-agent` (`{{REPO}}/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier, besonders L6 (Nahtregel) und L13 (Einigung im Verbund). Antworte auf Deutsch.

Gegenstand: Stellen, an denen zwei benachbarte Segmente an einer Kerngrenze (Naht, auch an der Ecke
von vier Teilkacheln) oder an einer Viertelgrenze (Mitte einer Teilkachel) ohne Bildkante aneinander-
grenzen, aber verschiedene Klassen tragen. Die Teilkacheln wurden von verschiedenen Agents beurteilt;
du urteilst jetzt **im Verbund**: Du siehst beide Seiten jeder Stelle und gibst ein Urteil, das für
alle Beteiligten gilt.

## Daten (eingefrorener Stand, nur lesen)

- `{{AUFTRAEGE}}/{{BUENDEL}}/auftrag.json`: je Paar `paar` (`<teilkachel>:<id>|<teilkachel>:<id>`),
  `art` (`naht` oder `viertel`), `strecken` (Lage in Bildpunkten des Ausschnitts), `randpunkte`, beide
  Segmente mit allen Feldern aus `segmente.json` (Klasse, Sicherheit, Beschreibung) und `bild`; dazu
  `klassen` (die Kategorienliste der Fassung) und `abgabe_muster`.
- `{{AUFTRAEGE}}/{{BUENDEL}}/paar_<nr>.jpg`: links das Luftbild um die Stelle, rechts dasselbe mit den
  beiden Segmenten (türkis, magenta) und der Grenzlinie (gelb).
- `{{DATEN}}/{{URTEILE}}/<teilkachel>/urteil.json`: die Urteile der Teilkacheln beider Seiten; lies
  sie zu jedem Segment mit, bevor du entscheidest.
- `{{DATEN}}/manifest.json` und das Ausschnittbild darin, falls du die Stelle weiter vergrößern willst
  (`{{PY}} -m landseg ansicht`, eigene Bilder nur in `{{ERGEBNIS}}`).

## Was

Je Paar genau eine Entscheidung:

- `gleich`: Beide Seiten zeigen dieselbe Fläche. Wähle die Klasse aus `klassen`, die am besten passt
  (feinste sicher erkennbare Ebene, Regeln aus `KATEGORIEN.md` bzw. der Liste der Fassung), und
  nenne sie unter `klasse`. Hängen mehrere Paare über ein gemeinsames Segment zusammen (Kette a–b–c,
  Ecke), bekommen alle Glieder dieselbe Klasse.
- `grenze`: Dort liegt wirklich eine Grenze zweier verschiedener Flächen, nur ohne Farbsprung;
  beide Klassen bleiben.
- `unklar`: Am Bild nicht sicher zu entscheiden; beide Segmente werden als unsicher markiert.

Jede Entscheidung braucht einen Satz `grund`, was das Bild zeigt. Nur Klassen: Grenzen, IDs und
Label-Karten bleiben, wie sie sind; Segmente nur im Kontextrand kommen nicht vor und werden nicht
geändert. Keine neue Klasse anlegen: Passt keine der Liste, entscheide `unklar`.

**Fassung A (Alles frei):** Die Kategorien der vier Teilkacheln sind schon zur gemeinsamen Liste
`kategorien-a.json` zusammengelegt; die Einigung läuft auf dieser Liste (`klasse` ist ein Code daraus,
der ursprüngliche Code der Teilkachel steht unter `klasse_teil`). Meinen beide Seiten dieselbe Fläche
unter verschiedenen Namen, wähle den Code der gemeinsamen Liste, der am besten passt, und nenne den
Grund.

## Wie

Ändere nichts an den Daten. Prüfe deine Abgabe mit
`{{PY}} -m landseg einigung anwenden --manifest {{DATEN}}/manifest.json --fassung {{FASSUNG}} --auftraege {{AUFTRAEGE}} --abgabe {{ERGEBNIS}}/einigung_abgabe.json --probe`
(Befehle im Ordner `{{REPO}}`); sie muss ohne „Abgelehnt“ durchlaufen. Umsetzen macht die
Hauptsession für alle Bündel gemeinsam.

## Ergebnis in `{{ERGEBNIS}}` (genau diese Namen)

- eigene Bilder, falls du welche gemacht hast (`einigung_<nr>.jpg`).
- `einigung_abgabe.json` (UTF-8), nach `abgabe_muster`:

```
{"schema": "landseg-einigung-abgabe/1", "fassung": "{{FASSUNG}}", "buendel": "{{BUENDEL}}",
 "bearbeiter": "{{BEARBEITER}}",
 "paare": [{"paar": "r0c0:12|r0c1:7", "entscheidung": "gleich|grenze|unklar",
            "klasse": "Code nur bei gleich, sonst null", "grund": "ein Satz, was das Bild zeigt"}],
 "offen": ["..."], "nicht_geprueft": ["..."]}
```

Jedes Paar des Auftrags genau einmal, kein anderes.

## Rückgabe

Paare gesamt, je Entscheidung die Zahl, die letzte Zeile der Probe, was offen blieb.

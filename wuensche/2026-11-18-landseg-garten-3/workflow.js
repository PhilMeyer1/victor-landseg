// landseg-garten — Teil 3 von landseg-garten (Wunsch-Datei
// C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3.md, Mutterwunsch …/2026-11-18-landseg-garten.md)
// samt Nacharbeit von landseg-sw-grob: H0 (Scan 1968) gröber machen, dann Gärten in den fertigen Ergebnissen T0 (Übergabe)
// und H0, je Fassung A, B, C: Kandidaten per Regel, Bestätigung am Bild durch Agents, anwenden, prüfen, zählen. Ohne Commit.
//
// Vorgaben des Nutzers (2026-11-18): Garten = eine Unterklasse unter Dauergrünland (C: 3.6); jede krautige Grünfläche und
// jedes Beet im Haus- oder Hofgarten, mit oder ohne Rasen; nur Haus- und Hofgärten (Parks, Friedhöfe, Sportrasen bleiben
// Wiese/Weide); Bäume, Sträucher, Hecken bleiben Gehölz; Umstellen = Regel, dann Agents am Bild; SW-Bilder gröber
// (Richtwert 600, Mindestfläche 100 m²), H0 automatisch zusammenlegen; klar erkennbare Gärten bleiben auch auf SW.
//
// args (JSON-Objekt):
//   run       string  Pflicht   Lauf-Kennung ^[\w-]{1,40}$
//   t0        string  Pflicht   abs. Ordner T0 der Übergabe (manifest.json, Fassungsordner)
//   h0        string  Pflicht   abs. Ordner H0 (manifest.json, Fassungsordner)
//   bericht   string  Pflicht   abs. Berichtsordner dieses Teils
//   repo      string  Pflicht   abs. Ordner des Repos landseg (nur lesen)
//   max       int     optional  Deckel der Bestätigungs-Einheiten (Standard 48); Rest steht unter rest
//
// Konstanten: MODEL_MECH sonnet/medium (vergröbern, anwenden: feste Befehle), MODEL_KAND opus/medium (Listen der freien
//   Fassungen nach L14 und Kandidatenregel: stumme Fehler teuer, aber kein Bildurteil), MODEL_BEST opus/medium (Ja/Nein am
//   Bild für wenige Kandidaten; falsche Klasse geht in die Trainingsdaten, die Frage ist aber eng).
// Läufe: (erster Lauf folgt)

// [BLOCK 1] meta — erstes Statement, reines Literal
export const meta = {
  name: 'landseg-garten',
  description: 'H0 gröber machen, Gärten in T0 und H0 je Fassung: Kandidaten per Regel, Bestätigung am Bild, anwenden, prüfen',
  whenToUse: 'Teil 3 von landseg-garten (mit Nacharbeit landseg-sw-grob). args: { run, t0, h0, bericht, repo, max? }.',
  phases: [
    { title: 'Vergröbern', detail: 'H0 je Fassung kleine Flächen zusammenlegen, prüfen, Einigung messen', model: 'sonnet' },
    { title: 'Kandidaten', detail: 'Listen mit Garten, Kandidaten per Regel, Einheiten mit Bildern', model: 'opus' },
    { title: 'Bestätigen', detail: 'je Einheit ein Agent: Garten ja/nein/unklar am Bild', model: 'opus' },
    { title: 'Anwenden', detail: 'Garten eintragen, prüfen, zusammentragen, zählen', model: 'sonnet' },
  ],
}

// [BLOCK 2] args — normalisieren, Pflicht-Guard, Whitelist
const A = typeof args === 'string' ? JSON.parse(args) : (args || {})
const RUN = String(A.run || '')
if (!/^[\w-]{1,40}$/.test(RUN)) throw new Error('args.run fehlt oder ungültig (^[\\w-]{1,40}$)')
const PFAD = /^C:\/Users\/Phil\/Developement\/Victor\/[\w./ -]+$/
function pruefePfad(p, name) { const s = String(p || ''); if (!PFAD.test(s) || s.includes('..')) throw new Error(name + ' ungültig: ' + s); return s }
const T0 = pruefePfad(A.t0, 'args.t0')
const H0 = pruefePfad(A.h0, 'args.h0')
const BERICHT = pruefePfad(A.bericht, 'args.bericht')
const REPO = pruefePfad(A.repo, 'args.repo')
const MAX = Number.isInteger(A.max) && A.max > 0 ? A.max : 48

// [BLOCK 3] Konstanten — jede mit einem Satz Warum
const MODEL_MECH = 'sonnet', EFFORT_MECH = 'medium'   // feste Befehle (vergroebern, eingriff, pruefen, zusammentragen)
const MODEL_KAND = 'opus', EFFORT_KAND = 'medium'     // Listen nach L14 und Regel: Fehler hier wären stumm
const MODEL_BEST = 'opus', EFFORT_BEST = 'medium'     // enges Bildurteil je Kandidat
const MAX_KAND_JE_EINHEIT = 30  // kurzer Kontext je Agent (Entscheidung K7), Viertel bleiben ganz
const PY = 'C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe'
const ORDNER = { A: 'a-alles-frei', B: 'b-kategorien-frei', C: 'c-feste-liste' }
const BILD = { T0: { pfad: T0, art: 'Farb-Orthofoto (fein, rund 0,2 m je Bildpunkt)' }, H0: { pfad: H0, art: 'Schwarz-Weiß-Scan von 1968 (rund 0,45 m je Bildpunkt, gröber: nur klar erkennbare Gärten)' } }
const GARTEN = [
  'Was „Garten“ ist (Entscheidungen des Nutzers vom 18.11.2026, Mutterwunsch landseg-garten):',
  '- eine einzige Unterklasse „Garten“ unter Dauergrünland (feste Liste: Code 3.6; freie Listen A/B: ihre eigene Klasse Garten unter ihrer Dauergrünland-Klasse, Regel L14 im Skill);',
  '- dazu gehört jede krautige Grünfläche und jedes Beet im Haus- oder Hofgarten (auch Vor-, Obst- und Gemüsegarten), ob gepflegter Rasen oder nicht — Rasen ist kein Kennzeichen;',
  '- nur Haus- und Hofgärten: Parks, Friedhöfe, Sportrasen und Wiesen am Ortsrand bleiben Wiese/Weide;',
  '- Bäume, Sträucher und Hecken im Garten bleiben Gehölz (von oben sieht man die Krone);',
  '- auf dem Schwarz-Weiß-Bild H0 nur klar erkennbare Gärten am Haus; Unklares bleibt, wie es ist.',
].join('\n')

// [BLOCK 4] Warum
// Reihenfolge aus der Sache: H0 erst gröber (sonst würden Kandidaten auf Flächen bestätigt, die gleich verschwinden),
// dann Kandidaten über beide Bilder (Barriere: Einheiten entstehen erst aus der Regel), Bestätigung als pipeline über
// unabhängige Einheiten (jede schreibt nur ihr entscheid.json), Anwenden als Barriere (alle Entscheide einer Karte).
// Kein Verify-Agent: die Frage ist eng (ja/nein/unklar), `pruefen` prüft die Form; unklar ändert nichts.

// [BLOCK 5] Schemas
const ZAHL_GROB = {
  type: 'object', additionalProperties: false, required: ['fassung', 'vorher', 'nachher'],
  properties: { fassung: { type: 'string', enum: ['A', 'B', 'C'] }, vorher: { type: 'integer', description: 'Kernsegmente vorher' },
                nachher: { type: 'integer', description: 'Kernsegmente nachher' }, pruefen_ok: { type: 'boolean' }, offen: { type: 'integer', description: 'offene Einigungspaare nach dem Nachziehen' } },
}
const QUITTUNG_GROB = {
  type: 'object', additionalProperties: false, required: ['ok', 'fassungen', 'offen'],
  properties: { ok: { type: 'boolean', description: 'alle drei Fassungen vergröbert, pruefen ok, Sicherung vorhanden' },
                fassungen: { type: 'array', items: ZAHL_GROB }, sicherung: { type: 'string' }, offen: { type: 'array', items: { type: 'string' } } },
}
const EINHEIT = {
  type: 'object', additionalProperties: false, required: ['name', 'bild', 'fassung', 'tk', 'n', 'ordner'],
  properties: { name: { type: 'string', description: '<bild>-<F>-<tk>-<nr>' }, bild: { type: 'string', enum: ['T0', 'H0'] },
                fassung: { type: 'string', enum: ['A', 'B', 'C'] }, tk: { type: 'string' }, viertel: { type: 'array', items: { type: 'integer' } },
                n: { type: 'integer', minimum: 1, description: 'Kandidaten' }, ordner: { type: 'string', description: 'abs. Ordner mit auftrag.md, kandidaten.json, Bildern' } },
}
const QUITTUNG_KAND = {
  type: 'object', additionalProperties: false, required: ['ok', 'einheiten', 'offen'],
  properties: { ok: { type: 'boolean', description: 'Listen mit Garten geprüft, Kandidaten und Einheiten vollständig geschrieben' },
                listen: { type: 'array', items: { type: 'string' }, description: 'je Bild/Fassung: Liste und Garten-Klasse (Code)' },
                kandidaten: { type: 'integer' }, einheiten: { type: 'array', items: EINHEIT }, skript: { type: 'string' },
                offen: { type: 'array', items: { type: 'string' } } },
}
const QUITTUNG_BEST = {
  type: 'object', additionalProperties: false, required: ['ok', 'garten', 'nein', 'unklar'],
  properties: { ok: { type: 'boolean', description: 'entscheid.json geschrieben, jede Kandidaten-ID genau einmal' },
                garten: { type: 'integer' }, nein: { type: 'integer' }, unklar: { type: 'integer' }, grund: { type: 'string' } },
}
const ZAHL_ANW = {
  type: 'object', additionalProperties: false, required: ['bild', 'fassung', 'garten'],
  properties: { bild: { type: 'string', enum: ['T0', 'H0'] }, fassung: { type: 'string', enum: ['A', 'B', 'C'] },
                garten: { type: 'integer', description: 'Garten-Segmente im Kern' }, flaeche_pct: { type: 'number' },
                pruefen_ok: { type: 'boolean' }, offen: { type: 'integer', description: 'offene Einigungspaare' } },
}
const QUITTUNG_ANW = {
  type: 'object', additionalProperties: false, required: ['ok', 'karten', 'offen'],
  properties: { ok: { type: 'boolean', description: 'alle bestätigten Gärten eingetragen, pruefen 24× ok, zusammentragen 6×' },
                karten: { type: 'array', items: ZAHL_ANW }, bericht: { type: 'string' }, offen: { type: 'array', items: { type: 'string' } } },
}

// [BLOCK 6] Helfer — halten nie Nutzdaten
function hashLabel(s) { let h = 0; for (const c of s) h = (h * 31 + c.charCodeAt(0)) >>> 0; return h }
const BACKOFF_MS = [20000, 60000, 120000, 180000]
async function withRetry(label, fn) {
  for (let i = 0; ; i++) {
    try { return await fn() } catch (e) {
      const msg = String(e && e.message || e)
      if (/budget/i.test(msg) || !/rate|overload|429|529|timeout|ECONN|ENOTFOUND|schema/i.test(msg) || i >= BACKOFF_MS.length) throw e
      const wait = BACKOFF_MS[i] + (hashLabel(label) % 3000)
      log(label + ': ' + msg.slice(0, 80) + ' — Wiederholung ' + (i + 1) + '/' + BACKOFF_MS.length + ' in ' + Math.round(wait / 1000) + ' s')
      await new Promise(r => setTimeout(r, wait))
    }
  }
}
const sicher = (label, fn) => withRetry(label, fn).catch(e => { log(label + ': Fehler ' + String(e && e.message || e).slice(0, 120)); return null })
const GRENZEN = 'Kein Subagent, kein ToolSearch, keine Fenster, keine Dauerprozesse, nichts installieren, kein git. Python nur ' + PY + ' (Skripte als Datei, ausführen mit -B); Befehle `' + PY + ' -B -m landseg …` im Ordner ' + REPO + '. Am Repo und an den Originalbildern unter daten/luftbilder änderst du nichts; nichts löschen.'
const KOPF = 'Du bist ein Agent des Projekts landseg (Segmentierung von Luftbildern). Antworte auf Deutsch. Regeln: `' + REPO + '/.claude/skills/landseg-agent/SKILL.md` (lies sie zuerst), Befehle: `' + REPO + '/README.md`.'

// [BLOCK 7] Prompt-Builder
function grobPrompt() {
  return [
    KOPF,
    'Auftrag: Das fertige Ergebnis H0 (`' + H0 + '`, Schwarz-Weiß-Scan 1968) gröber machen (Nacharbeit von landseg-sw-grob), ohne neue Urteile.',
    'Vorgabe des Nutzers: auf alten SW-Bildern etwa 600 Flächen je Ausschnitt; kleine Flächen automatisch mit dem passenden Nachbarn zusammenlegen; Klassen und Urteile bleiben.',
    '',
    'Schritte (Logs unter `' + BERICHT + '/vergroebern/`):',
    '  1. `bildart --manifest ' + H0 + '/manifest.json` (Richtwert, Mindestfläche) ins Log.',
    '  2. Sicherung: je Fassungsordner (' + Object.values(ORDNER).join(', ') + ') die Teilkachelordner (labels.tif, segmente.json) und `zusammen/` nach `' + BERICHT + '/sicherung-vor-vergroebern/<ordner>/` kopieren.',
    '  3. Je Fassung `vergroebern --manifest ' + H0 + '/manifest.json --ordner ' + H0 + '/<ordner> --kategorien <Liste der Fassung im Ordner> --bearbeiter wf:vergroebern:' + RUN + ' --probe`, dann ohne `--probe`.',
    '  4. Je Teilkachel `pruefen` mit der Liste der Fassung (A/B: kategorien-a.json/-b.json, sonst Scheinfehler „ungültige Klasse“); je Fassung `zusammentragen` mit der vorhandenen zusammentragen.json; Kernsegmente vorher/nachher zählen.',
    '  5. `einigung messen --manifest ' + H0 + '/manifest.json`. Sind Paare offen, weil Flächen zusammengelegt wurden, übernimm den Beschluss des alten Paars mit `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-4/skripte/einigung_nachziehen.py` (wie dort im Bericht beschrieben, Bearbeiter wf:vergroebern:' + RUN + ') und miss erneut.',
    'Du schreibst nur unter `' + H0 + '/<Fassungsordner>` und `' + BERICHT + '`.',
    GRENZEN,
    'RÜCKGABE: ausschließlich das JSON nach Schema.',
  ].join('\n')
}
function kandPrompt() {
  return [
    KOPF,
    'Auftrag: Gärten in den fertigen Ergebnissen vorbereiten — T0 (`' + T0 + '`, ' + BILD.T0.art + ') und H0 (`' + H0 + '`, ' + BILD.H0.art + '), je Fassung A, B, C (Ordner ' + JSON.stringify(ORDNER) + '). Du änderst keine Karte und keine Klasse eines Segments.',
    '',
    GARTEN,
    '',
    'Schritte (Skripte als Datei unter `' + BERICHT + '/skripte/`):',
    '  1. Listen: Je Bild und Fassung muss die Kategorienliste der Fassung Garten führen. C: Klasse 3.6 wie in `' + REPO + '/kategorien.json` (nur sie ergänzen). A und B: eine Klasse „Garten“ unter der eigenen Dauergrünland-Klasse nach Regel L14 (Code nach dem Schema der Liste). Prüfen mit `pruefen` (für freie Listen `--frei`, siehe README) und `C:/Users/Phil/AppData/Local/Programs/Python/Python313/python.exe -I ' + REPO + '/tools/pruefe_kategorien.py`.',
    '  2. Kandidaten per Regel (ein Skript für beide Bilder): Segmente im Kern mit Klasse Dauergrünland (außer Garten), Acker-Unterklassen mit kleiner Fläche (Beete, unter etwa 1000 m²) oder offenem Boden, die im Siedlungsgebiet liegen (Merkmal `im_siedlung`, sonst Grenze an Gebäude oder Hof). Erkennbare Parks, Friedhöfe, Sportplätze nicht.',
    '  3. Einheiten: je Bild, Fassung und Teilkachel mit Kandidaten; höchstens ' + MAX_KAND_JE_EINHEIT + ' Kandidaten je Einheit, ein Viertel wird nie geteilt (Viertel nach Schwerpunkt im Kern). Je Einheit ein Ordner `' + BERICHT + '/einheiten/<bild>-<F>-<tk>-<nr>/` mit:',
    '     - `kandidaten.json` (je Kandidat: id, Klasse, Fläche m², Viertel, Mittelpunkt in Bildpunkten der Teilkachel),',
    '     - je Viertel zwei Bilder mit `zoom`: Umriss und Nummern aller Kandidaten des Viertels (`--ids`) und dasselbe ohne Umriss (`--roh`),',
    '     - `auftrag.md`: Ziel, die Garten-Regeln oben wörtlich, Bild (' + 'T0 Farbe / H0 SW' + '), Bildpfade, Ergebnisdatei `entscheid.json` im selben Ordner mit `{"<id>": {"garten": "ja"|"nein"|"unklar", "grund": "<ein Satz>"}}` für jede Kandidaten-ID, Hinweis: bei Zweifel eine Nahansicht mit `zoom --ids <id>`.',
    '  4. Gesamtzahl und Zahl je Bild/Fassung in `' + BERICHT + '/kandidaten.md`.',
    'Du schreibst nur in die Kategorienlisten der Fassungsordner und unter `' + BERICHT + '`.',
    GRENZEN,
    'RÜCKGABE: ausschließlich das JSON nach Schema — alle Einheiten mit Ordner.',
  ].join('\n')
}
function bestPrompt(e) {
  return [
    KOPF,
    'Auftrag: Garten-Kandidaten bestätigen — Bild ' + e.bild + ' (' + BILD[e.bild].art + '), Fassung ' + e.fassung + ', Teilkachel ' + e.tk + ', ' + e.n + ' Kandidaten.',
    'Lies `' + e.ordner + '/auftrag.md` und `' + e.ordner + '/kandidaten.json`, sieh dir die Bilder im Ordner an (je Viertel mit und ohne Umriss) und entscheide je Kandidat ja/nein/unklar mit Grund in einem Satz.',
    '',
    GARTEN,
    '',
    'Schreibe nur `' + e.ordner + '/entscheid.json`. Kontrolle vor der Rückgabe: jede Kandidaten-ID genau einmal, gültiges JSON.',
    GRENZEN,
    'RÜCKGABE: ausschließlich das JSON nach Schema.',
  ].join('\n')
}
function anwPrompt(einheiten) {
  return [
    KOPF,
    'Auftrag: Die bestätigten Gärten eintragen — T0 (`' + T0 + '`) und H0 (`' + H0 + '`), je Fassung A, B, C.',
    'Einheiten (je Ordner `entscheid.json` und `kandidaten.json`): `' + BERICHT + '/einheiten/` — ' + einheiten.length + ' mit Entscheid: ' + einheiten.map(e => e.name).join(', ') + '.',
    '',
    'Schritte (Skripte als Datei unter `' + BERICHT + '/skripte/`, Logs unter `' + BERICHT + '/anwenden/`):',
    '  1. Sicherung der Teilkachelordner (labels.tif, segmente.json) aller sechs Fassungen nach `' + BERICHT + '/sicherung-vor-garten/<bild>/<ordner>/`.',
    '  2. Nur „ja“ wird Garten (Klasse Garten der Liste der Fassung: C 3.6, A/B die eigene Garten-Klasse); „nein“ und „unklar“ bleiben unverändert. Eintragen mit `eingriff … stapel` (Schritte `klasse`), Bearbeiter wf:garten:' + RUN + '.',
    '  3. `pruefen` aller 24 Teilkacheln mit der Liste der Fassung; je Bild und Fassung `zusammentragen`; je Bild `einigung messen`.',
    '  4. Je Bild und Fassung: Garten-Segmente im Kern, Anteil an der Fläche, offene Einigungspaare. Tabelle samt „unklar“-Zahlen in `' + BERICHT + '/ergebnis.md`. Neue offene Einigungspaare nur zählen und nennen, nicht selbst klären.',
    'Du schreibst nur in die Fassungsordner von T0 und H0 und unter `' + BERICHT + '`.',
    GRENZEN,
    'RÜCKGABE: ausschließlich das JSON nach Schema.',
  ].join('\n')
}

// [BLOCK 8] Leerlauf-Return
const leer = { run: RUN, vergroebert: null, einheiten: 0, bestaetigt: { garten: 0, nein: 0, unklar: 0 }, karten: [], rest: [], ohne_rueckmeldung: [], offen: [] }

// [BLOCK 9] Ablauf
phase('Vergröbern')
const grob = await sicher('vergroebern', () => agent(grobPrompt(), {
  label: 'vergroebern:H0', phase: 'Vergröbern', model: MODEL_MECH, effort: EFFORT_MECH, schema: QUITTUNG_GROB, // feste Befehle
}))
if (!grob) return { ...leer, ohne_rueckmeldung: ['vergroebern'] }
if (!grob.ok) return { ...leer, vergroebert: grob, offen: ['vergroebern nicht ok'].concat(grob.offen || []) }
log('Vergröbert: ' + grob.fassungen.map(f => f.fassung + ' ' + f.vorher + '→' + f.nachher + (f.offen ? ' offen ' + f.offen : '')).join(', '))

phase('Kandidaten')
const kand = await sicher('kandidaten', () => agent(kandPrompt(), {
  label: 'kandidaten', phase: 'Kandidaten', model: MODEL_KAND, effort: EFFORT_KAND, schema: QUITTUNG_KAND, // Regel und Listen
}))
if (!kand) return { ...leer, vergroebert: grob.fassungen, ohne_rueckmeldung: ['kandidaten'] }
if (!kand.ok) return { ...leer, vergroebert: grob.fassungen, offen: ['kandidaten nicht ok'].concat(kand.offen || []) }
const alle = kand.einheiten.filter(e => PFAD.test(e.ordner) && e.ordner.startsWith(BERICHT + '/einheiten/'))
if (alle.length !== kand.einheiten.length) log('Einheiten mit ungültigem Ordner verworfen: ' + (kand.einheiten.length - alle.length))
const lauf = alle.slice(0, MAX), rest = alle.slice(MAX).map(e => e.name)
log('Kandidaten ' + (kand.kandidaten || 0) + ', Einheiten ' + alle.length + (rest.length ? ', Rest ' + rest.length : ''))

const best = await pipeline(lauf, (e) => sicher('bestaetigen:' + e.name, () => agent(bestPrompt(e), {
  label: 'bestaetigen:' + e.name, phase: 'Bestätigen', model: MODEL_BEST, effort: EFFORT_BEST, schema: QUITTUNG_BEST, // enges Bildurteil
})).then(q => ({ e, q })))
const fertig = best.filter(r => r && r.q && r.q.ok)
const ohne = best.filter(r => !r || !r.q).map(r => r ? r.e.name : '?')
const nichtOk = best.filter(r => r && r.q && !r.q.ok).map(r => r.e.name + ': ' + (r.q.grund || ''))
const summe = fertig.reduce((s, r) => ({ garten: s.garten + r.q.garten, nein: s.nein + r.q.nein, unklar: s.unklar + r.q.unklar }), { garten: 0, nein: 0, unklar: 0 })
log('Bestätigt ' + fertig.length + '/' + lauf.length + ': Garten ' + summe.garten + ', nein ' + summe.nein + ', unklar ' + summe.unklar)

phase('Anwenden')
const anw = fertig.length ? await sicher('anwenden', () => agent(anwPrompt(fertig.map(r => r.e)), {
  label: 'anwenden', phase: 'Anwenden', model: MODEL_MECH, effort: EFFORT_MECH, schema: QUITTUNG_ANW, // feste Befehle
})) : null

// [BLOCK 10] Return — Statistik und Pfade
return {
  run: RUN,
  vergroebert: grob.fassungen,
  einheiten: alle.length,
  bestaetigt: summe,
  karten: anw ? anw.karten : [],
  bericht: anw ? anw.bericht || BERICHT + '/ergebnis.md' : null,
  rest,
  nicht_ok: nichtOk,
  ohne_rueckmeldung: ohne.concat(fertig.length && !anw ? ['anwenden'] : []),
  offen: (grob.offen || []).concat(kand.offen || [], anw ? (anw.ok ? [] : ['anwenden nicht ok']).concat(anw.offen || []) : []),
}

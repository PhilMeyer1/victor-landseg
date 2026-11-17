// landseg-urteile-t0 — Teil 2 von landseg-test-t0 (Wunsch-Datei
// C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-test-t0-2.md): Urteile im Verbund je Viertel
// für die Fassungen A (feste Liste) und B (Kategorien frei), freie Abgabe C je Teilkachel, Zweitagent
// (Gegenprobe) auf den vier Vierteln von r0c0, danach Vereinheitlichung der freien Klassen von B.
// Die Aufträge (auftrag.md je Einheit) hat Teil 1 geschrieben; dieses Skript reicht nur Pfade weiter.
//
// Vorgabe des Nutzers (2026-11-17): je Teilkachel vier Agents, je Viertel einer; jeder sieht ZUERST die
// ganze Teilkachel und arbeitet dann die Segmente seines Viertels einzeln nach Liste ab. Dafür zeichnet
// ein Vorbereitungs-Agent je Teilkachel ein Gesamtbild (Grenzen, Nummern, Viertelrahmen v1–v4).
//
// args (JSON-Objekt):
//   run       string    Pflicht   Lauf-Kennung ^[\w-]{1,40}$, z. B. "20261117k"
//   einheiten object[]  Pflicht   je Einheit {art: a|b|c|z, tk: rXcY, v: 0-4, n: Segmente, auftrag: abs. Pfad, ergebnis: abs. Ordner}
//   vereinheitlichen string Pflicht abs. Pfad des Auftrags zum Vereinheitlichen der Klassen von B
//   ganz_dir  string    Pflicht   abs. Ordner für die Gesamtbilder (je Teilkachel ein Unterordner)
//   t0_dir    string    Pflicht   abs. Ordner kern500 (manifest.json, vorstufe/, teilkacheln/)
//   max       int       optional  Deckel in Einheiten; 0/fehlend = alle
//
// Konstanten: MODEL_URTEIL=opus/high (Urteil am Bild — die teure Fehlerklasse ist eine falsche Klasse
//             oder Grenze, die in die Trainingsdaten geht), MODEL_MECH=sonnet/low (Gesamtbilder zeichnen),
//             MODEL_VEREIN=sonnet/medium (Namen zusammenführen, laut Klärung kein Urteil am Bild).
// Läufe: (erster Lauf folgt)

// [BLOCK 1] meta — erstes Statement, reines Literal
export const meta = {
  name: 'landseg-urteile-t0',
  description: 'Urteile im Verbund je Viertel für Testausschnitt T0 (Fassungen A, B), freie Abgabe C, Gegenprobe, Vereinheitlichung der Klassen von B',
  whenToUse: 'Teil 2 eines landseg-Tests: Viertel-Aufträge aus Teil 1 abarbeiten lassen. args: { run, einheiten: [{art, tk, v, n, auftrag, ergebnis}], vereinheitlichen: Pfad, ganz_dir: Ordner, t0_dir: Ordner, max? }.',
  phases: [
    { title: 'Gesamtbilder', detail: 'je Teilkachel ein Bild mit Grenzen, Nummern und Viertelrahmen', model: 'sonnet' },
    { title: 'Urteile', detail: 'je Viertel (A, B, Gegenprobe) bzw. Teilkachel (C) ein Agent', model: 'opus' },
    { title: 'Vereinheitlichen', detail: 'freie Klassen von B zu einer Liste', model: 'sonnet' },
  ],
}

// [BLOCK 2] args — normalisieren, Pflicht-Guard, Whitelist
const A = typeof args === 'string' ? JSON.parse(args) : (args || {})
const RUN = String(A.run || '')
if (!/^[\w-]{1,40}$/.test(RUN)) throw new Error('args.run fehlt oder ungültig (^[\\w-]{1,40}$)')
const PFAD = /^C:\/Users\/Phil\/Developement\/Victor\/[\w./ -]+$/
function pruefePfad(p, name) { const s = String(p || ''); if (!PFAD.test(s) || s.includes('..')) throw new Error(name + ' ungültig: ' + s); return s }
const GANZ_DIR = pruefePfad(A.ganz_dir, 'args.ganz_dir')
const T0_DIR = pruefePfad(A.t0_dir, 'args.t0_dir')
const VEREIN = pruefePfad(A.vereinheitlichen, 'args.vereinheitlichen')
const E_ARG = Array.isArray(A.einheiten) ? A.einheiten : []
if (!E_ARG.length) throw new Error('args.einheiten fehlt oder leer')
const EINHEITEN = E_ARG.map((e, i) => {
  const art = String(e.art), tk = String(e.tk), v = Number(e.v), n = Number(e.n) || 0
  if (!['a', 'b', 'c', 'z'].includes(art)) throw new Error('einheiten[' + i + '].art ungültig')
  if (!/^r\dc\d$/.test(tk)) throw new Error('einheiten[' + i + '].tk ungültig')
  if (!(Number.isInteger(v) && v >= 0 && v <= 4)) throw new Error('einheiten[' + i + '].v ungültig')
  return { art, tk, v, n, auftrag: pruefePfad(e.auftrag, 'einheiten[' + i + '].auftrag'), ergebnis: pruefePfad(e.ergebnis, 'einheiten[' + i + '].ergebnis') }
})
const LIMIT = Number.isInteger(A.max) && A.max > 0 ? A.max : 0

// [BLOCK 3] Konstanten — jede mit einem Satz Warum
const MAX_AGENTS = 18           // 1 Gesamtbilder + 13 Urteile (je Teilkachel) + 1 Vereinheitlichen = 15; Nutzer 2026-11-17 „je Fassung 4, Gegenprobe 1"
const MODEL_URTEIL = 'opus', EFFORT_URTEIL = 'high'      // Urteil am Bild, Segment für Segment: falsche Klasse/Grenze geht in die Trainingsdaten
const MODEL_MECH = 'sonnet', EFFORT_MECH = 'low'         // Gesamtbilder zeichnen: mechanisch nach festen Angaben
const MODEL_VEREIN = 'sonnet', EFFORT_VEREIN = 'medium'  // Namen zusammenführen nach Liste; Klärung legte Sonnet fest
const PY = 'C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe'
const ART_NAME = { a: 'Fassung A (feste Liste)', b: 'Fassung B (Kategorien frei)', c: 'Fassung C (alles frei)', z: 'Gegenprobe (Zweitagent, Fassung A)' }

// [BLOCK 4] Warum
// Ein Agent je Fassung und Teilkachel (Richtigstellung des Nutzers 2026-11-17, ersetzt „je Viertel"): er sieht
// erst ganz T0, dann seine Teilkachel, und arbeitet ihre vier Viertel-Aufträge nacheinander ab; nichts wird geteilt.
// Lauf wf_e81273d7-c88 (je Viertel) wurde nach 1 fertigen Agent (Gesamtbilder) gestoppt; dessen Ergebnis kommt beim Resume aus dem Cache.
// Die dichtesten Einheiten starten zuerst, damit sie nicht am Ende allein laufen (Concurrency ≤ 16).
// Gesamtbilder vor allen Urteilen: jeder Agent soll zuerst die ganze Teilkachel sehen; fehlt ein Bild
// (Vorbereitung ausgefallen), weicht der Agent auf das rohe Teilkachelbild aus und vermerkt das.
// Vereinheitlichung nach allen Urteilen: braucht alle 16 Viertel-Abgaben von B (sachliche Barriere).
// Keine Verify-Stufe im Skript: die Gegenprobe (art z) IST die Zweitmeinung auf r0c0; Vergleich in Teil 3/5.

// [BLOCK 5] Schemas
const QUITTUNG_GANZ = {
  type: 'object', additionalProperties: false, required: ['bilder'],
  properties: { bilder: { type: 'array', items: {
    type: 'object', additionalProperties: false, required: ['tk', 'ok'],
    properties: {
      tk: { type: 'string', enum: ['r0c0', 'r0c1', 'r1c0', 'r1c1'] },
      ok: { type: 'boolean' },
      nummern: { type: 'string', description: 'Absoluter Pfad von ganz_nummern.jpg' },
      roh: { type: 'string', description: 'Absoluter Pfad von ganz_roh.jpg' },
      grund: { type: 'string', description: 'Nur bei ok=false' },
    } } } },
}
const QUITTUNG_URTEIL = {
  type: 'object', additionalProperties: false, required: ['t0_gesehen', 'teile'],
  properties: {
    t0_gesehen: { type: 'boolean', description: 'Du hast zuerst T0.png und das Bild deiner Teilkachel angesehen' },
    teile: { type: 'array', items: {
      type: 'object', additionalProperties: false, required: ['v', 'ok', 'kontrolle_ok', 'segmente'],
      properties: {
        v: { type: 'integer', minimum: 0, maximum: 4, description: 'Viertelnummer des Auftrags, bei C 0' },
        ok: { type: 'boolean', description: 'Ergebnis vollständig nach Auftrag geschrieben' },
        kontrolle_ok: { type: 'boolean', description: 'Die Kontrolle aus dem Auftrag endete mit ok' },
        segmente: { type: 'integer', minimum: 0, description: 'Zahl der eingetragenen Segmente' },
        nicht_sauber: { type: 'integer', minimum: 0 },
        unsicher: { type: 'integer', minimum: 0, description: 'Zahl mit sicher: false' },
        pfad: { type: 'string', description: 'Absoluter Pfad der Hauptdatei (urteil.json bzw. labels.tif)' },
        grund: { type: 'string', description: 'Nur bei ok=false oder kontrolle_ok=false' },
      } } },
  },
}
const QUITTUNG_VEREIN = {
  type: 'object', additionalProperties: false, required: ['ok'],
  properties: { ok: { type: 'boolean' }, pfad: { type: 'string' }, kurz: { type: 'string' }, grund: { type: 'string' } },
}

// [BLOCK 6] Helfer — halten nie Nutzdaten
function hashLabel(s) { let h = 0; for (const c of s) h = (h * 31 + c.charCodeAt(0)) >>> 0; return h }
const BACKOFF_MS = [8000, 25000, 90000, 180000]
async function withRetry(label, fn) {
  for (let i = 0; ; i++) {
    try { return await fn() } catch (e) {
      const msg = String(e && e.message || e)
      if (/budget/i.test(msg) || !/rate|overload|429|529|timeout|ECONN|schema/i.test(msg) || i >= BACKOFF_MS.length) throw e
      const wait = BACKOFF_MS[i] + (hashLabel(label) % 3000)
      log(label + ': ' + msg.slice(0, 80) + ' — Wiederholung ' + (i + 1) + '/' + BACKOFF_MS.length + ' in ' + Math.round(wait / 1000) + ' s')
      await new Promise(r => setTimeout(r, wait))
    }
  }
}
function labelOf(e) { return e.art + ':' + e.tk + (e.v ? '-v' + e.v : '') }

// [BLOCK 7] Prompt-Builder
function ganzPrompt(tks) {
  return [
    'Du zeichnest für ' + tks.length + ' Teilkachel(n) je ein Gesamtbild als Überblick für die Agents, die danach die Viertel beurteilen.',
    'Stand: Ausschnitt in ' + T0_DIR + ' (manifest.json: Eintrag je Teilkachel unter "teilkacheln" mit "bild" und "kern_im_bild"; Label-Karte ' + T0_DIR + '/vorstufe/<tk>/labels.tif, segmente.json daneben).',
    'Python nur ' + PY + ' (tifffile, numpy, Pillow, scipy vorhanden); Skript als Datei unter ' + GANZ_DIR + ', ausführen mit -I. Du schreibst NUR unter ' + GANZ_DIR + '. Eingaben nur lesen.',
    '',
    'Teilkacheln: ' + tks.join(', '),
    'Je Teilkachel zwei Bilder in ' + GANZ_DIR + '/<tk>/ (JPEG, Qualität 90, 2fach vergrößert mit nearest, also 1256 × 1256 bei 628 px):',
    '  - ganz_roh.jpg: das Teilkachelbild unverändert.',
    '  - ganz_nummern.jpg: Segmentgrenzen gelb (1 px im Original), Kern weiß umrandet, Kontextrand leicht abgedunkelt,',
    '    die vier Viertel des Kerns cyan umrandet und groß beschriftet "v1" (oben links), "v2" (oben rechts), "v3" (unten links), "v4" (unten rechts);',
    '    Viertel = Kern (kern_im_bild) halbiert in x und y. Jedes Segment im Kern mit seiner Nummer = ID mod 100000 in Weiß mit schwarzem Rand,',
    '    an einem Punkt sicher im Segment (z. B. Maximum der Distanztransformation), Segmente unter 40 px ohne Nummer.',
    'Dazu ' + GANZ_DIR + '/<tk>/ganz.json mit {"tk", "faktor": 2, "kern_im_bild", "viertel": {"v1": [x0,y0,x1,y1], …}} in Bildpunkten der Teilkachel.',
    'Sieh dir jedes ganz_nummern.jpg einmal an (Read) und prüfe, dass Nummern lesbar sind und die Viertel stimmen.',
    '',
    'Höchstens 15 Werkzeugaufrufe. Kein Subagent, kein ToolSearch, nichts installieren, keine Fenster, keine Dauerprozesse.',
    'RÜCKGABE: ausschließlich {"bilder": [...]} nach Schema — ein Eintrag je Teilkachel, auch für gescheiterte (ok=false + grund).',
  ].join('\n')
}
// Ein Agent je Teilkachel (Vorgabe 2026-11-17, zweite Fassung): Er bekommt die Aufträge seiner Teilkachel
// (bei A, B und Gegenprobe die vier Viertel-Aufträge, bei C einen) und arbeitet sie nacheinander ab.
function urteilPrompt(g, ganz) {
  const tk = g.tk, viertel = g.art !== 'c'
  const gb = ganz[tk]
  const bildTk = gb && gb.ok
    ? gb.nummern + ' (Grenzen, Nummern, Viertel cyan v1–v4) und ' + gb.roh + ' (unverändert); Lage der Viertel in ' + GANZ_DIR + '/' + tk + '/ganz.json'
    : T0_DIR + '/teilkacheln/' + tk + '.png (Gesamtbild mit Nummern fehlt — vermerke das unter "nicht_geprueft")'
  const summe = g.teile.reduce((s, e) => s + e.n, 0)
  return [
    'Du beurteilst als einziger Agent ' + ART_NAME[g.art] + ' für Teilkachel ' + tk + (viertel ? ' (' + summe + ' Segmente in vier Vierteln)' : '') + ' des Testausschnitts T0.',
    'Du schreibst nur in die Ergebnisordner deiner Aufträge (unten). Alle Eingaben nur lesen; die Label-Karte der Vorstufe änderst du nicht.',
    '',
    'Vorgabe des Nutzers, geht den Aufträgen voran:',
    '  1. Sieh ZUERST den ganzen Ausschnitt T0 an (1000 × 1000 px, vier Teilkacheln r0c0 oben links, r0c1 oben rechts, r1c0 unten links, r1c1 unten rechts): ' + T0_DIR + '/T0.png',
    '  2. Dann deine ganze Teilkachel ' + tk + ': ' + bildTk + '.',
    viertel
      ? '  3. Dann arbeitest du die Segmente deiner Teilkachel nacheinander ab: Auftrag v1, dann v2, v3, v4 — jeden Auftrag ganz lesen, jedes Segment seiner Liste einzeln urteilen (im Zusammenhang mit Nachbarn, Teilkachel und T0), sein urteil.json schreiben und seine Kontrolle ausführen, bevor du den nächsten beginnst. Die Viertelbilder sind deine Nahansichten.'
      : '  3. Dann segmentierst und klassifizierst du die Teilkachel nach deinem eigenen Vorgehen, wie im Auftrag beschrieben.',
    '  4. Trage T0.png und das Bild der Teilkachel ' + (viertel ? 'in JEDEM urteil.json unter "bilder_angesehen" → "uebersicht" ein, vor den Viertelbildern.' : 'in arbeitsweise.md ein.'),
    '',
    'Aufträge (je einer maßgeblich für sein Ergebnis; Ergebnisordner steht im Auftrag):',
    ...g.teile.map(e => '  - ' + (viertel ? 'v' + e.v + ' (' + e.n + ' Segmente): ' : '') + e.auftrag + '  → ' + e.ergebnis),
    viertel ? 'Hinweis: Wo ein Auftrag andere Agents für die übrigen Viertel nennt, bist das hier du selbst, nacheinander; Segmente an der Viertelgrenze urteilst du nur in dem Auftrag, in dessen Liste sie stehen.' : '',
    '',
    'Im Zweifel `sicher: false` und eine Notiz unter "offen": eine ehrlich als unsicher markierte Fläche wird nachgeprüft, eine falsch als sicher markierte geht unbemerkt in die Trainingsdaten.',
    'Arbeite jedes Segment ab; überfliege nichts gegen Ende. Wird dir Zeit oder Platz knapp, schreib ehrlich unter "nicht_geprueft", was fehlt, statt zu raten.',
    '',
    'Kein Subagent, kein ToolSearch, keine Fenster, keine Dauerprozesse, nichts installieren, kein git.',
    'RÜCKGABE: ausschließlich das JSON nach Schema — unter "teile" ein Eintrag je Auftrag (v = Viertelnummer, bei C 0), nie den Inhalt deiner Dateien.',
  ].filter(z => z !== '').join('\n')
}
function vereinPrompt() {
  return [
    'Du arbeitest einen fertigen Auftrag ab: freie Klassen der 16 Viertel von Fassung B zu einer gestuften Liste vereinheitlichen.',
    'Auftrag (lies ihn ganz, er ist maßgeblich): ' + VEREIN,
    'Du schreibst nur in den Ergebnisordner des Auftrags. Alle Eingaben nur lesen.',
    'Fehlt eine Viertel-Abgabe, vereinheitliche die vorhandenen und nenne die fehlenden in deiner Rückgabe unter grund.',
    'Kein Subagent, kein ToolSearch, keine Fenster, kein git.',
    'RÜCKGABE: ausschließlich {"ok", "pfad", "kurz", "grund"?} nach Schema — "kurz" = die Rückgabe-Angaben des Auftrags in einer Zeile.',
  ].join('\n')
}

// [BLOCK 8] Katalog, Plan-Log, Deckel + Rest-Liste
const sortiert = EINHEITEN.slice().sort((x, y) => (y.n - x.n) || (labelOf(x) < labelOf(y) ? -1 : 1))   // dichteste zuerst
const units = LIMIT ? sortiert.slice(0, LIMIT) : sortiert
const rest = sortiert.slice(units.length).map(labelOf)
const TKS = Array.from(new Set(units.map(e => e.tk))).sort()
const RETURN_EMPTY = { run: RUN, einheiten: 0, ok: 0, kontrolle_fehlt: [], ohne_gesamtbild: [], ohne_rueckmeldung: [], rest, gesamtbilder: {}, vereinheitlichung: null }
if (!units.length) { log('Keine Einheit zu bearbeiten.'); return RETURN_EMPTY }
// Gruppen: je Fassung und Teilkachel ein Agent; Viertel darin aufsteigend (v1 … v4).
const gruppenMap = {}
for (const e of units) { const k = e.art + ':' + e.tk; (gruppenMap[k] = gruppenMap[k] || { art: e.art, tk: e.tk, teile: [] }).teile.push(e) }
const C_GEWICHT = 300   // freie Segmentierung C ist so aufwendig wie eine dichte Teilkachel: früh starten
const gruppen = Object.keys(gruppenMap).sort().map(k => gruppenMap[k])
for (const g of gruppen) g.teile.sort((x, y) => x.v - y.v)
const last = g => g.art === 'c' ? C_GEWICHT : g.teile.reduce((s, e) => s + e.n, 0)
gruppen.sort((x, y) => (last(y) - last(x)) || ((x.art + x.tk) < (y.art + y.tk) ? -1 : 1))   // dichteste zuerst
const glabel = g => g.art + ':' + g.tk
const geplant = 1 + gruppen.length + 1
if (geplant > MAX_AGENTS) throw new Error(geplant + ' Agents geplant > MAX_AGENTS=' + MAX_AGENTS + ' — args.max setzen')
const zaehl = k => gruppen.filter(g => g.art === k).length
log(units.length + ' Aufträge in ' + gruppen.length + ' Gruppen (A ' + zaehl('a') + ', B ' + zaehl('b') + ', C ' + zaehl('c') + ', Gegenprobe ' + zaehl('z') + ') → ' + geplant
    + ' Agents: 1 Gesamtbilder (' + MODEL_MECH + '), ' + gruppen.length + ' Urteile je Teilkachel (' + MODEL_URTEIL + '/' + EFFORT_URTEIL + '), 1 Vereinheitlichen (' + MODEL_VEREIN + ').')
if (rest.length) log('Deckel max=' + LIMIT + ': ' + rest.length + ' Einheiten bleiben liegen — nicht verloren, im return unter "rest".')

// [BLOCK 9] Hauptablauf
phase('Gesamtbilder')
const qg = await withRetry('ganz', () => agent(ganzPrompt(TKS), {
  label: 'gesamtbilder:' + TKS.join('+'), phase: 'Gesamtbilder', model: MODEL_MECH, effort: EFFORT_MECH, schema: QUITTUNG_GANZ }))   // mechanisch
const ganz = {}
for (const b of ((qg && qg.bilder) || [])) if (TKS.includes(b.tk)) ganz[b.tk] = { ok: !!b.ok && !!b.nummern && !!b.roh, nummern: b.nummern, roh: b.roh }
const ohneGanz = TKS.filter(t => !(ganz[t] && ganz[t].ok))
log((TKS.length - ohneGanz.length) + '/' + TKS.length + ' Gesamtbilder fertig' + (ohneGanz.length ? ' — ohne: ' + ohneGanz.join(', ') + ' (Agents nehmen das rohe Teilkachelbild)' : ''))

let fertig = 0
const ergebnisse = await pipeline(
  gruppen,
  (g) => withRetry(glabel(g), () => agent(urteilPrompt(g, ganz), {
    label: 'urteil:' + glabel(g), phase: 'Urteile', model: MODEL_URTEIL, effort: EFFORT_URTEIL, schema: QUITTUNG_URTEIL })),   // Urteil am Bild
  async (q, g) => {
    fertig += 1
    const zeilen = []
    for (const e of g.teile) {
      const t = q && Array.isArray(q.teile) ? q.teile.find(x => x.v === e.v) : null
      if (t) zeilen.push({ label: labelOf(e), art: e.art, ok: !!t.ok, kontrolle_ok: !!t.kontrolle_ok, gesamt: !!q.t0_gesehen, segmente: t.segmente || 0,
                           nicht_sauber: t.nicht_sauber || 0, unsicher: t.unsicher || 0, soll: e.n })
    }
    log(fertig + '/' + gruppen.length + ' Agents zurück (' + glabel(g) + (q ? ': ' + zeilen.filter(r => r.ok && r.kontrolle_ok).length + '/' + g.teile.length + ' Aufträge ok, '
        + zeilen.reduce((s, r) => s + r.segmente, 0) + ' Segmente' : ': ohne Rückmeldung') + ')')
    return zeilen
  })

const zurueck = ergebnisse.filter(Boolean).flat()
const gemeldet = new Set(zurueck.map(r => r.label))
const ohneRueck = units.map(labelOf).filter(l => !gemeldet.has(l))
const kontrolleFehlt = zurueck.filter(r => !(r.ok && r.kontrolle_ok)).map(r => r.label)
const ohneGesamt = zurueck.filter(r => !r.gesamt).map(r => r.label)
const zuWenig = zurueck.filter(r => (r.art === 'a' || r.art === 'b' || r.art === 'z') && r.soll && r.segmente !== r.soll).map(r => r.label + ' ' + r.segmente + '/' + r.soll)
log(zurueck.length + '/' + units.length + ' zurück; ' + kontrolleFehlt.length + ' ohne bestandene Kontrolle' + (kontrolleFehlt.length ? ' (' + kontrolleFehlt.join(', ') + ')' : '')
    + '; ' + ohneRueck.length + ' ohne Rückmeldung' + (ohneRueck.length ? ' — erneut per resumeFromRunId' : '') + (zuWenig.length ? '; Segmentzahl abweichend: ' + zuWenig.join(', ') : ''))

let verein = null
if (units.some(e => e.art === 'b')) {
  phase('Vereinheitlichen')
  verein = await withRetry('vereinheitlichen', () => agent(vereinPrompt(), {
    label: 'vereinheitlichen:b', phase: 'Vereinheitlichen', model: MODEL_VEREIN, effort: EFFORT_VEREIN, schema: QUITTUNG_VEREIN }))   // Zusammenführen nach Liste
  if (!verein || !verein.ok) log('Vereinheitlichung von B nicht fertig (' + (verein && verein.grund || 'ohne Rückmeldung') + ') — in Teil 3 nachholen.')
}

// [BLOCK 10] return — nur Statistik, Pfade, Kennungen
const summe = (k, f) => zurueck.filter(r => r.art === k).reduce((s, r) => s + r[f], 0)
return {
  run: RUN,
  einheiten: units.length,
  ok: zurueck.length - kontrolleFehlt.length,
  segmente: { a: summe('a', 'segmente'), b: summe('b', 'segmente'), z: summe('z', 'segmente'), c: summe('c', 'segmente') },
  nicht_sauber: { a: summe('a', 'nicht_sauber'), b: summe('b', 'nicht_sauber'), z: summe('z', 'nicht_sauber') },
  unsicher: { a: summe('a', 'unsicher'), b: summe('b', 'unsicher'), z: summe('z', 'unsicher'), c: summe('c', 'unsicher') },
  kontrolle_fehlt: kontrolleFehlt,
  segmentzahl_abweichend: zuWenig,
  ohne_gesamtbild: ohneGesamt,
  ohne_rueckmeldung: ohneRueck,
  rest,
  gesamtbilder: Object.fromEntries(TKS.map(t => [t, ganz[t] && ganz[t].ok ? ganz[t].nummern : null])),
  vereinheitlichung: verein ? { ok: !!verein.ok, pfad: verein.pfad || null, kurz: verein.kurz || null } : null,
}

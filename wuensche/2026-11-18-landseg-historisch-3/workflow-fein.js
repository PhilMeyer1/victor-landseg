// landseg-h0 — Teil 3 von landseg-historisch (Wunsch-Datei
// C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3.md, Mutterwunsch …/2026-11-18-landseg-historisch.md):
// Ausschnitt H0 (Scan 1968, Schwarz-Weiß) genauso wie T0: Urteile der Fassungen C (feste Liste, je Viertel),
// B (Kategorien frei, je Viertel), A (alles frei, je Teilkachel), Gegenprobe (C auf r0c0), Vereinheitlichung von B,
// Zusammenführen zum Aufbau der T0-Übergabe, Nahtklärung, Einigung an den Übergängen (höchstens 3 Runden).
// Die Aufträge der Urteile hat Teil 2 geschrieben (auftraege.json); dieses Skript reicht nur Pfade weiter.
//
// Vorgaben des Nutzers: je Fassung 4 Agents, ein Agent je Teilkachel, sieht zuerst den ganzen Ausschnitt, dann seine
// Teilkachel, arbeitet die Viertel nacheinander ab (2026-11-17); Einigung an den Übergängen als fester Schritt, nur
// Klassen (2026-11-18); nur Scan 1968, Fenster H0, Durchsicht erst am Ergebnis (F1–F3 landseg-historisch).
//
// args (JSON-Objekt):
//   run        string    Pflicht   Lauf-Kennung ^[\w-]{1,40}$
//   einheiten  object[]  Pflicht   aus auftraege.json: {art: a|b|c|z, tk, v, n, auftrag, ergebnis}; a = Alles frei (je Teilkachel, v 0),
//                                  b = Kategorien frei, c = Feste Liste (je Viertel), z = Gegenprobe (C auf r0c0, je Viertel)
//   plan       string    Pflicht   abs. Pfad von auftraege.json (Gesamtbilder, Vereinheitlichungs-Auftrag)
//   h0         string    Pflicht   abs. Ordner des Ausschnitts (manifest.json, H0.png, Fassungsordner)
//   bericht    string    Pflicht   abs. Berichtsordner dieses Teils (Skripte, Logs, Einigungs-Aufträge und -Abgaben)
//   repo       string    Pflicht   abs. Ordner des Repos landseg (Vorlagen, Befehle; nur lesen)
//   max_buendel int      optional  Deckel je Einigungsrunde (Standard 30); was liegen bleibt, steht unter rest
//
// Konstanten: MODEL_URTEIL=opus/high (Urteil am Bild; falsche Klasse geht in die Trainingsdaten — teure Fehlerklasse),
//             MODEL_VEREIN=sonnet/medium (Namen zusammenführen nach Liste, wie T0),
//             MODEL_BAU=opus/medium (Zusammenführen: T0-Skripte auf H0 übertragen, Fassungsbuchstaben vertauscht — Fehler
//             hier wären stumm, darum das starke Modell, aber ohne Bildurteil), MODEL_MECH=sonnet/medium (anwenden, messen,
//             finden: feste Befehle).
// Läufe: (erster Lauf folgt)

// [BLOCK 1] meta — erstes Statement, reines Literal
export const meta = {
  name: 'landseg-h0',
  description: 'Historischer Ausschnitt H0: Urteile A, B, C, Gegenprobe, Vereinheitlichung, Zusammenführen, Nähte, Einigung an den Übergängen',
  whenToUse: 'Teil 3 von landseg-historisch: Aufträge aus Teil 2 bis zur geeinigten Karte je Fassung abarbeiten. args: { run, einheiten, plan, h0, bericht, repo, max_buendel? }.',
  phases: [
    { title: 'Urteile', detail: 'je Fassung und Teilkachel ein Agent, Gegenprobe ein Agent', model: 'opus' },
    { title: 'Nachholen', detail: 'Viertel ohne bestandene Kontrolle einzeln neu', model: 'opus' },
    { title: 'Vereinheitlichen', detail: 'freie Klassen von B zu einer Liste', model: 'sonnet' },
    { title: 'Zusammenführen', detail: 'Aufbau wie T0-Übergabe, Kategorienlisten, zusammentragen, Nähte, Bündel finden', model: 'opus' },
    { title: 'Nähte', detail: 'je Fassung mit Nahtverstößen ein Agent nach vorlagen/naht.md', model: 'opus' },
    { title: 'Einigung', detail: 'je Bündel ein Agent, höchstens 3 Runden', model: 'opus' },
    { title: 'Anwenden', detail: 'Abgaben umsetzen, messen, nächste Runde finden', model: 'sonnet' },
  ],
}

// [BLOCK 2] args — normalisieren, Pflicht-Guard, Whitelist
const A = typeof args === 'string' ? JSON.parse(args) : (args || {})
const RUN = String(A.run || '')
if (!/^[\w-]{1,40}$/.test(RUN)) throw new Error('args.run fehlt oder ungültig (^[\\w-]{1,40}$)')
const PFAD = /^C:\/Users\/Phil\/Developement\/Victor\/[\w./ -]+$/
function pruefePfad(p, name) { const s = String(p || ''); if (!PFAD.test(s) || s.includes('..')) throw new Error(name + ' ungültig: ' + s); return s }
const PLAN = pruefePfad(A.plan, 'args.plan')
const H0 = pruefePfad(A.h0, 'args.h0')
const BERICHT = pruefePfad(A.bericht, 'args.bericht')
const REPO = pruefePfad(A.repo, 'args.repo')
const E_ARG = Array.isArray(A.einheiten) ? A.einheiten : []
if (!E_ARG.length) throw new Error('args.einheiten fehlt oder leer')
const EINHEITEN = E_ARG.map((e, i) => {
  const art = String(e.art), tk = String(e.tk), v = Number(e.v), n = Number(e.n) || 0
  if (!['a', 'b', 'c', 'z'].includes(art)) throw new Error('einheiten[' + i + '].art ungültig')
  if (!/^r\dc\d$/.test(tk)) throw new Error('einheiten[' + i + '].tk ungültig')
  if (!(Number.isInteger(v) && v >= 0 && v <= 4)) throw new Error('einheiten[' + i + '].v ungültig')
  if ((art === 'a') !== (v === 0)) throw new Error('einheiten[' + i + ']: art a hat v 0, alle anderen v 1–4')
  return { art, tk, v, n, auftrag: pruefePfad(e.auftrag, 'einheiten[' + i + '].auftrag'), ergebnis: pruefePfad(e.ergebnis, 'einheiten[' + i + '].ergebnis') }
})
const MAX_BUENDEL = Number.isInteger(A.max_buendel) && A.max_buendel > 0 ? A.max_buendel : 30

// [BLOCK 3] Konstanten — jede mit einem Satz Warum
const MODEL_URTEIL = 'opus', EFFORT_URTEIL = 'high'   // Urteil am Bild (siehe Kopf)
const MODEL_VEREIN = 'sonnet', EFFORT_VEREIN = 'medium' // Zusammenführen von Namen nach Auftrag, wie T0
const MODEL_BAU = 'opus', EFFORT_BAU = 'medium'       // Übertragen der T0-Skripte, stumme Fehler teuer
const MODEL_MECH = 'sonnet', EFFORT_MECH = 'medium'   // feste Befehle anwenden/messen/finden
const MAX_RUNDEN = 3            // Einigung: wie T0 (dort reichten 3 Runden bis offen 0)
const MAX_NACHHOLEN = 8         // höchstens so viele Viertel einzeln nachholen; mehr wäre ein Fehler im Ansatz
const PY = 'C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe'
const UEBERGABE_T0 = 'C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0'
const T0_SKRIPTE = 'C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-test-t0-3/skripte'
const UEB_SKRIPTE = 'C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-uebergabe/skripte'
const ART_NAME = { a: 'Fassung A „Alles frei“', b: 'Fassung B „Kategorien frei“', c: 'Fassung C „Feste Kategorienliste“', z: 'Gegenprobe (Zweitagent, Fassung C „Feste Kategorienliste“)' }
const FASSUNG = {
  A: { ordner: 'a-alles-frei', urteile: 'a-alles-frei/abgabe', liste: 'a-alles-frei/kategorien-a.json',
       hinweis: 'Fassung A hat keine urteil.json: lies je Teilkachel `' + H0 + '/a-alles-frei/abgabe/<teilkachel>/arbeitsweise.md` und die Felder in `' + H0 + '/a-alles-frei/<teilkachel>/segmente.json`.' },
  B: { ordner: 'b-kategorien-frei', urteile: 'b-kategorien-frei/urteil', liste: 'b-kategorien-frei/kategorien-b.json', hinweis: '' },
  C: { ordner: 'c-feste-liste', urteile: 'c-feste-liste/urteil', liste: 'c-feste-liste/kategorien-c.json', hinweis: '' },
}
const SW = 'Das Bild ist ein Schwarz-Weiß-Scan von 1968 (rund 0,45 m je Bildpunkt): urteile nach Grauton, Textur und Form; im Zweifel Elternklasse oder unklar mit Grund.'

// [BLOCK 4] Warum
// Urteile: ein Agent je Fassung und Teilkachel (Vorgabe 2026-11-17), dichteste zuerst, pipeline ohne Barriere.
// Nachholen: H0 hat bis 518 Segmente je Agent (T0 höchstens 301); ein Viertel ohne bestandene Kontrolle wird einzeln
//   von einem frischen Agent nachgeholt, statt die ganze Teilkachel zu wiederholen.
// Vereinheitlichen und Zusammenführen sind Barrieren aus der Sache: sie brauchen alle Abgaben.
// Nähte nur für Fassungen mit Verstößen (AK4 verlangt keinen offenen Verstoß). Einigung je Runde als pipeline über die
// Bündel aller Fassungen (Bündel sind unabhängig), danach ein Anwenden-Agent je Runde (Barriere: anwenden braucht alle
// Abgaben einer Fassung). Abbruch: offen 0 oder MAX_RUNDEN.
// Kein Verify-Agent: Gegenprobe (art z) ist die Zweitmeinung auf r0c0; `pruefen`, `naht`, `messen` prüfen die Form.

// [BLOCK 5] Schemas
const QUITTUNG_URTEIL = {
  type: 'object', additionalProperties: false, required: ['ganz_gesehen', 'teile'],
  properties: {
    ganz_gesehen: { type: 'boolean', description: 'Du hast zuerst H0.png bzw. das Rasterbild und dann das Bild deiner Teilkachel angesehen' },
    teile: { type: 'array', items: {
      type: 'object', additionalProperties: false, required: ['v', 'ok', 'kontrolle_ok', 'segmente'],
      properties: {
        v: { type: 'integer', minimum: 0, maximum: 4, description: 'Viertelnummer des Auftrags, bei A 0' },
        ok: { type: 'boolean', description: 'Ergebnis vollständig nach Auftrag geschrieben' },
        kontrolle_ok: { type: 'boolean', description: 'Die Kontrolle aus dem Auftrag endete mit ok' },
        segmente: { type: 'integer', minimum: 0, description: 'Zahl der eingetragenen Segmente' },
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
const BUENDEL_ITEM = {
  type: 'object', additionalProperties: false, required: ['fassung', 'name', 'auftraege'],
  properties: { fassung: { type: 'string', enum: ['A', 'B', 'C'] }, name: { type: 'string' }, auftraege: { type: 'string', description: 'abs. Ordner von finden (enthält <name>/auftrag.json)' } },
}
const ZAHLEN_F = {
  type: 'object', additionalProperties: false, required: ['fassung'],
  properties: { fassung: { type: 'string', enum: ['A', 'B', 'C'] }, offen: { type: 'integer' }, unsicher: { type: 'integer' }, geklaert: { type: 'integer' },
                naht_verstoesse: { type: 'integer' }, pruefen_ok: { type: 'boolean' }, segmente: { type: 'integer' } },
}
const QUITTUNG_BAU = {
  type: 'object', additionalProperties: false, required: ['ok', 'fassungen', 'buendel', 'offen'],
  properties: {
    ok: { type: 'boolean', description: 'Aufbau wie T0-Übergabe vollständig, pruefen 12× ok, zusammentragen 3× geschrieben' },
    fassungen: { type: 'array', items: ZAHLEN_F, description: 'je Fassung: Segmente, pruefen, Nahtverstöße, offen laut messen' },
    buendel: { type: 'array', items: BUENDEL_ITEM, description: 'Bündel aus einigung finden (Runde 1), alle Fassungen' },
    skript: { type: 'string', description: 'abs. Pfad des Skripts, das den Aufbau erzeugt' },
    offen: { type: 'array', items: { type: 'string' } },
  },
}
const QUITTUNG_NAHT = {
  type: 'object', additionalProperties: false, required: ['fassung', 'ok', 'verstoesse_vorher', 'verstoesse_nachher'],
  properties: { fassung: { type: 'string', enum: ['A', 'B', 'C'] }, ok: { type: 'boolean' }, verstoesse_vorher: { type: 'integer' }, verstoesse_nachher: { type: 'integer' },
                bestaetigt: { type: 'integer', description: 'als echte Grenze bestätigt' }, offen: { type: 'array', items: { type: 'string' } } },
}
const QUITTUNG_EINIGUNG = {
  type: 'object', additionalProperties: false,
  required: ['buendel', 'paare', 'gleich', 'grenze', 'unklar', 'probe_ok', 'probe_zeile', 'abgabe', 'offen'],
  properties: {
    buendel: { type: 'string' }, paare: { type: 'integer', minimum: 0 }, gleich: { type: 'integer', minimum: 0 },
    grenze: { type: 'integer', minimum: 0 }, unklar: { type: 'integer', minimum: 0 },
    probe_ok: { type: 'boolean', description: 'anwenden --probe lief ohne „Abgelehnt“' },
    probe_zeile: { type: 'string' }, abgabe: { type: 'string', description: 'abs. Pfad der einigung_abgabe.json' },
    offen: { type: 'array', items: { type: 'string' } },
  },
}
const QUITTUNG_ANWENDEN = {
  type: 'object', additionalProperties: false, required: ['ok', 'fassungen', 'buendel', 'offen'],
  properties: {
    ok: { type: 'boolean', description: 'anwenden lief für jede Fassung dieser Runde ohne Ablehnung' },
    fassungen: { type: 'array', items: ZAHLEN_F, description: 'messen je Fassung nach dieser Runde' },
    buendel: { type: 'array', items: BUENDEL_ITEM, description: 'Bündel der nächsten Runde (leer, wenn offen 0 oder letzte Runde)' },
    abgelehnt: { type: 'array', items: { type: 'string' }, description: 'Bündel, deren Abgabe anwenden ablehnte, mit Grund' },
    offen: { type: 'array', items: { type: 'string' } },
  },
}

// [BLOCK 6] Helfer — halten nie Nutzdaten
function hashLabel(s) { let h = 0; for (const c of s) h = (h * 31 + c.charCodeAt(0)) >>> 0; return h }
const BACKOFF_MS = [20000, 60000, 120000, 180000]
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
const sicher = (label, fn) => withRetry(label, fn).catch(e => { log(label + ': Fehler ' + String(e && e.message || e).slice(0, 120)); return null })
function labelOf(e) { return e.art + ':' + e.tk + (e.v ? '-v' + e.v : '') }
const GRENZEN = 'Kein Subagent, kein ToolSearch, keine Fenster, keine Dauerprozesse, nichts installieren, kein git. Python nur ' + PY + ' (Skripte als Datei, ausführen mit -B); Befehle `' + PY + ' -B -m landseg …` im Ordner ' + REPO + '. Am Repo und an den Originalbildern unter daten/luftbilder änderst du nichts.'

// [BLOCK 7] Prompt-Builder
function urteilPrompt(g) {
  const tk = g.tk, viertel = g.art !== 'a'
  const summe = g.teile.reduce((s, e) => s + e.n, 0)
  return [
    'Du beurteilst als einziger Agent ' + ART_NAME[g.art] + ' für Teilkachel ' + tk + (viertel ? ' (' + summe + ' Segmente in ' + g.teile.length + ' Vierteln)' : '') + ' des historischen Ausschnitts H0.',
    'Lies zuerst den Skill-Text `' + REPO + '/.claude/skills/landseg-agent/SKILL.md` (Regeln für alle landseg-Agents).',
    'Du schreibst nur in die Ergebnisordner deiner Aufträge (unten). Alle Eingaben nur lesen; die Label-Karte der Vorstufe änderst du nicht.',
    '',
    'Vorgabe des Nutzers, geht den Aufträgen voran:',
    '  1. Sieh ZUERST den ganzen Ausschnitt H0 an (1000 × 1000 px; r0c0 oben links, r0c1 oben rechts, r1c0 unten links, r1c1 unten rechts): ' + H0 + '/H0.png und ' + H0 + '/ganz/H0_raster.jpg.',
    '  2. Dann deine ganze Teilkachel ' + tk + ': ' + H0 + '/ganz/' + tk + '/ganz_nummern.jpg (Grenzen, Nummern, Viertel) und ' + H0 + '/ganz/' + tk + '/ganz_roh.jpg.',
    viertel
      ? '  3. Dann arbeitest du die Viertel-Aufträge nacheinander ab (' + g.teile.map(e => 'v' + e.v).join(', ') + ') — jeden ganz lesen, jedes Segment seiner Liste einzeln urteilen (im Zusammenhang mit Nachbarn, Teilkachel und H0), sein urteil.json schreiben und seine Kontrolle ausführen, bevor du den nächsten beginnst.'
      : '  3. Dann segmentierst und klassifizierst du die Teilkachel nach deinem eigenen Vorgehen, wie im Auftrag beschrieben.',
    '  4. Trage H0.png und das Bild der Teilkachel ' + (viertel ? 'in JEDEM urteil.json unter "bilder_angesehen" → "uebersicht" ein, vor den Viertelbildern.' : 'in arbeitsweise.md ein.'),
    '',
    'Aufträge (je einer maßgeblich für sein Ergebnis):',
    ...g.teile.map(e => '  - ' + (viertel ? 'v' + e.v + ' (' + e.n + ' Segmente): ' : '') + e.auftrag + '  → ' + e.ergebnis),
    viertel ? 'Wo ein Auftrag andere Agents für die übrigen Viertel nennt, bist das du selbst, nacheinander; ein Segment an der Viertelgrenze urteilst du nur in dem Auftrag, in dessen Liste es steht.' : '',
    '',
    SW,
    'Im Zweifel `sicher: false` und eine Notiz unter "offen": eine ehrlich als unsicher markierte Fläche wird nachgeprüft, eine falsch als sicher markierte geht unbemerkt in die Trainingsdaten.',
    'Arbeite jedes Segment ab; überfliege nichts gegen Ende. Schreibe jedes urteil.json, sobald sein Viertel fertig ist. Wird dir Platz knapp, schreib ehrlich unter "nicht_geprueft", was fehlt, statt zu raten.',
    '',
    GRENZEN,
    'RÜCKGABE: ausschließlich das JSON nach Schema — unter "teile" ein Eintrag je Auftrag (v = Viertelnummer, bei A 0), nie den Inhalt deiner Dateien.',
  ].filter(z => z !== '').join('\n')
}
function nachholPrompt(e) {
  return [
    'Du holst einen einzelnen Viertel-Auftrag nach: ' + ART_NAME[e.art] + ', Teilkachel ' + e.tk + ', Viertel v' + e.v + ' (' + e.n + ' Segmente) des historischen Ausschnitts H0.',
    'Der erste Agent dieser Teilkachel hat das Viertel nicht vollständig oder ohne bestandene Kontrolle abgegeben. Was im Ergebnisordner liegt, darfst du als Hinweis lesen; du schreibst urteil.json vollständig neu.',
    'Lies zuerst `' + REPO + '/.claude/skills/landseg-agent/SKILL.md`. Sieh zuerst ' + H0 + '/H0.png, dann ' + H0 + '/ganz/' + e.tk + '/ganz_nummern.jpg an und trage beide unter "bilder_angesehen" → "uebersicht" ein.',
    'Auftrag (maßgeblich): ' + e.auftrag + '  → ' + e.ergebnis,
    SW,
    'Im Zweifel `sicher: false` mit Notiz unter "offen". Führe die Kontrolle des Auftrags aus.',
    GRENZEN,
    'RÜCKGABE: ausschließlich das JSON nach Schema, "teile" mit genau einem Eintrag (v = ' + e.v + ').',
  ].join('\n')
}
function vereinPrompt(auftrag) {
  return [
    'Du arbeitest einen fertigen Auftrag ab: freie Klassen der Viertel von Fassung B (historischer Ausschnitt H0) zu einer gestuften Liste vereinheitlichen.',
    'Auftrag (lies ihn ganz, er ist maßgeblich): ' + auftrag,
    'Du schreibst nur in den Ergebnisordner des Auftrags. Alle Eingaben nur lesen. Fehlt eine Viertel-Abgabe, vereinheitliche die vorhandenen und nenne die fehlenden unter grund.',
    GRENZEN,
    'RÜCKGABE: ausschließlich {"ok", "pfad", "kurz", "grund"?} nach Schema — "kurz" = die Rückgabe-Angaben des Auftrags in einer Zeile.',
  ].join('\n')
}
function bauPrompt() {
  return [
    'Du baust den historischen Ausschnitt H0 nach den Urteilen genauso auf wie den Ausschnitt T0 in der Übergabe und bereitest die Einigung an den Übergängen vor.',
    'Lies zuerst `' + REPO + '/README.md` (Abschnitte pruefen, zusammentragen, naht, einigung) und `' + REPO + '/.claude/skills/landseg-agent/SKILL.md`.',
    '',
    'Vorbild (nur lesen): die T0-Übergabe `' + UEBERGABE_T0 + '` — je Fassung `<ordner>/<tk>/labels.tif` + `segmente.json`, Kategorienliste, `zusammentragen.json` und `zusammen/` (labels.tif, segmente.json, naht.json).',
    'So entstand sie: Skripte `' + T0_SKRIPTE + '` (zusammenfuehren.py: Urteile → Klassen in segmente.json; listen.py: Kategorienlisten; Zusammentragen) und `' + UEB_SKRIPTE + '/baue_uebergabe.py`.',
    'ACHTUNG Benennung: In jenen T0-Skripten heißt die feste Liste „A“ und die freie Abgabe „C“; heute (und in H0) ist A = „Alles frei“ (`a-alles-frei`, freie Abgabe je Teilkachel unter `abgabe/<tk>/`), B = „Kategorien frei“, C = „Feste Kategorienliste“ (`c-feste-liste`). Prüfe jede Zuordnung.',
    '',
    'Stand von H0 (`' + H0 + '`, Plan `' + PLAN + '`): manifest.json, vorstufe/<tk>/, Kopien der Vorstufe unter b-kategorien-frei/<tk>/ und c-feste-liste/<tk>/, Urteile unter b-kategorien-frei/urteil/<tk>/v<n>/ und c-feste-liste/urteil/<tk>/v<n>/, Vereinheitlichung von B unter b-kategorien-frei/vereinheitlichung/, freie Abgabe A unter a-alles-frei/abgabe/<tk>/. Die Gegenprobe (c-feste-liste/urteil-gegenprobe/) bleibt daneben und geht in keine Karte ein.',
    '',
    'Schritte (Skript als Datei unter `' + BERICHT + '/skripte/`, Logs unter `' + BERICHT + '/`):',
    '  1. Je Fassung `<ordner>/<tk>/labels.tif` + `segmente.json` mit den Klassen aus den Urteilen (B und C: Grenzen der Vorstufe; A: die Karte der freien Abgabe), Kategorienliste `kategorien-a.json`, `kategorien-b.json`, `kategorien-c.json` wie im Vorbild. Jedes Kernsegment genau einmal, unsichere als `sicher: false`.',
    '  2. `pruefen` für alle 12 Teilkacheln mit der Kategorienliste der Fassung, Prüfskript `' + REPO + '/tools/pruefe_kategorien.py` für jede Liste (mit `C:/Users/Phil/AppData/Local/Programs/Python/Python313/python.exe -I`).',
    '  3. Je Fassung `zusammentragen.json` wie im Vorbild und `zusammentragen` nach `<ordner>/zusammen/`; dann `naht` je Fassung. Zahl der Nahtverstöße je Fassung melden (nicht selbst beheben).',
    '  4. `einigung finden --manifest ' + H0 + '/manifest.json --fassung <F> --ziel ' + BERICHT + '/einigung/runde1/auftraege-<F>` je Fassung (Fassungsordner wenn nötig mit `--ordner`), danach `einigung messen --manifest ' + H0 + '/manifest.json`.',
    '',
    'Du schreibst nur unter `' + H0 + '` (Fassungsordner, nicht vorstufe/, teilkacheln/, viertel/, ganz/) und `' + BERICHT + '`. Die Urteile selbst änderst du nicht.',
    GRENZEN,
    'RÜCKGABE: ausschließlich das JSON nach Schema — je Fassung Zahlen, alle Bündel aus Schritt 4 mit Ordner, Pfad des Skripts, was offen blieb.',
  ].join('\n')
}
function nahtPrompt(f, n) {
  return [
    'Du klärst die Nahtverstöße der Fassung ' + f + ' im historischen Ausschnitt H0 (' + n + ' Verstöße laut `naht`).',
    'Lies `' + REPO + '/vorlagen/naht.md` ganz und folge ihr; Regeln: `' + REPO + '/.claude/skills/landseg-agent/SKILL.md`. Setze ein:',
    '- {{PY}} = ' + PY + ', {{REPO}} = ' + REPO + ', {{DATEN}} = ' + H0,
    '- {{AUFTRAG_ZUSAMMEN}} = ' + FASSUNG[f].ordner + '/zusammentragen.json, {{ZUSAMMEN}} = ' + FASSUNG[f].ordner + '/zusammen',
    '- {{ERGEBNIS}} = ' + BERICHT + '/naht-' + f + ', {{BEARBEITER}} = agent:naht-' + f + ':' + RUN + ', {{RUNDE}} = 1, {{ABWEICHUNGEN}} = keine',
    'Nach deiner Abgabe trägst du sie in `' + H0 + '/' + FASSUNG[f].ordner + '/zusammentragen.json` ein, rufst `zusammentragen` und `naht` erneut und meldest die Verstöße nachher.',
    SW,
    'Du schreibst nur unter `' + H0 + '/' + FASSUNG[f].ordner + '` und `' + BERICHT + '/naht-' + f + '`.',
    GRENZEN,
    'RÜCKGABE: ausschließlich das JSON nach Schema.',
  ].join('\n')
}
function einigungPrompt(b, runde) {
  const f = FASSUNG[b.fassung]
  const erg = BERICHT + '/einigung/runde' + runde + '/abgaben/' + b.name
  return [
    'Du bist ein Agent des Projekts landseg (Segmentierung von Luftbildern). Antworte auf Deutsch.',
    'Auftrag: Einigung an den Übergängen der Teilkacheln, historischer Ausschnitt H0, Fassung ' + b.fassung + ', Bündel ' + b.name + ' (Runde ' + runde + ').',
    '',
    'Lies zuerst die Vorlage `' + REPO + '/vorlagen/einigung.md` ganz und folge ihr. Setze darin ein:',
    '- {{FASSUNG}} = ' + b.fassung, '- {{BUENDEL}} = ' + b.name, '- {{REPO}} = ' + REPO, '- {{AUFTRAEGE}} = ' + b.auftraege,
    '- {{DATEN}} = ' + H0, '- {{URTEILE}} = ' + f.urteile, '- {{PY}} = ' + PY,
    '- {{ERGEBNIS}} = ' + erg + '  (lege den Ordner an, falls er fehlt)',
    '- {{BEARBEITER}} = agent:einigung-' + b.name + ':' + RUN + '-r' + runde,
    'Klassen-Codes aus `' + H0 + '/' + f.liste + '`. ' + f.hinweis,
    SW,
    '',
    'Du schreibst nur in `' + erg + '`. An den Daten unter `' + H0 + '`, an den Aufträgen und am Repo änderst du nichts; `anwenden` nur mit `--probe`.',
    'Schau dir jedes `paar_<nr>.jpg` an, bevor du entscheidest. Im Zweifel `unklar` mit Grund, nie raten. Bilder höchstens 2000 Bildpunkte an der langen Seite.',
    GRENZEN,
    'RÜCKGABE: die Quittung im Schema (Zahl der Paare, je Entscheidung die Zahl, Probe ohne „Abgelehnt“, ihre letzte Zeile wörtlich, Pfad der Abgabe, was offen blieb).',
  ].join('\n')
}
function anwendenPrompt(runde, abgaben, letzte) {
  const proF = {}
  for (const q of abgaben) (proF[q.fassung] = proF[q.fassung] || []).push(q)
  return [
    'Du setzt die Einigung an den Übergängen für den historischen Ausschnitt H0 um, Runde ' + runde + '. Lies `' + REPO + '/README.md`, Abschnitt einigung.',
    'Je Fassung mit Abgaben: zuerst `' + PY + ' -B -m landseg einigung anwenden --manifest ' + H0 + '/manifest.json --fassung <F> --auftraege <Ordner> --abgabe <…> [--abgabe …] --probe`, ist die Probe ohne Ablehnung, dasselbe ohne `--probe`.',
    'Lehnt anwenden eine einzelne Abgabe ab, lass sie weg, wende die übrigen an und nenne sie unter "abgelehnt" mit Grund. Log je Fassung nach `' + BERICHT + '/einigung/runde' + runde + '/anwenden-<F>.log`.',
    ...Object.keys(proF).sort().map(F => '  Fassung ' + F + ': Aufträge ' + proF[F][0].auftraege + '; Abgaben: ' + proF[F].map(q => q.abgabe).join(' ')),
    'Danach `einigung messen --manifest ' + H0 + '/manifest.json` (Log `' + BERICHT + '/einigung/runde' + runde + '/messen.txt`) und je Fassung die Zahlen offen / unsicher / geklärt melden.',
    letzte
      ? 'Das ist die letzte Runde: kein `finden` mehr. Trage danach je Fassung neu zusammen (`zusammentragen --datei ' + H0 + '/<ordner>/zusammentragen.json`), rufe `naht` und `pruefen` für alle 12 Teilkacheln und melde Nahtverstöße und pruefen je Fassung.'
      : 'Ist bei einer Fassung danach noch etwas offen: `einigung finden --manifest ' + H0 + '/manifest.json --fassung <F> --ziel ' + BERICHT + '/einigung/runde' + (runde + 1) + '/auftraege-<F>` und alle neuen Bündel unter "buendel" melden. Ist überall 0 offen: "buendel" leer, dann je Fassung neu zusammentragen, `naht` und `pruefen` wie in der letzten Runde und melden.',
    'Du schreibst nur unter `' + H0 + '` (Fassungsordner) und `' + BERICHT + '/einigung`.',
    GRENZEN,
    'RÜCKGABE: ausschließlich das JSON nach Schema.',
  ].join('\n')
}

// [BLOCK 8] Katalog, Gruppen, Plan-Log
const gruppenMap = {}
for (const e of EINHEITEN) { const k = e.art + ':' + e.tk; (gruppenMap[k] = gruppenMap[k] || { art: e.art, tk: e.tk, teile: [] }).teile.push(e) }
const gruppen = Object.keys(gruppenMap).sort().map(k => gruppenMap[k])
for (const g of gruppen) g.teile.sort((x, y) => x.v - y.v)
const last = g => g.teile.reduce((s, e) => s + e.n, 0)
gruppen.sort((x, y) => (last(y) - last(x)) || ((x.art + x.tk) < (y.art + y.tk) ? -1 : 1))   // dichteste zuerst
const glabel = g => g.art + ':' + g.tk
const zaehl = k => gruppen.filter(g => g.art === k).length
log(EINHEITEN.length + ' Aufträge in ' + gruppen.length + ' Urteils-Agents (A ' + zaehl('a') + ', B ' + zaehl('b') + ', C ' + zaehl('c') + ', Gegenprobe ' + zaehl('z') + ', ' + MODEL_URTEIL + '/' + EFFORT_URTEIL
    + '), danach Nachholen (≤ ' + MAX_NACHHOLEN + '), Vereinheitlichen (' + MODEL_VEREIN + '), Zusammenführen (' + MODEL_BAU + '), Nähte, Einigung ≤ ' + MAX_RUNDEN + ' Runden à ≤ ' + MAX_BUENDEL + ' Bündel.')
const VEREIN_AUFTRAG = PLAN.replace(/auftraege\.json$/, 'auftraege/b/vereinheitlichen.md')

// [BLOCK 9] Hauptablauf
// 9a Urteile
let fertig = 0
const urteilErg = await pipeline(gruppen, (g) => sicher('urteil:' + glabel(g), () => agent(urteilPrompt(g), {
  label: 'urteil:' + glabel(g), phase: 'Urteile', model: MODEL_URTEIL, effort: EFFORT_URTEIL, schema: QUITTUNG_URTEIL })),   // Urteil am Bild
  async (q, g) => {
    fertig += 1
    const zeilen = g.teile.map(e => {
      const t = q && Array.isArray(q.teile) ? q.teile.find(x => x.v === e.v) : null
      return { e, label: labelOf(e), da: !!t, ok: !!(t && t.ok && t.kontrolle_ok), segmente: t ? (t.segmente || 0) : 0, unsicher: t ? (t.unsicher || 0) : 0, gesamt: !!(q && q.ganz_gesehen) }
    })
    log(fertig + '/' + gruppen.length + ' Urteils-Agents zurück (' + glabel(g) + ': ' + zeilen.filter(r => r.ok).length + '/' + g.teile.length + ' ok, ' + zeilen.reduce((s, r) => s + r.segmente, 0) + ' Segmente)')
    return zeilen
  })
let zeilen = urteilErg.filter(Boolean).flat()
// fehlende Gruppen (Agent ganz ausgefallen) zählen als nicht ok
for (const g of gruppen) for (const e of g.teile) if (!zeilen.some(r => r.label === labelOf(e))) zeilen.push({ e, label: labelOf(e), da: false, ok: false, segmente: 0, unsicher: 0, gesamt: false })

// 9b Nachholen (nur Viertel-Aufträge; A je Teilkachel und Segmentzahl bei A frei)
// Nachhol-Grund ist nur ok/kontrolle_ok (fehlt die Rückmeldung, ist r.ok false). Eine Segmentzahl ≠ Plan (e.n) ist keiner:
// Urteils-Agents dürfen nachsegmentieren und haben kein Feld für Zugänge; sie bleibt als Hinweis (segAbweichung).
const schlecht = zeilen.filter(r => r.e.art !== 'a' && !r.ok)
const nachholen = schlecht.slice(0, MAX_NACHHOLEN)
const nachholRest = schlecht.slice(nachholen.length).map(r => r.label)
const schlechtA = zeilen.filter(r => r.e.art === 'a' && !r.ok).map(r => r.label)
if (nachholen.length) {
  log('Nachholen: ' + nachholen.map(r => r.label).join(', ') + (nachholRest.length ? ' — Deckel, liegen: ' + nachholRest.join(', ') : ''))
  const nq = await pipeline(nachholen, (r) => sicher('nachholen:' + r.label, () => agent(nachholPrompt(r.e), {
    label: 'nachholen:' + r.label, phase: 'Nachholen', model: MODEL_URTEIL, effort: EFFORT_URTEIL, schema: QUITTUNG_URTEIL })))   // Urteil am Bild
  nachholen.forEach((r, i) => {
    const t = nq[i] && Array.isArray(nq[i].teile) ? nq[i].teile[0] : null
    if (t && t.ok && t.kontrolle_ok) { r.ok = true; r.segmente = t.segmente || 0; r.unsicher = t.unsicher || 0; r.nachgeholt = true }
  })
}
const nichtOk = zeilen.filter(r => !r.ok).map(r => r.label)
const segAbweichung = zeilen.filter(r => r.e.art !== 'a' && r.ok && r.e.n && r.segmente !== r.e.n).map(r => ({ label: r.label, soll: r.e.n, ist: r.segmente }))
if (segAbweichung.length) log('Hinweis Segmentzahl (Soll→Ist, kein Nachhol-Grund): ' + segAbweichung.map(s => s.label + ' ' + s.soll + '→' + s.ist).join(', '))
if (schlechtA.length) log('Fassung A ohne bestandene Kontrolle: ' + schlechtA.join(', ') + ' — Zusammenführen meldet die Folgen.')

// 9c Vereinheitlichen B (Barriere: braucht alle B-Viertel)
let verein = null
if (EINHEITEN.some(e => e.art === 'b')) {
  verein = await sicher('vereinheitlichen', () => agent(vereinPrompt(VEREIN_AUFTRAG), {
    label: 'vereinheitlichen:b', phase: 'Vereinheitlichen', model: MODEL_VEREIN, effort: EFFORT_VEREIN, schema: QUITTUNG_VEREIN }))   // Namen nach Liste
  log('Vereinheitlichung B: ' + (verein && verein.ok ? 'ok' : 'nicht fertig (' + (verein && verein.grund || 'ohne Rückmeldung') + ')'))
}

// 9d Zusammenführen (Barriere: braucht alle Urteile und die Liste von B)
const bau = await sicher('zusammenfuehren', () => agent(bauPrompt(), {
  label: 'zusammenfuehren:h0', phase: 'Zusammenführen', model: MODEL_BAU, effort: EFFORT_BAU, schema: QUITTUNG_BAU }))   // Skripte übertragen
if (!bau) {
  log('Zusammenführen ohne Rückmeldung — Lauf endet hier; mit resumeFromRunId fortsetzen.')
  return { run: RUN, stufe: 'zusammenfuehren', urteile_nicht_ok: nichtOk, nachhol_rest: nachholRest, segmentzahl_abweichung: segAbweichung, vereinheitlichung: verein ? !!verein.ok : null, ohne_rueckmeldung: ['zusammenfuehren:h0'] }
}
log('Zusammenführen: ' + (bau.ok ? 'ok' : 'mit Befund') + '; ' + (bau.fassungen || []).map(f => f.fassung + ' Segmente ' + (f.segmente ?? '?') + ', Naht ' + (f.naht_verstoesse ?? '?') + ', offen ' + (f.offen ?? '?')).join(' · ') + '; Bündel ' + (bau.buendel || []).length)

// 9e Nähte (nur Fassungen mit Verstößen)
const mitNaht = (bau.fassungen || []).filter(f => (f.naht_verstoesse || 0) > 0)
let naehte = []
if (mitNaht.length) {
  naehte = (await pipeline(mitNaht, (f) => sicher('naht:' + f.fassung, () => agent(nahtPrompt(f.fassung, f.naht_verstoesse), {
    label: 'naht:' + f.fassung, phase: 'Nähte', model: MODEL_URTEIL, effort: EFFORT_URTEIL, schema: QUITTUNG_NAHT })))).filter(Boolean)   // Grenze am Bild
  log('Nähte: ' + naehte.map(n => n.fassung + ' ' + n.verstoesse_vorher + '→' + n.verstoesse_nachher).join(', '))
}

// 9f Einigung in Runden (Abbruch: keine Bündel mehr oder MAX_RUNDEN)
const runden = []
let buendel = (bau.buendel || []).filter(b => /^[ABC]-\d{2}$/.test(b.name) && b.name[0] === b.fassung && PFAD.test(b.auftraege))
let schluss = null
const einigungRest = []
for (let runde = 1; runde <= MAX_RUNDEN && buendel.length; runde++) {
  const lauf = buendel.slice(0, MAX_BUENDEL)
  einigungRest.push(...buendel.slice(lauf.length).map(b => 'r' + runde + ':' + b.name))
  log('Einigung Runde ' + runde + ': ' + lauf.length + ' Bündel (A ' + lauf.filter(b => b.fassung === 'A').length + ', B ' + lauf.filter(b => b.fassung === 'B').length + ', C ' + lauf.filter(b => b.fassung === 'C').length + ')')
  const qs = await pipeline(lauf, (b) => sicher('einigung:r' + runde + ':' + b.name, () => agent(einigungPrompt(b, runde), {
    label: 'einigung:r' + runde + ':' + b.name, phase: 'Einigung', model: MODEL_URTEIL, effort: EFFORT_URTEIL, schema: QUITTUNG_EINIGUNG }))   // Urteil am Bild beider Seiten
    .then(q => q ? { ...q, name: b.name, fassung: b.fassung, auftraege: b.auftraege } : null))
  const da = qs.filter(Boolean)
  const ohne = lauf.filter(b => !da.some(q => q.name === b.name)).map(b => b.name)
  const brauchbar = da.filter(q => q.probe_ok && PFAD.test(q.abgabe || ''))
  const letzte = runde === MAX_RUNDEN
  const an = brauchbar.length ? await sicher('anwenden:r' + runde, () => agent(anwendenPrompt(runde, brauchbar, letzte), {
    label: 'anwenden:r' + runde, phase: 'Anwenden', model: MODEL_MECH, effort: EFFORT_MECH, schema: QUITTUNG_ANWENDEN })) : null   // feste Befehle
  const summe = k => da.reduce((s, q) => s + (q[k] || 0), 0)
  runden.push({ runde, buendel: lauf.length, zurueck: da.length, ohne_rueckmeldung: ohne, probe_rot: da.filter(q => !q.probe_ok).map(q => q.name),
                paare: summe('paare'), gleich: summe('gleich'), grenze: summe('grenze'), unklar: summe('unklar'),
                angewendet: !!(an && an.ok), abgelehnt: an ? (an.abgelehnt || []) : [], messen: an ? an.fassungen : null })
  log('Runde ' + runde + ': ' + da.length + '/' + lauf.length + ' Bündel, Paare ' + summe('paare') + ' (gleich ' + summe('gleich') + ', grenze ' + summe('grenze') + ', unklar ' + summe('unklar') + '); anwenden ' + (an ? (an.ok ? 'ok' : 'mit Befund') : 'nicht gelaufen')
      + (an ? '; offen danach ' + (an.fassungen || []).map(f => f.fassung + ' ' + (f.offen ?? '?')).join(', ') : ''))
  schluss = an
  buendel = an && !letzte ? (an.buendel || []).filter(b => /^[ABC]-\d{2}$/.test(b.name) && b.name[0] === b.fassung && PFAD.test(b.auftraege)) : []
  if (!an) break
}

// [BLOCK 10] return — nur Statistik, Pfade, Kennungen
const sumArt = (k, f) => zeilen.filter(r => r.e.art === k).reduce((s, r) => s + r[f], 0)
return {
  run: RUN,
  urteile: { auftraege: zeilen.length, ok: zeilen.length - nichtOk.length, nachgeholt: zeilen.filter(r => r.nachgeholt).map(r => r.label),
             segmente: { a: sumArt('a', 'segmente'), b: sumArt('b', 'segmente'), c: sumArt('c', 'segmente'), z: sumArt('z', 'segmente') },
             unsicher: { a: sumArt('a', 'unsicher'), b: sumArt('b', 'unsicher'), c: sumArt('c', 'unsicher'), z: sumArt('z', 'unsicher') },
             nicht_ok: nichtOk, ohne_gesamtbild: zeilen.filter(r => r.da && !r.gesamt).map(r => r.label) },
  nachhol_rest: nachholRest,
  segmentzahl_abweichung: segAbweichung,
  vereinheitlichung: verein ? { ok: !!verein.ok, pfad: verein.pfad || null, kurz: verein.kurz || null } : null,
  zusammenfuehren: { ok: !!bau.ok, fassungen: bau.fassungen || [], skript: bau.skript || null, offen: bau.offen || [] },
  naehte: naehte.map(n => ({ fassung: n.fassung, ok: n.ok, vorher: n.verstoesse_vorher, nachher: n.verstoesse_nachher, offen: n.offen || [] })),
  einigung: runden,
  endstand: schluss ? { fassungen: schluss.fassungen || [], offen: schluss.offen || [], weitere_buendel: (schluss.buendel || []).length } : null,
  rest: einigungRest,
  ohne_rueckmeldung: zeilen.filter(r => !r.da).map(r => r.label).concat(runden.flatMap(r => r.ohne_rueckmeldung.map(n => 'r' + r.runde + ':' + n))),
}

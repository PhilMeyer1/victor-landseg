// landseg-einigung-t0 — Teil 2 von naht-einigung (Wunsch-Datei
// C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-naht-einigung-2.md, Mutterwunsch …/2026-11-18-naht-einigung.md):
// Einigung an den Übergängen der Teilkacheln für T0, Fassungen A, B, C. Je Bündel (aus `landseg einigung finden`)
// ein Agent, der beide Seiten jeder Stelle sieht und je Segment-Paar gleich | grenze | unklar entscheidet.
// Die Agents ändern keine Daten; sie schreiben nur einigung_abgabe.json und prüfen sie mit `anwenden --probe`.
// Umsetzen (`einigung anwenden`) und Messen macht die Hauptsession danach für alle Bündel gemeinsam.
//
// Vorgabe des Nutzers (2026-11-18): „Bei den Tiles am Ende sollen sich dann alle Agents bei den Übergängen mit
// den Klassifikationen einigen.“ F1: nur Klassen abgleichen, Karten und Segmentnummern bleiben.
//
// args (JSON-Objekt):
//   run      string    Pflicht   Lauf-Kennung ^[\w-]{1,40}$
//   buendel  object[]  Pflicht   je Bündel {fassung: A|B|C, name: z. B. "A-01", auftraege: abs. Ordner von finden, ergebnis: abs. Ordner}
//   daten    string    Pflicht   abs. Ordner mit manifest.json und den Fassungsordnern (Übergabe-T0)
//   repo     string    Pflicht   abs. Pfad des Repos landseg (Vorlage, Skill, Befehle)
//   max      int       optional  Deckel in Bündeln; 0/fehlend = alle
//
// Konstanten: MODEL_URTEIL=opus/high — Urteil am Bild beider Seiten; eine falsche Einigung geht als falsche
//             Klasse in die Trainingsdaten (teure Fehlerklasse). Kein Verify-Agent: `anwenden --probe` prüft
//             die Form, `unklar` ist als Ausweg erlaubt, `messen` zählt danach.
// Läufe: (erster Lauf folgt)

// [BLOCK 1] meta — erstes Statement, reines Literal
export const meta = {
  name: 'landseg-einigung-t0',
  description: 'Einigung an den Übergängen der Teilkacheln: je Bündel ein Agent entscheidet je Segment-Paar gleich, grenze oder unklar',
  whenToUse: 'Teil 2 von naht-einigung bzw. jeder landseg-Lauf nach dem Zusammentragen: Bündel aus `landseg einigung finden` abarbeiten lassen. args: { run, buendel: [{fassung, name, auftraege, ergebnis}], daten, repo, max? }.',
  phases: [
    { title: 'Einigung', detail: 'je Bündel ein Agent, beide Seiten im Blick, Abgabe mit Probe', model: 'opus' },
  ],
}

// [BLOCK 2] args — normalisieren, Pflicht-Guard, Whitelist
const A = typeof args === 'string' ? JSON.parse(args) : (args || {})
const RUN = String(A.run || '')
if (!/^[\w-]{1,40}$/.test(RUN)) throw new Error('args.run fehlt oder ungültig (^[\\w-]{1,40}$)')
const PFAD = /^C:\/Users\/Phil\/Developement\/Victor\/[\w./ -]+$/
function pruefePfad(p, name) { const s = String(p || ''); if (!PFAD.test(s) || s.includes('..')) throw new Error(name + ' ungültig: ' + s); return s }
const DATEN = pruefePfad(A.daten, 'args.daten')
const REPO = pruefePfad(A.repo, 'args.repo')
const B_ARG = Array.isArray(A.buendel) ? A.buendel : []
if (!B_ARG.length) throw new Error('args.buendel fehlt oder leer')
const BUENDEL = B_ARG.map((b, i) => {
  const fassung = String(b.fassung), name = String(b.name)
  if (!['A', 'B', 'C'].includes(fassung)) throw new Error('buendel[' + i + '].fassung ungültig')
  if (!/^[ABC]-\d{2}$/.test(name) || name[0] !== fassung) throw new Error('buendel[' + i + '].name ungültig')
  return { fassung, name, auftraege: pruefePfad(b.auftraege, 'buendel[' + i + '].auftraege'), ergebnis: pruefePfad(b.ergebnis, 'buendel[' + i + '].ergebnis') }
})
const LIMIT = Number.isInteger(A.max) && A.max > 0 ? A.max : 0

// [BLOCK 3] Konstanten — jede mit einem Satz Warum
const MAX_AGENTS = 16           // T0: 12 Bündel (je Fassung 4); Deckel mit Luft, mehr wäre ein anderer Lauf
const MODEL_URTEIL = 'opus', EFFORT_URTEIL = 'high'   // Urteil am Bild beider Seiten (siehe Kopf)
const PY = 'C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe'
const BACKOFF_MS = [20000, 60000, 120000]
const FASSUNG = {
  A: { name: 'A „Alles frei“', urteile: 'a-alles-frei/abgabe', hinweis: 'Fassung A hat keine urteil.json: lies statt dessen je Teilkachel `' + DATEN + '/a-alles-frei/abgabe/<teilkachel>/arbeitsweise.md` und die Felder in `' + DATEN + '/a-alles-frei/<teilkachel>/segmente.json`; Klassen-Codes aus `' + DATEN + '/a-alles-frei/kategorien-a.json`.' },
  B: { name: 'B „Kategorien frei“', urteile: 'b-kategorien-frei/urteil', hinweis: 'Klassen-Codes aus `' + DATEN + '/b-kategorien-frei/kategorien-b.json`.' },
  C: { name: 'C „Feste Kategorienliste“', urteile: 'c-feste-liste/urteil', hinweis: 'Klassen-Codes aus `' + DATEN + '/c-feste-liste/kategorien-c.json` bzw. der festen Liste `' + REPO + '/KATEGORIEN.md`.' },
}

// [BLOCK 4] Warum
// Ein Agent je Bündel (Prüfer-Entscheidung in der Klärung): zusammenhängende Segment-Paare (Ketten, Ecke mit vier
// Teilkacheln) liegen in einem Bündel und bekommen so eine gemeinsame Klasse. Alle Bündel sind unabhängig
// (jedes Segment in höchstens einem Bündel) → pipeline ohne Barriere, eine Stufe. Größte Bündel zuerst.

// [BLOCK 5] Schemas
const QUITTUNG = {
  type: 'object', additionalProperties: false,
  required: ['buendel', 'paare', 'gleich', 'grenze', 'unklar', 'probe_ok', 'probe_zeile', 'abgabe', 'offen'],
  properties: {
    buendel: { type: 'string' },
    paare: { type: 'integer', minimum: 0 },
    gleich: { type: 'integer', minimum: 0 },
    grenze: { type: 'integer', minimum: 0 },
    unklar: { type: 'integer', minimum: 0 },
    probe_ok: { type: 'boolean', description: 'anwenden --probe lief ohne „Abgelehnt“' },
    probe_zeile: { type: 'string', description: 'letzte Zeile der Probe, wörtlich' },
    abgabe: { type: 'string', description: 'absoluter Pfad der einigung_abgabe.json' },
    offen: { type: 'array', items: { type: 'string' }, description: 'was nicht entschieden oder nicht geprüft wurde' },
  },
}

// [BLOCK 6] Helfer
function hashLabel(s) { let h = 0; for (const c of s) h = (h * 31 + c.charCodeAt(0)) >>> 0; return h }
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

// [BLOCK 7] Prompt-Builder
function prompt(b) {
  const f = FASSUNG[b.fassung]
  return [
    'Du bist ein Agent des Projekts landseg (Segmentierung von Luftbildern). Antworte auf Deutsch.',
    'Auftrag: Einigung an den Übergängen der Teilkacheln, Fassung ' + f.name + ', Bündel ' + b.name + '.',
    '',
    'Lies zuerst die Vorlage `' + REPO + '/vorlagen/einigung.md` ganz und folge ihr. Setze darin ein:',
    '- {{FASSUNG}} = ' + b.fassung,
    '- {{BUENDEL}} = ' + b.name,
    '- {{REPO}} = ' + REPO,
    '- {{AUFTRAEGE}} = ' + b.auftraege,
    '- {{DATEN}} = ' + DATEN,
    '- {{URTEILE}} = ' + f.urteile,
    '- {{PY}} = ' + PY,
    '- {{ERGEBNIS}} = ' + b.ergebnis + '  (lege den Ordner an, falls er fehlt)',
    '- {{BEARBEITER}} = agent:einigung-' + b.name + ':' + RUN,
    '',
    f.hinweis,
    '',
    'Grenzen: Du schreibst nur in `' + b.ergebnis + '`. An den Daten unter `' + DATEN + '`, an den Aufträgen und am Repo änderst du nichts;',
    '`anwenden` nur mit `--probe`. Keine Fenster öffnen, Bilder höchstens 2000 Bildpunkte an der langen Seite.',
    'Schau dir jedes `paar_<nr>.jpg` an, bevor du entscheidest. Im Zweifel `unklar` mit Grund, nie raten.',
    '',
    'Gib zum Schluss die Quittung im Schema zurück: Zahl der Paare, je Entscheidung die Zahl, ob die Probe ohne „Abgelehnt“',
    'lief, ihre letzte Zeile wörtlich, den Pfad der Abgabe und was offen blieb.',
  ].join('\n')
}

// [BLOCK 8] Katalog und Deckel
const KATALOG = BUENDEL.slice()
const LAUF = LIMIT ? KATALOG.slice(0, LIMIT) : KATALOG
if (LAUF.length > MAX_AGENTS) throw new Error('mehr Bündel (' + LAUF.length + ') als MAX_AGENTS (' + MAX_AGENTS + '); args.max setzen')
const REST = KATALOG.slice(LAUF.length).map(b => b.name)
log('Bündel: ' + KATALOG.length + ' im Katalog, ' + LAUF.length + ' in diesem Lauf, Rest ' + REST.length)

// [BLOCK 9] Ausführung — eine Stufe, pipeline (keine Barriere nötig)
const quittungen = await pipeline(LAUF, (b) => withRetry('einigung:' + b.name, () => agent(prompt(b), {
  label: 'einigung:' + b.name, phase: 'Einigung', model: MODEL_URTEIL, effort: EFFORT_URTEIL, schema: QUITTUNG,
})).then(q => q ? { name: b.name, fassung: b.fassung, ...q } : null).catch(e => { log(b.name + ': Fehler ' + String(e && e.message || e).slice(0, 120)); return null }))

// [BLOCK 10] return — Statistik, Pfade, Ausfälle
const da = quittungen.filter(Boolean)
const ohne = LAUF.filter(b => !da.some(q => q.name === b.name)).map(b => b.name)
const probe_rot = da.filter(q => !q.probe_ok).map(q => q.name)
const je_fassung = {}
for (const q of da) {
  const s = je_fassung[q.fassung] || (je_fassung[q.fassung] = { buendel: 0, paare: 0, gleich: 0, grenze: 0, unklar: 0 })
  s.buendel++; s.paare += q.paare; s.gleich += q.gleich; s.grenze += q.grenze; s.unklar += q.unklar
}
log('fertig: ' + da.length + '/' + LAUF.length + ' Bündel, ohne Rückmeldung ' + ohne.length + ', Probe rot ' + probe_rot.length)
return {
  run: RUN,
  soll: LAUF.length, ist: da.length,
  je_fassung,
  abgaben: da.map(q => ({ name: q.name, fassung: q.fassung, abgabe: q.abgabe, probe_ok: q.probe_ok, probe_zeile: q.probe_zeile, offen: q.offen })),
  probe_rot, ohne_rueckmeldung: ohne, rest: REST,
}

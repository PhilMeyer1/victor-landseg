/* Platz e: Start auf dem ganzen Testfenster T0, Klick führt in eine Teilkachel, Ebenen als Reiter oben. */
(function () {
  'use strict'
  var REITER = [
    ['grob', 'Grob'], ['mittel', 'Mittel'], ['fein', 'Fein'],
    ['luecken', 'Lücken'], ['naht', 'Naht'], ['vorher', 'Vorher / Nachher']
  ]
  var aktiv = 'fein'

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c] })
  }

  function stand() { return aktiv === 'naht' || aktiv === 'vorher' ? 'runde1' : 'vorstufe' }

  function optionen(tk, auswahl) {
    var o = { stand: stand(), ausschnitt: tk ? tk.ausschnitt : [0, 0, 1000, 1000], grau: true, umriss: true, flaeche: 0.3, ebene: 3 }
    if (aktiv === 'grob') o.ebene = 1
    if (aktiv === 'mittel') o.ebene = 2
    if (aktiv === 'luecken') { o.luecken = true; o.flaeche = 0; o.umriss = false }
    if (aktiv === 'naht') { o.naht = true; o.flaeche = 0.1 }
    if (aktiv === 'vorher') { o.geaendert = true; o.flaeche = 0.2 }
    if (tk) { o.kern = tk.id; o.auswahl = auswahl ? +auswahl : null }
    return o
  }

  function rahmen(weg, innen) {
    Entwurf.inhalt.innerHTML =
      '<div class="e-rahmen"><header class="e-kopf">' +
      '<div class="e-weg">' + weg + '</div>' +
      '<div class="e-reiter" role="tablist" aria-label="Ebenen">' +
      REITER.map(function (r, i) {
        return (i === 3 ? '<span class="e-trenn"></span>' : '') +
          '<button role="tab" data-r="' + r[0] + '" aria-selected="' + (aktiv === r[0]) + '">' + r[1] + '</button>'
      }).join('') +
      '</div>' +
      '<a class="e-kommentare" href="#/kommentare">Kommentare (' + DATEN.kommentare.length + ')</a>' +
      '</header>' + innen + '</div>'
  }

  function reiterBinden(neu) {
    Entwurf.inhalt.querySelectorAll('[data-r]').forEach(function (b) {
      b.addEventListener('click', function () { aktiv = b.getAttribute('data-r'); neu() })
    })
  }

  function karteHtml(t) {
    var s = Karte.zaehle(stand(), t.id)
    var v = Karte.zaehle('vorstufe', t.id)
    var anteil = Math.round(100 * v.unsicher / Math.max(1, v.segmente))
    return '<a class="e-karte" data-tk="' + t.id + '" href="#/kachel/' + t.id + '">' +
      '<h3>' + esc(t.name) + '<span>' + esc(t.lage) + '</span></h3>' +
      '<div class="e-zahlen">' +
      '<div><b>' + v.segmente + '</b>Segmente</div>' +
      '<div class="e-warn"><b>' + v.unsicher + '</b>unsicher</div>' +
      '<div><b>' + s.kandidaten + '</b>Kandidaten</div>' +
      '<div class="' + (s.naht ? 'e-fehler' : '') + '"><b>' + s.naht + '</b>Nähte</div>' +
      '</div><div class="e-balken" title="Anteil unsicher"><i style="width:' + anteil + '%"></i></div></a>'
  }

  function uebersicht() {
    var gesamt = DATEN.teilkacheln.reduce(function (a, t) {
      var z = Karte.zaehle('vorstufe', t.id)
      a.seg += z.segmente; a.uns += z.unsicher; a.naht += Karte.zaehle(stand(), t.id).naht
      return a
    }, { seg: 0, uns: 0, naht: 0 })
    var luecken = Karte.zaehle(stand()).luecken
    rahmen('<b>Testfenster T0</b><span>' + esc(DATEN.fenster.kachel) + ' · ' + DATEN.fenster.breite + ' × ' + DATEN.fenster.hoehe + ' px</span>',
      '<div class="e-uebersicht"><div class="e-feld"><canvas aria-label="Testfenster T0 mit vier Teilkacheln"></canvas>' +
      '<span class="e-hinweis">Teilkachel anklicken, um hineinzugehen</span></div>' +
      '<aside class="e-seite"><div class="e-summe"><b>' + gesamt.seg + '</b> Segmente · <b>' + gesamt.uns + '</b> unsicher · <b>' +
      luecken + '</b> Lücken · <b>' + gesamt.naht + '</b> Nähte</div>' +
      DATEN.teilkacheln.map(karteHtml).join('') +
      '<span class="e-offen">Offen: Zahlen je Teilkachel erst nach dem Lauf</span></aside></div>')
    var cv = Entwurf.inhalt.querySelector('canvas')
    function zeichne() { Karte.passe(cv); Karte.zeichne(cv, optionen(null)) }
    zeichne()
    function teilkachelBei(ev) {
      var p = Karte.punkt(cv, [0, 0, 1000, 1000], ev)
      return DATEN.teilkacheln.filter(function (t) {
        return p[0] >= t.kern[0] && p[0] < t.kern[0] + t.kern[2] && p[1] >= t.kern[1] && p[1] < t.kern[1] + t.kern[3]
      })[0]
    }
    cv.addEventListener('click', function (ev) { var t = teilkachelBei(ev); if (t) Entwurf.gehe(['', 'kachel', t.id].join('/')) })
    cv.addEventListener('mousemove', function (ev) {
      var t = teilkachelBei(ev)
      Entwurf.inhalt.querySelectorAll('.e-karte').forEach(function (k) {
        k.classList.toggle('e-hervor', !!t && k.getAttribute('data-tk') === t.id)
      })
    })
    reiterBinden(uebersicht)
  }

  function kachel(tkId, auswahl) {
    var t = Karte.teilkachel(tkId) || DATEN.teilkacheln[0]
    var st = stand()
    var z = Karte.zaehle(st, t.id)
    var segs = Karte.segmente(st, t.id).slice().sort(function (a, b) { return b.flaeche - a.flaeche }).slice(0, 12)
    var seg = auswahl ? Karte.segment(st, +auswahl) : null
    var kat = seg ? Karte.klasse(seg.klasse) : null
    rahmen('<a href="#/uebersicht">T0</a><span>›</span><b>' + esc(t.name) + '</b><span>' + esc(t.lage) + '</span>',
      '<div class="e-kachel"><div class="e-feld"><canvas aria-label="' + esc(t.name) + '"></canvas></div>' +
      '<aside class="e-seite">' +
      '<div class="e-nachbarn">' + DATEN.teilkacheln.map(function (x) {
        return '<a href="#/kachel/' + x.id + '"' + (x.id === t.id ? ' aria-current="true"' : '') + '>' + esc(x.name) + '</a>'
      }).join('') + '</div>' +
      '<div class="e-summe"><b>' + z.segmente + '</b> Segmente · <b>' + z.unsicher + '</b> unsicher · <b>' + z.luecken + '</b> Lücken · <b>' + z.naht + '</b> Nähte</div>' +
      (seg
        ? '<div class="e-detail"><b>Segment ' + seg.id + '</b><span>' + esc(kat ? kat.name : seg.klasse) + ' (' + esc(seg.klasse) + ')</span>' +
          '<span class="e-leer">' + esc(seg.herkunft) + ' · Sicherheit ' + esc(seg.sicher) + ' · ' + seg.flaeche + ' px</span>' +
          (seg.kandidaten && seg.kandidaten.length ? '<span>' + esc(seg.kandidaten.join(', ')) + '</span>' : '') +
          '<textarea placeholder="Kommentar" aria-label="Kommentar"></textarea>' +
          '<div class="e-pfeile"><button>Kommentar ablegen</button><a href="#/kachel/' + t.id + '">Auswahl aufheben</a></div></div>'
        : '<h4>Größte Segmente</h4>') +
      '<div class="e-liste">' + segs.map(function (s) {
        var k = Karte.klasse(s.klasse)
        return '<button data-s="' + s.id + '" aria-pressed="' + (+auswahl === s.id) + '">' + s.id + ' ' + esc(k ? k.name : s.klasse) + '<span>' + s.flaeche + '</span></button>'
      }).join('') + '</div>' +
      '</aside></div>')
    var cv = Entwurf.inhalt.querySelector('canvas')
    Karte.passe(cv)
    Karte.zeichne(cv, optionen(t, auswahl))
    cv.addEventListener('click', function (ev) {
      var p = Karte.punkt(cv, t.ausschnitt, ev)
      var id = Karte.bei(st, p[0], p[1])
      if (id) Entwurf.gehe(['', 'kachel', t.id, 'segment', id].join('/'))
    })
    Entwurf.inhalt.querySelectorAll('[data-s]').forEach(function (b) {
      b.addEventListener('click', function () { Entwurf.gehe(['', 'kachel', t.id, 'segment', b.getAttribute('data-s')].join('/')) })
    })
    reiterBinden(function () { kachel(tkId, auswahl) })
  }

  Entwurf.route('/', function () { Entwurf.gehe('/uebersicht') })
  Entwurf.route('/uebersicht', uebersicht)
  Entwurf.route('/kachel/:tk', function (p) { kachel(p.tk) })
  Entwurf.route('/kachel/:tk/segment/:id', function (p) { kachel(p.tk, p.id) })
  Entwurf.route('/kommentare', function () {
    rahmen('<a href="#/uebersicht">T0</a><span>›</span><b>Kommentare</b>',
      '<div class="e-komm"><h2>Kommentare</h2>' + DATEN.kommentare.map(function (k) {
        return '<p><a href="#/kachel/' + k.teilkachel + '/segment/' + k.segment + '">Segment ' + k.segment + '</a> ' + esc(k.text) +
          '<small>' + esc(k.zeit) + ' · ' + esc(k.status) + '</small></p>'
      }).join('') + '<button>Als JSON ausgeben</button></div>')
    reiterBinden(function () { Entwurf.gehe('/uebersicht') })
  })
})()

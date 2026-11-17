/* Platz b: Vollbild mit schwebenden Inseln. Das Bild füllt den Schirm, Inseln darüber lassen sich ausblenden. */
(function () {
  'use strict'
  var D = window.DATEN
  var KOMMENTARE = DATEN.kommentare
  var S = { stand: 'vorstufe', ebene: 3, luecken: false, naht: false, geaendert: false, gitter: false,
            zu: { ebenen: false, legende: false, details: false, kommentare: true } }

  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c] }) }
  function btn(attr, text, an) { return '<button ' + attr + ' aria-pressed="' + (an ? 'true' : 'false') + '">' + text + '</button>' }

  function insel(name, titel, inhalt, klasse) {
    if (S.zu[name]) return ''
    return '<section class="i-insel ' + klasse + '" data-insel="' + name + '"><header><b>' + titel +
      '</b><button data-zu="' + name + '" aria-label="' + titel + ' ausblenden">–</button></header><div class="i-koerper">' + inhalt + '</div></section>'
  }

  function leiste() {
    var namen = { ebenen: 'Ebenen', legende: 'Legende', details: 'Details', kommentare: 'Kommentare' }
    return '<div class="i-dock">' + Object.keys(namen).map(function (k) {
      return '<button data-auf="' + k + '" aria-pressed="' + (!S.zu[k]) + '">' + namen[k] + '</button>'
    }).join('') + '</div>'
  }

  function ebenenInsel() {
    var e = D.ebenen.map(function (x) { return btn('data-ebene="' + x.ebene + '"', x.name + ' <small>' + x.klassen + '</small>', S.ebene === x.ebene) }).join('')
    var st = D.staende.map(function (x) { return btn('data-stand="' + x.id + '"', x.id === 'vorstufe' ? 'Vorher' : 'Nachher', S.stand === x.id) }).join('')
    return '<div class="i-zeile"><span>Einteilung</span><div class="i-gruppe">' + e + '</div></div>' +
      '<div class="i-zeile"><span>Stand</span><div class="i-gruppe">' + st + '</div></div>' +
      '<div class="i-zeile"><span>Anzeigen</span><div class="i-gruppe i-umbruch">' +
      btn('data-an="luecken"', 'Lückenkarte', S.luecken) + btn('data-an="naht"', 'Nähte', S.naht) +
      btn('data-an="geaendert"', 'Änderungen', S.geaendert) + btn('data-an="gitter"', 'Gitter', S.gitter) + '</div></div>'
  }

  function legendeInsel(segs) {
    var vor = {}
    segs.forEach(function (s) { var c = Karte.aufEbene(s.klasse, S.ebene); vor[c] = (vor[c] || 0) + 1 })
    return '<ul class="i-legende">' + Object.keys(vor).sort().map(function (c) {
      var k = Karte.klasse(c)
      return '<li><i style="background:' + Karte.farbe(c, S.ebene) + '"></i><span>' + esc(k ? k.name : c) + '</span><em>' + vor[c] + '</em></li>'
    }).join('') + '</ul>'
  }

  function detailsInsel(id) {
    if (!id) return '<p class="i-leise">Segment im Bild anklicken.</p>'
    var s = Karte.segment(S.stand, +id)
    if (!s) return '<p class="i-leise">Segment ' + esc(id) + ' gibt es in diesem Stand nicht.</p>'
    var k = Karte.klasse(s.klasse)
    var ks = D.kommentare.filter(function (c) { return c.segment === s.id && c.stand === S.stand })
    return '<dl class="i-dl"><dt>Segment</dt><dd>' + s.id + '</dd><dt>Klasse</dt><dd>' + esc(k ? k.code + ' ' + k.name : s.klasse) + '</dd>' +
      '<dt>Sicher</dt><dd>' + esc(s.sicher) + (s.wert ? ' (' + s.wert + ')' : '') + '</dd>' +
      '<dt>Herkunft</dt><dd>' + esc(s.herkunft || (s.eingriffe || []).join(', ') || '–') + '</dd>' +
      '<dt>Fläche</dt><dd>' + s.flaeche + ' px</dd></dl>' +
      ((s.kandidaten || []).length ? '<p class="i-hinweis">' + s.kandidaten.map(esc).join(' · ') + '</p>' : '') +
      ks.map(function (c) { return '<p class="i-komm">' + esc(c.text) + '</p>' }).join('') +
      '<textarea rows="3" placeholder="Kommentar zu Segment ' + s.id + '"></textarea>' +
      '<div class="i-gruppe"><button>Vormerken</button><button>Als Mangel</button></div>'
  }

  function kommentarInsel() {
    return '<ol class="i-kl">' + KOMMENTARE.slice(0, 4).map(function (k) {
      return '<li><a href="#/kachel/' + k.teilkachel + '/segment/' + k.segment + '">Segment ' + k.segment + '</a> ' + esc(k.text) + '</li>'
    }).join('') + '</ol><div class="i-gruppe"><a class="i-knopf" href="#/kommentare">Alle ' + D.kommentare.length + '</a><button>Exportieren</button></div>'
  }

  function kopfInsel(t, z) {
    return '<nav class="i-tabs">' + D.teilkacheln.map(function (x) {
      var akt = t && x.id === t.id ? ' aria-current="page"' : ''
      return '<a href="' + '#/kachel/' + x.id + '"' + akt + '>' + x.nummer + '</a>'
    }).join('') + '<a href="#/uebersicht"' + (!t ? ' aria-current="page"' : '') + '>T0</a></nav>' +
      '<span class="i-zahlen">' + z.segmente + ' Segmente · ' + z.unsicher + ' unsicher · ' + z.luecken + ' Lücken · ' + z.naht + ' Naht</span>'
  }

  function seite(t, id) {
    var segs = Karte.segmente(S.stand, t ? t.id : null)
    var z = Karte.zaehle(S.stand, t ? t.id : null)
    var el = Entwurf.inhalt
    el.innerHTML = '<div class="i-wurzel"><canvas class="i-bild" aria-label="Luftbild ' + (t ? t.name : 'Testfenster T0') + '"></canvas>' +
      '<div class="i-kopf">' + kopfInsel(t, z) + '</div>' +
      insel('ebenen', 'Ebenen', ebenenInsel(), 'i-links') +
      insel('legende', 'Legende', legendeInsel(segs), 'i-rechts') +
      (t ? insel('details', 'Details', detailsInsel(id), 'i-details') : '') +
      insel('kommentare', 'Kommentare', kommentarInsel(), 'i-unten') +
      leiste() + '</div>'
    var cv = el.querySelector('canvas')
    var a = t ? t.ausschnitt : [0, 0, 1000, 1000]
    function male() {
      Karte.passe(cv)
      Karte.zeichne(cv, { stand: S.stand, ausschnitt: a, ebene: S.ebene, flaeche: 0.35, luecken: S.luecken, naht: S.naht || !t,
        geaendert: S.geaendert, gitter: S.gitter, kern: t ? t.id : undefined, auswahl: id ? +id : null })
    }
    male()
    window.onresize = male
    el.firstChild.addEventListener('click', function (ev) {
      var b = ev.target.closest('button')
      if (!b) return
      if (b.dataset.zu) S.zu[b.dataset.zu] = true
      else if (b.dataset.auf) S.zu[b.dataset.auf] = !S.zu[b.dataset.auf]
      else if (b.dataset.ebene) S.ebene = +b.dataset.ebene
      else if (b.dataset.stand) S.stand = b.dataset.stand
      else if (b.dataset.an) S[b.dataset.an] = !S[b.dataset.an]
      else return
      seite(t, id)
    })
    cv.addEventListener('click', function (ev) {
      var p = Karte.punkt(cv, a, ev)
      var s = Karte.bei(S.stand, p[0], p[1])
      if (!s) return
      var tk = t || D.teilkacheln.filter(function (x) {
        return p[0] >= x.kern[0] && p[0] < x.kern[0] + x.kern[2] && p[1] >= x.kern[1] && p[1] < x.kern[1] + x.kern[3]
      })[0] || D.teilkacheln[0]
      S.zu.details = false
      Entwurf.gehe(['', 'kachel', t ? t.id : tk.id, 'segment', s].join('/'))
    })
  }

  Entwurf.route('/kachel/:tk', function (p) { seite(Karte.teilkachel(p.tk) || D.teilkacheln[0], null) })
  Entwurf.route('/kachel/:tk/segment/:id', function (p) { seite(Karte.teilkachel(p.tk) || D.teilkacheln[0], p.id) })
  Entwurf.route('/uebersicht', function () { seite(null, null) })
  Entwurf.route('/kommentare', function () {
    Entwurf.inhalt.innerHTML = '<div class="i-wurzel i-dunkel"><section class="i-insel i-mitte"><header><b>Kommentare</b><a class="i-knopf" href="#/kachel/r0c0">Zurück zum Bild</a></header><div class="i-koerper"><ol class="i-kl">' +
      D.kommentare.map(function (k) {
        return '<li><a href="#/kachel/' + k.teilkachel + '/segment/' + k.segment + '">Segment ' + k.segment + '</a> ' + esc(k.text) + ' <em>' + esc(k.status) + '</em></li>'
      }).join('') + '</ol><button>Als JSON exportieren</button></div></section></div>'
  })
})()

/* Platz a: Wie im Stitcher, aufgeräumt. Bild links, feste Leiste rechts (Ebenen, Segmentliste, Kommentarfeld). */
(function () {
  'use strict'
  var D = window.DATEN
  var T0 = DATEN.fenster.name
  var S = { stand: 'vorstufe', ebene: 3, luecken: false, naht: false, geaendert: false, filter: 'alle', kommentare: D.kommentare.slice(), listeTop: 0 }
  var STAENDE = [['vorstufe', 'Vorstufe'], ['runde1', 'Korrektur']]
  var EBENEN = [[1, 'Grob'], [2, 'Mittel'], [3, 'Fein']]
  var FILTER = [['alle', 'Alle'], ['unsicher', 'Unsicher'], ['kandidaten', 'Mit Mangel']]
  var aktuell = null

  function weg(tk, seg) { return '#/' + ['kachel', tk].concat(seg ? ['segment', seg] : []).join('/') }
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c] }) }
  function knoepfe(liste, wert, name) {
    return liste.map(function (x) {
      return '<button type="button" data-' + name + '="' + x[0] + '" aria-pressed="' + (x[0] === wert) + '">' + x[1] + '</button>'
    }).join('')
  }
  function klasseName(code, ebene) {
    var k = Karte.klasse(Karte.aufEbene(code, ebene))
    return k ? k.name : code
  }
  function passtFilter(seg) {
    if (S.filter === 'unsicher') return seg.sicher === 'nein'
    if (S.filter === 'kandidaten') return seg.kandidaten && seg.kandidaten.length > 0
    return true
  }
  function qm(seg) { return Math.round(seg.flaeche * D.fenster.aufloesung * D.fenster.aufloesung).toLocaleString('de-DE') + ' m²' }

  function ansicht(tkId, auswahl) {
    var t = Karte.teilkachel(tkId) || D.teilkacheln[0]
    var id = auswahl ? +auswahl : null
    var seg = id ? Karte.segment(S.stand, id) : null
    var z = Karte.zaehle(S.stand, t.id)
    var alle = Karte.segmente(S.stand, t.id)
    var liste = alle.filter(passtFilter).sort(function (a, b) { return b.flaeche - a.flaeche })
    var meine = id ? S.kommentare.filter(function (k) { return k.segment === id }) : []

    var ebenenKat = {}
    alle.forEach(function (s) { var c = Karte.aufEbene(s.klasse, S.ebene); ebenenKat[c] = (ebenenKat[c] || 0) + s.flaeche })
    var legende = Object.keys(ebenenKat).sort(function (a, b) { return ebenenKat[b] - ebenenKat[a] }).slice(0, 8).map(function (c) {
      return '<span class="a-leg"><i style="background:' + Karte.farbe(c, S.ebene) + '"></i>' + esc(klasseName(c, S.ebene)) + '</span>'
    }).join('')

    Entwurf.inhalt.innerHTML =
      '<div class="a-seite">' +
      '<section class="a-haupt">' +
      '<div class="a-bildrahmen"><canvas class="a-bild" aria-label="Luftbild ' + esc(t.name) + '"></canvas></div>' +
      '<div class="a-fuss">' + legende + '<span class="a-fuss-r">' + z.segmente + ' Segmente · ' + z.unsicher + ' unsicher · ' +
      (z.luecken ? '<b class="a-warn">' + z.luecken + ' Lücken</b>' : 'keine Lücken') + '</span></div>' +
      '</section>' +
      '<aside class="a-leiste">' +
      '<header class="a-kopf"><b>' + esc(t.name) + '</b><span>' + esc(t.lage) + ' · Testfenster ' + esc(T0) + '</span>' +
      '<nav class="a-tk">' + D.teilkacheln.map(function (x) {
        return '<a href="' + weg(x.id) + '"' + (x.id === t.id ? ' aria-current="page"' : '') + '>' + x.nummer + '</a>'
      }).join('') + '<a class="a-uebersicht" href="#/uebersicht">Testfenster</a></nav></header>' +
      '<div class="a-block"><div class="a-zeile"><label>Ebene</label><div class="a-gruppe">' + knoepfe(EBENEN, S.ebene, 'ebene') + '</div></div>' +
      '<div class="a-zeile"><label>Stand</label><div class="a-gruppe">' + knoepfe(STAENDE, S.stand, 'stand') + '</div></div>' +
      '<div class="a-zeile"><label>Zeigen</label><div class="a-gruppe">' +
      '<button type="button" data-an="luecken" aria-pressed="' + S.luecken + '">Lücken</button>' +
      '<button type="button" data-an="naht" aria-pressed="' + S.naht + '">Nähte</button>' +
      '<button type="button" data-an="geaendert" aria-pressed="' + S.geaendert + '">Änderungen</button></div></div></div>' +
      '<div class="a-detail">' + (seg
        ? '<canvas class="a-vorschau" aria-label="Segment ' + seg.id + '"></canvas><div><b>' + esc(klasseName(seg.klasse, 3)) + '</b>' +
          '<span>Segment ' + seg.id + ' · ' + qm(seg) + '</span><span>Herkunft ' + esc(seg.herkunft || 'Korrektur') + ' · Sicherheit ' + (seg.sicher === 'ja' ? 'sicher' : '<b class="a-warn">unsicher</b>') +
          (seg.wert !== undefined ? ' (' + Math.round(seg.wert * 100) + ' %)' : '') + '</span>' +
          (seg.kandidaten && seg.kandidaten.length ? '<span>' + esc(seg.kandidaten.join(', ')) + '</span>' : '') + '</div>'
        : '<p class="a-leise">Segment im Bild oder in der Liste wählen.</p>') + '</div>' +
      '<div class="a-filter"><div class="a-gruppe">' + knoepfe(FILTER, S.filter, 'filter') + '</div><span>' + liste.length + ' Treffer</span></div>' +
      '<ul class="a-liste">' + liste.map(function (s) {
        return '<li><a href="' + weg(t.id, s.id) + '"' + (s.id === id ? ' aria-current="true"' : '') + '>' +
          '<i style="background:' + Karte.farbe(s.klasse, S.ebene) + '"></i><span class="a-name">' + esc(klasseName(s.klasse, S.ebene)) +
          '</span><span class="a-mini">' + qm(s) + '</span>' + (s.sicher === 'nein' ? '<em>unsicher</em>' : '') + '</a></li>'
      }).join('') + (liste.length ? '' : '<li class="a-leise a-leer">Nichts gefunden.</li>') + '</ul>' +
      '<footer class="a-dock">' +
      (meine.length ? '<div class="a-komm">' + meine.map(function (k) { return '<p>' + esc(k.text) + ' <small>' + esc(k.zeit) + '</small></p>' }).join('') + '</div>' : '') +
      '<textarea rows="3" placeholder="' + (seg ? 'Kommentar zu Segment ' + seg.id : 'Erst ein Segment wählen') + '"' + (seg ? '' : ' disabled') + '></textarea>' +
      '<div class="a-zeile"><button type="button" data-aktion="speichern"' + (seg ? '' : ' disabled') + '>Kommentar speichern</button>' +
      '<a class="a-link" href="#/kommentare">Alle Kommentare (' + S.kommentare.length + ')</a></div></footer>' +
      '</aside></div>'

    var el = Entwurf.inhalt
    var cv = el.querySelector('.a-bild')
    var hervor = null
    function neu() {
      Karte.passe(cv)
      Karte.zeichne(cv, {
        stand: S.stand, ausschnitt: t.ausschnitt, ebene: S.ebene, kern: t.id, auswahl: id, hervor: hervor,
        luecken: S.luecken, naht: S.naht, geaendert: S.geaendert, flaeche: 0.3, grau: true,
        filter: S.filter === 'alle' ? null : passtFilter
      })
    }
    neu()
    if (seg) { var vp = el.querySelector('.a-vorschau'); Karte.passe(vp); Karte.vorschau(vp, S.stand, id, { ebene: S.ebene, grau: true }) }
    aktuell = neu
    cv.addEventListener('mousemove', function (ev) {
      var p = Karte.punkt(cv, t.ausschnitt, ev)
      var h = Karte.bei(S.stand, p[0], p[1]) || null
      if (h !== hervor) { hervor = h; neu() }
    })
    cv.addEventListener('click', function (ev) {
      var p = Karte.punkt(cv, t.ausschnitt, ev)
      var h = Karte.bei(S.stand, p[0], p[1])
      if (h) Entwurf.gehe(weg(t.id, h).slice(1))
    })
    var ul = el.querySelector('.a-liste')
    ul.scrollTop = S.listeTop
    ul.addEventListener('scroll', function () { S.listeTop = ul.scrollTop })
    var cur = ul.querySelector('[aria-current="true"]')
    if (cur && (cur.offsetTop < ul.scrollTop || cur.offsetTop > ul.scrollTop + ul.clientHeight - 30)) ul.scrollTop = cur.offsetTop - 60

    function neuZeichnen() { ansicht(t.id, id) }
    function setze(sel, fn) { el.querySelectorAll(sel).forEach(function (b) { b.addEventListener('click', function () { fn(b); neuZeichnen() }) }) }
    setze('[data-ebene]', function (b) { S.ebene = +b.getAttribute('data-ebene') })
    setze('[data-stand]', function (b) { S.stand = b.getAttribute('data-stand') })
    setze('[data-filter]', function (b) { S.filter = b.getAttribute('data-filter'); S.listeTop = 0 })
    setze('[data-an]', function (b) { var k = b.getAttribute('data-an'); S[k] = !S[k] })
    var sp = el.querySelector('[data-aktion="speichern"]')
    sp.addEventListener('click', function () {
      var ta = el.querySelector('textarea')
      if (!ta.value.trim() || !seg) return
      S.kommentare.push({ nr: S.kommentare.length + 1, teilkachel: t.id, stand: S.stand, segment: id, text: ta.value.trim(), status: 'offen', zeit: 'jetzt' })
      neuZeichnen()
    })
  }

  window.addEventListener('resize', function () { if (aktuell && document.querySelector('.a-bild')) aktuell() })

  Entwurf.route('/kachel/:tk', function (p) { ansicht(p.tk) })
  Entwurf.route('/kachel/:tk/segment/:id', function (p) { ansicht(p.tk, p.id) })

  Entwurf.route('/uebersicht', function () {
    aktuell = null
    var el = Entwurf.inhalt
    el.innerHTML =
      '<div class="a-seite"><section class="a-haupt"><div class="a-bildrahmen"><canvas class="a-bild" aria-label="Testfenster T0"></canvas></div>' +
      '<div class="a-fuss"><span>Nähte gestrichelt, Verstöße rosa</span></div></section>' +
      '<aside class="a-leiste"><header class="a-kopf"><b>Testfenster ' + esc(T0) + '</b><span>' + D.fenster.breite + ' × ' + D.fenster.hoehe + ' Bildpunkte · 4 Teilkacheln</span></header>' +
      '<ul class="a-liste">' + D.teilkacheln.map(function (x) {
        var zz = Karte.zaehle('vorstufe', x.id)
        return '<li><a href="' + weg(x.id) + '"><span class="a-name">' + esc(x.name) + ' · ' + esc(x.lage) + '</span><span class="a-mini">' + zz.segmente + ' Segmente · ' + zz.unsicher + ' unsicher · ' + zz.naht + ' Nahtverstöße</span></a></li>'
      }).join('') + '</ul></aside></div>'
    var cv = el.querySelector('.a-bild')
    Karte.passe(cv)
    Karte.zeichne(cv, { stand: 'runde1', ausschnitt: [0, 0, 1000, 1000], naht: true, flaeche: 0.25, grau: true })
  })

  Entwurf.route('/kommentare', function () {
    aktuell = null
    var el = Entwurf.inhalt
    el.innerHTML = '<div class="a-text"><h1>Kommentare</h1><p><button type="button" data-aktion="export">Als JSON exportieren</button> <a href="#/kachel/r0c0">Zurück zum Bild</a></p>' +
      '<ul class="a-kommliste">' + S.kommentare.map(function (k) {
        return '<li><a href="' + weg(k.teilkachel, k.segment) + '">Segment ' + k.segment + '</a> <small>' + esc(k.zeit) + ' · ' + esc(k.status) + '</small><p>' + esc(k.text) + '</p></li>'
      }).join('') + '</ul></div>'
    el.querySelector('[data-aktion="export"]').addEventListener('click', function () {
      var a = document.createElement('a')
      a.href = URL.createObjectURL(new Blob([JSON.stringify(S.kommentare, null, 2)], { type: 'application/json' }))
      a.download = 'kommentare.json'
      a.click()
    })
  })
})()

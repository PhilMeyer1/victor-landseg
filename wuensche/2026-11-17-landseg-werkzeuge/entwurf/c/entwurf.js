/* Platz c: Vorher und Nachher nebeneinander. Vorstufe links, Korrektur rechts, beide Bilder gekoppelt
   (Zoom, Verschieben, Auswahl), Steuerung in einer Leiste darunter.

   /kachel/:tk                Teilkachel, links Vorstufe, rechts Korrektur Runde 1
   /kachel/:tk/segment/:id    dasselbe, ein Segment der Korrektur gewählt (links dessen Vorstufen-Segmente)
   /uebersicht                ganzes Testfenster T0 mit den vier Teilkacheln und den Nähten
   /kommentare                Kommentare der Prüfung, Export als JSON */
(function () {
  'use strict'
  var D = window.DATEN; var TK = window.DATEN.teilkacheln
  var el = function (t, c, h) { var e = document.createElement(t); if (c) e.className = c; if (h !== undefined) e.innerHTML = h; return e }

  // Einstellungen bleiben beim Seitenwechsel
  var S = { ebene: 3, flaeche: 0.25, umriss: true, luecken: false, naht: true, geaendert: true, unsicher: false, gitter: false }
  var neu = []   // vorgemerkte Kommentare dieser Sitzung

  function name(code) { var k = Karte.klasse(code); return k ? code + ' ' + k.name : code }
  function punkt(farbe) { return '<i class="c-punkt" style="background:' + farbe + '"></i>' }

  function kopf(aktiv, tk) {
    var h = el('header', 'c-kopf')
    h.innerHTML = '<b>Testfenster T0</b>' +
      '<nav aria-label="Teilkacheln">' +
      '<a href="#/uebersicht"' + (aktiv === 'uebersicht' ? ' aria-current="page"' : '') + '>Übersicht</a>' +
      D.teilkacheln.map(function (x) {
        return '<a href="#/kachel/' + x.id + '"' + (aktiv === 'kachel' && tk === x.id ? ' aria-current="page"' : '') + '>' + x.name + '</a>'
      }).join('') + '</nav>' +
      '<span class="c-rechts"><a href="#/kommentare"' + (aktiv === 'kommentare' ? ' aria-current="page"' : '') + '>Kommentare (' + (D.kommentare.length + neu.length) + ')</a></span>'
    return h
  }

  function ansicht(tk, auswahl) {
    var t = Karte.teilkachel(tk) || D.teilkacheln[0]
    var sel = auswahl ? Karte.segment('runde1', +auswahl) : null
    var Z = { a: t.ausschnitt.slice(), sel: sel, hover: null }
    var zv = Karte.zaehle('vorstufe', t.id), zk = Karte.zaehle('runde1', t.id)

    var wurzel = el('div', 'c-seite')
    wurzel.appendChild(kopf('kachel', t.id))

    var paar = el('div', 'c-paar')
    function tafel(stand, titel, z, hinweis) {
      var d = Karte.stand(stand)
      var f = el('figure', 'c-tafel')
      f.innerHTML = '<figcaption><b>' + titel + '</b><span>' + d.zeit + '</span><span>' + z.segmente + ' Segmente · ' + z.unsicher + ' unsicher</span>' + hinweis + '</figcaption>'
      var cv = el('canvas', 'c-bild'); cv.setAttribute('aria-label', titel + ', ' + t.name)
      f.appendChild(cv)
      paar.appendChild(f)
      return cv
    }
    var cvL = tafel('vorstufe', 'Vorher: Vorstufe', zv, '<span class="c-warn">' + Karte.stand('vorstufe').pruefen.nicht_zusammenhaengend + ' nicht zusammenhängend</span>')
    var cvR = tafel('runde1', 'Nachher: Korrektur Runde 1', zk, '<span class="c-ok">pruefen: ok</span>')
    wurzel.appendChild(paar)

    // Leiste darunter
    var leiste = el('section', 'c-leiste')
    leiste.setAttribute('aria-label', 'Steuerung')
    leiste.innerHTML =
      '<div class="c-zeile">' +
      '<div class="c-gruppe"><span class="c-etikett">Ebene</span>' +
      D.ebenen.map(function (e) { return '<button data-ebene="' + e.ebene + '" aria-pressed="' + (S.ebene === e.ebene) + '">' + e.name + ' · ' + e.klassen + '</button>' }).join('') + '</div>' +
      '<div class="c-gruppe"><span class="c-etikett">Zeigen</span>' +
      '<button data-schalter="flaeche" aria-pressed="' + (S.flaeche > 0) + '">Flächen</button>' +
      '<button data-schalter="umriss" aria-pressed="' + S.umriss + '">Umriss</button>' +
      '<button data-schalter="geaendert" aria-pressed="' + S.geaendert + '">Änderungen</button>' +
      '<button data-schalter="luecken" aria-pressed="' + S.luecken + '">Lücken</button>' +
      '<button data-schalter="naht" aria-pressed="' + S.naht + '">Nähte (' + zk.naht + ')</button>' +
      '<button data-schalter="unsicher" aria-pressed="' + S.unsicher + '">Nur unsicher</button>' +
      '<button data-schalter="gitter" aria-pressed="' + S.gitter + '">Gitter</button></div>' +
      '<div class="c-gruppe"><span class="c-etikett">Bild</span>' +
      '<button data-zoom="0.5" aria-label="Verkleinern">−</button><button data-zoom="fit">Ganz</button><button data-zoom="2" aria-label="Vergrößern">+</button></div>' +
      '</div>' +
      '<div class="c-zeile c-unten">' +
      '<div class="c-detail" data-detail></div>' +
      '<form class="c-komm" data-komm><textarea rows="2" placeholder="Kommentar zum gewählten Segment" aria-label="Kommentar"></textarea>' +
      '<button type="submit">Vormerken</button><button type="button" data-export>Export (JSON)</button></form>' +
      '</div>'
    wurzel.appendChild(leiste)
    Entwurf.inhalt.innerHTML = ''
    Entwurf.inhalt.appendChild(wurzel)

    function opt(stand) {
      var o = {
        stand: stand, ausschnitt: Z.a, ebene: S.ebene, flaeche: S.flaeche, umriss: S.umriss,
        luecken: S.luecken, gitter: S.gitter, kern: t.id, hervor: Z.hover
      }
      if (stand === 'runde1') {
        o.naht = S.naht; o.geaendert = S.geaendert
        if (Z.sel) o.auswahl = Z.sel.id
        if (S.unsicher) o.filter = function (s) { return s.sicher === 'nein' }
      } else {
        if (Z.sel) { var aus = Z.sel.aus || []; o.filter = function (s) { return aus.indexOf(s.id) >= 0 } }
        else if (S.unsicher) o.filter = function (s) { return s.sicher === 'nein' }
      }
      return o
    }
    function zeichne() {
      Karte.passe(cvL); Karte.passe(cvR)
      Karte.zeichne(cvL, opt('vorstufe'))
      Karte.zeichne(cvR, opt('runde1'))
    }
    var plan = 0
    function spaeter() { if (!plan) plan = requestAnimationFrame(function () { plan = 0; zeichne() }) }

    function detail() {
      var d = leiste.querySelector('[data-detail]')
      var b = leiste.querySelector('[data-komm] textarea')
      if (!Z.sel) {
        d.innerHTML = '<span class="c-leise">Segment im Bild anklicken. Links die Vorstufe, rechts das Ergebnis der Korrektur.</span>'
        b.disabled = true
        return
      }
      b.disabled = false
      var s = Z.sel
      var vor = (s.aus || []).map(function (id) { return Karte.segment('vorstufe', id) }).filter(Boolean)
      var unsicher = vor.filter(function (x) { return x.sicher === 'nein' }).length
      d.innerHTML =
        '<div class="c-karte"><b>Nachher · Segment ' + s.id + '</b>' + punkt(Karte.farbe(s.klasse, 3)) + name(s.klasse) +
        '<span>' + s.flaeche + ' px² · ' + (s.sicher === 'nein' ? 'unsicher' : 'sicher') + '</span></div>' +
        '<div class="c-karte"><b>Vorher · ' + vor.length + ' Segment' + (vor.length === 1 ? '' : 'e') + '</b>' +
        '<span>' + vor.slice(0, 6).map(function (x) { return x.id }).join(', ') + (vor.length > 6 ? ' …' : '') + ' · ' + unsicher + ' unsicher</span></div>' +
        '<div class="c-karte"><b>Eingriffe</b><span>' + ((s.eingriffe || []).join('; ') || 'keine') + '</span></div>'
    }
    detail()

    // Zoom und Verschieben, für beide Bilder gleich
    function faktor(f, p) {
      var a = Z.a
      var w = Math.max(40, Math.min(628, a[2] / f)), h = w * a[3] / a[2]
      f = a[2] / w
      Z.a = [p[0] - (p[0] - a[0]) / f, p[1] - (p[1] - a[1]) / f, w, h]
      spaeter()
    }
    function mitte() { return [Z.a[0] + Z.a[2] / 2, Z.a[1] + Z.a[3] / 2] }
    ;[cvL, cvR].forEach(function (cv, i) {
      var stand = i ? 'runde1' : 'vorstufe'
      var zieh = null
      cv.addEventListener('wheel', function (ev) {
        ev.preventDefault()
        faktor(ev.deltaY < 0 ? 1.25 : 0.8, Karte.punkt(cv, Z.a, ev))
      }, { passive: false })
      cv.addEventListener('pointerdown', function (ev) {
        zieh = { x: ev.clientX, y: ev.clientY, a: Z.a.slice(), bewegt: false }
        cv.setPointerCapture(ev.pointerId)
      })
      cv.addEventListener('pointermove', function (ev) {
        if (zieh) {
          var dx = ev.clientX - zieh.x, dy = ev.clientY - zieh.y
          if (Math.abs(dx) + Math.abs(dy) > 4) zieh.bewegt = true
          if (zieh.bewegt) {
            var r = cv.getBoundingClientRect()
            var s = Math.min(r.width / zieh.a[2], r.height / zieh.a[3])
            Z.a = [zieh.a[0] - dx / s, zieh.a[1] - dy / s, zieh.a[2], zieh.a[3]]
            spaeter()
          }
          return
        }
        var p = Karte.punkt(cv, Z.a, ev)
        var id = Karte.bei(stand, p[0], p[1])
        if (stand === 'runde1' && id !== Z.hover) { Z.hover = id; spaeter() }
        else if (stand === 'vorstufe') {
          var j = Karte.bei('runde1', p[0], p[1])
          if (j !== Z.hover) { Z.hover = j; spaeter() }
        }
      })
      cv.addEventListener('pointerleave', function () { if (!zieh && Z.hover) { Z.hover = null; spaeter() } })
      cv.addEventListener('pointerup', function (ev) {
        var z = zieh; zieh = null
        if (!z || z.bewegt) return
        var p = Karte.punkt(cv, Z.a, ev)
        var id = Karte.bei('runde1', p[0], p[1])   // an derselben Stelle gilt das Segment der Korrektur
        if (id) Entwurf.gehe(['', 'kachel', t.id, 'segment', id].join('/'))
      })
    })

    // Leiste
    leiste.addEventListener('click', function (ev) {
      var b = ev.target.closest('button')
      if (!b) return
      if (b.dataset.ebene) {
        S.ebene = +b.dataset.ebene
        leiste.querySelectorAll('[data-ebene]').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)) })
      } else if (b.dataset.schalter) {
        var k = b.dataset.schalter
        S[k] = k === 'flaeche' ? (S.flaeche > 0 ? 0 : 0.25) : !S[k]
        b.setAttribute('aria-pressed', String(k === 'flaeche' ? S.flaeche > 0 : S[k]))
      } else if (b.dataset.zoom) {
        if (b.dataset.zoom === 'fit') Z.a = t.ausschnitt.slice(); else faktor(+b.dataset.zoom, mitte())
      } else if (b.hasAttribute('data-export')) {
        var daten = JSON.stringify(D.kommentare.concat(neu), null, 2)
        var a = el('a'); a.href = URL.createObjectURL(new Blob([daten], { type: 'application/json' })); a.download = 'kommentare.json'
        a.click(); return
      }
      spaeter()
    })
    leiste.querySelector('[data-komm]').addEventListener('submit', function (ev) {
      ev.preventDefault()
      var ta = ev.target.querySelector('textarea')
      if (!Z.sel || !ta.value.trim()) return
      neu.push({ nr: D.kommentare.length + neu.length + 1, teilkachel: t.id, stand: 'runde1', segment: Z.sel.id, text: ta.value.trim(), status: 'offen', zeit: 'jetzt' })
      ta.value = ''
      wurzel.querySelector('.c-rechts a').textContent = 'Kommentare (' + (D.kommentare.length + neu.length) + ')'
    })

    window.addEventListener('resize', spaeter)
    spaeter()
  }

  Entwurf.route('/kachel/:tk', function (p) { ansicht(p.tk) })
  Entwurf.route('/kachel/:tk/segment/:id', function (p) { ansicht(p.tk, p.id) })

  Entwurf.route('/uebersicht', function () {
    var w = el('div', 'c-seite')
    w.appendChild(kopf('uebersicht'))
    var m = el('div', 'c-uebersicht')
    var cvA = el('canvas', 'c-bild'); cvA.setAttribute('aria-label', 'Testfenster T0, Vorstufe')
    var cvB = el('canvas', 'c-bild'); cvB.setAttribute('aria-label', 'Testfenster T0, Korrektur')
    ;[['Vorher: Vorstufe', cvA], ['Nachher: Korrektur Runde 1', cvB]].forEach(function (x) {
      var f = el('figure', 'c-tafel'); f.innerHTML = '<figcaption><b>' + x[0] + '</b></figcaption>'; f.appendChild(x[1]); m.appendChild(f)
    })
    w.appendChild(m)
    var n = Karte.stand('runde1').naht
    var l = el('section', 'c-leiste')
    l.innerHTML = '<div class="c-zeile"><b>Nähte: ' + n.length + ' Verstöße</b>' +
      n.map(function (x) { return '<span class="c-karte">' + x.grenze + ' · ' + x.art + ' · ' + x.von + '–' + x.bis + '</span>' }).join('') + '</div>' +
      '<div class="c-zeile">' + D.teilkacheln.map(function (x) {
        return '<a class="c-karte" href="#/kachel/' + x.id + '"><b>' + x.name + '</b> ' + x.vorstufe.segmente + ' → ' + x.korrektur.segmente + ' Segmente</a>'
      }).join('') + '</div>'
    w.appendChild(l)
    Entwurf.inhalt.innerHTML = ''
    Entwurf.inhalt.appendChild(w)
    function z() {
      Karte.passe(cvA); Karte.passe(cvB)
      Karte.zeichne(cvA, { stand: 'vorstufe', ausschnitt: [0, 0, 1000, 1000], flaeche: 0.25, naht: true })
      Karte.zeichne(cvB, { stand: 'runde1', ausschnitt: [0, 0, 1000, 1000], flaeche: 0.25, naht: true, geaendert: true })
    }
    z(); window.addEventListener('resize', z)
  })

  Entwurf.route('/kommentare', function () {
    var w = el('div', 'c-seite')
    w.appendChild(kopf('kommentare'))
    var alle = D.kommentare.concat(neu)
    var l = el('div', 'c-liste')
    l.innerHTML = '<b>Kommentare</b>' + alle.map(function (k) {
      return '<p><a href="#/kachel/' + k.teilkachel + '/segment/' + k.segment + '">Segment ' + k.segment + '</a> · ' + k.teilkachel + ' · ' + k.zeit + '<br>' + k.text + '</p>'
    }).join('')
    w.appendChild(l)
    Entwurf.inhalt.innerHTML = ''
    Entwurf.inhalt.appendChild(w)
  })
})()

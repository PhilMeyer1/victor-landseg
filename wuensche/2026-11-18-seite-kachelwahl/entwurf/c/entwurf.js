/* Platz c: Lageplan im Bild. Die Wahl der Teilkacheln liegt als Einblendung in der rechten oberen Bildecke
   (2 × 2-Raster in der Lage der Teilkacheln, mit Miniatur und „oben links“ usw., darunter „Ganzer
   Ausschnitt“); über dem Bild steht groß „Teilkachel n von 4“ mit vorige/nächste. Pfeiltasten links/rechts
   gehen durch die vier Teilkacheln (nie in Eingabefeldern). Der Kopf verliert die kleinen Textlinks und
   behält seine Höhe; die Zeile über dem Bild ist in allen Zuständen gleich hoch, das Bild springt nicht. */
(function () {
  'use strict'
  var D = window.DATEN
  var esc = Seite.esc
  var ZU = false // Lageplan eingeklappt (bleibt über Wechsel von Teilkachel und Fassung)

  var TK = window.DATEN.teilkacheln.slice().sort(function (a, b) { return a.nr - b.nr })
  function nr(tk) { for (var i = 0; i < TK.length; i++) if (TK[i].id === tk) return i + 1; return 0 }
  function lage(t) { return t.lage || ((t.zeile ? 'unten' : 'oben') + ' ' + (t.spalte ? 'rechts' : 'links')) }

  // --- Kopf: wie heute, ohne die kleinen Textlinks (die Wahl liegt im Bild) ----------------------------------
  Seite.kopf = function (K, art) {
    var h = Seite.el('header', 'c-kopf c-kopf-c')
    h.innerHTML = '<b>Ausschnitt ' + esc(window.DATEN.ausschnitt.name) + '</b>' + Seite.fassungen(K, art) +
      Seite.kommentarLink() + Seite.beschreibung(K, art)
    return h
  }

  // --- Schritt-Knöpfe vorige / nächste (Links, am Ende abgeschaltet) -----------------------------------------
  function schritt(pfad, richtung, titel) {
    var inhalt = richtung < 0 ? '<span aria-hidden="true">‹</span><span class="c-wort">vorige</span>'
      : '<span class="c-wort">nächste</span><span aria-hidden="true">›</span>'
    var name = richtung < 0 ? 'vorige Teilkachel' : 'nächste Teilkachel'
    if (!pfad) return '<span class="c-schritt" aria-disabled="true" aria-label="' + name + '">' + inhalt + '</span>'
    return '<a class="c-schritt" href="#' + pfad + '" aria-label="' + name + '" title="' + esc(titel) + ' (Pfeiltaste ' + (richtung < 0 ? '←' : '→') + ')">' + inhalt + '</a>'
  }
  function nachbar(K, n, d) {
    var t = TK[n - 1 + d]
    return t ? { pfad: Seite.pfadKachel(K, t.id), titel: 'Teilkachel ' + (n + d) + ', ' + lage(t) } : { pfad: null, titel: '' }
  }

  // --- große Zeile über dem Bild: „Teilkachel n von 4“ -----------------------------------------------------------
  function zeileKachel(K, tk) {
    var t = Seite.teilkachel(tk), st = Seite.stand(K, tk), n = nr(tk)
    var vor = nachbar(K, n, -1), nach = nachbar(K, n, 1)
    var info = '<span class="c-lage">' + esc(lage(t)) + '</span><span class="c-kenn">' + esc(tk) + '</span>'
    if (st) {
      info += '<span>' + st.segmente + ' Segmente, ' + st.unsicher + ' davon unsicher</span>' +
        (st.luecken ? '<span class="c-fehler">' + st.luecken + ' Bildpunkte ohne Segment</span>' : '<span class="c-ok">lückenlos</span>') +
        (st.naht ? '<span class="c-warn">' + st.naht + ' Stellen an Nähten passen nicht</span>' : '<span>Nähte passen</span>')
    } else {
      info += '<span class="c-warn">Fassung ' + esc(K) + ' ohne Daten</span>'
    }
    return schritt(vor.pfad, -1, vor.titel) +
      '<div class="c-titel"><b class="c-gross">Teilkachel <em>' + n + '</em> von ' + TK.length + '</b><span class="c-unter">' + info + '</span></div>' +
      schritt(nach.pfad, 1, nach.titel)
  }
  function zeileGanz(K) {
    var f = Seite.fassung(K), verst = 0
    TK.forEach(function (t) { var st = Seite.stand(K, t.id); if (st) verst += st.naht })
    var info = '<span class="c-lage">alle ' + TK.length + ' Teilkacheln</span>' +
      (verst ? '<span class="c-warn">' + verst + ' Stellen an Nähten passen nicht</span>' : '<span class="c-ok">Nähte passen</span>') +
      '<span>' + f.naehte + ' Nähte zwischen Teilkacheln</span><span>Klick in ein Viertel öffnet die Teilkachel</span>'
    var erste = TK[0]
    return schritt(null, -1) +
      '<div class="c-titel"><b class="c-gross">Ganzer Ausschnitt <em>' + esc(window.DATEN.ausschnitt.name) + '</em></b><span class="c-unter">' + info + '</span></div>' +
      schritt(Seite.pfadKachel(K, erste.id), 1, 'Teilkachel 1, ' + lage(erste))
  }
  function setzeZeile(feld, html) {
    var cap = feld.closest('figure').querySelector('figcaption')
    cap.className = 'c-zeile'
    cap.innerHTML = html
  }

  // --- Lageplan in der Bildecke ---------------------------------------------------------------------------------
  function lageplan(K, art, tk) {
    var n = art === 'kachel' ? nr(tk) : 0
    var box = Seite.el('div', 'c-lp' + (ZU ? ' c-lp-zu' : ''))
    box.setAttribute('data-lageplan', '')
    box.setAttribute('role', 'navigation')
    box.setAttribute('aria-label', 'Lageplan der Teilkacheln')
    var zellen = TK.map(function (t, i) {
      var aktiv = art === 'kachel' && t.id === tk, st = Seite.stand(K, t.id)
      var titel = 'Teilkachel ' + (i + 1) + ', ' + lage(t) + ' (' + t.id + ') – ' + (st ? st.segmente + ' Segmente' : 'ohne Daten in Fassung ' + K)
      return '<a class="c-lp-zelle' + (st ? '' : ' c-lp-ohne') + '" href="#' + Seite.pfadKachel(K, t.id) + '"' +
        (aktiv ? ' aria-current="page"' : '') + ' title="' + esc(titel) + '" style="grid-row:' + (t.zeile + 1) + ';grid-column:' + (t.spalte + 1) + '">' +
        Seite.miniatur(t.id) + '<span class="c-lp-nr">' + (i + 1) + '</span>' +
        '<span class="c-lp-name">' + (aktiv ? 'hier · ' : '') + esc(lage(t)) + '</span>' +
        (st ? '' : '<span class="c-lp-leer">ohne Daten</span>') + '</a>'
    }).join('')
    var symbol = TK.map(function (t) {
      return '<i style="grid-row:' + (t.zeile + 1) + ';grid-column:' + (t.spalte + 1) + '"' + (art === 'kachel' && t.id === tk ? ' class="c-an"' : '') + '></i>'
    }).join('')
    box.innerHTML =
      '<div class="c-lp-offen">' +
        '<div class="c-lp-kopf"><span>' + TK.length + ' Teilkacheln</span>' +
          '<b>' + (n ? n + ' von ' + TK.length : 'alle') + '</b>' +
          '<button type="button" class="c-lp-knopf" data-lp-zu aria-label="Lageplan einklappen" title="Lageplan einklappen">–</button></div>' +
        '<div class="c-lp-raster">' + zellen + '</div>' +
        '<a class="c-lp-ganz" href="#' + Seite.pfadGanz(K) + '"' + (art === 'uebersicht' ? ' aria-current="page"' : '') + '>Ganzer Ausschnitt</a>' +
        '<p class="c-lp-tasten"><kbd>←</kbd><kbd>→</kbd> blättern</p>' +
      '</div>' +
      '<button type="button" class="c-lp-auf" data-lp-auf aria-label="Lageplan öffnen" title="Lageplan öffnen">' +
        '<span class="c-lp-symbol" aria-hidden="true">' + symbol + '</span><b>' + (n ? n + ' / ' + TK.length : 'alle') + '</b></button>'
    box.addEventListener('click', function (ev) {
      if (ev.target.closest('[data-lp-zu]')) { ZU = true; box.classList.add('c-lp-zu'); box.querySelector('[data-lp-auf]').focus() }
      else if (ev.target.closest('[data-lp-auf]')) { ZU = false; box.classList.remove('c-lp-zu'); box.querySelector('[data-lp-zu]').focus() }
    })
    return box
  }

  // --- Einhängen: Bild der Teilkachel und Ganzer Ausschnitt -------------------------------------------------------
  Seite.titel = function (K, tk) { return '<b>Teilkachel ' + nr(tk) + ' von ' + TK.length + '</b>' }
  Seite.imBild = function (feld, K, tk) {
    setzeZeile(feld, zeileKachel(K, tk))
    feld.appendChild(lageplan(K, 'kachel', tk))
  }
  Seite.inGanz = function (feld, K) {
    setzeZeile(feld, zeileGanz(K))
    // im Bild: jedes Viertel trägt Nummer und Lage, dort wählt man direkt
    feld.querySelectorAll('.c-viertel').forEach(function (a, i) {
      var t = TK.filter(function (x) { return a.style.left === (x.spalte * 50) + '%' && a.style.top === (x.zeile * 50) + '%' })[0] || TK[i]
      var st = Seite.stand(K, t.id)
      if (!st) a.classList.add('c-viertel-ohne')
      a.innerHTML = '<span class="c-marke"><b>' + nr(t.id) + '</b>' + esc(lage(t)) + '<small>' + (st ? st.segmente + ' Segmente' : 'ohne Daten') + '</small></span>'
    })
    feld.appendChild(lageplan(K, 'uebersicht'))
  }

  // --- Pfeiltasten: links/rechts durch die vier Teilkacheln, nie beim Tippen ---------------------------------------
  document.addEventListener('keydown', function (ev) {
    if (ev.ctrlKey || ev.metaKey || ev.altKey || ev.shiftKey || ev.defaultPrevented) return
    if (ev.key !== 'ArrowLeft' && ev.key !== 'ArrowRight') return
    var t = ev.target, tag = t && t.tagName ? t.tagName.toUpperCase() : ''
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || (t && t.isContentEditable)) return
    var m = String(Entwurf.pfad || '').match(/^\/([^/]+)\/(?:kachel\/([^/]+)|uebersicht)/)
    if (!m) return
    var K = m[1], d = ev.key === 'ArrowLeft' ? -1 : 1, ziel
    if (m[2]) { var n = nr(m[2]); ziel = TK[n - 1 + d] }
    else if (d > 0) ziel = TK[0]
    if (!ziel) return
    ev.preventDefault()
    Entwurf.gehe(Seite.pfadKachel(K, ziel.id))
  })

  // --- Routen des Gegenstands ---------------------------------------------------------------------------------------
  Entwurf.route('/:f/kachel/:tk', function (p) { Seite.kachel(p.f, p.tk) })
  Entwurf.route('/:f/kachel/:tk/segment/:id', function (p) { Seite.kachel(p.f, p.tk) })
  Entwurf.route('/:f/uebersicht', function (p) { Seite.ganz(p.f) })
  Entwurf.route('/', function () { Entwurf.gehe(Seite.pfadKachel(D.start.fassung, D.start.teilkachel)) })
})()

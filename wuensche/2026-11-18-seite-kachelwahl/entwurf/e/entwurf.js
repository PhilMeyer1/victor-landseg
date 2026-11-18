/* Platz e: Nachbarn am Bildrand. Gelbe Laschen im abgedunkelten Rand des Bildes zeigen die Nachbar-
   Teilkacheln (Miniatur, Lage, „n von 4“) und führen dorthin; der Kopf trägt eine kleine Übersicht:
   „Ganzer Ausschnitt“, 2 × 2-Raster, „Teilkachel n von 4“, vorige/nächste. Pfeiltasten links/rechts
   blättern, nie in Eingabefeldern. Kopfhöhe in allen Zuständen gleich (entwurf.css). */
(function () {
  'use strict'
  var DATEN = window.DATEN
  var esc = Seite.esc
  var N = DATEN.teilkacheln.length
  var AKT = { K: DATEN.start.fassung, art: 'kachel', tk: DATEN.start.teilkachel }
  var ERST = true

  // Kern: 64 von 628 Bildpunkten Rand je Seite (kern_im_bild), in Prozent des Bildfelds
  var RAND = 10.191, KERN = 79.618
  var RICHTUNG = {
    '-1,-1': ['oben-links', '↖'], '-1,0': ['oben', '↑'], '-1,1': ['oben-rechts', '↗'],
    '0,-1': ['links', '←'], '0,1': ['rechts', '→'],
    '1,-1': ['unten-links', '↙'], '1,0': ['unten', '↓'], '1,1': ['unten-rechts', '↘']
  }

  function an(z, s) { return DATEN.teilkacheln.filter(function (t) { return t.zeile === z && t.spalte === s })[0] || null }
  function index(tk) { for (var i = 0; i < N; i++) if (DATEN.teilkacheln[i].id === tk) return i; return -1 }
  function name(t) { return 'Teilkachel ' + t.nr + ' von ' + N + ', ' + t.lage + ' (' + t.id + ')' }

  // --- Kopf: Fassungen, kleine Kachel-Wahl, Kommentare, Beschreibung ---------------------------------------
  function wahl(K, art, tk) {
    var akt = art === 'kachel' ? Seite.teilkachel(tk) : null
    var raster = DATEN.teilkacheln.map(function (t) {
      var hat = Seite.hatDaten(K, t.id), aktiv = akt && akt.id === t.id
      return '<a class="e-zelle' + (aktiv ? ' e-aktiv' : '') + (hat ? '' : ' e-ohne') + '" href="#' + Seite.pfadKachel(K, t.id) + '"' +
        ' style="grid-row:' + (t.zeile + 1) + ';grid-column:' + (t.spalte + 1) + '"' +
        ' title="' + esc(name(t) + (hat ? '' : ' – ohne Daten')) + '" aria-label="' + esc(name(t)) + '">' + Seite.miniatur(t.id) + '</a>'
    }).join('')
    var stand = akt
      ? '<b>Teilkachel ' + akt.nr + ' von ' + N + '</b><span>' + esc(akt.lage) + ' · ' + esc(akt.id) + '</span>'
      : art === 'uebersicht'
        ? '<b>Ganzer Ausschnitt</b><span>' + N + ' Teilkacheln</span>'
        : '<b>' + N + ' Teilkacheln</b><span>eine wählen</span>'
    var i = akt ? index(akt.id) : -1
    var vorDis = !akt || i === 0, nachDis = akt && i === N - 1
    var f = Seite.fassung(K)
    return '<nav class="e-wahl' + (art === 'uebersicht' ? ' e-imganz' : '') + '" aria-label="Teilkacheln">' +
      '<a class="e-ganz' + (art === 'uebersicht' ? ' e-aktiv' : '') + '" href="#' + Seite.pfadGanz(K) + '" title="Ganzer Ausschnitt ' + esc(DATEN.ausschnitt.name) + '">' +
        '<span class="e-ganzbild" style="background-image:url(&quot;' + f.bild + '&quot;)" aria-hidden="true"></span><span class="e-gtext">Ganzer Ausschnitt</span></a>' +
      '<span class="e-trenn" aria-hidden="true"></span>' +
      '<div class="e-raster" role="group" aria-label="Lage der vier Teilkacheln">' + raster + '</div>' +
      '<div class="e-stand" aria-live="polite">' + stand + '</div>' +
      '<div class="e-schritt">' +
        '<button type="button" data-schritt="-1" aria-label="vorige Teilkachel" title="vorige (Pfeiltaste links)"' + (vorDis ? ' disabled' : '') + '><span aria-hidden="true">‹</span><span class="e-wort"> vorige</span></button>' +
        '<button type="button" data-schritt="1" aria-label="nächste Teilkachel" title="nächste (Pfeiltaste rechts)"' + (nachDis ? ' disabled' : '') + '><span class="e-wort">nächste </span><span aria-hidden="true">›</span></button>' +
      '</div></nav>'
  }

  Seite.kopf = function (K, art, tk) {
    AKT = { K: K, art: art, tk: tk }
    var h = Seite.el('header', 'c-kopf e-kopf')
    h.innerHTML = '<b class="e-name">Ausschnitt ' + esc(DATEN.ausschnitt.name) + '</b>' + Seite.fassungen(K, art) +
      wahl(K, art, tk) + Seite.kommentarLink() + Seite.beschreibung(K, art)
    return h
  }

  // Zeile über dem Bild
  Seite.titel = function (K, tk) {
    var t = Seite.teilkachel(tk)
    return '<b>Teilkachel ' + t.nr + ' von ' + N + ' · ' + esc(t.lage) + '</b><span class="e-kenn">' + esc(t.id) + '</span>'
  }

  // --- Laschen der Nachbarn im Rand des Bildes ----------------------------------------------------------------
  function streifen(r) {
    var d = r.split(',').map(Number), s = Seite.el('div', 'e-streifen')
    s.style.left = (d[1] < 0 ? 0 : d[1] > 0 ? RAND + KERN : RAND) + '%'
    s.style.top = (d[0] < 0 ? 0 : d[0] > 0 ? RAND + KERN : RAND) + '%'
    s.style.width = (d[1] ? RAND : KERN) + '%'
    s.style.height = (d[0] ? RAND : KERN) + '%'
    return s
  }
  function lasche(K, n, r) {
    var richtung = RICHTUNG[r], ecke = r.split(',').every(function (x) { return x !== '0' })
    var hat = Seite.hatDaten(K, n.id)
    var a = Seite.el('a', 'e-lasche ' + (ecke ? 'e-ecke' : 'e-kante') + ' e-' + richtung[0] + (hat ? '' : ' e-ohne'))
    a.setAttribute('href', '#' + Seite.pfadKachel(K, n.id))
    a.setAttribute('aria-label', 'Weiter zur ' + name(n) + (hat ? '' : ', ohne Daten'))
    a.title = 'Weiter: ' + name(n) + (hat ? '' : ' – ohne Daten')
    if (ecke) {
      a.innerHTML = Seite.miniatur(n.id, 'e-lmini') + '<span class="e-pfeil" aria-hidden="true">' + richtung[1] + '</span>'
    } else {
      a.innerHTML = Seite.miniatur(n.id, 'e-lmini') +
        '<span class="e-ltext"><b>' + esc(n.lage) + '</b><small>' + (hat ? n.nr + ' von ' + N : 'ohne Daten') + '</small></span>' +
        '<span class="e-pfeil" aria-hidden="true">' + richtung[1] + '</span>'
    }
    return a
  }
  Seite.imBild = function (feld, K, tk) {
    var t = Seite.teilkachel(tk)
    feld.classList.add('e-feld')
    Object.keys(RICHTUNG).forEach(function (r) {
      var d = r.split(',').map(Number), n = an(t.zeile + d[0], t.spalte + d[1])
      if (!n) return
      var s = streifen(r), a = lasche(K, n, r)
      function zeige(ja) { s.classList.toggle('e-an', ja) }
      a.addEventListener('mouseenter', function () { zeige(true) })
      a.addEventListener('mouseleave', function () { zeige(false) })
      a.addEventListener('focus', function () { zeige(true) })
      a.addEventListener('blur', function () { zeige(false) })
      feld.appendChild(s)
      feld.appendChild(a)
    })
    if (ERST) { feld.classList.add('e-erst'); ERST = false }
  }

  // --- Ganzer Ausschnitt: jedes Viertel beschriftet, die zuletzt gesehene Teilkachel markiert ---------------
  Seite.inGanz = function (feld, K) {
    var zuletzt = Seite.letzt.tk
    ERST = false
    var viertel = feld.querySelectorAll('.c-viertel')
    DATEN.teilkacheln.forEach(function (t, i) {
      var v = viertel[i]; if (!v) return
      var hat = Seite.hatDaten(K, t.id)
      if (t.id === zuletzt) v.classList.add('e-zuletzt')
      if (!hat) v.classList.add('e-ohne')
      v.setAttribute('aria-label', name(t) + ' öffnen' + (hat ? '' : ' (ohne Daten)'))
      v.innerHTML = '<span class="e-schild"><b>' + t.nr + '</b><span>' + esc(t.lage) + '<small>' + esc(t.id) +
        (hat ? '' : ' · ohne Daten') + (t.id === zuletzt ? ' · zuletzt angesehen' : '') + '</small></span></span>'
    })
  }

  // --- vorige / nächste, Pfeiltasten -----------------------------------------------------------------------------
  function schritt(d) {
    var j
    if (AKT.art === 'kachel') j = index(AKT.tk) + d
    else if (d > 0) j = 0
    else return
    if (j < 0 || j >= N) return
    Entwurf.gehe(Seite.pfadKachel(AKT.K, DATEN.teilkacheln[j].id))
  }
  document.addEventListener('click', function (ev) {
    var b = ev.target.closest && ev.target.closest('[data-schritt]')
    if (b && !b.disabled) schritt(+b.dataset.schritt)
  })
  document.addEventListener('keydown', function (ev) {
    var t = ev.target, tag = t && t.tagName
    if (tag === 'TEXTAREA' || tag === 'INPUT' || tag === 'SELECT' || (t && t.isContentEditable)) return
    if (ev.ctrlKey || ev.metaKey || ev.altKey || ev.shiftKey) return
    if (ev.key === 'ArrowRight') { ev.preventDefault(); schritt(1) }
    else if (ev.key === 'ArrowLeft') { ev.preventDefault(); schritt(-1) }
  })

  // Routen des Gegenstands
  Entwurf.route('/:f/kachel/:tk', function (p) { Seite.kachel(p.f, p.tk) })
  Entwurf.route('/:f/kachel/:tk/segment/:id', function (p) { Seite.kachel(p.f, p.tk) })
  Entwurf.route('/:f/uebersicht', function (p) { Seite.ganz(p.f) })
  Entwurf.route('/', function () { Entwurf.gehe(Seite.pfadKachel(DATEN.start.fassung, DATEN.start.teilkachel)) })
})()

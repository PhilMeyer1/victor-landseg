/* Platz d: Schrittleiste unter dem Kopf.
   Unter dem schlanken Kopf (Name, Fassungen, Kommentare) liegt eine eigene breite Leiste über die ganze
   Breite: „Ganzer Ausschnitt“ und die vier Teilkacheln als große Reiter in Lage-Reihenfolge (1 oben links …
   4 unten rechts), je mit Miniatur, Raster-Symbol und Stand; „vorige“ und „nächste“ an den Enden.
   Im Bild ein Fortschritts-Hinweis „Teilkachel n von 4“ mit dem nächsten Schritt; Pfeiltasten ← → gehen
   dieselben Schritte (nicht in Eingabefeldern). Die Leiste hat in allen Zuständen dieselbe Höhe. */
(function () {
  'use strict'
  var DATEN = window.DATEN
  var esc = Seite.esc

  // Reihenfolge der Schritte: Ganzer Ausschnitt, dann die vier Teilkacheln in Lage-Reihenfolge
  var KACHELN = DATEN.teilkacheln.slice().sort(function (a, b) { return a.zeile - b.zeile || a.spalte - b.spalte })
  var ANZAHL = KACHELN.length

  function nummer(tk) { for (var i = 0; i < ANZAHL; i++) if (KACHELN[i].id === tk) return i + 1; return 0 }
  function lage(t) { return t.lage || ('Zeile ' + (t.zeile + 1) + ', Spalte ' + (t.spalte + 1)) }

  // Schritt-Nummer: 0 = Ganzer Ausschnitt, 1 … 4 = Teilkacheln, -1 = keiner (Kommentare)
  function schritt(art, tk) { return art === 'uebersicht' ? 0 : art === 'kachel' ? nummer(tk) : -1 }
  function pfadSchritt(K, n) { return n === 0 ? Seite.pfadGanz(K) : Seite.pfadKachel(K, KACHELN[n - 1].id) }
  function nameSchritt(n) { return n === 0 ? 'Ganzer Ausschnitt' : lage(KACHELN[n - 1]) }

  // Raster-Symbol: 2 × 2 Felder in Lage der Teilkacheln, die gemeinten gelb
  function raster(an) {
    return '<span class="d-raster" aria-hidden="true">' + KACHELN.map(function (t) {
      return '<i' + (an === 'alle' || an === t.id ? ' class="d-an"' : '') + '></i>'
    }).join('') + '</span>'
  }

  // vorige / nächste: Link auf den Nachbarschritt, am Ende ein gesperrter Knopf
  function pfeil(K, n, richtung) {
    var ziel = n < 0 ? -1 : n + richtung
    var wort = richtung < 0 ? 'vorige' : 'nächste'
    var zeichen = richtung < 0 ? '<span class="d-zeichen" aria-hidden="true">‹</span>' : '<span class="d-zeichen" aria-hidden="true">›</span>'
    var klasse = 'd-pfeil d-pfeil-' + (richtung < 0 ? 'zurueck' : 'vor')
    var taste = 'Pfeiltaste ' + (richtung < 0 ? '←' : '→')
    if (ziel < 0 || ziel > ANZAHL) {
      return '<button type="button" class="' + klasse + '" disabled title="' + taste + '">' +
        (richtung < 0 ? zeichen : '') + '<span class="d-pfeiltext"><b>' + wort + '</b><small>' + (n === 0 && richtung < 0 ? 'Anfang' : n === ANZAHL ? 'letzte Teilkachel' : '–') + '</small></span>' +
        (richtung > 0 ? zeichen : '') + '</button>'
    }
    return '<a class="' + klasse + '" href="#' + pfadSchritt(K, ziel) + '" title="' + taste + '" data-schritt="' + ziel + '">' +
      (richtung < 0 ? zeichen : '') + '<span class="d-pfeiltext"><b>' + wort + '</b><small>' + esc(nameSchritt(ziel)) + '</small></span>' +
      (richtung > 0 ? zeichen : '') + '</a>'
  }

  function reiterGanz(K, n) {
    return '<a class="d-reiter d-reiter-ganz' + (n === 0 ? ' d-aktiv' : '') + '" href="#' + Seite.pfadGanz(K) + '" title="Ganzer Ausschnitt ' + esc(DATEN.ausschnitt.name) + '">' +
      '<span class="d-bild"><span class="d-mini d-mini-ganz" style="background-image:url(&quot;' + DATEN.ausschnitt.bild + '&quot;)" aria-hidden="true"></span></span>' +
      '<span class="d-text"><span class="d-ober">' + raster('alle') + 'Übersicht</span><b>Ganzer Ausschnitt</b><span class="d-stand">alle ' + ANZAHL + ' Teilkacheln</span></span></a>'
  }

  function reiter(K, n, t, i) {
    var st = Seite.stand(K, t.id)
    var aktiv = n === i + 1
    return '<a class="d-reiter' + (aktiv ? ' d-aktiv' : '') + (st ? '' : ' d-ohne') + '" href="#' + Seite.pfadKachel(K, t.id) + '" title="Teilkachel ' + (i + 1) + ' von ' + ANZAHL + ': ' + esc(lage(t)) + ' (' + t.id + ')' + (st ? '' : ', ohne Daten') + '">' +
      '<span class="d-bild">' + Seite.miniatur(t.id, 'd-mini') + '<span class="d-nr">' + (i + 1) + '</span></span>' +
      '<span class="d-text"><span class="d-ober">' + raster(t.id) + 'Teilkachel ' + (i + 1) + ' <span class="d-kennung">' + t.id + '</span></span>' +
      '<b>' + esc(lage(t)) + '</b>' +
      '<span class="d-stand">' + (st ? st.segmente + ' Segmente' : 'keine Daten') + '</span></span></a>'
  }

  function schritte(K, art, tk) {
    var n = schritt(art, tk)
    var nav = Seite.el('nav', 'd-schritte')
    nav.setAttribute('aria-label', 'Teilkacheln')
    nav.innerHTML = pfeil(K, n, -1) +
      '<div class="d-spur">' + reiterGanz(K, n) + '<span class="d-trenner" aria-hidden="true"></span>' +
      '<div class="d-vier">' + KACHELN.map(function (t, i) { return reiter(K, n, t, i) }).join('') + '</div></div>' +
      pfeil(K, n, 1)
    return nav
  }

  // Kopf: oben schlank wie heute (ohne die Textlinks), darunter die Schrittleiste
  Seite.kopf = function (K, art, tk) {
    var w = Seite.el('div', 'd-oben')
    var h = Seite.el('header', 'c-kopf')
    h.innerHTML = '<b>Ausschnitt ' + esc(DATEN.ausschnitt.name) + '</b>' + Seite.fassungen(K, art) + '<span></span>' +
      Seite.kommentarLink() + Seite.beschreibung(K, art)
    w.appendChild(h)
    w.appendChild(schritte(K, art, tk))
    return w
  }

  // Zeile über dem Bild: „Teilkachel n von 4 · Lage“
  Seite.titel = function (K, tk) {
    var t = Seite.teilkachel(tk)
    return '<b>Teilkachel ' + nummer(tk) + ' von ' + ANZAHL + ' · ' + esc(lage(t)) + '</b><span class="d-kennung">' + esc(tk) + '</span>'
  }

  // Im Bild: Fortschritt mit dem nächsten Schritt
  Seite.imBild = function (feld, K, tk) {
    var n = nummer(tk)
    var punkte = '<span class="d-punkte" aria-hidden="true">' + KACHELN.map(function (t, i) {
      return '<i class="' + (i + 1 === n ? 'd-hier' : i + 1 < n ? 'd-war' : '') + '"></i>'
    }).join('') + '</span>'
    var weiter = n < ANZAHL
      ? '<a class="d-weiter" href="#' + pfadSchritt(K, n + 1) + '">weiter: ' + esc(nameSchritt(n + 1)) + ' <span aria-hidden="true">›</span></a>'
      : '<a class="d-weiter" href="#' + Seite.pfadGanz(K) + '">alle vier gesehen · Ganzer Ausschnitt <span aria-hidden="true">›</span></a>'
    var hinweis = Seite.el('div', 'd-fortschritt')
    hinweis.innerHTML = '<span class="d-fz">Teilkachel <b>' + n + '</b> von ' + ANZAHL + '</span>' + punkte + weiter +
      '<span class="d-tasten" title="Pfeiltasten wechseln die Teilkachel"><kbd>←</kbd><kbd>→</kbd></span>'
    feld.appendChild(hinweis)
  }

  // Ganzer Ausschnitt: Nummer und Lage in jedem Viertel
  Seite.inGanz = function (feld, K) {
    var viertel = feld.querySelectorAll('.c-viertel')
    DATEN.teilkacheln.forEach(function (t, j) {
      var a = viertel[j]; if (!a) return
      var st = Seite.stand(K, t.id)
      a.innerHTML = '<span class="d-marke' + (st ? '' : ' d-ohne') + '"><span class="d-nr">' + nummer(t.id) + '</span>' + esc(lage(t)) +
        (st ? '' : ' · keine Daten') + '</span>'
    })
  }

  // Pfeiltasten ← →: vorige / nächste, nie beim Tippen
  document.addEventListener('keydown', function (ev) {
    if (ev.key !== 'ArrowLeft' && ev.key !== 'ArrowRight') return
    if (ev.ctrlKey || ev.metaKey || ev.altKey || ev.shiftKey || ev.defaultPrevented) return
    var t = ev.target, tag = t && t.tagName ? t.tagName.toLowerCase() : ''
    if (tag === 'input' || tag === 'textarea' || tag === 'select' || (t && t.isContentEditable)) return
    var a = document.querySelector('.d-schritte .d-pfeil-' + (ev.key === 'ArrowLeft' ? 'zurueck' : 'vor') + '[href]')
    if (!a) return
    ev.preventDefault()
    Entwurf.gehe(a.getAttribute('href').slice(1))
  })

  // Routen des Gegenstands
  Entwurf.route('/:f/kachel/:tk', function (p) { Seite.kachel(p.f, p.tk) })
  Entwurf.route('/:f/kachel/:tk/segment/:id', function (p) { Seite.kachel(p.f, p.tk) })
  Entwurf.route('/:f/uebersicht', function (p) { Seite.ganz(p.f) })
  Entwurf.route('/', function () { Entwurf.gehe(Seite.pfadKachel(DATEN.start.fassung, DATEN.start.teilkachel)) })
})()

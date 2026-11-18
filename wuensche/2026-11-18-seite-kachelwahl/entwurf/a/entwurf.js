/* Platz a: Raster im Kopf. Nah am heutigen Stand: der Kopf wird etwas höher (in allen Zuständen gleich) und
   trägt neben den Fassungen die Kachel-Wahl: „Ganzer Ausschnitt“ als eigene große Wahl, daneben das
   2 × 2-Raster der Teilkacheln in ihrer Lage (Miniatur, „oben links“ …, Kennung klein), rechts davon
   „Teilkachel n von 4“ mit vorige/nächste. Pfeiltasten links/rechts blättern (nie in Eingabefeldern).
   Im Bild weist ein Hinweis am unteren Rand auf die nächste Teilkachel. */
(function () {
  'use strict'
  var D = window.DATEN
  var esc = Seite.esc
  var TK = window.DATEN.teilkacheln.slice().sort(function (a, b) { return a.nr - b.nr })
  var N = TK.length

  function nr(tk) { var t = Seite.teilkachel(tk); return t ? t.nr : 0 }
  function nachNr(n) { return TK[((n - 1) % N + N) % N] }
  function nachbar(tk, schritt) {
    var n = tk ? nr(tk) : (schritt > 0 ? 0 : 1)
    return nachNr(n + schritt)
  }
  function pfeil(richtung) {
    return '<svg class="k-pfeil" viewBox="0 0 16 16" aria-hidden="true"><path d="' +
      (richtung < 0 ? 'M10 3 5 8l5 5' : 'M6 3l5 5-5 5') + '" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
  }

  // --- „Ganzer Ausschnitt“: eigene, gleich große Wahl links vom Raster ------------------------------------
  function ganzWahl(K, art) {
    var an = art === 'uebersicht'
    return '<a class="k-ganz' + (an ? ' ist-an' : '') + '" href="#' + Seite.pfadGanz(K) + '"' + (an ? ' aria-current="page"' : '') + '>' +
      '<span class="k-ganzbild" style="background-image:url(&quot;' + window.DATEN.ausschnitt.bild + '&quot;)" aria-hidden="true">' +
      TK.map(function (t) { return '<i style="left:' + (t.spalte * 50) + '%;top:' + (t.zeile * 50) + '%">' + t.nr + '</i>' }).join('') + '</span>' +
      '<span class="k-ganztext">Ganzer Ausschnitt</span></a>'
  }

  // --- 2 × 2-Raster in der Lage der Teilkacheln ------------------------------------------------------------
  function raster(K, art, tk) {
    return '<div class="k-raster" role="group" aria-label="Teilkacheln in ihrer Lage">' + TK.map(function (t) {
      var st = Seite.stand(K, t.id), an = art === 'kachel' && t.id === tk
      return '<a class="k-zelle' + (an ? ' ist-an' : '') + (st ? '' : ' ist-ohne') + '" href="#' + Seite.pfadKachel(K, t.id) + '"' +
        ' style="grid-row:' + (t.zeile + 1) + ';grid-column:' + (t.spalte + 1) + '"' +
        ' title="Teilkachel ' + t.nr + ' von ' + N + ': ' + esc(t.lage) + ' (' + t.id + ')"' + (an ? ' aria-current="page"' : '') + '>' +
        '<span class="k-mini">' + Seite.miniatur(t.id) + '<i>' + t.nr + '</i></span>' +
        '<span class="k-ztext"><b>' + esc(t.lage) + '</b><small>' + t.id + (st ? '<span class="k-zahl"> · ' + st.segmente + ' Segmente</span>' : ' · keine Daten') + '</small></span></a>'
    }).join('') + '</div>'
  }

  // --- „Teilkachel n von 4“ mit vorige/nächste --------------------------------------------------------------
  function schritt(K, art, tk) {
    var t = art === 'kachel' ? Seite.teilkachel(tk) : null
    var vor = nachbar(t && t.id, -1), nach = nachbar(t && t.id, 1)
    var stelle = t
      ? '<p class="k-stelle">Teilkachel <b>' + t.nr + '</b> von ' + N + '</p><p class="k-lage">' + esc(t.lage) + ' · ' + t.id + '</p>'
      : art === 'uebersicht'
        ? '<p class="k-stelle">Alle <b>' + N + '</b> Teilkacheln</p><p class="k-lage">Ganzer Ausschnitt</p>'
        : '<p class="k-stelle">Teilkachel wählen</p><p class="k-lage">' + N + ' Teilkacheln</p>'
    return '<div class="k-schritt">' + stelle +
      '<div class="k-blaettern">' +
      '<a class="k-knopf" data-schritt="-1" aria-label="vorige Teilkachel" href="#' + Seite.pfadKachel(K, vor.id) + '" title="Pfeiltaste links: ' + esc(vor.lage) + '">' + pfeil(-1) + '<span>vorige</span></a>' +
      '<a class="k-knopf" data-schritt="1" aria-label="nächste Teilkachel" href="#' + Seite.pfadKachel(K, nach.id) + '" title="Pfeiltaste rechts: ' + esc(nach.lage) + '"><span>nächste</span>' + pfeil(1) + '</a>' +
      '</div><p class="k-tasten"><kbd>←</kbd> <kbd>→</kbd> blättern</p></div>'
  }

  function wahl(K, art, tk) {
    return '<nav class="k-wahl" aria-label="Teilkacheln">' + ganzWahl(K, art) + raster(K, art, tk) + schritt(K, art, tk) + '</nav>'
  }

  // --- Kopf: links Name, Fassungen, Beschreibung; rechts die Kachel-Wahl -------------------------------------
  Seite.kopf = function (K, art, tk) {
    var h = Seite.el('header', 'c-kopf k-kopf')
    h.innerHTML = '<div class="k-links"><div class="k-zeile"><b>Ausschnitt ' + esc(D.ausschnitt.name) + '</b>' + Seite.kommentarLink() + '</div>' +
      Seite.fassungen(K, art) + Seite.beschreibung(K, art) + '</div>' + wahl(K, art, tk)
    return h
  }

  // --- Zeile über dem Bild ----------------------------------------------------------------------------------
  Seite.titel = function (K, tk) {
    var t = Seite.teilkachel(tk)
    return '<b>Teilkachel ' + t.nr + ' von ' + N + ' · ' + esc(t.lage) + '</b><span class="k-kennung">' + t.id + '</span>'
  }

  // --- Hinweis im Bild: es geht weiter -----------------------------------------------------------------------
  Seite.imBild = function (feld, K, tk) {
    var t = Seite.teilkachel(tk), nach = nachbar(tk, 1)
    var lage = '<span class="k-lageplan" aria-hidden="true">' + TK.map(function (x) {
      return '<i class="' + (x.id === tk ? 'ist-an' : '') + '" style="grid-row:' + (x.zeile + 1) + ';grid-column:' + (x.spalte + 1) + '"></i>'
    }).join('') + '</span>'
    var a = Seite.el('a', 'k-weiter')
    a.setAttribute('href', '#' + Seite.pfadKachel(K, nach.id))
    a.innerHTML = lage + '<span>Teilkachel ' + t.nr + ' von ' + N + '</span><span class="k-trenn"></span><span class="k-weitertext">' +
      (t.nr < N ? 'Weiter: ' : 'Wieder zu ') + esc(nach.lage) + '</span>' + pfeil(1)
    feld.appendChild(a)
  }

  // --- Ganzer Ausschnitt: die vier Teile beschriftet --------------------------------------------------------
  Seite.inGanz = function (feld, K) {
    TK.forEach(function (t) {
      var st = Seite.stand(K, t.id)
      var m = Seite.el('span', 'k-viertelname' + (st ? '' : ' ist-ohne'), '<b>' + t.nr + '</b>' + esc(t.lage) + (st ? '' : ' · keine Daten'))
      m.style.left = 'calc(' + (t.spalte * 50) + '% + 10px)'; m.style.top = 'calc(' + (t.zeile * 50) + '% + 10px)'
      feld.appendChild(m)
    })
  }

  // --- Pfeiltasten: links/rechts durch die vier Teilkacheln, nie beim Tippen ---------------------------------
  document.addEventListener('keydown', function (ev) {
    if (ev.key !== 'ArrowLeft' && ev.key !== 'ArrowRight') return
    if (ev.ctrlKey || ev.metaKey || ev.altKey || ev.shiftKey || ev.defaultPrevented) return
    var z = ev.target, tag = z && z.tagName
    if (tag === 'TEXTAREA' || tag === 'INPUT' || tag === 'SELECT' || (z && z.isContentEditable)) return
    var m = String(location.hash).match(/^#\/([^/]+)\/(kachel|uebersicht)(?:\/([^/]+))?/)
    var K = m ? m[1] : D.start.fassung, tk = m && m[2] === 'kachel' ? m[3] : null
    ev.preventDefault()
    Entwurf.gehe(Seite.pfadKachel(K, nachbar(tk, ev.key === 'ArrowRight' ? 1 : -1).id))
  })

  // Routen des Gegenstands
  Entwurf.route('/:f/kachel/:tk', function (p) { Seite.kachel(p.f, p.tk) })
  Entwurf.route('/:f/kachel/:tk/segment/:id', function (p) { Seite.kachel(p.f, p.tk) })
  Entwurf.route('/:f/uebersicht', function (p) { Seite.ganz(p.f) })
  Entwurf.route('/', function () { Entwurf.gehe(Seite.pfadKachel(D.start.fassung, D.start.teilkachel)) })
})()

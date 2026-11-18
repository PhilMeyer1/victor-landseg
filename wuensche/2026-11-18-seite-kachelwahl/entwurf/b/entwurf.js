/* Platz b: Lageplan in der linken Leiste.
   Oben in der festen Leiste links steht ein großes 2 × 2-Raster in der Lage der Teilkacheln (Miniatur-Luftbild,
   Nummer, „oben links“ …), darunter „Ganzer Ausschnitt“ als eigene Wahl und „vorige · Teilkachel n von 4 ·
   nächste“ (auch Pfeiltasten links/rechts). Der Kopf bleibt schlank: Name, Fassungen, Ort, Kommentare.
   Im Bild steht im Rand „Teilkachel n von 4“ und ein Knopf zur nächsten Teilkachel.
   Die Wahl hat in allen Zuständen dieselbe Höhe, auch im ganzen Ausschnitt: das Bild springt nicht. */
(function () {
  'use strict'
  var DATEN = window.DATEN
  var esc = Seite.esc, el = Seite.el
  var TK = DATEN.teilkacheln.slice().sort(function (a, b) { return a.nr - b.nr })
  var N = TK.length
  var JETZT = { art: 'kachel', K: DATEN.start.fassung, tk: DATEN.start.teilkachel }

  function index(tk) { for (var i = 0; i < N; i++) if (TK[i].id === tk) return i; return -1 }
  function lage(tk) { var t = Seite.teilkachel(tk); return t ? t.lage : tk }

  // kleines 2 × 2-Symbol, die gezeigte Teilkachel gefüllt
  function symbol(aktiv) {
    return '<span class="b-symbol" aria-hidden="true">' + TK.map(function (t, i) {
      return '<i' + (i === aktiv ? ' class="b-an"' : '') + '></i>'
    }).join('') + '</span>'
  }

  // --- Die Kachel-Wahl (Lageplan, Ganzer Ausschnitt, vorige/nächste) -----------------------------------------
  function wahl(K, art, tk) {
    var i = art === 'kachel' ? index(tk) : -1
    var zellen = TK.map(function (t, j) {
      var ohne = !Seite.hatDaten(K, t.id), aktiv = j === i
      var name = 'Teilkachel ' + (j + 1) + ' von ' + N + ', ' + t.lage + ' (' + t.id + ')' + (ohne ? ', keine Daten in Fassung ' + K : '')
      return '<a class="b-zelle' + (aktiv ? ' b-aktiv' : '') + (ohne ? ' b-ohne' : '') + '" href="#' + Seite.pfadKachel(K, t.id) + '"' +
        ' style="grid-row:' + (t.zeile + 1) + ';grid-column:' + (t.spalte + 1) + '" aria-label="' + esc(name) + '" title="' + esc(name) + '">' +
        Seite.miniatur(t.id) +
        '<span class="b-nr">' + (j + 1) + '</span>' +
        (ohne ? '<span class="b-keine">keine Daten</span>' : '') +
        '<span class="b-name"><b>' + esc(t.lage) + '</b><small>' + esc(t.id) + '</small></span></a>'
    }).join('')

    var zaehler = art === 'kachel'
      ? 'Teilkachel <b>' + (i + 1) + '</b> von ' + N + '<small>' + esc(lage(tk)) + '</small>'
      : '<b>Ganzer Ausschnitt</b><small>alle ' + N + ' Teilkacheln</small>'
    var vorige = art === 'kachel' && i > 0
    var naechste = art !== 'kachel' || i < N - 1

    var s = el('section', 'b-wahl')
    s.setAttribute('aria-label', 'Wahl der Teilkacheln')
    s.innerHTML =
      '<h3 class="b-titel">Ausschnitt in ' + N + ' Teilkacheln</h3>' +
      '<nav class="b-plan" aria-label="Teilkacheln in ihrer Lage">' + zellen + '</nav>' +
      '<a class="b-ganz' + (art === 'uebersicht' ? ' b-aktiv' : '') + '" href="#' + Seite.pfadGanz(K) + '">' +
        '<span class="b-ganz-bild" style="background-image:url(&quot;' + esc(DATEN.ausschnitt.bild) + '&quot;)" aria-hidden="true"></span>' +
        '<span class="b-ganz-text"><b>Ganzer Ausschnitt</b><small>alle ' + N + ' Teilkacheln in einem Bild</small></span></a>' +
      '<div class="b-schritt">' +
        '<button type="button" data-schritt="-1" title="vorige Teilkachel (Pfeiltaste links)"' + (vorige ? '' : ' disabled') + '><kbd>←</kbd> vorige</button>' +
        '<span class="b-zaehler" aria-live="polite">' + zaehler + '</span>' +
        '<button type="button" data-schritt="1" title="nächste Teilkachel (Pfeiltaste rechts)"' + (naechste ? '' : ' disabled') + '>nächste <kbd>→</kbd></button>' +
      '</div>'
    s.addEventListener('click', function (ev) {
      var b = ev.target.closest('[data-schritt]')
      if (b && !b.disabled) schritt(+b.dataset.schritt)
    })
    return s
  }

  // vorige/nächste: durch die vier Teilkacheln, ohne Umlauf; aus dem ganzen Ausschnitt geht „nächste“ zur ersten
  function schritt(d) {
    var K = JETZT.K
    if (JETZT.art === 'uebersicht') { if (d > 0) Entwurf.gehe(Seite.pfadKachel(K, TK[0].id)); return }
    if (JETZT.art !== 'kachel') return
    var j = index(JETZT.tk) + d
    if (j < 0 || j >= N) return
    Entwurf.gehe(Seite.pfadKachel(K, TK[j].id))
  }

  document.addEventListener('keydown', function (ev) {
    if (ev.ctrlKey || ev.metaKey || ev.altKey || ev.shiftKey || ev.defaultPrevented) return
    if (ev.key !== 'ArrowLeft' && ev.key !== 'ArrowRight') return
    var t = ev.target, tag = t && t.tagName
    if (tag === 'TEXTAREA' || tag === 'INPUT' || tag === 'SELECT' || (t && t.isContentEditable)) return
    ev.preventDefault()
    schritt(ev.key === 'ArrowLeft' ? -1 : 1)
  })

  // --- Kopf: schlank wie heute, ohne die Textlinks; dafür der Ort ------------------------------------------
  Seite.kopf = function (K, art, tk) {
    var h = el('header', 'c-kopf')
    var ort = art === 'kachel'
      ? symbol(index(tk)) + 'Teilkachel ' + (index(tk) + 1) + ' von ' + N + ' · ' + esc(lage(tk))
      : art === 'uebersicht' ? symbol(-1) + 'Ganzer Ausschnitt' : ''
    h.innerHTML = '<b>Ausschnitt ' + esc(DATEN.ausschnitt.name) + '</b>' + Seite.fassungen(K, art) +
      '<span class="b-ort">' + ort + '</span>' + Seite.kommentarLink() + Seite.beschreibung(K, art)
    return h
  }

  // Zeile über dem Bild
  Seite.titel = function (K, tk) {
    return '<b>Teilkachel ' + (index(tk) + 1) + ' von ' + N + ' · ' + esc(lage(tk)) + '</b><span>' + esc(tk) + '</span>'
  }

  // Leiste links: die Wahl oben, der Rest wie heute darunter
  Seite.inLeiste = function (info, K, art, tk) {
    info.classList.add('b-info')
    info.insertBefore(wahl(K, art, tk), info.firstChild)
  }

  // Im Bild: Ort oben links im Rand, Weiter-Knopf unten rechts im Rand
  Seite.imBild = function (feld, K, tk) {
    var i = index(tk)
    feld.appendChild(el('div', 'b-marke', symbol(i) + '<span>Teilkachel <b>' + (i + 1) + '</b> von ' + N + ' · ' + esc(lage(tk)) + '</span>'))
    var w = el('a', 'b-weiter')
    if (i < N - 1) {
      w.setAttribute('href', '#' + Seite.pfadKachel(K, TK[i + 1].id))
      w.innerHTML = 'Weiter: Teilkachel ' + (i + 2) + ' · <b>' + esc(TK[i + 1].lage) + '</b> <span aria-hidden="true">→</span>'
    } else {
      w.setAttribute('href', '#' + Seite.pfadGanz(K))
      w.innerHTML = 'Alle ' + N + ' gesehen · <b>Ganzer Ausschnitt</b> <span aria-hidden="true">→</span>'
    }
    feld.appendChild(w)
  }

  // Ganzer Ausschnitt: Nummer und Lage in jedem Viertel
  Seite.inGanz = function (feld, K) {
    var v = feld.querySelectorAll('.c-viertel')
    DATEN.teilkacheln.forEach(function (t, j) {
      if (!v[j]) return
      var ohne = !Seite.hatDaten(K, t.id)
      v[j].appendChild(el('span', 'b-viertel', '<i>' + t.nr + '</i>' + esc(t.lage) + (ohne ? ' · keine Daten' : '')))
    })
  }

  // --- Ganzer Ausschnitt mit derselben Leiste links und Liste rechts, damit das Bild an seinem Platz bleibt ----
  function ganz(K) {
    var w = Seite.ganz(K)
    if (!w) return
    JETZT = { art: 'uebersicht', K: K, tk: JETZT.tk }
    var mitte = w.querySelector('[data-inhalt]')
    mitte.className = 'c-mitte'
    var info = el('aside', 'c-info b-info'); info.setAttribute('aria-label', 'Wahl und Hinweise')
    info.innerHTML = '<section class="c-mausfeld"><h3>Unter der Maus</h3><p class="c-leise">Klick in ein Viertel öffnet diese Teilkachel.</p></section>'
    info.insertBefore(wahl(K, 'uebersicht'), info.firstChild)
    mitte.insertBefore(info, mitte.firstChild)

    var kat = el('aside', 'c-kat'); kat.setAttribute('aria-label', 'Teilkacheln')
    kat.innerHTML = '<h2>Im Bild · ' + N + ' Teilkacheln · Fassung ' + esc(K) + '</h2>' + TK.map(function (t, j) {
      var st = Seite.stand(K, t.id)
      return '<a class="b-zeile' + (st ? '' : ' b-ohne') + '" href="#' + Seite.pfadKachel(K, t.id) + '">' +
        '<i>' + (j + 1) + '</i><span><b>' + esc(t.lage) + '</b><small>' + esc(t.id) + '</small></span>' +
        '<span class="c-za">' + (st ? st.segmente + ' Segm. · ' + st.naht + ' Nahtst.' : 'keine Daten') + '</span></a>'
    }).join('')
    kat.hidden = !Seite.S.liste
    mitte.appendChild(kat)

    // untere Leiste: dieselben vier, mit Lage statt Kennung
    var unten = w.querySelector('.c-leiste')
    unten.innerHTML = '<div class="c-gruppe"><span class="c-etikett">Teilkachel öffnen</span>' + TK.map(function (t, j) {
      var st = Seite.stand(K, t.id)
      return '<a class="c-karte" href="#' + Seite.pfadKachel(K, t.id) + '"><b>' + (j + 1) + ' · ' + esc(t.lage) + '</b><span>' + (st ? st.segmente + ' Segmente' : 'keine Daten') + '</span></a>'
    }).join('') + '</div>'
  }

  function kachel(K, tk) {
    if (Seite.fassung(K) && Seite.teilkachel(tk)) JETZT = { art: 'kachel', K: K, tk: tk }
    Seite.kachel(K, tk)
  }

  // Routen des Gegenstands
  Entwurf.route('/:f/kachel/:tk', function (p) { kachel(p.f, p.tk) })
  Entwurf.route('/:f/kachel/:tk/segment/:id', function (p) { kachel(p.f, p.tk) })
  Entwurf.route('/:f/uebersicht', function (p) { ganz(p.f) })
  Entwurf.route('/', function () { Entwurf.gehe(Seite.pfadKachel(DATEN.start.fassung, DATEN.start.teilkachel)) })
  // auf anderen Seiten (Kommentare) blättern die Pfeiltasten nicht
  window.addEventListener('entwurf:route', function (ev) {
    if (!/\/(kachel|uebersicht)(\/|$)/.test(ev.detail.pfad)) JETZT = { art: 'andere', K: JETZT.K, tk: JETZT.tk }
  })
})()

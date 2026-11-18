/* Nachbau der Prüfseite (landseg seite, ergebnisse/T0.html) nach landseg/seite_vorlage/seite.js, als
   Baukasten window.Seite für die Entwürfe. Gegenstand ist die Wahl der Teilkacheln: Seite.kopf zeichnet sie
   heute als kleine Textlinks neben den Fassungen. Ein Entwurf ersetzt, was er braucht:

     Seite.kopf = function (K, art, tk) { return <header> }   Kopf (art: 'kachel' | 'uebersicht' | 'kommentare')
     Seite.imBild = function (feld, K, tk) { … }              Zusätze im Bild der Teilkachel (feld: .c-bildfeld)
     Seite.inLeiste = function (info, K, art, tk) { … }       Zusätze in der linken Leiste (Ansicht Teilkachel)
     Seite.inGanz = function (feld, K) { … }                  Zusätze im Bild „Ganzer Ausschnitt“
     Seite.titel = function (K, tk) { return '<b>…</b>' }     Anfang der Zeile über dem Bild

   oder meldet die Routen neu an und setzt die Teile selbst zusammen (Seite.kachel, Seite.ganz, Seite.aufbau,
   Seite.leiste, Seite.tafel, Seite.kategorien, Seite.steuerung, Seite.fassungen, Seite.miniatur).

   Routen wie die echte Seite:
     #/<F>/kachel/<tk>               Teilkachel in Fassung F
     #/<F>/kachel/<tk>/segment/<id>  dasselbe, ein Segment gewählt
     #/<F>/uebersicht                Ganzer Ausschnitt
     #/kommentare                    Kommentare (nicht Gegenstand, Platzhalter)
   Ein Wechsel der Fassung behält die Teilkachel bzw. den ganzen Ausschnitt (Klick oder Umschalt + A/B/C). */
(function () {
  'use strict'
  var D = window.DATEN
  var app = document.getElementById('app')
  var S = { ebene: 3, deck: 40, flaeche: true, umriss: true, luecken: false, naht: true, unsicher: false, gitter: false, liste: true, hervor: null }
  var LETZT = { art: 'kachel', tk: D.start.teilkachel }

  function el(t, c, h) { var e = document.createElement(t); if (c) e.className = c; if (h !== undefined) e.innerHTML = h; return e }
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c] }) }
  function fassung(K) { return D.fassungen.filter(function (f) { return f.kennung === K })[0] || null }
  function teilkachel(id) { return D.teilkacheln.filter(function (t) { return t.id === id })[0] || null }
  function stand(K, tk) { var f = fassung(K); return f && f.teilkacheln[tk] || null }
  function hatDaten(K, tk) { return !!stand(K, tk) }
  function pfadKachel(K, tk) { return '/' + K + '/kachel/' + tk }
  function pfadGanz(K) { return '/' + K + '/uebersicht' }
  function punkt(f) { return '<i class="c-punkt" style="background:' + f + '"></i>' }
  function kommentarZahl() { return D.kommentare.length }

  // --- Fassungen: Knopfgruppe wie heute (aria-pressed, gelber Rand) ---------------------------------------
  function fassungen(K, art) {
    return '<div class="c-fassungen" role="group" aria-label="Fassung">' + D.fassungen.map(function (f) {
      return '<button type="button" data-fassung="' + esc(f.kennung) + '" aria-pressed="' + (art !== 'kommentare' && f.kennung === K) + '" title="Umschalt + ' + esc(f.kennung) + '">' +
        esc(f.kennung) + '<span class="c-fname"> · ' + esc(f.name) + '</span></button>'
    }).join('') + '</div>'
  }
  function beschreibung(K, art) {
    var f = fassung(K)
    return '<p class="c-beschr" title="' + (art === 'kommentare' ? '' : esc(f.beschreibung)) + '">' +
      (art === 'kommentare' ? 'Kommentare zu allen Fassungen' : '<b>' + esc(f.kennung + ' · ' + f.name) + '</b>' + esc(f.beschreibung)) + '</p>'
  }
  function kommentarLink() { return '<span class="c-rechts"><a href="#/kommentare">Kommentare (' + kommentarZahl() + ')</a></span>' }

  // --- Kopf wie heute: kleine Textlinks „Ganzer Ausschnitt“, r0c0 … r1c1 neben den Fassungen ---------------
  function kopfHeute(K, art, tk) {
    var h = el('header', 'c-kopf')
    h.innerHTML = '<b>Ausschnitt ' + esc(D.ausschnitt.name) + '</b>' + fassungen(K, art) +
      '<nav aria-label="Teilkacheln"><a href="#/' + K + '/uebersicht">Ganzer Ausschnitt</a>' +
      D.teilkacheln.map(function (t) {
        return '<a href="#/' + K + '/kachel/' + t.id + '"' + (hatDaten(K, t.id) ? ' title="Teilkachel ' + t.id + ' (Zeile ' + (t.zeile + 1) + ', Spalte ' + (t.spalte + 1) + ')"' : ' class="c-ohne" title="ohne Daten"') + '>' + t.id + '</a>'
      }).join('') + '</nav>' + kommentarLink() + beschreibung(K, art)
    return h
  }

  // --- linke Leiste: Unter der Maus, Gewählt, Kommentar, Legende ---------------------------------------------
  var LEGENDE = '<details class="c-legende"><summary>Was bedeutet …?</summary><dl>' +
    '<dt>Fassung</dt><dd>Eine Art, die Flächen einzuteilen; oben umschalten (auch mit Umschalt + A, B, C).</dd>' +
    '<dt>Teilkachel</dt><dd>Eines der Bildstücke, in die der Ausschnitt geteilt ist (r = Zeile, c = Spalte).</dd>' +
    '<dt>Kern</dt><dd>Der Teil im hellen Rahmen: nur er zählt für diese Teilkachel.</dd>' +
    '<dt>Rand</dt><dd>Der abgedunkelte Streifen außen: Überlappung mit den Nachbarn, nur zur Orientierung.</dd>' +
    '<dt>Naht</dt><dd>Grenze zwischen zwei Teilkacheln.</dd></dl></details>'
  function leiste(K, tk) {
    var info = el('aside', 'c-info'); info.setAttribute('aria-label', 'Segment')
    var st = stand(K, tk)
    info.innerHTML = '<section class="c-mausfeld" data-maus aria-live="polite"><h3>Unter der Maus</h3><p class="c-leise">' +
      (st ? 'Mit der Maus über das Bild fahren: Hier steht, zu welchem Segment und welcher Kategorie die Stelle gehört.' : 'Für diese Teilkachel gibt es in dieser Fassung keine Daten.') + '</p></section>' +
      '<section class="c-wahl" data-wahl>' + (st ? '<h3>Gewählt</h3><p class="c-leise">Ein Segment im Bild anklicken, um es zu wählen und zu kommentieren. Esc hebt die Wahl auf.</p>' : '') + '</section>' +
      '<form class="c-komm" data-komm><textarea id="kommentar" rows="3" placeholder="Kommentar zum gewählten Segment" aria-label="Kommentar" disabled></textarea>' +
      '<div class="c-knoepfe"><button type="submit" disabled>Vormerken</button><button type="button" data-export>Export (JSON)</button></div>' +
      '<p class="c-status" data-status>Kommentare bleiben nur in diesem Browser, bis Sie sie exportieren.</p></form>' + LEGENDE
    info.querySelector('[data-komm]').addEventListener('submit', function (ev) { ev.preventDefault() })
    info.querySelector('[data-export]').addEventListener('click', function () {
      info.querySelector('[data-status]').textContent = kommentarZahl() + ' Kommentare exportiert (Datei kommentare-T0.json, meist im Ordner Downloads).'
    })
    return info
  }

  // --- Bildtafel einer Teilkachel: Zeile über dem Bild, Luftbild mit Segmenten im Kern ----------------------
  function befund(st) {
    if (!st.luecken) return '<span class="c-ok">lückenlos</span>'
    return '<span class="c-fehler">' + st.luecken + ' Bildpunkte ohne Segment</span>'
  }
  function bildfeld(K, tk) {
    var t = teilkachel(tk), f = fassung(K), st = stand(K, tk)
    var buehne = el('div', 'c-buehne'), feld = el('div', 'c-bildfeld')
    feld.setAttribute('data-bildfeld', tk)
    var img = el('img', 'c-luftbild'); img.alt = 'Luftbild der Teilkachel ' + tk; img.src = t.bild
    var kern = el('div', 'c-kern' + (st ? '' : ' c-roh'))
    if (st) {
      kern.style.backgroundImage = 'url("' + f.bild + '")'
      kern.style.backgroundPosition = (t.spalte * 100) + '% ' + (t.zeile * 100) + '%'
      kern.style.opacity = S.flaeche ? '1' : '0.0001'
    }
    feld.appendChild(img); feld.appendChild(kern)
    if (!st) feld.appendChild(el('div', 'c-leer', 'Fassung ' + esc(K) + ' hat für ' + esc(tk) + ' noch keine Ergebnisse.'))
    buehne.appendChild(feld)
    return buehne
  }
  function tafel(K, tk) {
    var st = stand(K, tk)
    var f = el('figure', 'c-tafel')
    var cap = Seite.titel(K, tk)
    if (st) {
      cap += '<span>' + st.segmente + ' Segmente, ' + st.unsicher + ' davon unsicher</span>' + befund(st) +
        '<span>' + (st.naht ? '<span class="c-warn">' + st.naht + ' Stellen an Nähten passen nicht</span>' : 'Nähte passen') + '</span>'
    }
    f.innerHTML = '<figcaption>' + cap + '</figcaption>'
    var b = bildfeld(K, tk)
    f.appendChild(b)
    Seite.imBild(b.querySelector('[data-bildfeld]'), K, tk)
    return f
  }

  // --- Kategorienliste rechts -------------------------------------------------------------------------------
  function kategorien(K, tk) {
    var kat = el('aside', 'c-kat'); kat.setAttribute('aria-label', 'Kategorien')
    var st = stand(K, tk), f = fassung(K), e = f.ebenen[2]
    if (!st) { kat.innerHTML = '<h2>Im Bild</h2><p class="c-leise">Keine Daten in dieser Fassung.</p>'; return kat }
    function zeichne() {
      kat.innerHTML = '<h2>Im Bild · Ebene ' + esc(e.name) + ' · ' + st.kategorien.length + ' von ' + e.klassen + ' Kategorien</h2>' +
        '<button type="button" class="c-aufheben" data-aufheben' + (S.hervor ? '' : ' disabled') + '>Hervorhebung aufheben</button>' +
        st.kategorien.map(function (k) {
          return '<button type="button" class="c-kl" data-klasse="' + esc(k.code) + '" aria-pressed="' + (S.hervor === k.code) + '">' + punkt(k.farbe) +
            '<span>' + esc(k.code + ' ' + k.name) + '</span><span class="c-za">' + k.segmente + ' Segm. · ' + k.anteil.toFixed(1).replace('.', ',') + ' %</span></button>'
        }).join('') +
        '<p class="c-quelle">Anteil an der Fläche der Teilkachel samt Rand. Klick hebt eine Kategorie hervor.</p>'
    }
    kat.addEventListener('click', function (ev) {
      if (ev.target.closest('[data-aufheben]')) { S.hervor = null; zeichne(); return }
      var b = ev.target.closest('[data-klasse]'); if (!b) return
      S.hervor = S.hervor === b.dataset.klasse ? null : b.dataset.klasse; zeichne()
    })
    zeichne()
    kat.hidden = !S.liste
    return kat
  }

  // --- untere Leiste: Ebene, Zeigen, Bild ---------------------------------------------------------------------
  function steuerung(K) {
    var f = fassung(K), l = el('section', 'c-leiste'); l.setAttribute('aria-label', 'Steuerung')
    function an(k) { return ' aria-pressed="' + !!S[k] + '"' }
    l.innerHTML = '<div class="c-gruppe"><span class="c-etikett">Ebene</span>' + f.ebenen.map(function (e) {
      return '<button type="button" data-ebene="' + e.ebene + '" aria-pressed="' + (S.ebene === e.ebene) + '">' + esc(e.name) + '</button>' }).join('') + '</div>' +
      '<div class="c-gruppe"><span class="c-etikett">Zeigen</span>' +
      '<button type="button" data-schalter="flaeche"' + an('flaeche') + '>Flächen</button>' +
      '<label class="c-regler"><span data-deckwert>Deckkraft ' + S.deck + ' %</span><input id="deckkraft" type="range" min="0" max="100" value="' + S.deck + '" aria-label="Deckkraft der Flächen" data-deck></label>' +
      '<button type="button" data-schalter="umriss"' + an('umriss') + '>Umriss</button>' +
      '<button type="button" data-schalter="luecken"' + an('luecken') + '>Lücken</button>' +
      '<button type="button" data-schalter="naht"' + an('naht') + '>Nähte</button>' +
      '<button type="button" data-schalter="unsicher"' + an('unsicher') + '>Nur unsicher</button>' +
      '<button type="button" data-schalter="gitter"' + an('gitter') + '>Gitter</button>' +
      '<button type="button" data-schalter="liste"' + an('liste') + '>Liste rechts</button></div>' +
      '<div class="c-gruppe"><span class="c-etikett">Bild</span><button type="button" aria-label="Verkleinern">−</button><button type="button">Ganz</button><button type="button" aria-label="Vergrößern">+</button>' +
      '<span class="c-zoomwert">Zoom 100 %</span></div>'
    l.addEventListener('input', function (ev) {
      if (!ev.target.hasAttribute('data-deck')) return
      S.deck = +ev.target.value; l.querySelector('[data-deckwert]').textContent = 'Deckkraft ' + S.deck + ' %'
    })
    l.addEventListener('click', function (ev) {
      var b = ev.target.closest('button'); if (!b) return
      if (b.dataset.ebene) {
        S.ebene = +b.dataset.ebene
        l.querySelectorAll('[data-ebene]').forEach(function (y) { y.setAttribute('aria-pressed', String(y === b)) })
      } else if (b.dataset.schalter) {
        var k = b.dataset.schalter; S[k] = !S[k]; b.setAttribute('aria-pressed', String(S[k]))
        var kat = document.querySelector('.c-kat'); if (k === 'liste' && kat) kat.hidden = !S.liste
        var kern = document.querySelector('.c-kern:not(.c-roh)'); if (k === 'flaeche' && kern) kern.style.opacity = S.flaeche ? '1' : '0.0001'
      }
    })
    return l
  }

  // --- Seitenaufbau: Kopf, Mitte (data-inhalt), untere Leiste -------------------------------------------------
  function aufbau(kopf, mitte, unten) {
    var w = el('div', 'c-seite')
    w.appendChild(kopf)
    mitte.setAttribute('data-inhalt', '')
    w.appendChild(mitte)
    w.appendChild(unten)
    app.innerHTML = ''
    app.appendChild(w)
    Entwurf.inhalt = mitte
    return w
  }

  // --- Ansicht einer Teilkachel ---------------------------------------------------------------------------------
  function kachel(K, tk) {
    if (!fassung(K)) { Entwurf.gehe(pfadKachel(D.start.fassung, D.start.teilkachel)); return }
    if (!teilkachel(tk)) { Entwurf.gehe(pfadKachel(K, D.teilkacheln[0].id)); return }
    LETZT = { art: 'kachel', tk: tk }
    var mitte = el('div', 'c-mitte'), info = leiste(K, tk)
    mitte.appendChild(info)
    mitte.appendChild(tafel(K, tk))
    mitte.appendChild(kategorien(K, tk))
    Seite.inLeiste(info, K, 'kachel', tk)
    return aufbau(Seite.kopf(K, 'kachel', tk), mitte, steuerung(K))
  }

  // --- Ganzer Ausschnitt -----------------------------------------------------------------------------------------
  function ganz(K) {
    if (!fassung(K)) { Entwurf.gehe(pfadGanz(D.start.fassung)); return }
    LETZT = { art: 'uebersicht', tk: LETZT.tk }
    var f = fassung(K)
    var mitte = el('div', 'c-uebersicht'), fig = el('figure', 'c-tafel')
    var verst = 0
    D.teilkacheln.forEach(function (t) { var st = stand(K, t.id); if (st) verst += st.naht })
    fig.innerHTML = '<figcaption><b>Ganzer Ausschnitt ' + esc(D.ausschnitt.name) + '</b><span>' +
      (verst ? '<span class="c-warn">' + verst + ' Stellen an Nähten passen nicht</span>' : '<span class="c-ok">Nähte passen</span>') + ' · ' + f.naehte + ' Nähte zwischen Teilkacheln</span>' +
      '<span>Klick ins Bild öffnet die Teilkachel an dieser Stelle.</span></figcaption>'
    var buehne = el('div', 'c-buehne'), feld = el('div', 'c-bildfeld')
    feld.setAttribute('data-bildfeld', 'ganz')
    var bild = el('div', 'c-ganz'); bild.style.backgroundImage = 'url("' + f.bild + '")'
    bild.setAttribute('role', 'img'); bild.setAttribute('aria-label', 'Ausschnitt ' + D.ausschnitt.name + ', Fassung ' + K)
    feld.appendChild(bild)
    D.teilkacheln.forEach(function (t) {
      var a = el('a', 'c-viertel')
      a.setAttribute('href', '#' + pfadKachel(K, t.id))
      a.style.left = (t.spalte * 50) + '%'; a.style.top = (t.zeile * 50) + '%'
      a.setAttribute('aria-label', 'Teilkachel ' + t.id + ' öffnen')
      feld.appendChild(a)
    })
    buehne.appendChild(feld); fig.appendChild(buehne); mitte.appendChild(fig)
    Seite.inGanz(feld, K)
    var unten = el('section', 'c-leiste')
    unten.innerHTML = '<div class="c-gruppe">' + D.teilkacheln.map(function (t) {
      var st = stand(K, t.id)
      return '<a class="c-karte" href="#/' + K + '/kachel/' + t.id + '"><b>' + t.id + '</b><span>' + (st ? st.segmente + ' Segmente' : 'keine Daten') + '</span></a>'
    }).join('') + '</div>'
    return aufbau(Seite.kopf(K, 'uebersicht'), mitte, unten)
  }

  // --- Kommentare: nicht Gegenstand ---------------------------------------------------------------------------
  function kommentare() {
    var K = D.start.fassung, mitte = el('div', 'c-liste'), unten = el('section', 'c-leiste')
    aufbau(Seite.kopf(K, 'kommentare'), mitte, unten)
    Entwurf.platzhalter('Kommentare (' + kommentarZahl() + ')', mitte)
  }

  // --- Miniatur einer Teilkachel (Kern des Luftbilds) für die Kachel-Wahl -------------------------------------
  function miniatur(tk, klasse) {
    var t = teilkachel(tk)
    return '<span class="c-mini' + (klasse ? ' ' + klasse : '') + '" style="background-image:url(&quot;' + t.bild + '&quot;)" aria-hidden="true"></span>'
  }

  // --- Fassung wechseln: Teilkachel bzw. ganzer Ausschnitt bleibt -------------------------------------------
  function wechsle(K) {
    if (!fassung(K)) return
    if (LETZT.art === 'uebersicht') Entwurf.gehe(pfadGanz(K))
    else Entwurf.gehe(pfadKachel(K, LETZT.tk))
  }
  document.addEventListener('click', function (ev) {
    var b = ev.target.closest && ev.target.closest('[data-fassung]')
    if (b && !b.disabled) wechsle(b.dataset.fassung)
  })
  document.addEventListener('keydown', function (ev) {
    var t = ev.target && ev.target.tagName
    if (t === 'TEXTAREA' || t === 'INPUT' || !ev.shiftKey || ev.ctrlKey || ev.metaKey || ev.altKey) return
    var k = String(ev.key || '').toUpperCase()
    if (fassung(k)) wechsle(k)
  })

  window.Seite = {
    D: D, S: S, el: el, esc: esc,
    fassung: fassung, teilkachel: teilkachel, stand: stand, hatDaten: hatDaten,
    pfadKachel: pfadKachel, pfadGanz: pfadGanz,
    fassungen: fassungen, beschreibung: beschreibung, kommentarLink: kommentarLink,
    kopfHeute: kopfHeute, leiste: leiste, tafel: tafel, kategorien: kategorien, steuerung: steuerung,
    aufbau: aufbau, kachel: kachel, ganz: ganz, miniatur: miniatur, wechsle: wechsle,
    get letzt() { return LETZT },
    // Stellen, die ein Entwurf ersetzt
    kopf: kopfHeute,
    titel: function (K, tk) { return '<b>Teilkachel ' + esc(tk) + '</b>' },
    imBild: function () {},
    inLeiste: function () {},
    inGanz: function () {},
  }

  Entwurf.route('/', function () { Entwurf.gehe(pfadKachel(D.start.fassung, D.start.teilkachel)) })
  Entwurf.route('/:f/kachel/:tk', function (p) { kachel(p.f, p.tk) })
  Entwurf.route('/:f/kachel/:tk/segment/:id', function (p) { kachel(p.f, p.tk) })
  Entwurf.route('/:f/uebersicht', function (p) { ganz(p.f) })
  Entwurf.route('/kommentare', function () { kommentare() })
})()

/* Startpunkt jedes Platzes: die Routen der Prüfseite, schlicht gezeichnet. Die Entwerfer ersetzen die
   Zeichnung durch ihren Ansatz und behalten die Routen (oder lösen eine Seite anders, etwa als Dialog).

   /kachel/:tk                Prüfansicht einer Teilkachel (r0c0, r0c1, r1c0, r1c1): Bild mit Segmenten
   /kachel/:tk/segment/:id    dieselbe Ansicht, ein Segment gewählt (Details, Kommentar)
   /uebersicht                ganzes Testfenster T0 mit den vier Teilkacheln und den Nähten
   /kommentare                Kommentare der Prüfung, Export als JSON

   Daten: DATEN (gemeinsam/daten.js), Zeichnen: Karte (gemeinsam/umgebung.js). */
(function () {
  'use strict'
  var D = window.DATEN

  function ansicht(tk, auswahl) {
    var t = Karte.teilkachel(tk) || D.teilkacheln[0]
    var z = Karte.zaehle('vorstufe', t.id)
    var el = Entwurf.inhalt
    el.innerHTML =
      '<div class="v-seite">' +
      '<canvas class="v-bild" aria-label="Luftbild ' + t.name + '"></canvas>' +
      '<aside class="v-leiste">' +
      '<b>' + t.name + ' · ' + t.lage + '</b>' +
      '<span>' + z.segmente + ' Segmente · ' + z.unsicher + ' unsicher · ' + z.luecken + ' Lücken</span>' +
      '<nav>' + D.teilkacheln.map(function (x) { return '<a href="#/kachel/' + x.id + '">' + x.name + '</a>' }).join('') + '</nav>' +
      '<a href="#/uebersicht">Ganzes Testfenster</a><a href="#/kommentare">Kommentare</a>' +
      '</aside></div>'
    var cv = el.querySelector('canvas')
    Karte.passe(cv)
    Karte.zeichne(cv, { stand: 'vorstufe', ausschnitt: t.ausschnitt, kern: t.id, auswahl: auswahl ? +auswahl : null })
    cv.addEventListener('click', function (ev) {
      var p = Karte.punkt(cv, t.ausschnitt, ev)
      var id = Karte.bei('vorstufe', p[0], p[1])
      if (id) Entwurf.gehe(['', 'kachel', t.id, 'segment', id].join('/'))
    })
  }

  Entwurf.route('/kachel/:tk', function (p) { ansicht(p.tk) })
  Entwurf.route('/kachel/:tk/segment/:id', function (p) { ansicht(p.tk, p.id) })
  Entwurf.route('/uebersicht', function () {
    Entwurf.inhalt.innerHTML = '<div class="v-seite"><canvas class="v-bild" aria-label="Testfenster T0"></canvas>' +
      '<aside class="v-leiste"><b>Testfenster T0</b><a href="#/kachel/r0c0">Teilkachel 1</a></aside></div>'
    var cv = Entwurf.inhalt.querySelector('canvas')
    Karte.passe(cv)
    Karte.zeichne(cv, { stand: 'runde1', ausschnitt: [0, 0, 1000, 1000], naht: true, flaeche: 0.25 })
  })
  Entwurf.route('/kommentare', function () {
    Entwurf.inhalt.innerHTML = '<div class="v-liste"><b>Kommentare</b>' +
      D.kommentare.map(function (k) {
        return '<p><a href="#/kachel/' + k.teilkachel + '/segment/' + k.segment + '">Segment ' + k.segment + '</a> ' + k.text + '</p>'
      }).join('') + '</div>'
  })
})()

/* Platz d: Prüfliste Fall für Fall. Fälle = unsichere Segmente, Kandidaten (Vorstufe) und Nahtverstöße (Runde 1).
   Routen: /kachel/:tk, /kachel/:tk/segment/:id, /kachel/:tk/naht/:nr, /uebersicht, /kommentare */
(function () {
  'use strict'
  var D = window.DATEN
  var el = Entwurf.inhalt
  function pfadKachel(id) { return ['', 'kachel', id].join('/') }

  var erledigt = {}
  var notiz = {}
  var klasseNeu = {}
  var filter = 'alle'
  var ebene = 3
  var umschalter = { luecken: false, naht: true, umriss: true }

  var ESC = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return ESC[c] }) }
  function klassenName(code) { var k = Karte.klasse(code); return k ? k.name : code }

  function faelle(tk) {
    var res = []
    Karte.segmente('vorstufe', tk).forEach(function (s) {
      var gruende = (s.kandidaten || []).slice()
      var unsicher = s.sicher === 'nein'
      if (!unsicher && !gruende.length) return
      res.push({
        schluessel: tk + ':s' + s.id, art: unsicher ? 'unsicher' : 'Kandidat', segment: s, gruende: gruende,
        pfad: pfadKachel(tk) + '/segment/' + s.id, rang: unsicher ? (s.wert || 0) : 1 + (s.wert || 0)
      })
    })
    Karte.stand('runde1').naht.forEach(function (n, i) {
      if (n.grenze.split(' | ').indexOf(tk) < 0) return
      res.push({
        schluessel: tk + ':n' + i, art: 'Naht', naht: n, nr: i, gruende: [n.art],
        pfad: pfadKachel(tk) + '/naht/' + i, rang: -1
      })
    })
    res.sort(function (a, b) { return a.rang - b.rang })
    return res
  }
  function sichtbar(liste) {
    return liste.filter(function (f) {
      if (filter === 'offen') return !erledigt[f.schluessel]
      if (filter === 'naht') return f.art === 'Naht'
      if (filter === 'unsicher') return f.art === 'unsicher'
      return true
    })
  }
  function ausschnittFall(f) {
    if (f.naht) {
      var n = f.naht
      var mitte = (n.von + n.bis) / 2
      var seite = Math.max(n.bis - n.von + 120, 200)
      return n.achse === 'senkrecht'
        ? [n.lage - seite / 2, mitte - seite / 2, seite, seite]
        : [mitte - seite / 2, n.lage - seite / 2, seite, seite]
    }
    var k = f.segment.kasten
    var s = Math.max(Math.max(k[2], k[3]) * 1.6 + 40, 140)
    return [k[0] + k[2] / 2 - s / 2, k[1] + k[3] / 2 - s / 2, s, s]
  }
  function titel(f) {
    if (f.naht) return 'Naht ' + f.naht.grenze + ' · ' + (f.naht.achse === 'senkrecht' ? 'y ' : 'x ') + f.naht.von + '–' + f.naht.bis
    return 'Segment ' + f.segment.id + ' · ' + klassenName(f.segment.klasse)
  }

  function ansicht(tkId, art, id) {
    var t = Karte.teilkachel(tkId) || DATEN.teilkacheln[0]
    var alle = faelle(t.id)
    var liste = sichtbar(alle)
    var fertig = alle.filter(function (f) { return erledigt[f.schluessel] }).length
    var aktuell = null
    alle.forEach(function (f) {
      if (art === 'segment' && f.segment && String(f.segment.id) === String(id)) aktuell = f
      if (art === 'naht' && f.naht && String(f.nr) === String(id)) aktuell = f
    })
    var freiesSeg = (art === 'segment' && !aktuell) ? Karte.segment('vorstufe', +id) : null
    if (!art && liste.length) { Entwurf.gehe(liste[0].pfad); return }
    if (freiesSeg) {
      aktuell = {
        schluessel: t.id + ':s' + freiesSeg.id, art: 'Segment', segment: freiesSeg, gruende: [],
        pfad: pfadKachel(t.id) + '/segment/' + freiesSeg.id
      }
    }

    var kopf =
      '<div class="d-kopf"><b>Prüfliste · ' + esc(t.name) + '</b>' +
      '<div class="d-reiter">' + DATEN.teilkacheln.map(function (x) {
        return '<button type="button" data-tk="' + x.id + '" aria-pressed="' + (x.id === t.id) + '">' + x.nummer + '</button>'
      }).join('') + '</div>' +
      '<div class="d-fortschritt"><i style="width:' + (alle.length ? Math.round(fertig * 100 / alle.length) : 0) + '%"></i></div>' +
      '<div class="d-zahl"><span>' + fertig + ' von ' + alle.length + ' geprüft</span><span>' + (alle.length - fertig) + ' offen</span></div>' +
      '<div class="d-filter">' + [['alle', 'Alle'], ['offen', 'Offen'], ['unsicher', 'Unsicher'], ['naht', 'Naht']].map(function (p) {
        return '<button type="button" data-filter="' + p[0] + '" aria-pressed="' + (filter === p[0]) + '">' + p[1] + '</button>'
      }).join('') + '</div></div>'

    var zeilen = liste.map(function (f) {
      var akt = aktuell && aktuell.schluessel === f.schluessel
      return '<li><a href="#' + f.pfad + '" class="' + (erledigt[f.schluessel] ? 'd-erledigt' : '') + '"' + (akt ? ' aria-current="true"' : '') + '>' +
        '<i class="d-haken"></i><span><span class="d-titel">' + esc(titel(f)) + '</span><span class="d-grund">' +
        esc(f.gruende.join(' · ') || 'Klasse unsicher') + '</span></span>' +
        '<span class="d-art' + (f.naht ? ' naht' : '') + '">' + f.art + '</span></a></li>'
    }).join('')
    if (!liste.length) zeilen = '<li class="d-leer">Keine Fälle in dieser Ansicht.</li>'

    var leiste =
      '<div class="d-leiste">' +
      [3, 2, 1].map(function (e) {
        var n = DATEN.ebenen[e - 1].name
        return '<button type="button" data-ebene="' + e + '" aria-pressed="' + (ebene === e) + '">' + n.charAt(0).toUpperCase() + n.slice(1) + '</button>'
      }).join('') +
      '<span class="d-trenn"></span>' +
      '<button type="button" data-schalter="umriss" aria-pressed="' + umschalter.umriss + '">Umriss</button>' +
      '<button type="button" data-schalter="luecken" aria-pressed="' + umschalter.luecken + '">Lückenkarte</button>' +
      '<button type="button" data-schalter="naht" aria-pressed="' + umschalter.naht + '">Naht-Ebene</button>' +
      '<span class="d-rechts"><a href="#/uebersicht">Ganzes Testfenster</a> · <a href="#/kommentare">Kommentare</a></span></div>'

    var fall
    if (aktuell) {
      var s = aktuell.segment
      var key = aktuell.schluessel
      var sel = klasseNeu[key] || (s ? s.klasse : '')
      var klassen = DATEN.kategorien.filter(function (k) { return k.blatt })
      var kopfzeile, text
      if (aktuell.naht) {
        kopfzeile = titel(aktuell)
        text = aktuell.naht.art + ' · Segmente ' + aktuell.naht.ids.join(' und ') + ' · Klassen ' + aktuell.naht.klassen.map(klassenName).join(' / ')
      } else {
        kopfzeile = 'Segment ' + s.id + ' · ' + klassenName(s.klasse)
        text = 'Herkunft ' + s.herkunft + ' · Sicherheit ' + s.wert + ' · ' + s.flaeche + ' Bildpunkte'
      }
      fall =
        '<div class="d-fall"><div>' +
        '<h2>' + esc(kopfzeile) + '</h2><p>' + esc(text) + '</p>' +
        '<div class="d-grundliste">' + aktuell.gruende.map(function (g) { return '<span>' + esc(g) + '</span>' }).join('') + '</div>' +
        (s ? '<div class="d-zeile"><label for="d-klasse">Klasse setzen</label><select id="d-klasse">' +
          klassen.map(function (k) { return '<option value="' + k.code + '"' + (k.code === sel ? ' selected' : '') + '>' + k.code + ' ' + esc(k.name) + '</option>' }).join('') +
          '</select></div>' : '') +
        '</div><div>' +
        '<textarea id="d-notiz" placeholder="Kommentar zu diesem Fall">' + esc(notiz[key] || '') + '</textarea>' +
        '<div class="d-aktion"><button type="button" id="d-zurueck">Zurück</button>' +
        '<button type="button" id="d-ueber">Überspringen</button>' +
        '<button type="button" class="d-weiter" id="d-weiter">' + (erledigt[key] ? 'Weiter' : 'Abhaken und weiter') + '</button></div></div></div>'
    } else {
      fall = '<div class="d-fall"><div><h2>Alle Fälle dieser Ansicht erledigt</h2><p>Weiter mit der nächsten Teilkachel oder dem ganzen Testfenster.</p></div><div></div></div>'
    }

    el.innerHTML =
      '<div class="d-seite"><aside class="d-liste">' + kopf + '<ul class="d-faelle">' + zeilen + '</ul></aside>' +
      '<div class="d-mitte">' + leiste + '<div class="d-bildfeld"><canvas aria-label="Luftbild ' + esc(t.name) + '"></canvas>' +
      (aktuell && aktuell.segment ? '<canvas class="d-nah" aria-label="Nahaufnahme"></canvas>' : '') + '</div>' + fall + '</div></div>'

    var cv = el.querySelector('.d-bildfeld > canvas')
    var aus = aktuell ? ausschnittFall(aktuell) : t.ausschnitt
    var stand = (aktuell && aktuell.naht) ? 'runde1' : 'vorstufe'
    Karte.passe(cv)
    Karte.zeichne(cv, {
      stand: stand, ausschnitt: aus, kern: t.id, ebene: ebene, umriss: umschalter.umriss, luecken: umschalter.luecken,
      naht: umschalter.naht, auswahl: aktuell && aktuell.segment ? aktuell.segment.id : null
    })
    var nah = el.querySelector('.d-nah')
    if (nah) { Karte.passe(nah); Karte.vorschau(nah, 'vorstufe', aktuell.segment.id) }
    cv.addEventListener('click', function (ev) {
      var p = Karte.punkt(cv, aus, ev)
      var sid = Karte.bei(stand, p[0], p[1])
      if (sid && stand === 'vorstufe') Entwurf.gehe(pfadKachel(t.id) + '/segment/' + sid)
    })

    function neu() { ansicht(tkId, art, id) }
    el.querySelectorAll('[data-tk]').forEach(function (b) { b.addEventListener('click', function () { Entwurf.gehe(pfadKachel(b.getAttribute('data-tk'))) }) })
    el.querySelectorAll('[data-filter]').forEach(function (b) { b.addEventListener('click', function () { filter = b.getAttribute('data-filter'); neu() }) })
    el.querySelectorAll('[data-ebene]').forEach(function (b) { b.addEventListener('click', function () { ebene = +b.getAttribute('data-ebene'); neu() }) })
    el.querySelectorAll('[data-schalter]').forEach(function (b) {
      b.addEventListener('click', function () { var k = b.getAttribute('data-schalter'); umschalter[k] = !umschalter[k]; neu() })
    })
    var feld = el.querySelector('#d-notiz')
    if (feld && aktuell) feld.addEventListener('input', function () { notiz[aktuell.schluessel] = feld.value })
    var wahl = el.querySelector('#d-klasse')
    if (wahl && aktuell) wahl.addEventListener('change', function () { klasseNeu[aktuell.schluessel] = wahl.value })

    function nachbar(richtung, abhaken) {
      if (abhaken && aktuell) erledigt[aktuell.schluessel] = true
      var pos = -1
      liste.forEach(function (f, i) { if (aktuell && f.schluessel === aktuell.schluessel) pos = i })
      var ziel = null
      for (var i = 1; i <= liste.length; i++) {
        var q = liste[((pos + richtung * i) % liste.length + liste.length) % liste.length]
        if (!abhaken || !erledigt[q.schluessel]) { ziel = q; break }
      }
      if (ziel && (!aktuell || ziel.schluessel !== aktuell.schluessel)) Entwurf.gehe(ziel.pfad)
      else neu()
    }
    var w = el.querySelector('#d-weiter'); if (w) w.addEventListener('click', function () { nachbar(1, true) })
    var u = el.querySelector('#d-ueber'); if (u) u.addEventListener('click', function () { nachbar(1, false) })
    var z = el.querySelector('#d-zurueck'); if (z) z.addEventListener('click', function () { nachbar(-1, false) })
    var akt = el.querySelector('.d-faelle [aria-current="true"]')
    if (akt && akt.scrollIntoView) akt.scrollIntoView({ block: 'nearest' })
  }

  Entwurf.route('/kachel/:tk', function (p) { ansicht(p.tk) })
  Entwurf.route('/kachel/:tk/segment/:id', function (p) { ansicht(p.tk, 'segment', p.id) })
  Entwurf.route('/kachel/:tk/naht/:nr', function (p) { ansicht(p.tk, 'naht', p.nr) })

  Entwurf.route('/uebersicht', function () {
    var zeilen = DATEN.teilkacheln.map(function (t) {
      var a = faelle(t.id)
      var f = a.filter(function (x) { return erledigt[x.schluessel] }).length
      return '<div class="d-karte"><b><a href="#' + pfadKachel(t.id) + '">' + esc(t.name) + '</a> · ' + esc(t.lage) + '</b>' +
        '<span>' + a.length + ' Fälle, ' + f + ' geprüft</span></div>'
    }).join('')
    el.innerHTML = '<div class="d-uebersicht"><canvas aria-label="Testfenster T0"></canvas><aside class="d-seitl"><b>Testfenster T0</b>' + zeilen +
      '<a href="#/kommentare">Kommentare</a></aside></div>'
    var cv = el.querySelector('canvas')
    Karte.passe(cv)
    Karte.zeichne(cv, { stand: 'runde1', ausschnitt: [0, 0, 1000, 1000], naht: true, flaeche: 0.25 })
  })

  Entwurf.route('/kommentare', function () {
    var eigene = Object.keys(notiz).filter(function (k) { return notiz[k] }).map(function (k) {
      return '<p><b>' + esc(k) + '</b> ' + esc(notiz[k]) + '</p>'
    }).join('')
    el.innerHTML = '<div class="d-text"><b>Kommentare</b>' + DATEN.kommentare.map(function (k) {
      return '<p><a href="#' + pfadKachel(k.teilkachel) + '/segment/' + k.segment + '">Segment ' + k.segment + '</a> ' + esc(k.text) + '</p>'
    }).join('') + eigene + '<p><a href="#' + pfadKachel('r0c0') + '">Zurück zur Prüfliste</a></p></div>'
  })
})()

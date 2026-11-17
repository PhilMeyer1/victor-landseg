/* Umgebung der Prüfseite (landseg). Die Seite steht für sich (kein Menü, kein App-Rahmen); die Entwürfe
   zeichnen alles in das Element mit data-inhalt.

   Dazu window.Karte: zeichnet die Platzhalter-Landschaft aus DATEN auf ein <canvas>, für alle Plätze gleich.
   Koordinaten sind Bildpunkte im Testfenster T0 (0 … 1000, Kontextrand bis −64 und 1064).

     Karte.zeichne(canvas, {
       stand: 'vorstufe' | 'runde1',          Segmente dieses Stands (Pflicht)
       ausschnitt: [x, y, breite, hoehe],     sichtbarer Teil in T0-Bildpunkten (Pflicht)
       bild: true,                            Luftbild (Platzhalter) darunter
       grau: false,                           Luftbild in Graustufen
       ebene: 3,                              Kategorie-Ebene 1 grob, 2 mittel, 3 fein
       flaeche: 0.35,                         Deckkraft der Kategorie-Farben (0: aus)
       umriss: true,                          Segmentgrenzen
       auswahl: <id>, hervor: <id>,           gewähltes bzw. überfahrenes Segment
       filter: function (seg) → bool,         andere Segmente abdunkeln
       luecken: false,                        Lückenkarte: Bildpunkte ohne Segment rot
       naht: false,                           Kerngrenzen und Nahtverstöße
       geaendert: false,                      Unterschied Vorstufe → Runde 1 markieren
       kern: '<teilkachel>',                  Kontextrand abdunkeln, Kern umranden
       gitter: false                          Koordinatengitter alle 100 px mit Beschriftung
     })
     Karte.passe(canvas)                      Zeichenfläche an Größe und Pixeldichte anpassen
     Karte.vorschau(canvas, stand, id)        Ausschnitt um ein Segment, Segment hervorgehoben
     Karte.punkt(canvas, ausschnitt, ev)      Maus-Ereignis → [x, y] in T0
     Karte.bei(stand, x, y)                   Segment-ID an einer Stelle
     Karte.stand(id), Karte.segment(stand, id), Karte.segmente(stand, teilkachel)
     Karte.teilkachel(id), Karte.klasse(code), Karte.aufEbene(code, ebene), Karte.farbe(code, ebene)
     Karte.zaehle(stand, teilkachel)          Zahlen: Segmente, unsicher, Kandidaten, Lücken, Naht
*/
(function () {
  'use strict'
  var D = window.DATEN
  var N = D.raster.n
  var Z = D.raster.zelle
  var UX = D.raster.ursprung[0]
  var UY = D.raster.ursprung[1]
  var KAT = {}
  D.kategorien.forEach(function (k) { KAT[k.code] = k })

  function dekodiere(s) {
    var a = new Int32Array(N * N)
    var p = 0
    s.split('/').forEach(function (zeile) {
      zeile.split(',').forEach(function (t) {
        var q = t.split('*')
        var v = parseInt(q[0], 36)
        var n = q.length > 1 ? parseInt(q[1], 36) : 1
        for (var i = 0; i < n; i++) a[p++] = v
      })
    })
    return a
  }

  var karten = {}
  var segIndex = {}
  function standDaten(id) {
    for (var i = 0; i < D.staende.length; i++) if (D.staende[i].id === id) return D.staende[i]
    throw new Error('Karte: Stand fehlt: ' + id)
  }
  function ids(stand) {
    if (!karten[stand]) karten[stand] = dekodiere(standDaten(stand).karte)
    return karten[stand]
  }
  function segment(stand, id) {
    if (!segIndex[stand]) {
      segIndex[stand] = {}
      standDaten(stand).segmente.forEach(function (s) { segIndex[stand][s.id] = s })
    }
    return segIndex[stand][id] || null
  }
  function aufEbene(code, ebene) {
    var t = String(code).split('.')
    return t.slice(0, Math.min(ebene || 3, t.length)).join('.')
  }
  function farbe(code, ebene) {
    var k = KAT[aufEbene(code, ebene)]
    return k ? k.farbe : '#808080'
  }
  function hexRgb(h) {
    return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)]
  }

  /* ---------- Luftbild (Platzhalter): Texturen je Klasse, einmal berechnet ---------- */
  var NATUR = {
    '1.1.1': [150, 92, 66], '1.1.2': [132, 136, 140], '1.2.1': [86, 89, 93], '1.2.2': [140, 136, 130],
    '1.2.3': [178, 162, 132], '1.2.4': [150, 146, 138], '1.3.3': [70, 176, 190], '1.4.1': [104, 146, 72],
    '1.4.2': [118, 96, 70], '1.4.3': [58, 86, 44], '2.1': [134, 154, 80], '2.2': [158, 130, 94],
    '2.3': [150, 146, 92], '2.4.1': [120, 128, 76], '3.1.1': [124, 156, 82], '3.1.2': [116, 148, 76],
    '3.3': [136, 140, 86], '3.4': [138, 152, 90], '4.2.1': [56, 84, 42], '4.2.2': [52, 80, 40],
    '4.2.3': [58, 86, 44], '4.2.4': [74, 98, 52], '5.1.2': [52, 70, 58], '5.2': [44, 72, 76],
    '5.3': [98, 116, 66], '6.1': [214, 196, 156]
  }
  function rausch(x, y) {
    var n = (x * 374761393 + y * 668265263) | 0
    n = (n ^ (n >>> 13)) * 1274126177 | 0
    return ((n ^ (n >>> 16)) >>> 0) / 4294967296
  }
  function glatt(x, y, s) {
    var gx = Math.floor(x / s), gy = Math.floor(y / s)
    var fx = x / s - gx, fy = y / s - gy
    var a = rausch(gx, gy), b = rausch(gx + 1, gy), c = rausch(gx, gy + 1), d = rausch(gx + 1, gy + 1)
    fx = fx * fx * (3 - 2 * fx); fy = fy * fy * (3 - 2 * fy)
    return a + (b - a) * fx + (c - a) * fy + (a - b - c + d) * fx * fy
  }
  var luftbild = null
  function bildCanvas() {
    if (luftbild) return luftbild
    var B = N * Z
    var kl = D.bild.klassen
    var karte = dekodiere(D.bild.karte)
    var cv = document.createElement('canvas')
    cv.width = B; cv.height = B
    var ctx = cv.getContext('2d')
    var img = ctx.createImageData(B, B)
    var px = img.data
    for (var y = 0; y < B; y++) {
      for (var x = 0; x < B; x++) {
        var jx = (glatt(x, y, 5) - 0.5) * 5, jy = (glatt(x + 91, y + 37, 5) - 0.5) * 5
        var ci = Math.max(0, Math.min(N - 1, Math.floor((x + jx) / Z)))
        var cj = Math.max(0, Math.min(N - 1, Math.floor((y + jy) / Z)))
        var code = kl[karte[cj * N + ci]]
        var f = NATUR[code] || [120, 120, 120]
        var ax = x + UX, ay = y + UY
        var m = 0.86 + 0.18 * glatt(ax, ay, 40) + 0.1 * (rausch(ax, ay) - 0.5)
        if (code === '2.4.1') m *= (Math.floor(ax / 10) % 2) ? 1.12 : 0.8
        else if (code === '2.1' || code === '3.1.1') m *= (Math.floor((ax + ay * 0.05) / 60) % 2) ? 1.04 : 0.96
        else if (code === '2.2') m *= 0.92 + 0.12 * Math.sin(ax / 3)
        else if (code.indexOf('4.2') === 0 || code === '1.4.3') m *= 0.7 + 0.55 * glatt(ax, ay, 6)
        else if (code === '1.1.1') m *= (ay < 104) ? 1.08 : 0.86
        else if (code === '5.2' || code === '5.1.2') m = 0.95 + 0.08 * glatt(ax, ay, 25)
        var o = (y * B + x) * 4
        px[o] = Math.min(255, f[0] * m); px[o + 1] = Math.min(255, f[1] * m); px[o + 2] = Math.min(255, f[2] * m); px[o + 3] = 255
      }
    }
    ctx.putImageData(img, 0, 0)
    luftbild = cv
    return cv
  }
  var luftbildGrau = null
  function bildGrau() {
    if (luftbildGrau) return luftbildGrau
    var farb = bildCanvas()
    var cv = document.createElement('canvas')
    cv.width = farb.width; cv.height = farb.height
    var ctx = cv.getContext('2d')
    ctx.drawImage(farb, 0, 0)
    var img = ctx.getImageData(0, 0, cv.width, cv.height)
    var p = img.data
    for (var i = 0; i < p.length; i += 4) {
      var g = 0.3 * p[i] + 0.59 * p[i + 1] + 0.11 * p[i + 2]
      p[i] = p[i + 1] = p[i + 2] = g
    }
    ctx.putImageData(img, 0, 0)
    luftbildGrau = cv
    return cv
  }

  /* ---------- Zeichnen ---------- */
  function passe(canvas) {
    var r = canvas.getBoundingClientRect()
    var d = window.devicePixelRatio || 1
    var b = Math.max(1, Math.round(r.width * d)), h = Math.max(1, Math.round(r.height * d))
    if (canvas.width !== b || canvas.height !== h) { canvas.width = b; canvas.height = h }
    return canvas
  }

  function zeichne(canvas, o) {
    o = o || {}
    var stand = o.stand || 'vorstufe'
    var a = o.ausschnitt || [UX, UY, N * Z, N * Z]
    var ebene = o.ebene || 3
    var flaeche = o.flaeche === undefined ? 0.35 : o.flaeche
    var umriss = o.umriss !== false
    var ctx = canvas.getContext('2d')
    var W = canvas.width, H = canvas.height
    var s = Math.min(W / a[2], H / a[3])
    var ox = (W - a[2] * s) / 2 - a[0] * s, oy = (H - a[3] * s) / 2 - a[1] * s
    ctx.save()
    ctx.fillStyle = '#0e0f11'
    ctx.fillRect(0, 0, W, H)
    ctx.beginPath()
    ctx.rect((W - a[2] * s) / 2, (H - a[3] * s) / 2, a[2] * s, a[3] * s)
    ctx.clip()
    ctx.imageSmoothingEnabled = s < 1
    if (o.bild !== false) ctx.drawImage(o.grau ? bildGrau() : bildCanvas(), ox + UX * s, oy + UY * s, N * Z * s, N * Z * s)

    var karte = ids(stand)
    var i0 = Math.max(0, Math.floor((a[0] - UX) / Z) - 1), i1 = Math.min(N - 1, Math.ceil((a[0] + a[2] - UX) / Z) + 1)
    var j0 = Math.max(0, Math.floor((a[1] - UY) / Z) - 1), j1 = Math.min(N - 1, Math.ceil((a[1] + a[3] - UY) / Z) + 1)
    var zs = Z * s
    function sx(i) { return ox + (UX + i * Z) * s }
    function sy(j) { return oy + (UY + j * Z) * s }

    // Flächen in Kategorie-Farbe (auf einem Raster in Zellauflösung, dann skaliert)
    if (flaeche > 0 || o.filter || o.luecken || o.geaendert) {
      var bw = i1 - i0 + 1, bh = j1 - j0 + 1
      var off = document.createElement('canvas')
      off.width = bw; off.height = bh
      var octx = off.getContext('2d')
      var img = octx.createImageData(bw, bh)
      var p = img.data
      var andere = o.geaendert ? ids(stand === 'vorstufe' ? 'runde1' : 'vorstufe') : null
      var andererStand = stand === 'vorstufe' ? 'runde1' : 'vorstufe'
      var farbCache = {}
      for (var j = j0; j <= j1; j++) {
        for (var i = i0; i <= i1; i++) {
          var id = karte[j * N + i]
          var q = ((j - j0) * bw + (i - i0)) * 4
          var r = 0, g = 0, b = 0, al = 0
          if (id === 0) {
            if (o.luecken) { r = 255; g = 40; b = 40; al = 255 }
          } else {
            var seg = segment(stand, id)
            if (o.filter && seg && !o.filter(seg)) { r = 8; g = 9; b = 11; al = 150 }
            else if (flaeche > 0 && seg) {
              var fc = farbCache[seg.klasse + '/' + ebene] || (farbCache[seg.klasse + '/' + ebene] = hexRgb(farbe(seg.klasse, ebene)))
              r = fc[0]; g = fc[1]; b = fc[2]; al = Math.round(255 * flaeche)
            }
            if (andere) {
              var alt = segment(andererStand, andere[j * N + i])
              var kneu = seg ? aufEbene(seg.klasse, ebene) : '', kalt = alt ? aufEbene(alt.klasse, ebene) : ''
              var grenzeNeu = (i < N - 1 && karte[j * N + i + 1] !== id) || (j < N - 1 && karte[(j + 1) * N + i] !== id)
              var aid = andere[j * N + i]
              var grenzeAlt = (i < N - 1 && andere[j * N + i + 1] !== aid) || (j < N - 1 && andere[(j + 1) * N + i] !== aid)
              if (kneu !== kalt || grenzeNeu !== grenzeAlt) { r = 255; g = 122; b = 217; al = 170 }
            }
          }
          p[q] = r; p[q + 1] = g; p[q + 2] = b; p[q + 3] = al
        }
      }
      octx.putImageData(img, 0, 0)
      ctx.imageSmoothingEnabled = false
      ctx.drawImage(off, sx(i0), sy(j0), bw * zs, bh * zs)
    }

    // Segmentgrenzen
    function grenzen(nur, farbeLinie, breite) {
      ctx.beginPath()
      for (var j = j0; j <= j1; j++) {
        for (var i = i0; i <= i1; i++) {
          var id = karte[j * N + i]
          if (i < N - 1) {
            var r = karte[j * N + i + 1]
            if (r !== id && (nur === undefined || id === nur || r === nur)) { ctx.moveTo(sx(i + 1), sy(j)); ctx.lineTo(sx(i + 1), sy(j + 1)) }
          }
          if (j < N - 1) {
            var u = karte[(j + 1) * N + i]
            if (u !== id && (nur === undefined || id === nur || u === nur)) { ctx.moveTo(sx(i), sy(j + 1)); ctx.lineTo(sx(i + 1), sy(j + 1)) }
          }
        }
      }
      ctx.strokeStyle = farbeLinie
      ctx.lineWidth = breite
      ctx.stroke()
    }
    if (umriss) grenzen(undefined, 'rgba(255,255,255,0.55)', Math.max(1, s * 0.6))
    if (o.hervor && o.hervor !== o.auswahl) grenzen(o.hervor, '#ffffff', 2)
    if (o.auswahl) grenzen(o.auswahl, '#ffeb3c', 2.5)

    // Kern und Kontextrand
    if (o.kern) {
      var tk = teilkachel(o.kern)
      if (tk) {
        var k = tk.kern
        ctx.fillStyle = 'rgba(8,9,11,0.55)'
        ctx.beginPath()
        ctx.rect(ox + a[0] * s - 2, oy + a[1] * s - 2, a[2] * s + 4, a[3] * s + 4)
        ctx.rect(ox + k[0] * s, oy + (k[1] + k[3]) * s, k[2] * s, -k[3] * s)
        ctx.fill('evenodd')
        ctx.strokeStyle = 'rgba(214,216,220,0.9)'
        ctx.lineWidth = 1.5
        ctx.strokeRect(ox + k[0] * s, oy + k[1] * s, k[2] * s, k[3] * s)
      }
    }

    // Nähte
    if (o.naht) {
      ctx.setLineDash([6, 5])
      ctx.strokeStyle = 'rgba(255,255,255,0.8)'
      ctx.lineWidth = 1.5
      ctx.beginPath()
      ctx.moveTo(ox + 500 * s, oy + 0); ctx.lineTo(ox + 500 * s, oy + 1000 * s)
      ctx.moveTo(ox + 0, oy + 500 * s); ctx.lineTo(ox + 1000 * s, oy + 500 * s)
      ctx.stroke()
      ctx.setLineDash([])
      standDaten(stand).naht.forEach(function (n) {
        ctx.strokeStyle = '#ff7ad9'
        ctx.lineWidth = Math.max(4, 6 * s)
        ctx.beginPath()
        if (n.achse === 'senkrecht') { ctx.moveTo(ox + n.lage * s, oy + n.von * s); ctx.lineTo(ox + n.lage * s, oy + n.bis * s) }
        else { ctx.moveTo(ox + n.von * s, oy + n.lage * s); ctx.lineTo(ox + n.bis * s, oy + n.lage * s) }
        ctx.stroke()
      })
    }

    // Koordinatengitter
    if (o.gitter) {
      ctx.strokeStyle = 'rgba(255,235,60,0.45)'
      ctx.lineWidth = 1
      ctx.fillStyle = 'rgba(255,235,60,0.9)'
      ctx.font = Math.round(11 * (window.devicePixelRatio || 1)) + 'px Segoe UI, system-ui, sans-serif'
      ctx.beginPath()
      for (var gx = Math.ceil(a[0] / 100) * 100; gx <= a[0] + a[2]; gx += 100) { ctx.moveTo(ox + gx * s, oy + a[1] * s); ctx.lineTo(ox + gx * s, oy + (a[1] + a[3]) * s) }
      for (var gy = Math.ceil(a[1] / 100) * 100; gy <= a[1] + a[3]; gy += 100) { ctx.moveTo(ox + a[0] * s, oy + gy * s); ctx.lineTo(ox + (a[0] + a[2]) * s, oy + gy * s) }
      ctx.stroke()
      for (gx = Math.ceil(a[0] / 100) * 100; gx <= a[0] + a[2]; gx += 100) ctx.fillText(String(gx), ox + gx * s + 3, oy + a[1] * s + 13)
      for (gy = Math.ceil(a[1] / 100) * 100; gy <= a[1] + a[3]; gy += 100) ctx.fillText(String(gy), ox + a[0] * s + 3, oy + gy * s - 3)
    }
    ctx.restore()
  }

  function teilkachel(id) {
    for (var i = 0; i < D.teilkacheln.length; i++) if (D.teilkacheln[i].id === id) return D.teilkacheln[i]
    return null
  }

  function vorschau(canvas, stand, id, extra) {
    var seg = segment(stand, id)
    if (!seg) return
    var k = seg.kasten
    var seite = Math.max(k[2], k[3]) * 1.5 + 24
    var cx = k[0] + k[2] / 2, cy = k[1] + k[3] / 2
    var o = { stand: stand, ausschnitt: [cx - seite / 2, cy - seite / 2, seite, seite], auswahl: id, flaeche: 0, umriss: false }
    if (extra) for (var key in extra) o[key] = extra[key]
    zeichne(canvas, o)
  }

  function punkt(canvas, a, ev) {
    var r = canvas.getBoundingClientRect()
    var s = Math.min(r.width / a[2], r.height / a[3])
    var x0 = (r.width - a[2] * s) / 2, y0 = (r.height - a[3] * s) / 2
    return [a[0] + (ev.clientX - r.left - x0) / s, a[1] + (ev.clientY - r.top - y0) / s]
  }

  function bei(stand, x, y) {
    var i = Math.floor((x - UX) / Z), j = Math.floor((y - UY) / Z)
    if (i < 0 || j < 0 || i >= N || j >= N) return 0
    return ids(stand)[j * N + i]
  }

  function segmente(stand, tk) {
    var alle = standDaten(stand).segmente
    return tk ? alle.filter(function (s) { return s.teilkacheln.indexOf(tk) >= 0 }) : alle.slice()
  }

  function zaehle(stand, tk) {
    var segs = segmente(stand, tk)
    var karte = ids(stand)
    var luecken = 0
    for (var i = 0; i < karte.length; i++) if (karte[i] === 0) luecken++
    return {
      segmente: segs.length,
      unsicher: segs.filter(function (s) { return s.sicher === 'nein' }).length,
      kandidaten: segs.filter(function (s) { return s.kandidaten && s.kandidaten.length }).length,
      luecken: luecken,
      naht: standDaten(stand).naht.filter(function (n) { return !tk || n.grenze.split(' | ').indexOf(tk) >= 0 }).length
    }
  }

  window.Karte = {
    zeichne: zeichne, passe: passe, vorschau: vorschau, punkt: punkt, bei: bei,
    stand: standDaten, segment: segment, segmente: segmente, teilkachel: teilkachel, zaehle: zaehle,
    klasse: function (code) { return KAT[code] || null }, aufEbene: aufEbene, farbe: farbe
  }

  /* ---------- Seite ---------- */
  document.getElementById('app').innerHTML = '<main class="u-inhalt" data-inhalt></main>'
  Entwurf.route('/', function () { Entwurf.gehe((window.RAHMEN && window.RAHMEN.start) || '/kachel/r0c0') })
})()

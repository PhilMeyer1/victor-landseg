/* Übersichtsseite (landseg seite). Je Bild ein Stand, das Ergebnis, in einem großen Bild; oben der
   Umschalter zwischen den Fassungen desselben Ausschnitts, darunter die Kachel-Wahl (vorige, Ganzer Ausschnitt,
   die Teilkacheln mit Miniatur und Lage, nächste; Pfeiltasten), links eine feste Leiste mit den Angaben zum
   Segment (unter der Maus, gewählt, Kommentar), unten die Schalter, rechts die Kategorienliste.
   Was sich beim Überfahren, Klicken oder Ziehen ändert, steht nur in der linken Leiste (feste Breite)
   oder im Bild selbst: Lage und Größe des Bildes bleiben dabei gleich.

   #/<F>/kachel/<tk>                Teilkachel in Fassung F
   #/<F>/kachel/<tk>/segment/<id>   dasselbe, ein Segment gewählt
   #/<F>/uebersicht                 ganzer Ausschnitt mit Kerngrenzen und Nahtabweichungen
   #/kommentare                     Kommentare, Export als JSON

   Klassen, Namen und Farben nur aus der Kategorienliste der jeweiligen Fassung (window.DATEN.fassungen). */
(function () {
  'use strict'
  var D = window.DATEN, E = D.einstellungen, F = E.farben
  var app = document.getElementById('app')
  var S = { ebene: E.start_ebene, deck: E.deckkraft, flaeche: true, umriss: true, luecken: false,
    naht: true, unsicher: false, gitter: false, liste: E.kategorienliste !== false }
  var SPEICHER = 'landseg-seite:' + D.manifest
  var neu = []
  try { neu = JSON.parse(localStorage.getItem(SPEICHER) || '[]') } catch (e) { neu = [] }
  function merke() { try { localStorage.setItem(SPEICHER, JSON.stringify(neu)) } catch (e) { /* ohne Speicher */ } }
  function alleKommentare() { return D.kommentare.concat(neu) }

  function el(t, c, h) { var e = document.createElement(t); if (c) e.className = c; if (h !== undefined) e.innerHTML = h; return e }
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c] }) }
  function rgba(h) {
    var a = h.length > 7 ? parseInt(h.slice(7, 9), 16) : 255
    return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16), a]
  }
  function css(h) { var c = rgba(h); return 'rgba(' + c[0] + ',' + c[1] + ',' + c[2] + ',' + (c[3] / 255).toFixed(3) + ')' }
  var FARBE = {}
  Object.keys(F).forEach(function (k) { FARBE[k] = rgba(F[k]) })
  if (!FARBE.kommentar) FARBE.kommentar = rgba('#4fc3f7')
  function zeit(z) { var d = new Date(z); return isNaN(d) ? String(z || '') : d.toLocaleString('de-AT', { dateStyle: 'short', timeStyle: 'short' }) }

  // --- Fassungen: jede mit eigener Kategorienliste ----------------------------------------------------
  var FS = {}, ERSTE = null
  D.fassungen.forEach(function (f) {
    var x = FS[f.kennung] = { f: f, KAT: {}, EBENEN: [], tk: {}, gesamt: null }
    if (!f.vorhanden) return
    f.kategorien.forEach(function (k) { x.KAT[k.code] = k })
    x.EBENEN = f.ebenen.map(function (e) { return e.ebene })
    if (!ERSTE) ERSTE = f.kennung
  })
  var FA = FS[ERSTE]
  // Ebene in der aktiven Fassung: die gewählte, sonst die nächstgröbere, die es dort gibt
  function EB() {
    var L = FA.EBENEN, e = L[0]
    L.forEach(function (x) { if (x <= S.ebene) e = x })
    return e
  }
  function ebeneInfo(e) { return FA.f.ebenen.filter(function (x) { return x.ebene === e })[0] || { name: String(e), klassen: 0 } }

  // --- Kategorien: ein Format für Maus, Auswahl und Liste --------------------------------------------
  function aufEbene(code, e) { var K = FA.KAT, k = K[code]; while (k && k.level > e && k.parent) k = K[k.parent]; return k || null }
  function kette(code) { var t = [], k = FA.KAT[code]; while (k) { t.unshift(k); k = k.parent ? FA.KAT[k.parent] : null } return t }
  function farbe(code, e) { var k = aufEbene(code, e); return k && k.color ? k.color : '#808080' }
  function unsicher(s) { return s.sicher === 'nein' || s.sicher === false }
  function sicherText(s) { return unsicher(s) ? '<span class="c-warn">unsicher</span>' : 'sicher' }
  function punkt(f) { return '<i class="c-punkt" style="background:' + f + '"></i>' }
  function janein(v) { return v === true || v === 'ja' ? 'ja' : v === false || v === 'nein' ? 'nein' : (v === undefined || v === null ? '–' : esc(v)) }
  function sicherheit(s) {
    var v = s.sicherheit
    if (v && typeof v === 'object') v = v.wert
    return typeof v === 'number' ? Math.round(v * 100) + ' %' : '–'
  }
  // Beschlüsse der Einigung an den Übergängen (`einigung` in segmente.json): je Beschluss Entscheidung, Nachbar, Klasse, Grund
  var EINIGUNG_ART = { gleich: 'gleiche Fläche', grenze: 'echte Grenze', unklar: 'unklar, als unsicher belegt' }
  function einigungZeilen(s) {
    if (!Array.isArray(s.einigung) || !s.einigung.length) return ''
    return s.einigung.map(function (b) {
      var k = b.klasse && FA.KAT[b.klasse]
      return '<dt>Einigung</dt><dd>' + esc(EINIGUNG_ART[b.entscheidung] || b.entscheidung) + ' mit ' + esc(b.mit) +
        (b.klasse ? ', Klasse ' + esc(k ? k.code + ' ' + k.name : b.klasse) : '') + ': ' + esc(b.grund) + '</dd>'
    }).join('')
  }
  // Segment in einer Form: Kopfzeile, dann je Ebene eine Zeile (die gezeigte Ebene hervorgehoben)
  function segZeilen(id, s) {
    if (!id) return '<div class="c-z c-fehler">kein Segment (Lücke)</div>'
    if (!s) return '<div class="c-z"><b>Segment ' + id + '</b> · <span class="c-fehler">ohne Eintrag in segmente.json</span></div>'
    var t = kette(s.klasse), e = EB(), h = '<div class="c-z"><b>Segment ' + id + '</b> · ' + sicherText(s) + '</div>'
    if (!t.length) return h + '<div class="c-z c-fehler">unbekannte Klasse ' + esc(s.klasse) + '</div>'
    h += t.map(function (k) {
      return '<div class="c-z' + (aufEbene(s.klasse, e) === k ? ' c-aktiv' : '') + '" title="' + esc(k.code + ' ' + k.name) + '">' +
        punkt(k.color || '#808080') + esc(k.code + ' ' + k.name) + '</div>'
    }).join('')
    if (FA.EBENEN.some(function (x) { return x > t[t.length - 1].level })) h += '<div class="c-z c-leise">feinere Stufe nicht unterschieden</div>'
    return h
  }

  // --- Daten laden: Bilder und Label-Karten (ID = R + 256·G + 65536·B) -------------------------------
  function bild(src) { return new Promise(function (ok, nein) { var i = new Image(); i.onload = function () { ok(i) }; i.onerror = nein; i.src = src }) }
  function alsCanvas(img) { var c = el('canvas'); c.width = img.width; c.height = img.height; c.getContext('2d').drawImage(img, 0, 0); return c }
  function alsIds(img) {
    var c = alsCanvas(img), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data
    var ids = new Int32Array(c.width * c.height)
    for (var i = 0; i < ids.length; i++) ids[i] = d[i * 4] + (d[i * 4 + 1] << 8) + (d[i * 4 + 2] << 16)
    return ids
  }
  function stand(roh, img, w, h) {
    var st = { roh: roh, ids: alsIds(img), w: w, h: h, seg: {}, flaeche: {} }
    roh.segmente.forEach(function (s) { st.seg[s.id] = s })
    for (var i = 0; i < st.ids.length; i++) st.flaeche[st.ids[i]] = (st.flaeche[st.ids[i]] || 0) + 1
    return st
  }
  var TK = {}, AUSSCHNITT = null, BLICK = {}
  // Zuletzt angeklickte Stelle: nach dem Wechsel der Fassung wird dort wieder gewählt
  var LETZT = null, UEBERNAHME = false
  // Aktuelle Ansicht für Tasten: { abwaehlen, wechsle }
  var AKTIV = {}
  function laden() {
    var arbeit = [bild(D.ausschnitt.bild).then(function (i) { AUSSCHNITT = alsCanvas(i) })]
    D.teilkacheln.forEach(function (t) {
      var x = TK[t.id] = { t: t, w: t.kontext.breite, h: t.kontext.hoehe }
      arbeit.push(bild(t.bild).then(function (i) { x.bild = alsCanvas(i) }))
    })
    D.fassungen.forEach(function (f) {
      if (!f.vorhanden) return
      var x = FS[f.kennung]
      if (f.gesamt) arbeit.push(bild(f.gesamt).then(function (i) { x.gesamt = { ids: alsIds(i), w: i.width, h: i.height } }))
      D.teilkacheln.forEach(function (t) {
        var r = f.teilkacheln[t.id]
        if (r) arbeit.push(bild(r.labels).then(function (i) { x.tk[t.id] = stand(r, i, t.kontext.breite, t.kontext.hoehe) }))
      })
    })
    return Promise.all(arbeit)
  }
  function ersteKachel(fx) { return (D.teilkacheln.filter(function (t) { return fx.tk[t.id] })[0] || D.teilkacheln[0]).id }

  // --- Teilkacheln in Lage-Reihenfolge (1 oben links … zeilenweise), Miniaturen für die Kachel-Wahl ----
  var REIHE = D.teilkacheln.slice().sort(function (a, b) { return a.nummer - b.nummer })
  var ANZAHL = REIHE.length
  var SPALTEN = 1 + Math.max.apply(null, REIHE.map(function (t) { return t.spalte }))
  var MINI = {}
  function nummer(tk) { for (var i = 0; i < ANZAHL; i++) if (REIHE[i].id === tk) return i + 1; return 0 }
  // Miniaturen einmal nach dem Laden aus denselben Bildern verkleinert (keine zweite Kopie in der Datei)
  function miniaturen() {
    function klein(quelle, x, y, b, h) {
      var c = el('canvas'), s = 112 / Math.max(b, h)
      c.width = Math.max(1, Math.round(b * s)); c.height = Math.max(1, Math.round(h * s))
      var ctx = c.getContext('2d'); ctx.imageSmoothingQuality = 'high'
      ctx.drawImage(quelle, x, y, b, h, 0, 0, c.width, c.height)
      return c.toDataURL('image/jpeg', 0.85)
    }
    REIHE.forEach(function (t) { var x = TK[t.id], k = t.kern_im_bild; MINI[t.id] = klein(x.bild, k.x, k.y, k.breite, k.hoehe) })
    MINI.ganz = klein(AUSSCHNITT, 0, 0, AUSSCHNITT.width, AUSSCHNITT.height)
  }
  // Schritt: 0 = Ganzer Ausschnitt, 1 … ANZAHL = Teilkacheln, -1 = keiner (Kommentare)
  function schritt(aktiv, tk) { return aktiv === 'uebersicht' ? 0 : aktiv === 'kachel' ? nummer(tk) : -1 }
  function wegSchritt(K, n) { return n === 0 ? '/' + K + '/uebersicht' : '/' + K + '/kachel/' + REIHE[n - 1].id }
  function nameSchritt(n) { return n === 0 ? 'Ganzer Ausschnitt' : REIHE[n - 1].lage }
  // Raster-Symbol: die Teilkacheln in ihrer Lage, die gemeinten hell (aktiv: gelb)
  function raster(an) {
    return '<span class="c-raster" style="grid-template-columns:repeat(' + SPALTEN + ',6px)" aria-hidden="true">' + REIHE.map(function (t) {
      return '<i' + (an === 'alle' || an === t.id ? ' class="c-an"' : '') + '></i>'
    }).join('') + '</span>'
  }
  // vorige / nächste: Link auf den Nachbarschritt, am Ende ein gesperrter Knopf (gleich groß)
  function pfeil(K, n, richtung) {
    var ziel = n < 0 ? -1 : n + richtung, wort = richtung < 0 ? 'vorige' : 'nächste'
    var zeichen = '<span class="c-zeichen" aria-hidden="true">' + (richtung < 0 ? '‹' : '›') + '</span>'
    var klasse = 'c-pfeil c-pfeil-' + (richtung < 0 ? 'zurueck' : 'vor'), taste = 'Pfeiltaste ' + (richtung < 0 ? '←' : '→')
    var gesperrt = ziel < 0 || ziel > ANZAHL
    var unter = gesperrt ? (n === 0 && richtung < 0 ? 'Anfang' : n === ANZAHL ? 'letzte Teilkachel' : '–') : esc(nameSchritt(ziel))
    var innen = (richtung < 0 ? zeichen : '') + '<span class="c-pfeiltext"><b>' + wort + '</b><small>' + unter + '</small></span>' + (richtung > 0 ? zeichen : '')
    return gesperrt ? '<button type="button" class="' + klasse + '" disabled title="' + taste + '">' + innen + '</button>'
      : '<a class="' + klasse + '" href="#' + esc(wegSchritt(K, ziel)) + '" title="' + taste + '">' + innen + '</a>'
  }
  // Kachel-Wahl unter dem Kopf: vorige | Ganzer Ausschnitt | Teilkacheln mit Miniatur, Raster und Lage | nächste.
  // Gleiche Höhe in allen Ansichten und Fassungen: das Bild darunter springt beim Umschalten nicht.
  function kachelWahl(K, aktiv, tk) {
    var n = schritt(aktiv, tk)
    var nav = el('nav', 'c-kachelwahl'); nav.setAttribute('aria-label', 'Teilkacheln')
    var ganz = '<a class="c-reiter c-reiter-ganz" href="#/' + esc(K) + '/uebersicht"' + (n === 0 ? ' aria-current="page"' : '') +
      ' title="Ganzer Ausschnitt ' + esc(D.name) + '"><span class="c-bild"><img class="c-mini" src="' + MINI.ganz + '" alt=""></span>' +
      '<span class="c-text"><span class="c-ober">' + raster('alle') + 'Übersicht</span><b>Ganzer Ausschnitt</b>' +
      '<span class="c-stand">alle ' + ANZAHL + ' Teilkacheln</span></span></a>'
    var reiter = REIHE.map(function (t, i) {
      var st = FA.tk[t.id]
      return '<a class="c-reiter' + (st ? '' : ' c-ohne') + '" href="#/' + esc(K) + '/kachel/' + t.id + '"' + (n === i + 1 ? ' aria-current="page"' : '') +
        ' title="Teilkachel ' + (i + 1) + ' von ' + ANZAHL + ': ' + esc(t.lage) + ' (' + t.id + ')' + (st ? '' : ', ohne Daten') + '">' +
        '<span class="c-bild"><img class="c-mini" src="' + MINI[t.id] + '" alt=""><span class="c-nr">' + (i + 1) + '</span></span>' +
        '<span class="c-text"><span class="c-ober">' + raster(t.id) + 'Teilkachel ' + (i + 1) + ' <span class="c-kennung">' + t.id + '</span></span>' +
        '<b>' + esc(t.lage) + '</b><span class="c-stand">' + (st ? st.roh.segmente.length + ' Segmente' : 'keine Daten') + '</span></span></a>'
    }).join('')
    nav.innerHTML = pfeil(K, n, -1) + '<div class="c-spur">' + ganz + '<span class="c-trenner" aria-hidden="true"></span>' +
      '<div class="c-vier" style="grid-template-columns:repeat(' + ANZAHL + ',minmax(0,1fr))">' + reiter + '</div></div>' + pfeil(K, n, 1)
    return nav
  }
  // Hinweis im Bild der Teilkachel: „Teilkachel n von N“, Fortschritt und der nächste Schritt
  function fortschritt(K, tkId) {
    var n = nummer(tkId)
    var punkte = '<span class="c-punkte" aria-hidden="true">' + REIHE.map(function (t, i) {
      return '<i class="' + (i + 1 === n ? 'c-hier' : i + 1 < n ? 'c-war' : '') + '"></i>'
    }).join('') + '</span>'
    var weiter = n < ANZAHL
      ? '<a class="c-weiter" href="#' + esc(wegSchritt(K, n + 1)) + '">weiter: Teilkachel ' + (n + 1) + ', ' + esc(nameSchritt(n + 1)) + ' <span aria-hidden="true">›</span></a>'
      : '<a class="c-weiter" href="#' + esc(wegSchritt(K, 0)) + '">alle ' + ANZAHL + ' gesehen · Ganzer Ausschnitt <span aria-hidden="true">›</span></a>'
    return el('div', 'c-fortschritt', '<span class="c-fz">Teilkachel <b>' + n + '</b> von ' + ANZAHL + '</span>' + punkte + weiter +
      '<span class="c-tasten" title="Pfeiltasten wechseln die Teilkachel"><kbd>←</kbd><kbd>→</kbd></span>')
  }

  // --- Zeichnen --------------------------------------------------------------------------------------
  function passe(c) {
    var r = c.getBoundingClientRect(), d = window.devicePixelRatio || 1
    var b = Math.max(1, Math.round(r.width * d)), h = Math.max(1, Math.round(r.height * d))
    if (c.width !== b || c.height !== h) { c.width = b; c.height = h }
  }
  function lage(c, a) {
    var s = Math.min(c.width / a[2], c.height / a[3])
    return { s: s, ox: (c.width - a[2] * s) / 2 - a[0] * s, oy: (c.height - a[3] * s) / 2 - a[1] * s }
  }
  function punktIm(c, a, ev) {
    var r = c.getBoundingClientRect(), d = c.width / r.width, L = lage(c, a)
    return [((ev.clientX - r.left) * d - L.ox) / L.s, ((ev.clientY - r.top) * d - L.oy) / L.s]
  }
  // Farbe f mit Deckkraft al über den Bildpunkt legen („über“-Mischung, Bildpuffer bleibt durchsichtig,
  // wo nichts liegt): das Luftbild darunter scheint durch
  function setze(p, i, f, al) {
    var a = al === undefined ? f[3] / 255 : al
    if (a <= 0) return
    var ad = p[i + 3] / 255, ao = a + ad * (1 - a)
    p[i] = (f[0] * a + p[i] * ad * (1 - a)) / ao
    p[i + 1] = (f[1] * a + p[i + 1] * ad * (1 - a)) / ao
    p[i + 2] = (f[2] * a + p[i + 2] * ad * (1 - a)) / ao
    p[i + 3] = ao * 255
  }
  function randVon(ids, w, n, i, id, weite) {
    var x = i % w
    for (var d = 1; d <= weite; d++) {
      if (x - d < 0 || x + d >= w || i - d * w < 0 || i + d * w >= n) return true
      if (ids[i - d] !== id || ids[i + d] !== id || ids[i - d * w] !== id || ids[i + d * w] !== id) return true
    }
    return false
  }
  // Überlagerung in Bildpunkten der Teilkachel: Flächen, Abblenden, Lücken, Grenzen, Kommentare, Maus, Auswahl
  function ueberlagerung(st, o) {
    var w = st.w, h = st.h, ids = st.ids, aus = new ImageData(w, h), p = aus.data, e = EB(), dk = {}
    for (var i = 0, n = w * h; i < n; i++) {
      var q = i * 4, id = ids[i], s = st.seg[id], x = i % w
      if (!id || !s) { if (o.luecken) setze(p, q, FARBE.luecke, 1); continue }
      var k = aufEbene(s.klasse, e), code = k ? k.code : ''
      var dunkel = (o.filter && !o.filter(s)) || (o.hervor && code !== o.hervor)
      if (dunkel) setze(p, q, FARBE.abgedunkelt)
      else if (S.flaeche && S.deck > 0) { var f = dk[code] || (dk[code] = rgba(farbe(s.klasse, e))); setze(p, q, f, S.deck) }
      if (S.umriss && ((x + 1 < w && ids[i + 1] !== id) || (i + w < n && ids[i + w] !== id))) setze(p, q, FARBE.umriss)
      if (o.kommentiert[id] && randVon(ids, w, n, i, id, 1)) setze(p, q, FARBE.kommentar, 1)
    }
    ;[[o.hover, FARBE.hover, 1], [o.auswahl, FARBE.auswahl, 2]].forEach(function (z) {
      if (!z[0]) return
      for (var i = 0, n = w * h; i < n; i++) {
        if (ids[i] !== z[0]) continue
        if (randVon(ids, w, n, i, z[0], z[2])) setze(p, i * 4, z[1], 1)
        else if (z[2] === 2) setze(p, i * 4, [255, 255, 255, 255], 0.12)
      }
    })
    return aus
  }
  function zeichneTafel(c, x, st, o, a) {
    passe(c)
    var ctx = c.getContext('2d'), L = lage(c, a), s = L.s
    ctx.save()
    ctx.fillStyle = '#0e0f11'; ctx.fillRect(0, 0, c.width, c.height)
    ctx.imageSmoothingEnabled = s < 1
    ctx.drawImage(x.bild, L.ox, L.oy, x.w * s, x.h * s)
    if (st) {
      var off = el('canvas'); off.width = x.w; off.height = x.h
      off.getContext('2d').putImageData(ueberlagerung(st, o), 0, 0)
      ctx.imageSmoothingEnabled = false
      ctx.drawImage(off, L.ox, L.oy, x.w * s, x.h * s)
    }
    // Kern und Kontextrand
    var k = x.t.kern_im_bild
    ctx.fillStyle = 'rgba(8,9,11,0.5)'; ctx.beginPath()
    ctx.rect(L.ox, L.oy, x.w * s, x.h * s); ctx.rect(L.ox + k.x * s, L.oy + (k.y + k.hoehe) * s, k.breite * s, -k.hoehe * s)
    ctx.fill('evenodd')
    ctx.strokeStyle = css(F.kern); ctx.lineWidth = 1.5; ctx.strokeRect(L.ox + k.x * s, L.oy + k.y * s, k.breite * s, k.hoehe * s)
    if (S.naht && st) naehte(ctx, L, st.roh.naht)
    if (S.gitter) gitter(ctx, L, [0, 0, x.w, x.h])
    ctx.restore()
  }
  function naehte(ctx, L, liste) {
    ctx.strokeStyle = css(F.naht_verstoss); ctx.lineWidth = Math.max(3, 2.5 * L.s); ctx.lineCap = 'round'
    ctx.beginPath()
    liste.forEach(function (v) {
      var senk = v.von[0] === v.bis[0]
      var x0 = v.von[0], y0 = v.von[1], x1 = v.bis[0] + (senk ? 0 : 1), y1 = v.bis[1] + (senk ? 1 : 0)
      ctx.moveTo(L.ox + x0 * L.s, L.oy + y0 * L.s); ctx.lineTo(L.ox + x1 * L.s, L.oy + y1 * L.s)
    })
    ctx.stroke()
  }
  function gitter(ctx, L, r) {
    var g = E.gitter_abstand, d = window.devicePixelRatio || 1
    ctx.strokeStyle = css(F.gitter); ctx.fillStyle = css(F.auswahl); ctx.lineWidth = 1
    ctx.font = Math.round(11 * d) + 'px Segoe UI, system-ui, sans-serif'
    ctx.beginPath()
    for (var gx = 0; gx <= r[2]; gx += g) { ctx.moveTo(L.ox + gx * L.s, L.oy); ctx.lineTo(L.ox + gx * L.s, L.oy + r[3] * L.s) }
    for (var gy = 0; gy <= r[3]; gy += g) { ctx.moveTo(L.ox, L.oy + gy * L.s); ctx.lineTo(L.ox + r[2] * L.s, L.oy + gy * L.s) }
    ctx.stroke()
    for (gx = 0; gx <= r[2]; gx += g) ctx.fillText(String(gx), L.ox + gx * L.s + 3, L.oy + 13 * d)
    for (gy = g; gy <= r[3]; gy += g) ctx.fillText(String(gy), L.ox + 3, L.oy + gy * L.s - 3)
  }

  // --- Kopf: Fassungen, Teilkacheln, Kommentare -------------------------------------------------------
  function wechsleFassung(kennung, aktiv, tk) {
    var ziel = FS[kennung]
    if (!ziel || !ziel.f.vorhanden) return
    if (aktiv === 'uebersicht') { gehe('/' + ziel.f.kennung + '/uebersicht'); return }
    UEBERNAHME = aktiv === 'kachel'
    gehe('/' + ziel.f.kennung + '/kachel/' + (aktiv === 'kachel' ? tk : ersteKachel(ziel)))
  }
  // Kopf: schlanke Zeile (Name, Fassungen, Kommentare), darunter die Kachel-Wahl
  function kopf(aktiv, tk) {
    var oben = el('div', 'c-oben'), h = el('header', 'c-kopf'), K = FA.f.kennung
    h.innerHTML = '<b>Ausschnitt ' + esc(D.name) + '</b>' +
      '<div class="c-fassungen" role="group" aria-label="Fassung">' + D.fassungen.map(function (f) {
        return '<button data-fassung="' + esc(f.kennung) + '" aria-pressed="' + (aktiv !== 'kommentare' && f.kennung === K) + '"' +
          (f.vorhanden ? ' title="Umschalt + ' + esc(f.kennung) + '"' : ' disabled title="Für diese Fassung gibt es noch keine Ergebnisse"') + '>' +
          esc(f.kennung) + '<span class="c-fname"> · ' + esc(f.name) + '</span>' + (f.vorhanden ? '' : ' <span>(noch leer)</span>') + '</button>'
      }).join('') + '</div><span></span>' +
      '<span class="c-rechts"><a href="#/kommentare"' + (aktiv === 'kommentare' ? ' aria-current="page"' : '') + ' data-kommzahl>Kommentare (' + alleKommentare().length + ')</a></span>' +
      '<p class="c-beschr" title="' + esc(aktiv === 'kommentare' ? '' : FA.f.beschreibung) + '">' +
      (aktiv === 'kommentare' ? 'Kommentare zu allen Fassungen' : '<b>' + esc(K + ' · ' + FA.f.name) + '</b> ' + esc(FA.f.beschreibung)) + '</p>'
    h.addEventListener('click', function (ev) {
      var b = ev.target.closest('[data-fassung]'); if (!b || b.disabled) return
      wechsleFassung(b.dataset.fassung, aktiv, tk)
    })
    AKTIV.wechsle = function (kennung) { wechsleFassung(kennung, aktiv, tk) }
    oben.appendChild(h)
    oben.appendChild(kachelWahl(K, aktiv, tk))
    return oben
  }
  // Zwei getrennte Zahlen an den Übergängen: Schnittlinien ohne Bildkante (Nahtregel, wie `landseg naht`) und
  // Stellen, an denen gleiche Flächen verschiedene Klassen haben (wie `landseg einigung messen`, davon unsicher belegt)
  function schnittText(n) {
    return n ? '<span class="c-warn">' + n + (n === 1 ? ' Schnittlinie' : ' Schnittlinien') + ' an Nähten ohne Bildkante</span>' : '<span class="c-ok">keine Schnittlinie an Nähten ohne Bildkante</span>'
  }
  function einigungText(e, fehler) {
    if (!e) return '<span class="c-leise">Klassen an den Übergängen nicht gezählt' + (fehler ? ': ' + esc(fehler) : ': nicht alle Teilkacheln haben Daten') + '</span>'
    if (!e.stellen) return '<span class="c-ok">Gleiche Flächen haben überall dieselbe Klasse</span>'
    return '<span class="' + (e.offen.paare ? 'c-warn' : 'c-leise') + '">' + e.stellen + (e.stellen === 1 ? ' Stelle, an der gleiche Flächen verschiedene Klassen haben' : ' Stellen, an denen gleiche Flächen verschiedene Klassen haben') +
      ' (davon ' + e.unsicher.paare + ' unsicher belegt)</span>'
  }
  function befundText(st) {
    var b = st.roh.pruefen
    if (b.ok) return '<span class="c-ok">lückenlos</span>'
    var t = []
    if (b.ohne_segment) t.push(b.ohne_segment + ' Bildpunkte ohne Segment')
    if (b.nicht_zusammenhaengend.length) t.push(b.nicht_zusammenhaengend.length + ' Segmente zerfallen in Teile')
    if (!t.length) t.push(b.maengel.length + ' Mängel')
    return '<span class="c-fehler">' + t.join(', ') + '</span>'
  }
  var LEGENDE = '<details class="c-legende"><summary>Was bedeutet …?</summary><dl>' +
    '<dt>Fassung</dt><dd>Eine Art, die Flächen einzuteilen; oben umschalten (auch mit Umschalt + A, B, C …).</dd>' +
    '<dt>Teilkachel</dt><dd>Eines der Bildstücke, in die der Ausschnitt geteilt ist; oben in der Kachel-Wahl oder mit den Pfeiltasten ← → wechseln (Kennung r = Zeile, c = Spalte).</dd>' +
    '<dt>Kern</dt><dd>Der Teil im hellen Rahmen: nur er zählt für diese Teilkachel.</dd>' +
    '<dt>Rand</dt><dd>Der abgedunkelte Streifen außen: Überlappung mit den Nachbarn, nur zur Orientierung.</dd>' +
    '<dt>Naht</dt><dd>Grenze zwischen zwei Teilkacheln. Rosa Linie: Schnittlinie ohne Bildkante, dort passen die Segmente der Nachbarn nicht zusammen. Getrennt gezählt: Stellen, an denen gleiche Flächen über einen Übergang (Naht oder Mitte der Teilkachel) verschiedene Klassen haben; unsicher belegt heißt, die Einigung der KI blieb dort offen, mit Grund.</dd>' +
    '<dt>Lücke</dt><dd>Bildpunkt ohne Segment; mit „Lücken“ rot gezeigt.</dd>' +
    '<dt>unsicher</dt><dd>Die KI war sich bei der Kategorie nicht sicher.</dd>' +
    '<dt>Blauer Rand</dt><dd>Segment mit Kommentar.</dd></dl></details>'

  // --- Ansicht einer Teilkachel ----------------------------------------------------------------------
  function ansicht(tkId, auswahl) {
    var x = TK[tkId]
    if (!x) { gehe('/' + FA.f.kennung + '/kachel/' + ersteKachel(FA)); return }
    var st = FA.tk[tkId] || null
    var Z = { a: BLICK[tkId] || [0, 0, x.w, x.h], sel: auswahl && st && st.seg[auswahl] ? +auswahl : null, hover: null, hervor: null, maus: null }
    if (!Z.sel && UEBERNAHME && st && LETZT && LETZT.tk === tkId) {
      var j = Math.floor(LETZT.y) * x.w + Math.floor(LETZT.x)
      if (st.ids[j] && st.seg[st.ids[j]]) Z.sel = st.ids[j]
    }
    UEBERNAHME = false
    var K = FA.f.kennung
    function kommentiert() {
      var m = {}
      alleKommentare().forEach(function (k) { if ((k.fassung || ERSTE) === K && k.teilkachel === tkId) m[k.segment] = (m[k.segment] || 0) + 1 })
      return m
    }
    var KOM = kommentiert()

    var wurzel = el('div', 'c-seite')
    wurzel.appendChild(kopf('kachel', tkId))
    var mitte = el('div', 'c-mitte')
    // linke Leiste: feste Breite, feste Bereiche; hier ändert sich alles, was Maus und Klick zeigen
    var info = el('aside', 'c-info'); info.setAttribute('aria-label', 'Segment')
    info.innerHTML = '<section class="c-mausfeld" data-maus aria-live="polite"></section>' +
      '<section class="c-wahl" data-wahl></section>' +
      '<form class="c-komm" data-komm><textarea rows="3" placeholder="Kommentar zum gewählten Segment" aria-label="Kommentar"></textarea>' +
      '<div class="c-knoepfe"><button type="submit" data-vormerken disabled>Vormerken</button><button type="button" data-export>Export (JSON)</button></div>' +
      '<p class="c-status" data-status>Kommentare bleiben nur in diesem Browser, bis Sie sie exportieren.</p></form>' + LEGENDE
    mitte.appendChild(info)
    var f = el('figure', 'c-tafel')
    var cap = '<b>Teilkachel ' + nummer(tkId) + ' von ' + ANZAHL + ' · ' + esc(x.t.lage) + '</b><span class="c-kennung">' + tkId + '</span>'
    if (st) {
      var un = st.roh.segmente.filter(unsicher).length
      cap += '<span>' + st.roh.segmente.length + ' Segmente, ' + un + ' davon unsicher</span>' + befundText(st) +
        '<span>' + (FA.f.naht ? schnittText(st.roh.naht.length) : '<span class="c-leise">Nähte nicht geprüft: nicht alle Teilkacheln haben Daten</span>') + '</span>' +
        '<span>' + einigungText(st.roh.einigung, FA.f.einigung_fehler) + '</span>'
    }
    f.innerHTML = '<figcaption>' + cap + '</figcaption>'
    var cv = el('canvas', 'c-bild'); cv.setAttribute('aria-label', 'Teilkachel ' + tkId + ', Fassung ' + K)
    f.appendChild(cv)
    if (!st) f.appendChild(el('div', 'c-leer', 'Fassung ' + esc(K) + ' hat für ' + tkId + ' noch keine Ergebnisse.'))
    f.appendChild(fortschritt(K, tkId))
    mitte.appendChild(f)
    var kat = el('aside', 'c-kat'); kat.setAttribute('aria-label', 'Kategorien'); kat.hidden = !S.liste
    mitte.appendChild(kat)
    wurzel.appendChild(mitte)

    // Zahl der Kategorien je Ebene, die in dieser Teilkachel vorkommen
    function imBild(e) {
      if (!st) return 0
      var m = {}
      st.roh.segmente.forEach(function (s) { var k = aufEbene(s.klasse, e); m[k ? k.code : '?'] = 1 })
      return Object.keys(m).length
    }
    var leiste = el('section', 'c-leiste'); leiste.setAttribute('aria-label', 'Steuerung')
    function an(k) { return ' aria-pressed="' + !!S[k] + '"' }
    leiste.innerHTML =
      '<div class="c-gruppe"><span class="c-etikett">Ebene</span>' + FA.f.ebenen.map(function (e) {
        return '<button data-ebene="' + e.ebene + '" aria-pressed="' + (EB() === e.ebene) + '" title="im Bild ' + imBild(e.ebene) + ' von ' + e.klassen +
          ' Kategorien dieser Ebene">' + esc(e.name) + '</button>' }).join('') + '</div>' +
      '<div class="c-gruppe"><span class="c-etikett">Zeigen</span>' +
      '<button data-schalter="flaeche"' + an('flaeche') + '>Flächen</button>' +
      '<label class="c-regler"><span data-deckwert>Deckkraft ' + Math.round(S.deck * 100) + ' %</span>' +
      '<input type="range" min="0" max="100" value="' + Math.round(S.deck * 100) + '" aria-label="Deckkraft der Flächen" data-deck></label>' +
      '<button data-schalter="umriss"' + an('umriss') + '>Umriss</button>' +
      '<button data-schalter="luecken"' + an('luecken') + '>Lücken</button>' +
      '<button data-schalter="naht"' + an('naht') + '>Nähte</button>' +
      '<button data-schalter="unsicher"' + an('unsicher') + '>Nur unsicher</button>' +
      '<button data-schalter="gitter"' + an('gitter') + '>Gitter</button>' +
      '<button data-schalter="liste"' + an('liste') + '>Liste rechts</button></div>' +
      '<div class="c-gruppe"><span class="c-etikett">Bild</span>' +
      '<button data-zoom="0.667" aria-label="Verkleinern">−</button><button data-zoom="fit">Ganz</button><button data-zoom="1.5" aria-label="Vergrößern">+</button>' +
      '<span class="c-zoomwert" data-zoomwert></span></div>'
    wurzel.appendChild(leiste)
    app.innerHTML = ''; app.appendChild(wurzel)

    var mausFeld = info.querySelector('[data-maus]'), wahl = info.querySelector('[data-wahl]')
    var ta = info.querySelector('[data-komm] textarea'), vormerken = info.querySelector('[data-vormerken]'), status = info.querySelector('[data-status]')
    var zoomwert = leiste.querySelector('[data-zoomwert]')

    function opt() {
      return { luecken: S.luecken, hervor: Z.hervor, auswahl: Z.sel, hover: Z.hover, filter: S.unsicher ? unsicher : null, kommentiert: KOM }
    }
    var plan = 0
    function zeichne() {
      BLICK[tkId] = Z.a
      zeichneTafel(cv, x, st, opt(), Z.a)
      zoomwert.textContent = 'Zoom ' + Math.round(100 * Math.max(x.w, x.h) / Math.max(Z.a[2], Z.a[3])) + ' %'
    }
    function spaeter() { if (!plan) plan = requestAnimationFrame(function () { plan = 0; zeichne() }) }

    function zeigeMaus() {
      if (!st) { mausFeld.innerHTML = '<h3>Unter der Maus</h3><p class="c-leise">Für diese Teilkachel gibt es in dieser Fassung keine Daten.</p>'; return }
      if (!Z.maus) { mausFeld.innerHTML = '<h3>Unter der Maus</h3><p class="c-leise">Mit der Maus über das Bild fahren: Hier steht, zu welchem Segment und welcher Kategorie die Stelle gehört.</p>'; return }
      var id = Z.hover
      mausFeld.innerHTML = '<h3>Unter der Maus <span>x ' + Math.floor(Z.maus[0]) + ', y ' + Math.floor(Z.maus[1]) + (Z.sel && id === Z.sel ? ' · gewählt' : '') + '</span></h3>' + segZeilen(id, st.seg[id])
    }
    function zeigeWahl() {
      vormerkenPruefen()
      if (!st) { wahl.innerHTML = ''; return }
      if (!Z.sel) {
        wahl.innerHTML = '<h3>Gewählt</h3><p class="c-leise">Ein Segment im Bild anklicken, um es zu wählen und zu kommentieren. ' +
          'Esc oder ein Klick neben das Bild hebt die Wahl auf.</p>'
        return
      }
      var s = st.seg[Z.sel], h = '<h3>Gewählt <button type="button" data-abwaehlen>Auswahl aufheben</button></h3>' + segZeilen(Z.sel, s)
      if (s) {
        h += '<dl class="c-werte"><dt>Fläche</dt><dd>' + (st.flaeche[Z.sel] || 0) + ' Bildpunkte</dd>' +
          '<dt>Sicherheit</dt><dd>' + sicherheit(s) + '</dd>' +
          '<dt>Liegt im Kern</dt><dd>' + janein(s.im_kern) + '</dd>' +
          (s.im_siedlung !== undefined ? '<dt>Im Siedlungsgebiet</dt><dd>' + janein(s.im_siedlung) + '</dd>' : '') +
          (s.eingriffe ? '<dt>Bearbeitet</dt><dd>' + s.eingriffe.length + '×</dd>' : '') + einigungZeilen(s) + '</dl>'
        var eigene = alleKommentare().filter(function (k) { return (k.fassung || ERSTE) === K && k.teilkachel === tkId && +k.segment === Z.sel })
        if (eigene.length) h += '<div class="c-eigene"><b>Kommentare</b>' + eigene.map(function (k) { return '<p>' + esc(k.text) + ' <span>' + esc(zeit(k.zeit)) + '</span></p>' }).join('') + '</div>'
        var felder = Object.keys(s).map(function (k) {
          var v = s[k]; if (typeof v === 'object' && v !== null) v = JSON.stringify(v)
          return '<tr><td>' + esc(k) + '</td><td>' + esc(v) + '</td></tr>' }).join('')
        var kk = FA.KAT[s.klasse]
        if (kk && kk.image_cue) felder += '<tr><td>Merkmal</td><td>' + esc(kk.image_cue) + '</td></tr>'
        h += '<details class="c-technik"><summary>Technische Angaben</summary><table>' + felder + '</table><p>Daten: ' + esc(st.roh.quelle) + '</p></details>'
      }
      wahl.innerHTML = h
    }
    function vormerkenPruefen() { ta.disabled = !Z.sel; vormerken.disabled = !Z.sel || !ta.value.trim() }
    function liste() {
      if (!S.liste || !st) { kat.innerHTML = ''; return }
      var z = {}, fl = {}, gesamt = 0, e = EB()
      st.roh.segmente.forEach(function (s) {
        var k = aufEbene(s.klasse, e), c = k ? k.code : '?'
        z[c] = (z[c] || 0) + 1; fl[c] = (fl[c] || 0) + (st.flaeche[s.id] || 0); gesamt += st.flaeche[s.id] || 0
      })
      var info = ebeneInfo(e)
      kat.innerHTML = '<h2>Im Bild · Ebene ' + esc(info.name) + ' · ' + Object.keys(z).length + ' von ' + info.klassen + ' Kategorien</h2>' +
        // Knopf immer da (ohne Hervorhebung ausgegraut), damit die Liste darunter nicht verrutscht
        '<button class="c-aufheben" data-aufheben' + (Z.hervor ? '' : ' disabled') + '>Hervorhebung aufheben</button>' +
        Object.keys(z).sort(function (a, b) { return fl[b] - fl[a] }).map(function (c) {
          var k = FA.KAT[c] || { name: 'unbekannt', color: '#808080' }
          return '<button class="c-kl" data-klasse="' + esc(c) + '" aria-pressed="' + (Z.hervor === c) + '">' + punkt(k.color || '#808080') +
            '<span>' + esc(c + ' ' + k.name) + '</span><span class="c-za">' + z[c] + ' Segm. · ' + (100 * fl[c] / Math.max(1, gesamt)).toFixed(1) + ' %</span></button>'
        }).join('') +
        '<p class="c-quelle">Anteil an der Fläche der Teilkachel samt Rand. Klick hebt eine Kategorie hervor.</p>' +
        '<details class="c-technik"><summary>Technik</summary><p>Kategorienliste: ' + esc(FA.f.kategorien_quelle) + '</p><p>Daten: ' + esc(st.roh.quelle) + '</p></details>'
    }
    kat.addEventListener('click', function (ev) {
      if (ev.target.closest('[data-aufheben]')) { Z.hervor = null; liste(); spaeter(); return }
      var b = ev.target.closest('[data-klasse]'); if (!b) return
      Z.hervor = Z.hervor === b.dataset.klasse ? null : b.dataset.klasse; liste(); spaeter()
    })
    function waehle(id) {
      Z.sel = id || null
      history.replaceState(null, '', '#/' + K + '/kachel/' + tkId + (Z.sel ? '/segment/' + Z.sel : ''))
      zeigeWahl(); zeigeMaus(); spaeter()
    }
    zeigeMaus(); zeigeWahl(); liste()
    if (Z.sel && !auswahl) history.replaceState(null, '', '#/' + K + '/kachel/' + tkId + '/segment/' + Z.sel)
    info.addEventListener('click', function (ev) { if (ev.target.closest('[data-abwaehlen]')) waehle(null) })
    ta.addEventListener('input', vormerkenPruefen)
    AKTIV.abwaehlen = function () { if (Z.sel) waehle(null) }

    function innen(p) { return p[0] >= 0 && p[1] >= 0 && p[0] < x.w && p[1] < x.h }
    function faktor(fk, p) {
      var a = Z.a, w = Math.max(24, Math.min(Math.max(x.w, x.h) * 1.2, a[2] / fk)), h = w * a[3] / a[2]
      fk = a[2] / w
      Z.a = [p[0] - (p[0] - a[0]) / fk, p[1] - (p[1] - a[1]) / fk, w, h]
      spaeter()
    }
    var zieh = null
    cv.addEventListener('wheel', function (ev) { ev.preventDefault(); faktor(ev.deltaY < 0 ? 1.25 : 0.8, punktIm(cv, Z.a, ev)) }, { passive: false })
    cv.addEventListener('dblclick', function (ev) { faktor(2, punktIm(cv, Z.a, ev)) })
    cv.addEventListener('pointerdown', function (ev) { zieh = { x: ev.clientX, y: ev.clientY, a: Z.a.slice(), bewegt: false }; if (cv.setPointerCapture) cv.setPointerCapture(ev.pointerId) })
    cv.addEventListener('pointermove', function (ev) {
      if (zieh) {
        var dx = ev.clientX - zieh.x, dy = ev.clientY - zieh.y
        if (Math.abs(dx) + Math.abs(dy) > 4) zieh.bewegt = true
        if (zieh.bewegt) {
          var r = cv.getBoundingClientRect(), s = Math.min(r.width / zieh.a[2], r.height / zieh.a[3])
          Z.a = [zieh.a[0] - dx / s, zieh.a[1] - dy / s, zieh.a[2], zieh.a[3]]; spaeter()
        }
        return
      }
      var p = punktIm(cv, Z.a, ev)
      if (!st || !innen(p)) { if (Z.maus) { Z.hover = null; Z.maus = null; zeigeMaus(); spaeter() } return }
      var id = st.ids[Math.floor(p[1]) * x.w + Math.floor(p[0])]
      Z.maus = p
      if (id !== Z.hover) { Z.hover = id; spaeter() }
      zeigeMaus()
    })
    cv.addEventListener('pointerleave', function () { if (!zieh) { Z.hover = null; Z.maus = null; zeigeMaus(); spaeter() } })
    cv.addEventListener('pointerup', function (ev) {
      var z = zieh; zieh = null
      if (!z || z.bewegt || !st) return
      var p = punktIm(cv, Z.a, ev)
      if (!innen(p)) { waehle(null); return }   // Klick neben das Bild hebt die Wahl auf
      var id = st.ids[Math.floor(p[1]) * x.w + Math.floor(p[0])]
      LETZT = { tk: tkId, x: p[0], y: p[1] }
      waehle(Z.sel === id ? null : id)
      if (Z.sel && ta.focus) ta.focus({ preventScroll: true })   // gleich losschreiben, ohne ins Feld zu klicken
    })

    leiste.addEventListener('input', function (ev) {
      if (!ev.target.hasAttribute('data-deck')) return
      S.deck = ev.target.value / 100
      leiste.querySelector('[data-deckwert]').textContent = 'Deckkraft ' + ev.target.value + ' %'
      spaeter()
    })
    leiste.addEventListener('click', function (ev) {
      var b = ev.target.closest('button'); if (!b) return
      if (b.dataset.ebene) {
        S.ebene = +b.dataset.ebene; Z.hervor = null
        leiste.querySelectorAll('[data-ebene]').forEach(function (y) { y.setAttribute('aria-pressed', String(y === b)) })
        liste(); zeigeWahl(); zeigeMaus()
      } else if (b.dataset.schalter) {
        var k = b.dataset.schalter; S[k] = !S[k]; b.setAttribute('aria-pressed', String(S[k]))
        if (k === 'liste') { kat.hidden = !S.liste; liste(); requestAnimationFrame(zeichne); return }
      } else if (b.dataset.zoom) {
        if (b.dataset.zoom === 'fit') Z.a = [0, 0, x.w, x.h]; else faktor(+b.dataset.zoom, [Z.a[0] + Z.a[2] / 2, Z.a[1] + Z.a[3] / 2])
      }
      spaeter()
    })
    info.querySelector('[data-export]').addEventListener('click', function () { status.textContent = exportieren() })
    info.querySelector('[data-komm]').addEventListener('submit', function (ev) {
      ev.preventDefault()
      var s = Z.sel ? st.seg[Z.sel] : null
      if (!Z.sel || !ta.value.trim()) return
      var nr = alleKommentare().length + 1
      neu.push({ nr: nr, fassung: K, teilkachel: tkId, segment: Z.sel, klasse: s ? s.klasse : null, text: ta.value.trim(),
        status: 'offen', zeit: new Date().toISOString() })
      merke(); ta.value = ''
      KOM = kommentiert()
      status.textContent = 'Kommentar ' + nr + ' vorgemerkt – noch nicht exportiert. Nur in diesem Browser gespeichert: bitte „Export (JSON)“.'
      wurzel.querySelector('[data-kommzahl]').textContent = 'Kommentare (' + alleKommentare().length + ')'
      zeigeWahl(); spaeter()
    })
    window.onresize = spaeter
    spaeter()
  }

  function exportieren() {
    var daten = { schema: D.kommentar_schema, ausschnitt: D.name, manifest: D.manifest,
      fassungen: D.fassungen.map(function (f) { return { kennung: f.kennung, name: f.name, quelle: f.quelle } }),
      exportiert: new Date().toISOString(), kommentare: alleKommentare() }
    var name = 'kommentare-' + D.name + '.json'
    var a = el('a'); a.href = URL.createObjectURL(new Blob([JSON.stringify(daten, null, 2)], { type: 'application/json' }))
    a.download = name; document.body.appendChild(a); a.click(); a.remove()
    var n = alleKommentare().length
    return n + (n === 1 ? ' Kommentar' : ' Kommentare') + ' exportiert (Datei ' + name + ', meist im Ordner Downloads).'
  }

  // --- Ganzer Ausschnitt ------------------------------------------------------------------------------
  function uebersicht() {
    var w = el('div', 'c-seite c-ohne-info'); w.appendChild(kopf('uebersicht'))
    var m = el('div', 'c-uebersicht'), f = el('figure', 'c-tafel'), nb = FA.f.naht
    f.innerHTML = '<figcaption><b>Ganzer Ausschnitt ' + esc(D.name) + '</b><span>' + (nb ? schnittText(nb.verstoesse.length) + ' · ' + nb.naehte.length + ' Nähte zwischen Teilkacheln' : 'Nähte nicht geprüft: nicht alle Teilkacheln haben Daten') + '</span><span>' + einigungText(FA.f.einigung, FA.f.einigung_fehler) + '</span><span>Klick ins Bild öffnet die Teilkachel an dieser Stelle.</span></figcaption>'
    var cv = el('canvas', 'c-bild'); cv.setAttribute('aria-label', 'Ausschnitt ' + D.name + ', Fassung ' + FA.f.kennung)
    f.appendChild(cv); m.appendChild(f); w.appendChild(m)
    var l = el('section', 'c-leiste'), nv = nb ? nb.verstoesse : [], je = {}
    nv.forEach(function (v) { var z = je[v.naht] || (je[v.naht] = { n: 0, px: 0 }); z.n++; z.px += v.laenge || 0 })
    l.innerHTML = '<div class="c-gruppe">' + D.teilkacheln.map(function (t) {
      var st = FA.tk[t.id]
      return '<a class="c-karte" href="#/' + esc(FA.f.kennung) + '/kachel/' + t.id + '"><b>' + t.id + '</b><span>' + (st ? st.roh.segmente.length + ' Segmente' : 'keine Daten') + '</span></a>'
    }).join('') + '</div><div class="c-gruppe c-leise">' + (nv.length ? 'Schnittlinien ohne Bildkante, je Naht: ' +
      Object.keys(je).map(function (k) { return esc(k.replace('|', ' / ')) + ' ' + je[k].n }).join(' · ') : '') + '</div>'
    w.appendChild(l)
    app.innerHTML = ''; app.appendChild(w)
    AKTIV.abwaehlen = null
    var a = [0, 0, D.ausschnitt.breite, D.ausschnitt.hoehe]
    function z() {
      passe(cv)
      var ctx = cv.getContext('2d'), L = lage(cv, a), e = EB()
      ctx.fillStyle = '#0e0f11'; ctx.fillRect(0, 0, cv.width, cv.height)
      ctx.drawImage(AUSSCHNITT, L.ox, L.oy, a[2] * L.s, a[3] * L.s)
      var g = FA.gesamt
      if (g) {
        var seg = {}
        D.teilkacheln.forEach(function (t) { var st = FA.tk[t.id]; if (st) st.roh.segmente.forEach(function (s) { seg[s.id] = s }) })
        var img = new ImageData(g.w, g.h), p = img.data
        for (var i = 0; i < g.ids.length; i++) {
          var s = seg[g.ids[i]], x = i % g.w
          if (s && S.flaeche) setze(p, i * 4, rgba(farbe(s.klasse, e)), S.deck)
          if ((x + 1 < g.w && g.ids[i + 1] !== g.ids[i]) || (i + g.w < g.ids.length && g.ids[i + g.w] !== g.ids[i])) setze(p, i * 4, FARBE.umriss)
        }
        var off = el('canvas'); off.width = g.w; off.height = g.h; off.getContext('2d').putImageData(img, 0, 0)
        ctx.imageSmoothingEnabled = L.s < 1; ctx.drawImage(off, L.ox, L.oy, g.w * L.s, g.h * L.s)
      }
      ctx.setLineDash([6, 5]); ctx.strokeStyle = css(F.naht); ctx.lineWidth = 1.5
      D.teilkacheln.forEach(function (t) { var k = t.kern; ctx.strokeRect(L.ox + k.x * L.s, L.oy + k.y * L.s, k.breite * L.s, k.hoehe * L.s) })
      ctx.setLineDash([])
      if (nb) naehte(ctx, L, nb.verstoesse)
      marken(ctx, L)
    }
    // Nummer und Lage in jedem Kern: der Ausschnitt besteht aus den Teilkacheln der Kachel-Wahl
    function marken(ctx, L) {
      var d = window.devicePixelRatio || 1, r = 10 * d, h = 2 * r + 8 * d
      ctx.font = '600 ' + Math.round(13 * d) + 'px Segoe UI, system-ui, sans-serif'; ctx.textBaseline = 'middle'
      REIHE.forEach(function (t) {
        var k = t.kern, x0 = L.ox + k.x * L.s + 10 * d, y0 = L.oy + k.y * L.s + 10 * d, mit = !!FA.tk[t.id]
        var text = t.lage + (mit ? '' : ' · keine Daten'), b = h + ctx.measureText(text).width + 14 * d
        ctx.fillStyle = 'rgba(14,15,17,0.85)'; ctx.beginPath()
        if (ctx.roundRect) ctx.roundRect(x0, y0, b, h, h / 2); else ctx.rect(x0, y0, b, h)
        ctx.fill()
        ctx.beginPath(); ctx.arc(x0 + h / 2, y0 + h / 2, r, 0, 2 * Math.PI)
        ctx.fillStyle = '#0e0f11'; ctx.fill(); ctx.strokeStyle = '#454b53'; ctx.lineWidth = d; ctx.stroke()
        ctx.fillStyle = '#d6d8dc'; ctx.textAlign = 'center'; ctx.fillText(String(t.nummer), x0 + h / 2, y0 + h / 2)
        ctx.fillStyle = mit ? '#d6d8dc' : '#8b9099'; ctx.textAlign = 'left'; ctx.fillText(text, x0 + h + 6 * d, y0 + h / 2)
      })
    }
    cv.addEventListener('click', function (ev) {
      var p = punktIm(cv, a, ev)
      var t = D.teilkacheln.filter(function (t) { var k = t.kern; return p[0] >= k.x && p[0] < k.x + k.breite && p[1] >= k.y && p[1] < k.y + k.hoehe })[0]
      if (!t) return
      LETZT = { tk: t.id, x: p[0] - t.kontext.x, y: p[1] - t.kontext.y }; UEBERNAHME = true
      gehe('/' + FA.f.kennung + '/kachel/' + t.id)
    })
    window.onresize = z
    z()
  }

  // --- Kommentare -------------------------------------------------------------------------------------
  function kommentare() {
    var w = el('div', 'c-seite c-ohne-info'); w.appendChild(kopf('kommentare'))
    var alle = alleKommentare(), l = el('div', 'c-liste')
    l.innerHTML = '<b>Kommentare (' + alle.length + ')</b> <button type="button" data-export>Export (JSON)</button> <span class="c-leise" data-status></span>' +
      '<p class="c-leise">Neue Kommentare stehen nur im Speicher dieses Browsers, bis Sie sie exportieren.</p>' +
      (alle.length ? '' : '<p class="c-leise">Noch keine Kommentare. In einer Teilkachel ein Segment anklicken und links einen Kommentar vormerken.</p>') +
      alle.map(function (k, i) {
        var fk = FS[k.fassung] && FS[k.fassung].f.vorhanden ? k.fassung : ERSTE
        var lokal = i >= D.kommentare.length
        return '<p><a href="#/' + esc(fk) + '/kachel/' + esc(k.teilkachel) + '/segment/' + esc(k.segment) + '">Segment ' + esc(k.segment) + '</a> · Fassung ' + esc(k.fassung || '–') +
          ' · ' + esc(k.teilkachel) + ' · ' + esc(zeit(k.zeit)) +
          (lokal ? ' <button type="button" data-loeschen="' + (i - D.kommentare.length) + '">Löschen</button>' : ' <span class="c-leise">(aus Datei)</span>') +
          '<br>' + esc(k.text) + '</p>'
      }).join('')
    l.querySelector('[data-export]').onclick = function () { l.querySelector('[data-status]').textContent = exportieren() }
    l.addEventListener('click', function (ev) {
      var b = ev.target.closest('[data-loeschen]'); if (!b) return
      neu.splice(+b.dataset.loeschen, 1); merke(); kommentare()
    })
    w.appendChild(l); app.innerHTML = ''; app.appendChild(w)
    AKTIV.abwaehlen = null
    window.onresize = null
  }

  // --- Tasten: Esc hebt die Wahl auf (auch im Kommentarfeld), Umschalt + Kennung schaltet die Fassung
  //     (nie beim Tippen in ein Eingabefeld; ohne Umschalt geht kein Buchstabe verloren) ------------------
  // Pfeiltasten ← → gehen wie „vorige“ / „nächste“ der Kachel-Wahl (nie in Eingabefeldern, nie mit Umschalt usw.)
  document.addEventListener('keydown', function (ev) {
    var t = ev.target && ev.target.tagName
    if (ev.key === 'ArrowLeft' || ev.key === 'ArrowRight') {
      if (t === 'TEXTAREA' || t === 'INPUT' || t === 'SELECT' || (ev.target && ev.target.isContentEditable)) return
      if (ev.shiftKey || ev.ctrlKey || ev.metaKey || ev.altKey || ev.defaultPrevented) return
      var a = document.querySelector('.c-kachelwahl .c-pfeil-' + (ev.key === 'ArrowLeft' ? 'zurueck' : 'vor') + '[href]')
      if (a) { ev.preventDefault(); location.hash = a.getAttribute('href') }
      return
    }
    if (ev.key === 'Escape') {
      if (t === 'TEXTAREA' && ev.target.value && ev.target.value.trim()) return
      if (t === 'TEXTAREA' && ev.target.blur) ev.target.blur()
      if (AKTIV.abwaehlen) AKTIV.abwaehlen()
      return
    }
    if (t === 'TEXTAREA' || t === 'INPUT' || !ev.shiftKey || ev.ctrlKey || ev.metaKey || ev.altKey) return
    var k = String(ev.key || '').toUpperCase()
    if (FS[k] && FS[k].f.vorhanden && AKTIV.wechsle) AKTIV.wechsle(k)
  })

  // --- Wege -------------------------------------------------------------------------------------------
  function gehe(p) { location.hash = '#' + p }
  function weg() {
    var t = (location.hash.replace(/^#/, '') || '/').split('/').filter(Boolean)
    if (t[0] === 'kommentare') return kommentare()
    var fx = FS[t[0]]
    if (!fx || !fx.f.vorhanden) { gehe('/' + ERSTE + '/kachel/' + ersteKachel(FS[ERSTE])); return }
    FA = fx
    if (t[1] === 'kachel' && t[2]) return ansicht(t[2], t[3] === 'segment' ? t[4] : null)
    if (t[1] === 'uebersicht') return uebersicht()
    gehe('/' + FA.f.kennung + '/kachel/' + ersteKachel(FA))
  }
  app.innerHTML = '<p class="c-liste">Lade Bilder …</p>'
  laden().then(function () { miniaturen(); window.addEventListener('hashchange', weg); weg() },
    function () { app.innerHTML = '<p class="c-liste c-fehler">Bilder ließen sich nicht lesen.</p>' })
})()

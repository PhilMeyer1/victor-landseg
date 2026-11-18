/* Anschluss eines Entwurfs an den Vergleichsrahmen des Wunsch-Systems (Vorlage, nicht ändern: kommt aus
   plugins/wunsch/skills/wunsch/assets/entwurf/ und wird bei jedem `entwurf.py anlegen` erneuert).

   Jede Seite eines Platzes (a/ … e/, vorlage/) lädt nacheinander:
     ../gemeinsam/daten.js      window.DATEN, die Platzhalterdaten aller Entwürfe
     ../gemeinsam/anschluss.js  dieses Skript: window.Entwurf
     ../gemeinsam/umgebung.js   Nachbau der Umgebung (Kopf, Seitenleiste, Menü) mit Platzhalterseiten
     entwurf.js                 der Entwurf des Platzes
   und ruft zuletzt Entwurf.start().

   Navigation: jede Seite der Anwendung ist eine Route im Hash (`#/proben/12`). Links führen mit
   `<a href="#/…">` dorthin, Aktionen ohne Seitenwechsel sind `<button>`. Routen meldet man mit
   Entwurf.route('/proben/:id', function (p, pfad) { … }) an; später angemeldete gehen vor (der Entwurf
   überschreibt Platzhalterseiten der Umgebung). Eine Route ohne Anmeldung zeigt „Seite fehlt" und setzt
   `data-fehlt` am <html>: das zählt die Prüfung als Navigation ins Leere.

   Der Rahmen (index.html eine Ebene höher) bekommt jede neue Route per postMessage und schickt die
   Route anderer Entwürfe zurück (Mitlaufen); die Tasten 0–5 und N, E, D, H, M, V, ? reicht der
   Anschluss an den Rahmen weiter, solange kein Eingabefeld den Fokus hat. */
(function () {
  'use strict'
  var routen = []
  var inhalt = null
  var startPfad = '/'
  var aktuell = null
  var vonAussen = null
  var gestartet = false
  var imRahmen = false
  try { imRahmen = window.parent && window.parent !== window } catch (e) { imRahmen = true }
  var platz = (decodeURIComponent(location.pathname).match(/[\\/]([a-e]|vorlage)[\\/][^\\/]*$/) || [])[1] || ''

  function zerlege(pfad) {
    return String(pfad || '').replace(/^#/, '').split('?')[0].split('/').filter(Boolean)
  }
  function alsPfad(teile) { return '/' + teile.join('/') }

  function passt(route, teile) {
    if (route.teile.length !== teile.length) return null
    var p = {}
    for (var i = 0; i < teile.length; i++) {
      var m = route.teile[i]
      if (m.charAt(0) === ':') p[m.slice(1)] = decodeURIComponent(teile[i])
      else if (m !== teile[i]) return null
    }
    return p
  }
  function finde(teile) {
    for (var i = routen.length - 1; i >= 0; i--) {
      var p = passt(routen[i], teile)
      if (p) return { route: routen[i], params: p }
    }
    return null
  }

  function ziel() {
    if (inhalt && document.contains(inhalt)) return inhalt
    inhalt = document.querySelector('[data-inhalt]') || document.querySelector('main') || document.body
    return inhalt
  }

  function fehltSeite(pfad) {
    var z = ziel()
    z.innerHTML = ''
    var box = document.createElement('div')
    box.setAttribute('data-entwurf-fehlt', '')
    box.style.cssText = 'margin:48px auto;max-width:420px;padding:20px 24px;border:1px dashed #c2410c;' +
      'border-radius:8px;color:#9a3412;background:#fff7ed;font:14px/1.5 system-ui,sans-serif'
    box.textContent = 'Seite fehlt in diesem Entwurf: ' + pfad
    z.appendChild(box)
  }

  function markiereAktive(pfad) {
    var links = document.querySelectorAll('a[href^="#/"]')
    var best = null, bestLen = -1
    for (var i = 0; i < links.length; i++) {
      var ziel = alsPfad(zerlege(links[i].getAttribute('href')))
      links[i].removeAttribute('aria-current')
      if ((pfad === ziel || pfad.indexOf(ziel === '/' ? '/' : ziel + '/') === 0) && ziel.length > bestLen) {
        bestLen = ziel.length
        best = ziel
      }
    }
    if (best === null) return
    for (var j = 0; j < links.length; j++) {
      if (alsPfad(zerlege(links[j].getAttribute('href'))) === best) links[j].setAttribute('aria-current', 'page')
    }
  }

  function melde(nachricht) {
    if (!imRahmen) return
    nachricht.entwurf = nachricht.entwurf || 'route'
    nachricht.platz = platz
    try { window.parent.postMessage(nachricht, '*') } catch (e) { /* Rahmen nicht erreichbar */ }
  }

  function zeige() {
    var teile = zerlege(location.hash)
    if (!teile.length && startPfad !== '/') {
      history.replaceState(null, '', '#' + startPfad)
      teile = zerlege(startPfad)
    }
    var pfad = alsPfad(teile)
    var treffer = finde(teile)
    var html = document.documentElement
    html.removeAttribute('data-fehlt')
    if (treffer) {
      treffer.route.zeichne(treffer.params, pfad)
    } else {
      html.setAttribute('data-fehlt', pfad)
      fehltSeite(pfad)
    }
    html.setAttribute('data-route', pfad)
    markiereAktive(pfad)
    var echo = vonAussen === pfad
    vonAussen = null
    var alt = aktuell
    aktuell = pfad
    if (alt !== pfad || !gestartet) melde({ entwurf: 'route', pfad: pfad, gefunden: !!treffer, echo: echo })
    try {
      window.dispatchEvent(new CustomEvent('entwurf:route', { detail: { pfad: pfad, params: treffer ? treffer.params : {} } }))
    } catch (e) { /* alte Browser */ }
  }

  // Route aus dem Rahmen: die längste bekannte Route, die vorn mit dem Pfad übereinstimmt; ohne Treffer bleibt
  // der Entwurf, wo er ist (er hat diese Seite anders gelöst).
  function geheVonAussen(pfad) {
    var teile = zerlege(pfad)
    while (teile.length && !finde(teile)) teile.pop()
    if (!teile.length && !finde([])) return
    var neu = alsPfad(teile)
    if (neu === aktuell) return
    vonAussen = neu
    location.hash = '#' + neu
  }

  var TASTEN = /^[0-5nNeEdDhHmMvV?]$/
  document.addEventListener('keydown', function (ev) {
    if (!imRahmen || ev.ctrlKey || ev.altKey || ev.metaKey || ev.defaultPrevented) return
    var t = ev.target
    var tag = t && t.tagName ? t.tagName.toLowerCase() : ''
    if (tag === 'input' || tag === 'textarea' || tag === 'select' || (t && t.isContentEditable)) return
    if (TASTEN.test(ev.key)) melde({ entwurf: 'taste', taste: ev.key })
  }, true)

  window.addEventListener('message', function (ev) {
    var d = ev.data
    if (!d || typeof d !== 'object' || ev.source !== window.parent) return
    if (d.entwurf === 'gehe' && typeof d.pfad === 'string' && gestartet) geheVonAussen(d.pfad)
  })

  window.Entwurf = {
    platz: platz,
    imRahmen: imRahmen,
    get daten() { return window.DATEN },
    // Route anmelden: muster wie '/proben' oder '/proben/:id'; zeichne(params, pfad) füllt Entwurf.inhalt.
    route: function (muster, zeichne) {
      if (typeof zeichne !== 'function') throw new Error('Entwurf.route(' + muster + '): zeichne fehlt')
      routen.push({ muster: muster, teile: zerlege(muster), zeichne: zeichne })
      return this
    },
    routen: function () { return routen.map(function (r) { return r.muster }) },
    // Behälter, in den Routen zeichnen: setzt die Umgebung (Element mit data-inhalt), sonst <main>.
    get inhalt() { return ziel() },
    set inhalt(el) { inhalt = el },
    gehe: function (pfad) { location.hash = '#' + alsPfad(zerlege(pfad)) },
    get pfad() { return aktuell },
    // Einfache Platzhalterseite für Menüpunkte, die nicht Gegenstand des Entwurfs sind.
    platzhalter: function (titel, el) {
      var z = el || ziel()
      z.innerHTML = ''
      var h = document.createElement('h1')
      h.textContent = titel
      h.style.cssText = 'margin:0 0 6px;font-size:22px;font-weight:600'
      var hinweis = document.createElement('p')
      hinweis.textContent = 'Platzhalter, nicht Teil dieses Entwurfs'
      hinweis.style.cssText = 'margin:0 0 20px;color:#6b7280;font-size:13px'
      z.appendChild(h)
      z.appendChild(hinweis)
      var breiten = [92, 76, 84, 58]
      for (var i = 0; i < breiten.length; i++) {
        var b = document.createElement('div')
        b.style.cssText = 'height:14px;margin:0 0 12px;border-radius:4px;background:rgba(127,127,127,.16);width:' + breiten[i] + '%'
        z.appendChild(b)
      }
      return z
    },
    // Start: einmal am Ende der Seite. start: Route, auf der die Seite ohne Hash beginnt (sonst rahmen.json).
    start: function (opts) {
      opts = opts || {}
      if (opts.inhalt) inhalt = typeof opts.inhalt === 'string' ? document.querySelector(opts.inhalt) : opts.inhalt
      startPfad = alsPfad(zerlege(opts.start || (window.RAHMEN && window.RAHMEN.start) || '/'))
      if (gestartet) return zeige()
      window.addEventListener('hashchange', zeige)
      zeige()
      gestartet = true
      melde({ entwurf: 'bereit', pfad: aktuell, routen: this.routen() })
    },
  }
})()

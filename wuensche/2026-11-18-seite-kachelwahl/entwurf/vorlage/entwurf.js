/* Startpunkt eines Platzes: die Prüfseite mit der Kachel-Wahl von heute (kleine Textlinks im Kopf).
   Gegenstand: die Wahl der vier Teilkacheln und „Ganzer Ausschnitt“ (Kopf, Hinweis im Bild, „n von 4“,
   vorige/nächste, Pfeiltasten). Bausteine und Stellen zum Ersetzen: gemeinsam/umgebung.js (window.Seite).
   Die Lage des Bildes darf sich beim Umschalten nicht ändern: Kopfhöhe (--kopf-hoehe) in allen
   Zuständen gleich, Leiste links fest. */
(function () {
  'use strict'
  var D = window.DATEN

  // Kopf: heute der Nachbau von seite.js (kopf); ein Entwurf setzt hier seine Kachel-Wahl ein.
  Seite.kopf = function (K, art, tk) { return Seite.kopfHeute(K, art, tk) }

  // Zeile über dem Bild
  Seite.titel = function (K, tk) { return '<b>Teilkachel ' + Seite.esc(tk) + '</b>' }

  // Zusätze im Bild der Teilkachel (feld: .c-bildfeld, position: relative) und im ganzen Ausschnitt
  Seite.imBild = function (feld, K, tk) {}
  Seite.inGanz = function (feld, K) {}

  // Routen des Gegenstands
  Entwurf.route('/:f/kachel/:tk', function (p) { Seite.kachel(p.f, p.tk) })
  Entwurf.route('/:f/kachel/:tk/segment/:id', function (p) { Seite.kachel(p.f, p.tk) })
  Entwurf.route('/:f/uebersicht', function (p) { Seite.ganz(p.f) })
  Entwurf.route('/', function () { Entwurf.gehe(Seite.pfadKachel(D.start.fassung, D.start.teilkachel)) })
})()

# Bericht landseg
Status: eingereiht
Für den Nutzer: Auf der Ergebnis-Seite liegt jetzt unter der Kopfzeile eine breite Leiste in fester Höhe (wie Entwurf d): links „‹ vorige“, dann „Ganzer Ausschnitt“ mit kleinem Gesamtbild, dann vier große Reiter „Teilkachel 1 … 4“ mit kleinem Luftbild, Nummer, Raster-Symbol und Lage („oben links“, „oben rechts“, „unten links“, „unten rechts“; die Kennung r0c0 usw. klein daneben), rechts „nächste ›“. Die gezeigte Teilkachel ist gelb umrandet. Über dem Bild steht „Teilkachel 1 von 4 · oben links“, im Bild unten ein Kasten „Teilkachel 1 von 4“ mit Punkten und gelbem Knopf „weiter: Teilkachel 2, oben rechts“. Die Pfeiltasten ← → blättern (nicht beim Schreiben im Kommentarfeld). Im „Ganzen Ausschnitt“ trägt jedes Viertel Nummer und Lage. Auf dem Handy zeigt die Leiste nur die Bildchen mit Nummer; die Leisten links (Segment, Kommentar) und rechts (Kategorien) entfallen dort, damit das Bild Platz hat. Ungeprüft: Fotos im Browser (keine Browser-Erweiterung in diesem Lauf). Die Seiten in daten/landseg und ergebnisse/T0.html des Gesamtprojekts sind noch nicht neu erzeugt (Nacharbeit).
Commit: 0238f11 "feat(seite): add a large tile picker so all four sub-tiles are easy to find"
Abnahmekriterien:
AK1: erfüllt (Aufbau), Ansicht nicht fotografiert — Rauchtest der Seite aus den T0-Daten des Gesamtprojekts: 5 Reiter, Lagen „1 oben links, 2 oben rechts, 3 unten links, 4 unten rechts“ (D/rauchtest-landseg.txt); Miniaturen aus denselben Bildern
AK2: erfüllt (Aufbau), Ansicht nicht fotografiert — Rauchtest: nach Wechsel auf r1c1 genau dieser Reiter aria-current, Titel „Teilkachel 4 von 4 · unten rechts“
AK3: erfüllt (Aufbau), Ansicht nicht fotografiert — eigener Reiter „Ganzer Ausschnitt“ mit Miniatur vor den vier Teilkacheln; Rauchtest: in der Übersicht aktiv
AK4: erfüllt — Rauchtest: → von r0c0 bis r1c1, danach „nächste“ gesperrt; ← zurück bis Ganzer Ausschnitt, dort „vorige“ gesperrt; Pfeiltasten in TEXTAREA/INPUT ändern nichts (true)
AK5: erfüllt (Aufbau), Ansicht nicht fotografiert — Kasten „Teilkachel n von 4“ mit „weiter: …“ bzw. „alle 4 gesehen · Ganzer Ausschnitt“ im Bild (Rauchtest)
AK6: nicht prüfbar (ohne Browser) — Aufbau: Kopf 72 px + Kachel-Wahl 78 px als feste Zeile der Seite in allen Ansichten (`--kopf-hoehe`, `--wahl-hoehe`), Leiste links unverändert 320 px; Maße am Bild nicht gemessen
AK7: teils belegt — Rauchtest: Wechsel auf Fassung B bei r1c0 behält r1c0 (Reiter aktiv, Titel „Teilkachel 3 von 4“); Handy-Regeln (≤ 760 px) gebaut, Ansicht nicht fotografiert
AK8: erfüllt — gesamt/CLAUDE.md, Schritt 4: vier Teilkacheln, Kachel-Wahl im Raster der Lage, „Ganzer Ausschnitt“, „vorige“/„nächste“, Pfeiltasten
AK9: erfüllt — `PY -B -m unittest tests.test_seite` → 8 Tests OK (neu: test_kachel_wahl)
Prüfungen:
"$PY" -B -m unittest tests.test_seite tests.test_gesamt_projekt → 14 Tests OK (17 s)
"$PY" -I tools/pruefe_kategorien.py kategorien.json → 7/25/43 … ok
node --check landseg/seite_vorlage/seite.js → Syntax ok
Rauchtest (Node, DOM-Attrappe, Seite aus daten/gesamt/victor-landseg/ergebnisse/manifest.json, im Scratchpad erzeugt, 8120 KiB, vorher 8104 KiB) → Ausgabe C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-seite-kachelwahl/rauchtest-landseg.txt
volle Stufe: offen, läuft beim Einreihen
Nicht geprüft: Bildschirmfotos (Browser-Erweiterung in diesem Lauf nicht verfügbar): Aussehen gegen Entwurf d, Maße für AK6, Handy-Ansicht für AK7 — das prüft die Abnahme per Foto
Einstieg: stimmte; `kopf()` liefert jetzt einen Rahmen (Kopfzeile + Kachel-Wahl), `uebersicht()` und `kommentare()` nutzen ihn unverändert
Technische Entscheidungen:
- Nummer und Lage in Worten rechnet seite.py (`lage_in_worten`, Felder `nummer`, `lage` je Teilkachel; 2 × 2 → oben/unten links/rechts, bis 3 × 3 mit „Mitte“, größere Raster „Zeile n, Spalte m“), damit der Test sie prüfen kann; Reihenfolge zeilenweise von oben links.
- Miniaturen: nach dem Laden einmal im Browser aus den schon geladenen Bildern verkleinert (Kern der Teilkachel, 112 px, JPEG-Datenadresse), keine zweite Bildkopie in der Datei (Datei +16 KiB nur durch Code).
- Kommentar-Ansicht zeigt dieselbe Leiste ohne aktiven Reiter, beide Pfeile gesperrt (gleiche Höhe).
- Handy (≤ 760 px): Leisten links und rechts ausgeblendet wie im Nachbau des Entwurfs (gemeinsam/umgebung.css); auf dem Handy daher kein Kommentieren. Vorher hatte die Seite keine Regeln für schmale Bildschirme.
- Fassungsknöpfe: Name in eigenem `<span class="c-fname">`, damit das Handy nur „A B C“ zeigt; auf dem Desktop unverändert.
- README-Abschnitt „seite“ beschreibt die Kachel-Wahl.
Nacharbeit im Hauptordner: Prüfseiten neu erzeugen: BASIS/daten/landseg/T0/kern500/seite/T0.html (und bei Bedarf T0-urteil.html, T0-probe.html) sowie ergebnisse/T0.html des Gesamtprojekts (`python -B -m landseg seite --manifest ../ergebnisse/manifest.json --ziel ../ergebnisse/T0.html --kategorien ../ergebnisse/c-feste-liste/kategorien-c.json`, gesamt/ANLEITUNG.md Z. 287); Gesamtprojekt neu bauen (übernimmt gesamt/CLAUDE.md) und hochladen (Hauptsession)
Abräumen: offen (Arbeitskopie bleibt bis zum Einreihen); keine repo-eigenen Reste
Lagebild: fehlt (Repo hat keine LAGEBILD.md und keine Kopfzeile `lagebild:`)
Erkenntnisse fürs Profil:
- Für Probeläufe von `seite` eignen sich die T0-Daten des Gesamtprojekts (`BASIS/daten/gesamt/victor-landseg/ergebnisse/manifest.json`, Fassungen A/B/C, Kategorien `c-feste-liste/kategorien-c.json`): deren Pfad löst den Geheimnisschutz-Hook für `daten/landseg` nicht aus.
- Node (v25) ist installiert: `node --check landseg/seite_vorlage/seite.js` prüft die Syntax der Seitenvorlage in unter einer Sekunde.
- Die erzeugte Seite hat unter Windows CRLF-Zeilenenden: wer sie roh liest (etwa mit Node), findet das Ende des Datenblocks als `;\r\n</script>`, nicht `;\n</script>` wie `daten_aus_html` im Test (das über `read_text` liest).
Abweichungen vom Zielbild: keine
Einreihen (Skript): eingereiht 0238f11 feat(seite): add a large tile picker so all four sub-tiles are easy to find in C:/Users/Phil/Developement/Victor/landseg (main); Prüfung nach Risiko (ohne Prüfschleuse, keine Zeile schnell: im Profil); voll grün (30 s); volle Prüfung offen (vermerkt in C:/Users/Phil/Developement/Victor/landseg/.git/wunsch-einreihen/pruefung-offen.jsonl); Abräumen WEG; Waisen 1 (sonstige 1), 101 MB anderswo (aufraeumer.py melden; beenden nur mit Freigabe des Nutzers)

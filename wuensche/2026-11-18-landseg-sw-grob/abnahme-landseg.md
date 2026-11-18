abgenommen
Wunschtext und Verhalten (Nachbesserung, Commit 95cb45b, genau ein Commit mit Wish-Zeile) bestätigt; der einzige Kandidat (AK6, `naht`) ist kein Mangel der Umsetzung, bleibt aber als offene Teilzeile von AK6 sichtbar (siehe unten).

Verworfen:
- AK6 „`naht` ok“ (Log `wuensche/2026-11-18-landseg-sw-grob/vergroebern-h0.txt`: Zusammentragen FEHLER 163/141/105 Nahtverstöße in A/B/C): verworfen als Mangel, weil die Verstöße schon vor dem Wunsch bestanden (187/152/119 in „H0-vorher“, ungefähr gleiche Ursache: Segmente beidseits einer Kerngrenze mit verschiedener Id ohne Bildkante, `landseg/naht.py` `pruefe_naehte`), der Wunsch sie nicht erzeugt, sondern verringert hat, und ein Beheben neue Naht-Agents bräuchte, was F2 („automatisch zusammenlegen, ohne neue Agents, Klassen und Urteile bleiben“) ausschließt. Erfüllt sind die übrigen Teile von AK6: Segmente A 566 / B 468 / C 297 (Richtwert 600), `pruefen` je Teilkachel ok, lückenlos, 0 zerteilte Segmente, `einigung messen` offen 0 in A/B/C.

Offen für den Nutzer (kein Halt): Die Teilzeile „`naht` ok“ von AK6 ist nicht erreicht, `zusammentragen`/`naht` bleiben auf H0 rot (Ursache vor dem Wunsch). Das gehört in die Naht-Bearbeitung der H0-Daten, nicht in diese Nachbesserung.

Nicht geprüft: AK7 (Prüfseite mit echten H0-Daten) und die echten Daten unter `daten/landseg/H0` (Nacharbeit im Hauptordner, kein Mangel); volle Suite und `vergroebern` selbst nicht neu gefahren (Bestätiger startet keine Tests); gerendertes Bild nicht angesehen. Ungeprüft im Sinn von `UNGEPRUEFT`: keine.

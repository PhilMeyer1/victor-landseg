# Erkenntnisse fürs Profil: unterlagen (aus landseg-methode, 2026-11-17)

Erkenntnisse fürs Profil:

- Luftbilder im Datenraum `BASIS/daten/luftbilder/` (nur lesen): `orthofoto-aktuell/` zwei Kacheln
  5236-55 und 5236-56, je 6250 × 5000 px, RGB 8 Bit, **kein Infrarot**, unkomprimiert, ein Strip je
  Zeile, 0,2 m, EPSG:31255 (MGI GK Central, false_northing −5 000 000), nahtlos nebeneinander
  (55: E 67 500–68 750, 56: E 68 750–70 000, N 353 000–354 000); Lage Linz-Urfahr,
  Pöstlingberg-Südhang, Sommeraufnahme, Jahr unbekannt. Beleg:
  `wuensche/2026-11-17-landseg-methode/einheiten/e01.md` B1–B5.
- `historisch/1957004_004A_1557.tif`: 12 513 × 13 237 px, Palettenbild mit reiner Graurampe, keine
  DPI-Angabe; `historisch/1968105_0014_0228.tif`: 16 283 × 15 750 px, Graustufen, 1694 dpi (15 µm),
  BEV 1968. Beide ohne Lagebezug, Rahmen/Marken/Datenstreifen im Bild (bis 10–14 % der Bildpunkte),
  Bodenauflösung geschätzt 0,43–0,47 m. Sie zeigen **nicht** das Gebiet des Orthofotos
  (wahrscheinlich Seewinkel/Neusiedler See, nur Augenschein).
- Lesen ohne Speicherlast: `tifffile.memmap(...)` bzw. `TiffFile(...).pages[0]` für Tags; Python mit
  Bildbibliotheken: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I`
  (PIL, cv2, skimage, tifffile, torch, transformers; **kein** rasterio/GDAL/pyproj). Vorschauen nie im
  Datenraum ablegen.
- Testfenster für Segmentier-Versuche: T0 = Kachel 5236-56, x 2000, y 2400, 1000 × 1000 px;
  H0 = Scan 1968, x 1500, y 2000, 1000 × 1000 px.
- Bezugsquellen für weitere Luftbilder (Stand 2026-11-17, Beleg `einheiten/n02.md`): DORIS OÖ
  aktuelles Orthofoto 0,2 m je Gemeinde frei (Lizenz offen, nur „unentgeltlich" + Quellenangabe
  „Datenquelle: Land Oö., doris.at"); DORIS-Altorthofotos ab 1953 nur Ansicht; BEV Orthophoto
  historisch 0,5 m 1 EUR/km², Luftbildscan 25 EUR (ohne Georeferenz); Burgenland Orthofoto 2019/2025
  0,2 m, EPSG:31259, CC BY 4.0 AT, frei. Das Burgenland nutzt EPSG:31259 (GK M34), nicht 31255 wie
  die Linzer Kacheln.
- Falle beim Zitieren von Bericht 48/46: Die DKM-Mindestflächen stehen in § 4 BANU-V (Gebäude ab
  20 m², Streifen ab 4 m, Wald 10 m/1 000 m², übrige 200 m²), nicht „200 m² außer Bauflächen".

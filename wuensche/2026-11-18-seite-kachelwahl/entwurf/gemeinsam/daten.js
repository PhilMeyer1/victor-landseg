/* Platzhalterdaten aller Entwürfe: Ausschnitt T0 mit vier Teilkacheln und drei Fassungen.
   Zahlen der Segmente und Kategorien nach dem Ergebnis von T0, Nahtstellen, Lücken und Kommentare
   ausgedacht; Fassung A hat für r1c1 absichtlich keine Daten (Zustand „ohne Daten“). */
window.DATEN = {
 "ausschnitt": {
  "name": "T0",
  "breite": 1000,
  "hoehe": 1000,
  "bild": "../gemeinsam/bilder/ausschnitt.png",
  "masstab": "0,2 m je Bildpunkt",
  "flaeche": "200 × 200 m"
 },
 "teilkacheln": [
  {
   "id": "r0c0",
   "nr": 1,
   "zeile": 0,
   "spalte": 0,
   "lage": "oben links",
   "bild": "../gemeinsam/bilder/luftbild-r0c0.png",
   "kern": {
    "x": 0,
    "y": 0,
    "breite": 500,
    "hoehe": 500
   },
   "kontext": {
    "breite": 628,
    "hoehe": 628
   },
   "kern_im_bild": {
    "x": 64,
    "y": 64,
    "breite": 500,
    "hoehe": 500
   }
  },
  {
   "id": "r0c1",
   "nr": 2,
   "zeile": 0,
   "spalte": 1,
   "lage": "oben rechts",
   "bild": "../gemeinsam/bilder/luftbild-r0c1.png",
   "kern": {
    "x": 500,
    "y": 0,
    "breite": 500,
    "hoehe": 500
   },
   "kontext": {
    "breite": 628,
    "hoehe": 628
   },
   "kern_im_bild": {
    "x": 64,
    "y": 64,
    "breite": 500,
    "hoehe": 500
   }
  },
  {
   "id": "r1c0",
   "nr": 3,
   "zeile": 1,
   "spalte": 0,
   "lage": "unten links",
   "bild": "../gemeinsam/bilder/luftbild-r1c0.png",
   "kern": {
    "x": 0,
    "y": 500,
    "breite": 500,
    "hoehe": 500
   },
   "kontext": {
    "breite": 628,
    "hoehe": 628
   },
   "kern_im_bild": {
    "x": 64,
    "y": 64,
    "breite": 500,
    "hoehe": 500
   }
  },
  {
   "id": "r1c1",
   "nr": 4,
   "zeile": 1,
   "spalte": 1,
   "lage": "unten rechts",
   "bild": "../gemeinsam/bilder/luftbild-r1c1.png",
   "kern": {
    "x": 500,
    "y": 500,
    "breite": 500,
    "hoehe": 500
   },
   "kontext": {
    "breite": 628,
    "hoehe": 628
   },
   "kern_im_bild": {
    "x": 64,
    "y": 64,
    "breite": 500,
    "hoehe": 500
   }
  }
 ],
 "fassungen": [
  {
   "kennung": "A",
   "name": "Alles frei",
   "beschreibung": "Eigene Kategorien, eigene Grenzen und eigene Arbeitsweise der KI je Teilkachel, ohne feste Regeln; Liste danach zusammengelegt.",
   "vorhanden": true,
   "bild": "../gemeinsam/bilder/fassung-a.png",
   "ebenen": [
    {
     "ebene": 1,
     "name": "grob",
     "klassen": 7
    },
    {
     "ebene": 2,
     "name": "mittel",
     "klassen": 18
    },
    {
     "ebene": 3,
     "name": "fein",
     "klassen": 32
    }
   ],
   "naehte": 4,
   "teilkacheln": {
    "r0c0": {
     "segmente": 128,
     "unsicher": 89,
     "naht": 52,
     "luecken": 0,
     "kategorien": [
      {
       "code": "4.3",
       "name": "Verbuschte Wiese / Lichtung",
       "farbe": "#165a16",
       "segmente": 1,
       "anteil": 19.0
      },
      {
       "code": "4.1.1",
       "name": "Wiese ungemäht / langgrasig",
       "farbe": "#88f290",
       "segmente": 3,
       "anteil": 17.7
      },
      {
       "code": "6.2",
       "name": "Baumgruppe / Feldgehölz",
       "farbe": "#224f3c",
       "segmente": 7,
       "anteil": 11.6
      },
      {
       "code": "1.1.1",
       "name": "Wohnhaus (Hauptgebäude)",
       "farbe": "#fba856",
       "segmente": 7,
       "anteil": 7.6
      },
      {
       "code": "6.3",
       "name": "Einzelbaum",
       "farbe": "#b6eddf",
       "segmente": 22,
       "anteil": 7.6
      },
      {
       "code": "4.1.2",
       "name": "Wiese niedrig",
       "farbe": "#a2ea3e",
       "segmente": 2,
       "anteil": 7.4
      },
      {
       "code": "6.5",
       "name": "Strauch / Gebüsch",
       "farbe": "#8bc577",
       "segmente": 32,
       "anteil": 5.6
      },
      {
       "code": "5.1",
       "name": "Feld gemäht / abgeerntet",
       "farbe": "#7eaa18",
       "segmente": 1,
       "anteil": 4.5
      },
      {
       "code": "3.1",
       "name": "Gartenrasen",
       "farbe": "#bd8bee",
       "segmente": 5,
       "anteil": 4.4
      },
      {
       "code": "2.1.2",
       "name": "Hof / Zufahrt / Terrasse / Vorplatz",
       "farbe": "#e75d55",
       "segmente": 5,
       "anteil": 3.2
      },
      {
       "code": "3.2",
       "name": "Gemischte Gartenfläche",
       "farbe": "#421174",
       "segmente": 8,
       "anteil": 2.7
      },
      {
       "code": "2.1.1",
       "name": "Straße / Fahrweg",
       "farbe": "#eeeb8b",
       "segmente": 2,
       "anteil": 2.7
      },
      {
       "code": "6.3.1",
       "name": "Laubbaum",
       "farbe": "#69bfa9",
       "segmente": 1,
       "anteil": 1.1
      },
      {
       "code": "6.4",
       "name": "Hecke / Gehölzstreifen",
       "farbe": "#88f2b4",
       "segmente": 8,
       "anteil": 0.9
      },
      {
       "code": "2.1.3",
       "name": "Gartenweg / Stufen / Platten",
       "farbe": "#ac5356",
       "segmente": 5,
       "anteil": 0.9
      },
      {
       "code": "1.2.1",
       "name": "Schwimmbecken",
       "farbe": "#962c61",
       "segmente": 2,
       "anteil": 0.9
      },
      {
       "code": "4.2",
       "name": "Saum / Feldrain / Böschung",
       "farbe": "#a2d7a7",
       "segmente": 4,
       "anteil": 0.8
      },
      {
       "code": "0.1",
       "name": "Schlagschatten",
       "farbe": "#d1d1d1",
       "segmente": 5,
       "anteil": 0.6
      },
      {
       "code": "1.2.4",
       "name": "Holzhaufen / Schnittgut",
       "farbe": "#571929",
       "segmente": 1,
       "anteil": 0.5
      },
      {
       "code": "1.2.2",
       "name": "Mauer / Stützmauer / Einfassung",
       "farbe": "#bd4205",
       "segmente": 3,
       "anteil": 0.2
      },
      {
       "code": "1.1.2",
       "name": "Nebengebäude / Anbau / Schuppen",
       "farbe": "#810318",
       "segmente": 2,
       "anteil": 0.1
      },
      {
       "code": "1.2.3",
       "name": "Kleinobjekt",
       "farbe": "#ddb288",
       "segmente": 2,
       "anteil": 0.1
      }
     ]
    },
    "r0c1": {
     "segmente": 272,
     "unsicher": 205,
     "naht": 88,
     "luecken": 312,
     "kategorien": [
      {
       "code": "5.1",
       "name": "Feld gemäht / abgeerntet",
       "farbe": "#7eaa18",
       "segmente": 1,
       "anteil": 19.4
      },
      {
       "code": "6.2",
       "name": "Baumgruppe / Feldgehölz",
       "farbe": "#224f3c",
       "segmente": 53,
       "anteil": 14.5
      },
      {
       "code": "6.3.1",
       "name": "Laubbaum",
       "farbe": "#69bfa9",
       "segmente": 31,
       "anteil": 13.6
      },
      {
       "code": "1.1.1",
       "name": "Wohnhaus (Hauptgebäude)",
       "farbe": "#fba856",
       "segmente": 16,
       "anteil": 10.6
      },
      {
       "code": "3.1",
       "name": "Gartenrasen",
       "farbe": "#bd8bee",
       "segmente": 37,
       "anteil": 10.2
      },
      {
       "code": "4.1.1",
       "name": "Wiese ungemäht / langgrasig",
       "farbe": "#88f290",
       "segmente": 6,
       "anteil": 7.9
      },
      {
       "code": "3.2",
       "name": "Gemischte Gartenfläche",
       "farbe": "#421174",
       "segmente": 20,
       "anteil": 7.6
      },
      {
       "code": "2.1.1",
       "name": "Straße / Fahrweg",
       "farbe": "#eeeb8b",
       "segmente": 8,
       "anteil": 4.4
      },
      {
       "code": "0.1.2",
       "name": "Schlagschatten von Gehölz",
       "farbe": "#a8a8a8",
       "segmente": 19,
       "anteil": 3.4
      },
      {
       "code": "2.1.3",
       "name": "Gartenweg / Stufen / Platten",
       "farbe": "#ac5356",
       "segmente": 16,
       "anteil": 1.7
      },
      {
       "code": "6.3.2",
       "name": "Laubbaum rotlaubig",
       "farbe": "#40c115",
       "segmente": 1,
       "anteil": 1.0
      },
      {
       "code": "0.1.1",
       "name": "Schlagschatten von Gebäude",
       "farbe": "#808080",
       "segmente": 10,
       "anteil": 1.0
      },
      {
       "code": "4.2",
       "name": "Saum / Feldrain / Böschung",
       "farbe": "#a2d7a7",
       "segmente": 16,
       "anteil": 1.0
      },
      {
       "code": "6.5",
       "name": "Strauch / Gebüsch",
       "farbe": "#8bc577",
       "segmente": 12,
       "anteil": 1.0
      },
      {
       "code": "1.1.2",
       "name": "Nebengebäude / Anbau / Schuppen",
       "farbe": "#810318",
       "segmente": 5,
       "anteil": 0.7
      },
      {
       "code": "2.1.2",
       "name": "Hof / Zufahrt / Terrasse / Vorplatz",
       "farbe": "#e75d55",
       "segmente": 5,
       "anteil": 0.6
      },
      {
       "code": "1.2.1",
       "name": "Schwimmbecken",
       "farbe": "#962c61",
       "segmente": 2,
       "anteil": 0.4
      },
      {
       "code": "6.3.3",
       "name": "Nadelbaum / Konifere",
       "farbe": "#15c16b",
       "segmente": 2,
       "anteil": 0.4
      },
      {
       "code": "5.2",
       "name": "Offener Boden / vegetationsarm",
       "farbe": "#a96d04",
       "segmente": 3,
       "anteil": 0.3
      },
      {
       "code": "1.2.3",
       "name": "Kleinobjekt",
       "farbe": "#ddb288",
       "segmente": 9,
       "anteil": 0.3
      }
     ]
    },
    "r1c0": {
     "segmente": 64,
     "unsicher": 54,
     "naht": 31,
     "luecken": 0,
     "kategorien": [
      {
       "code": "6.1.1",
       "name": "Kronendach besonnt",
       "farbe": "#46a45e",
       "segmente": 1,
       "anteil": 56.9
      },
      {
       "code": "4.1",
       "name": "Wiese / Grünland",
       "farbe": "#0f8a0f",
       "segmente": 2,
       "anteil": 20.1
      },
      {
       "code": "4.2",
       "name": "Saum / Feldrain / Böschung",
       "farbe": "#a2d7a7",
       "segmente": 2,
       "anteil": 5.8
      },
      {
       "code": "6.1.2",
       "name": "Kronendach beschattet",
       "farbe": "#17d356",
       "segmente": 2,
       "anteil": 5.0
      },
      {
       "code": "4.3",
       "name": "Verbuschte Wiese / Lichtung",
       "farbe": "#165a16",
       "segmente": 5,
       "anteil": 3.9
      },
      {
       "code": "6.3",
       "name": "Einzelbaum",
       "farbe": "#b6eddf",
       "segmente": 8,
       "anteil": 2.0
      },
      {
       "code": "5.2",
       "name": "Offener Boden / vegetationsarm",
       "farbe": "#a96d04",
       "segmente": 12,
       "anteil": 1.8
      },
      {
       "code": "6.2",
       "name": "Baumgruppe / Feldgehölz",
       "farbe": "#224f3c",
       "segmente": 4,
       "anteil": 1.6
      },
      {
       "code": "1",
       "name": "Gebäude und bauliche Anlagen",
       "farbe": "#f90606",
       "segmente": 2,
       "anteil": 1.4
      },
      {
       "code": "6.5",
       "name": "Strauch / Gebüsch",
       "farbe": "#8bc577",
       "segmente": 16,
       "anteil": 0.7
      },
      {
       "code": "6.1",
       "name": "Wald / geschlossener Bestand",
       "farbe": "#17d3a4",
       "segmente": 1,
       "anteil": 0.3
      },
      {
       "code": "3.2",
       "name": "Gemischte Gartenfläche",
       "farbe": "#421174",
       "segmente": 5,
       "anteil": 0.2
      },
      {
       "code": "2.2.2",
       "name": "Trampelpfad / Erdweg",
       "farbe": "#cdaa1d",
       "segmente": 3,
       "anteil": 0.1
      },
      {
       "code": "5.1",
       "name": "Feld gemäht / abgeerntet",
       "farbe": "#7eaa18",
       "segmente": 1,
       "anteil": 0.1
      }
     ]
    },
    "r1c1": null
   }
  },
  {
   "kennung": "B",
   "name": "Kategorien frei",
   "beschreibung": "Die KI benennt und stuft die Flächen selbst, sonst gleiche Arbeitsweise wie C (Grenzen der Vorstufe, Urteil Segment für Segment).",
   "vorhanden": true,
   "bild": "../gemeinsam/bilder/fassung-b.png",
   "ebenen": [
    {
     "ebene": 1,
     "name": "grob",
     "klassen": 7
    },
    {
     "ebene": 2,
     "name": "mittel",
     "klassen": 21
    },
    {
     "ebene": 3,
     "name": "fein",
     "klassen": 31
    }
   ],
   "naehte": 4,
   "teilkacheln": {
    "r0c0": {
     "segmente": 206,
     "unsicher": 177,
     "naht": 61,
     "luecken": 0,
     "kategorien": [
      {
       "code": "2.1.2",
       "name": "Wiese ungemäht",
       "farbe": "#a68905",
       "segmente": 19,
       "anteil": 36.6
      },
      {
       "code": "1.1.2",
       "name": "Baumgruppe",
       "farbe": "#0dd9b7",
       "segmente": 29,
       "anteil": 12.5
      },
      {
       "code": "2.1",
       "name": "Wiese",
       "farbe": "#6b3b05",
       "segmente": 8,
       "anteil": 10.0
      },
      {
       "code": "1.1.1",
       "name": "Einzelbaum",
       "farbe": "#d0d33d",
       "segmente": 18,
       "anteil": 6.7
      },
      {
       "code": "4.1.1",
       "name": "Wohnhaus",
       "farbe": "#feb7dc",
       "segmente": 7,
       "anteil": 6.5
      },
      {
       "code": "2.1.1",
       "name": "Wiese gemäht",
       "farbe": "#fdc082",
       "segmente": 4,
       "anteil": 5.1
      },
      {
       "code": "0",
       "name": "Nicht bestimmbar",
       "farbe": "#474747",
       "segmente": 39,
       "anteil": 4.8
      },
      {
       "code": "2.2",
       "name": "Rasen",
       "farbe": "#937f49",
       "segmente": 12,
       "anteil": 3.6
      },
      {
       "code": "1.3",
       "name": "Gebüsch",
       "farbe": "#193c10",
       "segmente": 22,
       "anteil": 3.4
      },
      {
       "code": "3.3.2",
       "name": "Parzelle gemischt",
       "farbe": "#b4612e",
       "segmente": 10,
       "anteil": 3.1
      },
      {
       "code": "6.1.1",
       "name": "Asphaltstraße",
       "farbe": "#cc80fd",
       "segmente": 1,
       "anteil": 2.5
      },
      {
       "code": "6.1.2",
       "name": "Betonstraße",
       "farbe": "#9a99e5",
       "segmente": 3,
       "anteil": 2.0
      },
      {
       "code": "6.3",
       "name": "Hof und Zufahrt",
       "farbe": "#103755",
       "segmente": 3,
       "anteil": 0.6
      },
      {
       "code": "1.4",
       "name": "Hecke",
       "farbe": "#74a40b",
       "segmente": 8,
       "anteil": 0.6
      },
      {
       "code": "4.4.1",
       "name": "Holzlager",
       "farbe": "#f686c5",
       "segmente": 3,
       "anteil": 0.5
      },
      {
       "code": "5.1",
       "name": "Schwimmbecken",
       "farbe": "#49c1fe",
       "segmente": 2,
       "anteil": 0.3
      },
      {
       "code": "1.2.2",
       "name": "Wald beschattet",
       "farbe": "#0c9628",
       "segmente": 4,
       "anteil": 0.3
      },
      {
       "code": "6.5",
       "name": "Randstein und Bankett",
       "farbe": "#635375",
       "segmente": 7,
       "anteil": 0.3
      },
      {
       "code": "4.2",
       "name": "Mauer",
       "farbe": "#502b1e",
       "segmente": 1,
       "anteil": 0.1
      },
      {
       "code": "4.3",
       "name": "Kleinobjekt",
       "farbe": "#f8608f",
       "segmente": 1,
       "anteil": 0.1
      },
      {
       "code": "4.1.2",
       "name": "Nebengebäude",
       "farbe": "#ae105c",
       "segmente": 1,
       "anteil": 0.0
      },
      {
       "code": "2.3",
       "name": "Saum und Randstreifen",
       "farbe": "#f7b631",
       "segmente": 1,
       "anteil": 0.0
      },
      {
       "code": "1.2.1",
       "name": "Wald belichtet",
       "farbe": "#a0c175",
       "segmente": 1,
       "anteil": 0.0
      },
      {
       "code": "3.1.1",
       "name": "Feld abgeerntet",
       "farbe": "#6a0f22",
       "segmente": 1,
       "anteil": 0.0
      },
      {
       "code": "6.2.2",
       "name": "Feld- und Erdweg",
       "farbe": "#447bad",
       "segmente": 1,
       "anteil": 0.0
      }
     ]
    },
    "r0c1": {
     "segmente": 234,
     "unsicher": 176,
     "naht": 74,
     "luecken": 0,
     "kategorien": [
      {
       "code": "3.1.1",
       "name": "Feld abgeerntet",
       "farbe": "#6a0f22",
       "segmente": 22,
       "anteil": 20.6
      },
      {
       "code": "1.3",
       "name": "Gebüsch",
       "farbe": "#193c10",
       "segmente": 20,
       "anteil": 16.2
      },
      {
       "code": "1.1.2",
       "name": "Baumgruppe",
       "farbe": "#0dd9b7",
       "segmente": 24,
       "anteil": 12.1
      },
      {
       "code": "4.1.1",
       "name": "Wohnhaus",
       "farbe": "#feb7dc",
       "segmente": 10,
       "anteil": 9.4
      },
      {
       "code": "0",
       "name": "Nicht bestimmbar",
       "farbe": "#474747",
       "segmente": 53,
       "anteil": 9.4
      },
      {
       "code": "2.1",
       "name": "Wiese",
       "farbe": "#6b3b05",
       "segmente": 13,
       "anteil": 8.8
      },
      {
       "code": "1.1.1",
       "name": "Einzelbaum",
       "farbe": "#d0d33d",
       "segmente": 21,
       "anteil": 8.0
      },
      {
       "code": "2.2",
       "name": "Rasen",
       "farbe": "#937f49",
       "segmente": 14,
       "anteil": 5.0
      },
      {
       "code": "6.1.2",
       "name": "Betonstraße",
       "farbe": "#9a99e5",
       "segmente": 7,
       "anteil": 3.3
      },
      {
       "code": "2.3",
       "name": "Saum und Randstreifen",
       "farbe": "#f7b631",
       "segmente": 13,
       "anteil": 1.5
      },
      {
       "code": "1.2.2",
       "name": "Wald beschattet",
       "farbe": "#0c9628",
       "segmente": 1,
       "anteil": 1.1
      },
      {
       "code": "6.1.1",
       "name": "Asphaltstraße",
       "farbe": "#cc80fd",
       "segmente": 2,
       "anteil": 1.0
      },
      {
       "code": "1.4",
       "name": "Hecke",
       "farbe": "#74a40b",
       "segmente": 2,
       "anteil": 0.6
      },
      {
       "code": "6.3",
       "name": "Hof und Zufahrt",
       "farbe": "#103755",
       "segmente": 5,
       "anteil": 0.5
      },
      {
       "code": "2.1.2",
       "name": "Wiese ungemäht",
       "farbe": "#a68905",
       "segmente": 4,
       "anteil": 0.5
      },
      {
       "code": "4.1.2",
       "name": "Nebengebäude",
       "farbe": "#ae105c",
       "segmente": 3,
       "anteil": 0.4
      },
      {
       "code": "6.4",
       "name": "Terrasse",
       "farbe": "#d6d3fd",
       "segmente": 5,
       "anteil": 0.4
      },
      {
       "code": "0.1",
       "name": "Schlagschatten",
       "farbe": "#c1c1c1",
       "segmente": 4,
       "anteil": 0.4
      },
      {
       "code": "5.1",
       "name": "Schwimmbecken",
       "farbe": "#49c1fe",
       "segmente": 3,
       "anteil": 0.4
      },
      {
       "code": "6.2.1",
       "name": "Gartenweg",
       "farbe": "#754496",
       "segmente": 6,
       "anteil": 0.3
      },
      {
       "code": "6.5",
       "name": "Randstein und Bankett",
       "farbe": "#635375",
       "segmente": 1,
       "anteil": 0.0
      },
      {
       "code": "2.1.1",
       "name": "Wiese gemäht",
       "farbe": "#fdc082",
       "segmente": 1,
       "anteil": 0.0
      }
     ]
    },
    "r1c0": {
     "segmente": 86,
     "unsicher": 62,
     "naht": 28,
     "luecken": 0,
     "kategorien": [
      {
       "code": "1.2.1",
       "name": "Wald belichtet",
       "farbe": "#a0c175",
       "segmente": 7,
       "anteil": 50.1
      },
      {
       "code": "1.2.2",
       "name": "Wald beschattet",
       "farbe": "#0c9628",
       "segmente": 15,
       "anteil": 16.7
      },
      {
       "code": "2.1",
       "name": "Wiese",
       "farbe": "#6b3b05",
       "segmente": 18,
       "anteil": 15.5
      },
      {
       "code": "2.3",
       "name": "Saum und Randstreifen",
       "farbe": "#f7b631",
       "segmente": 10,
       "anteil": 11.3
      },
      {
       "code": "1.1.2",
       "name": "Baumgruppe",
       "farbe": "#0dd9b7",
       "segmente": 5,
       "anteil": 2.1
      },
      {
       "code": "3.3.2",
       "name": "Parzelle gemischt",
       "farbe": "#b4612e",
       "segmente": 4,
       "anteil": 1.2
      },
      {
       "code": "1.1.1",
       "name": "Einzelbaum",
       "farbe": "#d0d33d",
       "segmente": 3,
       "anteil": 1.0
      },
      {
       "code": "0",
       "name": "Nicht bestimmbar",
       "farbe": "#474747",
       "segmente": 11,
       "anteil": 0.8
      },
      {
       "code": "3.2",
       "name": "Offener Boden",
       "farbe": "#aa2800",
       "segmente": 2,
       "anteil": 0.6
      },
      {
       "code": "1.3",
       "name": "Gebüsch",
       "farbe": "#193c10",
       "segmente": 5,
       "anteil": 0.3
      },
      {
       "code": "4.1.2",
       "name": "Nebengebäude",
       "farbe": "#ae105c",
       "segmente": 2,
       "anteil": 0.2
      },
      {
       "code": "6.2.3",
       "name": "Trampelpfad",
       "farbe": "#4a49c0",
       "segmente": 1,
       "anteil": 0.2
      },
      {
       "code": "2.1.2",
       "name": "Wiese ungemäht",
       "farbe": "#a68905",
       "segmente": 1,
       "anteil": 0.2
      },
      {
       "code": "3.1.1",
       "name": "Feld abgeerntet",
       "farbe": "#6a0f22",
       "segmente": 1,
       "anteil": 0.1
      },
      {
       "code": "6.4",
       "name": "Terrasse",
       "farbe": "#d6d3fd",
       "segmente": 1,
       "anteil": 0.0
      }
     ]
    },
    "r1c1": {
     "segmente": 408,
     "unsicher": 275,
     "naht": 93,
     "luecken": 0,
     "kategorien": [
      {
       "code": "2.1",
       "name": "Wiese",
       "farbe": "#6b3b05",
       "segmente": 5,
       "anteil": 16.3
      },
      {
       "code": "1.2.1",
       "name": "Wald belichtet",
       "farbe": "#a0c175",
       "segmente": 8,
       "anteil": 15.3
      },
      {
       "code": "2.2",
       "name": "Rasen",
       "farbe": "#937f49",
       "segmente": 64,
       "anteil": 13.6
      },
      {
       "code": "3.3.2",
       "name": "Parzelle gemischt",
       "farbe": "#b4612e",
       "segmente": 24,
       "anteil": 12.8
      },
      {
       "code": "0",
       "name": "Nicht bestimmbar",
       "farbe": "#474747",
       "segmente": 93,
       "anteil": 8.8
      },
      {
       "code": "1.1.2",
       "name": "Baumgruppe",
       "farbe": "#0dd9b7",
       "segmente": 19,
       "anteil": 8.5
      },
      {
       "code": "3.1.1",
       "name": "Feld abgeerntet",
       "farbe": "#6a0f22",
       "segmente": 7,
       "anteil": 7.2
      },
      {
       "code": "4.1.2",
       "name": "Nebengebäude",
       "farbe": "#ae105c",
       "segmente": 42,
       "anteil": 5.7
      },
      {
       "code": "1.3",
       "name": "Gebüsch",
       "farbe": "#193c10",
       "segmente": 40,
       "anteil": 3.1
      },
      {
       "code": "1.1.1",
       "name": "Einzelbaum",
       "farbe": "#d0d33d",
       "segmente": 17,
       "anteil": 2.1
      },
      {
       "code": "3.3.1",
       "name": "Beete",
       "farbe": "#9e5b50",
       "segmente": 10,
       "anteil": 1.2
      },
      {
       "code": "0.1.1",
       "name": "Gebäudeschatten",
       "farbe": "#818181",
       "segmente": 23,
       "anteil": 1.0
      },
      {
       "code": "6.3",
       "name": "Hof und Zufahrt",
       "farbe": "#103755",
       "segmente": 6,
       "anteil": 0.9
      },
      {
       "code": "6.4",
       "name": "Terrasse",
       "farbe": "#d6d3fd",
       "segmente": 16,
       "anteil": 0.8
      },
      {
       "code": "4.1",
       "name": "Gebäude",
       "farbe": "#a45080",
       "segmente": 3,
       "anteil": 0.7
      },
      {
       "code": "6.2.3",
       "name": "Trampelpfad",
       "farbe": "#4a49c0",
       "segmente": 4,
       "anteil": 0.6
      },
      {
       "code": "6.2.1",
       "name": "Gartenweg",
       "farbe": "#754496",
       "segmente": 5,
       "anteil": 0.5
      },
      {
       "code": "1.4",
       "name": "Hecke",
       "farbe": "#74a40b",
       "segmente": 7,
       "anteil": 0.4
      },
      {
       "code": "4.3",
       "name": "Kleinobjekt",
       "farbe": "#f8608f",
       "segmente": 4,
       "anteil": 0.1
      },
      {
       "code": "4.3.1",
       "name": "Frühbeet",
       "farbe": "#ffccba",
       "segmente": 4,
       "anteil": 0.1
      },
      {
       "code": "2.3",
       "name": "Saum und Randstreifen",
       "farbe": "#f7b631",
       "segmente": 3,
       "anteil": 0.1
      },
      {
       "code": "4.1.3",
       "name": "Gewächshaus",
       "farbe": "#591f42",
       "segmente": 2,
       "anteil": 0.1
      },
      {
       "code": "0.1.2",
       "name": "Heckenschatten",
       "farbe": "#a0a0a0",
       "segmente": 1,
       "anteil": 0.1
      },
      {
       "code": "6.2.2",
       "name": "Feld- und Erdweg",
       "farbe": "#447bad",
       "segmente": 1,
       "anteil": 0.0
      }
     ]
    }
   }
  },
  {
   "kennung": "C",
   "name": "Feste Kategorienliste",
   "beschreibung": "Flächen nach der festen Kategorienliste des Projekts (geordnet nach Bedeckung), Urteil der KI Segment für Segment auf den Grenzen der Vorstufe.",
   "vorhanden": true,
   "bild": "../gemeinsam/bilder/fassung-c.png",
   "ebenen": [
    {
     "ebene": 1,
     "name": "grob",
     "klassen": 7
    },
    {
     "ebene": 2,
     "name": "mittel",
     "klassen": 25
    },
    {
     "ebene": 3,
     "name": "fein",
     "klassen": 43
    }
   ],
   "naehte": 4,
   "teilkacheln": {
    "r0c0": {
     "segmente": 206,
     "unsicher": 159,
     "naht": 67,
     "luecken": 0,
     "kategorien": [
      {
       "code": "3.5",
       "name": "Verbuschende Fläche (Grünland mit Gehölzanflug)",
       "farbe": "#749146",
       "segmente": 5,
       "anteil": 30.1
      },
      {
       "code": "3.1",
       "name": "Wiese / Weide (gemeinsam)",
       "farbe": "#3de723",
       "segmente": 48,
       "anteil": 24.0
      },
      {
       "code": "4.2",
       "name": "Gehölz außerhalb Wald",
       "farbe": "#13ae95",
       "segmente": 45,
       "anteil": 13.3
      },
      {
       "code": "1.1.1",
       "name": "Hauptgebäude (Wohn-, Betriebsgebäude)",
       "farbe": "#e61382",
       "segmente": 14,
       "anteil": 8.3
      },
      {
       "code": "2.1",
       "name": "Acker mit Bewuchs",
       "farbe": "#a4771e",
       "segmente": 7,
       "anteil": 5.0
      },
      {
       "code": "4.2.1",
       "name": "Einzelbaum",
       "farbe": "#15bc58",
       "segmente": 15,
       "anteil": 4.4
      },
      {
       "code": "1.2.4",
       "name": "Platz / Parkplatz / Hoffläche versiegelt",
       "farbe": "#ce5678",
       "segmente": 11,
       "anteil": 3.1
      },
      {
       "code": "4.2.2",
       "name": "Baumgruppe / Feldgehölz",
       "farbe": "#4f926e",
       "segmente": 6,
       "anteil": 2.9
      },
      {
       "code": "4.2.4",
       "name": "Gebüsch / Strauchfläche",
       "farbe": "#0c3c34",
       "segmente": 12,
       "anteil": 2.6
      },
      {
       "code": "1.2.1",
       "name": "Straße (versiegelt)",
       "farbe": "#f19daa",
       "segmente": 2,
       "anteil": 2.6
      },
      {
       "code": "1.3.3",
       "name": "Schwimmbecken",
       "farbe": "#840b2d",
       "segmente": 3,
       "anteil": 0.8
      },
      {
       "code": "0.2",
       "name": "Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund",
       "farbe": "#d9d9d9",
       "segmente": 7,
       "anteil": 0.6
      },
      {
       "code": "1.3.1",
       "name": "Lager-, Schotter-, Kiesfläche (künstlich, unversiegelt)",
       "farbe": "#a21771",
       "segmente": 3,
       "anteil": 0.5
      },
      {
       "code": "4.1",
       "name": "Wald (geschlossener Bestand)",
       "farbe": "#19e697",
       "segmente": 8,
       "anteil": 0.5
      },
      {
       "code": "1.2.2",
       "name": "Weg, befestigt (Asphalt, Pflaster)",
       "farbe": "#d4aee0",
       "segmente": 7,
       "anteil": 0.5
      },
      {
       "code": "3.4",
       "name": "Krautsaum linear (Feldrain, Wegrand, Böschung)",
       "farbe": "#47b521",
       "segmente": 6,
       "anteil": 0.3
      },
      {
       "code": "4.2.3",
       "name": "Hecke / Baumreihe / Ufergehölz (linear)",
       "farbe": "#19e65c",
       "segmente": 5,
       "anteil": 0.3
      },
      {
       "code": "1.3",
       "name": "Sonstige künstliche Fläche",
       "farbe": "#740b84",
       "segmente": 1,
       "anteil": 0.1
      },
      {
       "code": "3.1.1",
       "name": "Wiese (Mahdspuren sichtbar)",
       "farbe": "#80ef6f",
       "segmente": 1,
       "anteil": 0.0
      }
     ]
    },
    "r0c1": {
     "segmente": 234,
     "unsicher": 196,
     "naht": 59,
     "luecken": 0,
     "kategorien": [
      {
       "code": "4.2",
       "name": "Gehölz außerhalb Wald",
       "farbe": "#13ae95",
       "segmente": 17,
       "anteil": 20.2
      },
      {
       "code": "3.1.1",
       "name": "Wiese (Mahdspuren sichtbar)",
       "farbe": "#80ef6f",
       "segmente": 13,
       "anteil": 20.2
      },
      {
       "code": "4.2.1",
       "name": "Einzelbaum",
       "farbe": "#15bc58",
       "segmente": 45,
       "anteil": 16.7
      },
      {
       "code": "3.1",
       "name": "Wiese / Weide (gemeinsam)",
       "farbe": "#3de723",
       "segmente": 41,
       "anteil": 15.1
      },
      {
       "code": "1.1.1",
       "name": "Hauptgebäude (Wohn-, Betriebsgebäude)",
       "farbe": "#e61382",
       "segmente": 24,
       "anteil": 10.9
      },
      {
       "code": "1.2.1",
       "name": "Straße (versiegelt)",
       "farbe": "#f19daa",
       "segmente": 14,
       "anteil": 4.4
      },
      {
       "code": "4.1",
       "name": "Wald (geschlossener Bestand)",
       "farbe": "#19e697",
       "segmente": 14,
       "anteil": 3.1
      },
      {
       "code": "0.2",
       "name": "Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund",
       "farbe": "#d9d9d9",
       "segmente": 14,
       "anteil": 2.1
      },
      {
       "code": "3.4",
       "name": "Krautsaum linear (Feldrain, Wegrand, Böschung)",
       "farbe": "#47b521",
       "segmente": 11,
       "anteil": 1.7
      },
      {
       "code": "2.1",
       "name": "Acker mit Bewuchs",
       "farbe": "#a4771e",
       "segmente": 3,
       "anteil": 1.4
      },
      {
       "code": "1.2.4",
       "name": "Platz / Parkplatz / Hoffläche versiegelt",
       "farbe": "#ce5678",
       "segmente": 10,
       "anteil": 1.2
      },
      {
       "code": "3.5",
       "name": "Verbuschende Fläche (Grünland mit Gehölzanflug)",
       "farbe": "#749146",
       "segmente": 8,
       "anteil": 1.0
      },
      {
       "code": "4.2.4",
       "name": "Gebüsch / Strauchfläche",
       "farbe": "#0c3c34",
       "segmente": 9,
       "anteil": 0.9
      },
      {
       "code": "1.1.2",
       "name": "Nebengebäude / Schuppen / Stadel",
       "farbe": "#d370f3",
       "segmente": 4,
       "anteil": 0.6
      },
      {
       "code": "1.3.3",
       "name": "Schwimmbecken",
       "farbe": "#840b2d",
       "segmente": 3,
       "anteil": 0.4
      },
      {
       "code": "3.3",
       "name": "Grünlandbrache / Ruderalflur",
       "farbe": "#a5d19f",
       "segmente": 1,
       "anteil": 0.2
      },
      {
       "code": "1.3",
       "name": "Sonstige künstliche Fläche",
       "farbe": "#740b84",
       "segmente": 1,
       "anteil": 0.0
      },
      {
       "code": "1.2.2",
       "name": "Weg, befestigt (Asphalt, Pflaster)",
       "farbe": "#d4aee0",
       "segmente": 1,
       "anteil": 0.0
      },
      {
       "code": "4.2.2",
       "name": "Baumgruppe / Feldgehölz",
       "farbe": "#4f926e",
       "segmente": 1,
       "anteil": 0.0
      }
     ]
    },
    "r1c0": {
     "segmente": 86,
     "unsicher": 67,
     "naht": 24,
     "luecken": 0,
     "kategorien": [
      {
       "code": "4.1",
       "name": "Wald (geschlossener Bestand)",
       "farbe": "#19e697",
       "segmente": 28,
       "anteil": 67.8
      },
      {
       "code": "3.1",
       "name": "Wiese / Weide (gemeinsam)",
       "farbe": "#3de723",
       "segmente": 21,
       "anteil": 18.6
      },
      {
       "code": "3.5",
       "name": "Verbuschende Fläche (Grünland mit Gehölzanflug)",
       "farbe": "#749146",
       "segmente": 7,
       "anteil": 7.4
      },
      {
       "code": "4.2",
       "name": "Gehölz außerhalb Wald",
       "farbe": "#13ae95",
       "segmente": 10,
       "anteil": 3.1
      },
      {
       "code": "2.1",
       "name": "Acker mit Bewuchs",
       "farbe": "#a4771e",
       "segmente": 4,
       "anteil": 1.2
      },
      {
       "code": "6.1",
       "name": "Offene Sand-, Löss-, Lehmstelle (Abbruch, Hohlweg, Grube)",
       "farbe": "#763c23",
       "segmente": 1,
       "anteil": 0.5
      },
      {
       "code": "6.6",
       "name": "Weg, unbefestigt (Feld-, Wald-, Schotterweg)",
       "farbe": "#a0522d",
       "segmente": 2,
       "anteil": 0.4
      },
      {
       "code": "1.1.2",
       "name": "Nebengebäude / Schuppen / Stadel",
       "farbe": "#d370f3",
       "segmente": 4,
       "anteil": 0.3
      },
      {
       "code": "4.2.2",
       "name": "Baumgruppe / Feldgehölz",
       "farbe": "#4f926e",
       "segmente": 2,
       "anteil": 0.3
      },
      {
       "code": "0.2",
       "name": "Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund",
       "farbe": "#d9d9d9",
       "segmente": 2,
       "anteil": 0.1
      },
      {
       "code": "3.1.1",
       "name": "Wiese (Mahdspuren sichtbar)",
       "farbe": "#80ef6f",
       "segmente": 1,
       "anteil": 0.1
      },
      {
       "code": "4.2.1",
       "name": "Einzelbaum",
       "farbe": "#15bc58",
       "segmente": 1,
       "anteil": 0.0
      },
      {
       "code": "1.1.1",
       "name": "Hauptgebäude (Wohn-, Betriebsgebäude)",
       "farbe": "#e61382",
       "segmente": 1,
       "anteil": 0.0
      },
      {
       "code": "1.3.4",
       "name": "Sport-, Spielplatz (künstlicher Belag)",
       "farbe": "#b370c9",
       "segmente": 1,
       "anteil": 0.0
      },
      {
       "code": "1.3.2",
       "name": "Baustelle",
       "farbe": "#572768",
       "segmente": 1,
       "anteil": 0.0
      }
     ]
    },
    "r1c1": {
     "segmente": 408,
     "unsicher": 352,
     "naht": 81,
     "luecken": 0,
     "kategorien": [
      {
       "code": "3.1",
       "name": "Wiese / Weide (gemeinsam)",
       "farbe": "#3de723",
       "segmente": 119,
       "anteil": 32.3
      },
      {
       "code": "4.1",
       "name": "Wald (geschlossener Bestand)",
       "farbe": "#19e697",
       "segmente": 30,
       "anteil": 17.6
      },
      {
       "code": "3.5",
       "name": "Verbuschende Fläche (Grünland mit Gehölzanflug)",
       "farbe": "#749146",
       "segmente": 3,
       "anteil": 15.7
      },
      {
       "code": "4.2.1",
       "name": "Einzelbaum",
       "farbe": "#15bc58",
       "segmente": 60,
       "anteil": 7.3
      },
      {
       "code": "4.2.2",
       "name": "Baumgruppe / Feldgehölz",
       "farbe": "#4f926e",
       "segmente": 11,
       "anteil": 6.3
      },
      {
       "code": "1.1.2",
       "name": "Nebengebäude / Schuppen / Stadel",
       "farbe": "#d370f3",
       "segmente": 55,
       "anteil": 6.3
      },
      {
       "code": "4.2.4",
       "name": "Gebüsch / Strauchfläche",
       "farbe": "#0c3c34",
       "segmente": 24,
       "anteil": 2.7
      },
      {
       "code": "1.1.1",
       "name": "Hauptgebäude (Wohn-, Betriebsgebäude)",
       "farbe": "#e61382",
       "segmente": 35,
       "anteil": 2.6
      },
      {
       "code": "2.1",
       "name": "Acker mit Bewuchs",
       "farbe": "#a4771e",
       "segmente": 3,
       "anteil": 2.4
      },
      {
       "code": "1.2.4",
       "name": "Platz / Parkplatz / Hoffläche versiegelt",
       "farbe": "#ce5678",
       "segmente": 16,
       "anteil": 1.4
      },
      {
       "code": "6.6",
       "name": "Weg, unbefestigt (Feld-, Wald-, Schotterweg)",
       "farbe": "#a0522d",
       "segmente": 6,
       "anteil": 1.0
      },
      {
       "code": "1.3",
       "name": "Sonstige künstliche Fläche",
       "farbe": "#740b84",
       "segmente": 6,
       "anteil": 0.8
      },
      {
       "code": "4.2.3",
       "name": "Hecke / Baumreihe / Ufergehölz (linear)",
       "farbe": "#19e65c",
       "segmente": 8,
       "anteil": 0.8
      },
      {
       "code": "3.1.1",
       "name": "Wiese (Mahdspuren sichtbar)",
       "farbe": "#80ef6f",
       "segmente": 6,
       "anteil": 0.6
      },
      {
       "code": "0.2",
       "name": "Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund",
       "farbe": "#d9d9d9",
       "segmente": 7,
       "anteil": 0.6
      },
      {
       "code": "2.2",
       "name": "Acker ohne Bewuchs (gepflügt, Saatbett)",
       "farbe": "#fdf8a5",
       "segmente": 4,
       "anteil": 0.4
      },
      {
       "code": "1.2.1",
       "name": "Straße (versiegelt)",
       "farbe": "#f19daa",
       "segmente": 3,
       "anteil": 0.4
      },
      {
       "code": "1.1.3",
       "name": "Gewächshaus / Folientunnel",
       "farbe": "#e63d13",
       "segmente": 4,
       "anteil": 0.3
      },
      {
       "code": "1.3.1",
       "name": "Lager-, Schotter-, Kiesfläche (künstlich, unversiegelt)",
       "farbe": "#a21771",
       "segmente": 2,
       "anteil": 0.2
      },
      {
       "code": "1.2.2",
       "name": "Weg, befestigt (Asphalt, Pflaster)",
       "farbe": "#d4aee0",
       "segmente": 3,
       "anteil": 0.2
      },
      {
       "code": "1.1",
       "name": "Gebäude",
       "farbe": "#eb21ed",
       "segmente": 1,
       "anteil": 0.1
      },
      {
       "code": "1",
       "name": "Versiegelt / bebaut (Siedlung und Verkehr)",
       "farbe": "#bd2835",
       "segmente": 1,
       "anteil": 0.1
      },
      {
       "code": "3.4",
       "name": "Krautsaum linear (Feldrain, Wegrand, Böschung)",
       "farbe": "#47b521",
       "segmente": 1,
       "anteil": 0.0
      }
     ]
    }
   }
  }
 ],
 "start": {
  "fassung": "C",
  "teilkachel": "r0c0"
 },
 "kommentare": [
  {
   "nr": 1,
   "fassung": "C",
   "teilkachel": "r0c0",
   "segment": 100214,
   "text": "Beispiel: Grenze zur Wiese zu weit im Gehölz",
   "zeit": "2026-11-17T18:04:00"
  },
  {
   "nr": 2,
   "fassung": "B",
   "teilkachel": "r1c1",
   "segment": 100377,
   "text": "Beispiel: Rasen und Wiese hier nicht trennbar",
   "zeit": "2026-11-17T18:11:00"
  }
 ]
}

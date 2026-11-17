"""Baut urteil.json eines Viertels aus spec.py (gleicher Ordner). Aufruf: <py> -I baue_urteil.py <ordner>"""
import json
import runpy
import sys
from pathlib import Path

BASIS = "C:/Users/Phil/Developement/Victor/daten/landseg/T0"

KLASSEN = {
    "Gehölz": ("grob", None, "Kronen mit Struktur und Schlagschatten, dunkler als Gras."),
    "Baumgruppe": ("mittel", "Gehölz", "Mehrere ineinander greifende Kronen als eine Masse."),
    "Einzelbaum": ("mittel", "Gehölz", "Eine runde Krone mit eigenem Schatten, freistehend."),
    "Laubbaum": ("fein", "Einzelbaum", "Runde, weich gekörnte Krone in hellem bis mittlerem Grün."),
    "Nadelbaum": ("fein", "Einzelbaum", "Spitz-runde, bläulich- oder dunkelgrüne Krone mit feiner Körnung."),
    "Blutbuche": ("fein", "Einzelbaum", "Große Krone in rotbraun-violettem Ton."),
    "Gebüsch": ("mittel", "Gehölz", "Kleine dunkle Krone, niedriger als ein Baum, oft unregelmäßig."),
    "Gebüsch oder kleiner Baum": ("fein", "Gebüsch", "Kleine dunkle Krone, Höhe aus der Draufsicht nicht zu entscheiden."),
    "Hecke": ("mittel", "Gehölz", "Schmales, langes dunkelgrünes Band an Grundstücksgrenzen."),
    "Wald": ("mittel", "Gehölz", "Großflächig geschlossene Kronen ohne Lücken zum Boden."),
    "Grünland": ("grob", None, "Offene Grasflächen außerhalb von Gärten."),
    "Wiese ungemäht": ("mittel", "Grünland", "Hohes, unruhiges Gras mit Flecken, keine Mähspuren."),
    "Altgras mit Gebüsch": ("fein", "Wiese ungemäht", "Ungemähtes Gras mit eingestreuten kleinen Sträuchern und Trockenstellen."),
    "Wiese gemäht": ("mittel", "Grünland", "Gleichmäßig kurzes Gras, glatte Fläche."),
    "Wiesenstreifen": ("fein", "Wiese gemäht", "Schmaler Grasstreifen am Rand eines Feldes oder Gehölzes."),
    "Mähwiese mit Heu": ("fein", "Wiese gemäht", "Gemähte Fläche mit braunen Heu- oder Strohschwaden in Bögen."),
    "Siedlungsgrün": ("grob", None, "Gepflegte Grünflächen an Häusern und Straßen."),
    "Grünstreifen": ("mittel", "Siedlungsgrün", "Schmaler gemähter Grasstreifen entlang einer Straße."),
    "Straßenbegleitgrün": ("fein", "Grünstreifen", "Grasstreifen direkt am Straßenrand."),
    "Garten": ("mittel", "Siedlungsgrün", "Kleinteilige Fläche mit Rasen, Beeten und Sträuchern auf einem Wohngrundstück."),
    "Garten mit Gehölz": ("fein", "Garten", "Garten mit vielen Sträuchern oder kleinen Bäumen."),
    "Rasen": ("mittel", "Siedlungsgrün", "Gleichmäßig kurzes, sattgrünes Gras auf einem Wohngrundstück."),
    "Hausrasen": ("fein", "Rasen", "Gemähter Rasen direkt am Haus."),
    "Gartenausstattung": ("fein", "Garten", "Kleines helles Objekt im Garten: Sandkiste, Hochbeet, Spielgerät, Deckel."),
    "Bebaut": ("grob", None, "Gebäude und Bauwerke mit Dach oder Mauer."),
    "Gebäude": ("mittel", "Bebaut", "Dachfläche mit geraden Kanten und Schatten."),
    "Wohnhaus": ("fein", "Gebäude", "Großes Dach (Ziegel oder Flachdach) auf einem Wohngrundstück."),
    "Nebengebäude": ("fein", "Gebäude", "Kleines Dach (Schuppen, Garage, Gartenhütte) neben einem Haus."),
    "Terrasse": ("mittel", "Bebaut", "Helle befestigte Fläche direkt am Haus, mit Möbeln oder Stufen."),
    "Schwimmbecken": ("mittel", "Bebaut", "Rechteckiges Becken mit hellem Rand, Wasser oder Abdeckung innen."),
    "Mauer": ("mittel", "Bebaut", "Schmales gerades Band mit Schlagschatten."),
    "Stützmauer": ("fein", "Mauer", "Mauer an einer Geländestufe zwischen Garten und Zufahrt oder Wiese."),
    "Verkehrsfläche": ("grob", None, "Befestigte Flächen für Fahrzeuge oder Fußgänger."),
    "Straße": ("mittel", "Verkehrsfläche", "Durchgehendes Fahrband zwischen Grundstücken."),
    "Asphaltstraße": ("fein", "Straße", "Dunkelgraues glattes Fahrband."),
    "Betonfahrbahn": ("fein", "Straße", "Hellgraues Fahrband, Beton oder heller Belag."),
    "Randstein": ("mittel", "Verkehrsfläche", "Heller schmaler Betonstreifen am Straßenrand."),
    "Zufahrt": ("mittel", "Verkehrsfläche", "Befestigte Fläche von der Straße zu einem Grundstück."),
    "Betonfläche": ("fein", "Zufahrt", "Hellgraue glatte Fläche ohne Fahrbahnmarkierung."),
    "Straßenrand": ("mittel", "Verkehrsfläche", "Unbefestigter oder geschotterter Rand neben der Fahrbahn."),
    "Schotterbankett": ("fein", "Straßenrand", "Graubrauner, körniger Streifen neben dem Asphalt."),
    "Weg": ("mittel", "Verkehrsfläche", "Schmales Band für Fußgänger oder landwirtschaftliche Fahrzeuge."),
    "Trampelpfad": ("fein", "Weg", "Schmale helle Spur im Gras ohne Belag."),
    "Erdweg": ("fein", "Weg", "Unbefestigter Weg mit hellem Boden oder Fahrspuren."),
    "Lagerfläche": ("grob", None, "Abgelegtes Material auf offenem Gelände."),
    "Holzlager": ("mittel", "Lagerfläche", "Gelagertes Holz, helle Stämme und Äste."),
    "Holzstapel": ("fein", "Holzlager", "Haufen aus hellen, kreuz und quer liegenden Stämmen und Ästen."),
    "Acker": ("grob", None, "Bewirtschaftete Feldfläche mit Bearbeitungsspuren."),
    "Acker abgeerntet": ("mittel", "Acker", "Braune bis strohgelbe Fläche mit Stoppeln oder Schwaden."),
    "Stoppelfeld mit Schwaden": ("fein", "Acker abgeerntet", "Strohfarbene Fläche mit bogenförmigen Schwaden der Ernte."),
    "Offener Boden": ("grob", None, "Fläche ohne Bewuchs, Erde oder Steine sichtbar."),
    "Erdfläche": ("mittel", "Offener Boden", "Helle braune bis graue Bodenstelle ohne Gras."),
    "Wiese": ("mittel", "Grünland", "Gleichmäßig glatte Grasfläche, Mahd nicht sicher erkennbar."),
    "Gebüschfläche": ("mittel", "Gehölz", "Flächig dichter, grob gekörnter Bewuchs aus Sträuchern und Jungwuchs ohne große Kronen."),
}


def main():
    ordner = Path(sys.argv[1])
    spec = runpy.run_path(str(ordner / "spec.py"))
    v = spec["VIERTEL"]
    vdir = f"{BASIS}/fassung-b/viertel/r0c0/{v}"
    odir = f"{BASIS}/fassung-b/urteil/r0c0/{v}"
    kurz = {"u": "uebersicht_nummern.jpg", "ur": "uebersicht_roh.jpg", "uk": "uebersicht_kontrast.jpg"}
    for i in range(1, 5):
        kurz[f"n{i}"] = f"nah{i}_nummern.jpg"
        kurz[f"r{i}"] = f"nah{i}_roh.jpg"

    def pfad(k):
        if k in kurz:
            return f"{vdir}/{kurz[k]}"
        if k.startswith("eigen:"):
            return f"{odir}/{k[6:]}"
        return k

    segs = []
    benutzt = []
    for s in spec["SEG"]:
        sid, heute, was, urteil, (g, m, f), sicher, punkte, bilder = s
        for n in (g, m, f):
            if n not in KLASSEN:
                raise SystemExit(f"Klasse fehlt im Verzeichnis: {n}")
            if n not in benutzt:
                benutzt.append(n)
        segs.append({"id": sid, "klasse_heute": heute, "was_ist_es": was,
                     "urteil": "sauber" if urteil == "s" else "nicht_sauber", "klasse_vorschlag": None,
                     "klasse_frei": {"grob": g, "mittel": m, "fein": f}, "sicher": sicher,
                     "punkte": [{"nr": i + 1, "art": p[0], "text": p[1], "flaeche_px": p[2]} for i, p in enumerate(punkte)],
                     "bilder": [pfad(b) for b in bilder]})
        if urteil == "s" and punkte:
            raise SystemExit(f"{sid}: sauber mit Punkten")
        if urteil != "s" and not punkte:
            raise SystemExit(f"{sid}: nicht sauber ohne Punkte")
    ueb = [f"{BASIS}/kern500/T0.png", f"{BASIS}/kern500/ganz/r0c0/ganz_nummern.jpg",
           f"{BASIS}/kern500/ganz/r0c0/ganz_roh.jpg"] + [pfad(b) for b in spec["UEBERSICHT"]]
    out = {"teilkachel": "r0c0", "viertel": v, "bearbeiter": f"urt-b-r0c0-{v}",
           "bilder_angesehen": {"uebersicht": ueb, "nah": [pfad(b) for b in spec["NAH"]]},
           "segmente": segs, "naht": spec["NAHT"], "unsicher": spec["UNSICHER"],
           "nicht_geprueft": spec["NICHT_GEPRUEFT"], "offen": spec["OFFEN"],
           "klassen_frei": [{"name": n, "ebene": KLASSEN[n][0], "eltern": KLASSEN[n][1], "merkmal": KLASSEN[n][2]}
                            for n in benutzt]}
    (ordner / "urteil.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("geschrieben", len(segs), "Segmente,", sum(1 for x in segs if x["urteil"] == "nicht_sauber"), "nicht sauber,",
          sum(len(x["punkte"]) for x in segs), "Punkte,", sum(1 for x in segs if not x["sicher"]), "unsicher")


if __name__ == "__main__":
    main()

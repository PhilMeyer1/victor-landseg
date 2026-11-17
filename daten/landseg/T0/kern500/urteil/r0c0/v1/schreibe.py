"""Hilfsmodul: baut urteil.json eines Viertels aus einer knappen Liste.
Bildkürzel: n1..n4 = vorbereitete nahX_nummern.jpg, r1..r4 = nahX_roh.jpg, u = uebersicht_nummern.jpg,
ur = uebersicht_roh.jpg, uk = uebersicht_kontrast.jpg, e:<name> = eigenes Bild im Ergebnisordner."""
import json

B = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500"


def pfad(v, k):
    V = f"{B}/viertel/r0c0/{v}/"
    U = f"{B}/urteil/r0c0/{v}/"
    if k.startswith("e:"):
        return U + k[2:]
    if k.startswith("x:"):
        return B + "/" + k[2:]
    m = {"u": "uebersicht_nummern.jpg", "ur": "uebersicht_roh.jpg", "uk": "uebersicht_kontrast.jpg",
         "uv": "uebersicht_vorschlag.jpg", "um": "uebersicht_maengel.jpg"}
    if k in m:
        return V + m[k]
    if k[0] == "n":
        return V + f"nah{k[1]}_nummern.jpg"
    if k[0] == "r":
        return V + f"nah{k[1]}_roh.jpg"
    raise ValueError(k)


def schreibe(v, uebersicht, nah, segs, naht, unsicher, nicht_geprueft, offen):
    out = {"teilkachel": "r0c0", "viertel": v, "bearbeiter": f"urt-a-r0c0-{v}",
           "bilder_angesehen": {"uebersicht": [pfad(v, k) for k in uebersicht], "nah": [pfad(v, k) for k in nah]},
           "segmente": [], "naht": naht, "unsicher": unsicher, "nicht_geprueft": nicht_geprueft, "offen": offen}
    for s in segs:
        sid, heute, was, vorschlag, sicher, punkte, bilder = s
        out["segmente"].append({
            "id": sid, "klasse_heute": heute, "was_ist_es": was,
            "urteil": "nicht_sauber" if punkte else "sauber",
            "klasse_vorschlag": vorschlag, "sicher": sicher,
            "punkte": [{"nr": i + 1, "art": p[0], "text": p[1], "flaeche_px": p[2]} for i, p in enumerate(punkte)],
            "bilder": [pfad(v, k) for k in bilder]})
    with open(f"{B}/urteil/r0c0/{v}/urteil.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(v, len(out["segmente"]), "Segmente,", sum(1 for e in out["segmente"] if e["urteil"] == "nicht_sauber"),
          "nicht sauber,", sum(len(e["punkte"]) for e in out["segmente"]), "Punkte,",
          sum(1 for e in out["segmente"] if not e["sicher"]), "unsicher")

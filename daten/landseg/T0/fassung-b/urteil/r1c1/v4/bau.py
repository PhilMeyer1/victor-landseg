"""Baut urteil.json und die Ergebnisbilder dieses Viertels aus daten.json (im Ordner dieses Skripts).

daten.json: {"nah": [...], "segmente": [{"id", "was", "kf": [grob, mittel, fein], "sicher", "urteil",
             "punkte": [{"art", "text", "xy": [x, y], "flaeche_px"}], "bilder": [...]}],
             "naht": [...], "unsicher": [...], "offen": [...], "nicht_geprueft": [...],
             "klassen_frei": [{"name", "ebene", "eltern", "merkmal"}]}
"""
import json
import shutil
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

B = Path("C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b")
OUT = Path(__file__).parent
V = OUT.name
VD = B / "viertel/r1c1" / V
vj = json.loads((VD / "viertel.json").read_text(encoding="utf-8"))
seg = {s["id"]: s for s in json.loads((B / "vorstufe/r1c1/segmente.json").read_text(encoding="utf-8"))["segmente"]}
d = json.loads((OUT / "daten.json").read_text(encoding="utf-8"))
lab = tifffile.imread(B / "vorstufe/r1c1/labels.tif").astype(np.int64)
tile = Image.open(B / "teilkacheln/r1c1.png").convert("RGB")

fen = vj["bilder"]["uebersicht_roh.jpg"]["fenster"]
FX, FY, FW, FH, F = fen["x"], fen["y"], fen["breite"], fen["hoehe"], fen["faktor"]
vib = vj["viertel_im_bild"]
UE = [str(Path("C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/T0.png")),
      str(Path("C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/ganz/r1c1/ganz_nummern.jpg")),
      str(Path("C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/ganz/r1c1/ganz_roh.jpg"))]
UE = [p.replace("\\", "/") for p in UE] + [f"{VD.as_posix()}/{n}" for n in
                                           ("uebersicht_nummern.jpg", "uebersicht_roh.jpg", "uebersicht_vorschlag.jpg",
                                            "uebersicht_maengel.jpg", "uebersicht_kontrast.jpg")]
NAH = [f"{VD.as_posix()}/nah{i}_{t}.jpg" for i in (1, 2, 3, 4) for t in ("nummern", "roh")] + \
      [f"{OUT.as_posix()}/{n}" for n in d.get("nah", [])]


def bild(n):
    if "/" in n:
        return n
    if n.startswith("nah_"):
        return f"{OUT.as_posix()}/{n}"
    return f"{VD.as_posix()}/{n}"


segs = []
for s in d["segmente"]:
    sid = s["id"] if s["id"] > 100000 else 400000 + s["id"]
    pk = []
    for i, p in enumerate(s.get("punkte", []), 1):
        pk.append({"nr": i, "art": p["art"], "text": p["text"], "flaeche_px": p.get("flaeche_px")})
    segs.append({"id": sid, "klasse_heute": seg[sid]["klasse"], "was_ist_es": s["was"],
                 "urteil": "nicht_sauber" if pk or s.get("urteil") == "nicht_sauber" else "sauber",
                 "klasse_vorschlag": None,
                 "klasse_frei": {"grob": s["kf"][0], "mittel": s["kf"][1], "fein": s["kf"][2]},
                 "sicher": bool(s["sicher"]), "punkte": pk,
                 "bilder": [bild(b) for b in s.get("bilder", ["uebersicht_nummern.jpg"])]})
# Namensliste: aus allen daten.json der Viertel dieser Teilkachel gesammelt, auf die hier benutzten Namen
# (samt Eltern) beschränkt; fehlt ein Name, bricht der Bau ab.
alle_kl = {}
for vv in ("v1", "v2", "v3", "v4"):
    pf = OUT.parent / vv / "daten.json"
    if pf.is_file():
        for k in json.loads(pf.read_text(encoding="utf-8")).get("klassen_frei", []):
            alle_kl.setdefault(k["name"], k)
for k in d.get("klassen_frei", []):
    alle_kl[k["name"]] = k
benutzt = set()
for s in d["segmente"]:
    for n in s["kf"]:
        while n and n not in benutzt:
            if n not in alle_kl:
                raise SystemExit(f"Klassenname ohne Beschreibung: {n}")
            benutzt.add(n)
            n = alle_kl[n]["eltern"]
klassen = [k for k in alle_kl.values() if k["name"] in benutzt]
urteil = {"teilkachel": "r1c1", "viertel": V, "bearbeiter": f"urt-b-r1c1-{V}",
          "bilder_angesehen": {"uebersicht": UE, "nah": NAH},
          "segmente": segs, "naht": d.get("naht", []), "unsicher": d.get("unsicher", []),
          "nicht_geprueft": d.get("nicht_geprueft", []), "offen": d.get("offen", []),
          "klassen_frei": klassen}
(OUT / "urteil.json").write_text(json.dumps(urteil, ensure_ascii=False, indent=1), encoding="utf-8")

# Bilder
shutil.copyfile(VD / "uebersicht_roh.jpg", OUT / "roh.jpg")
shutil.copyfile(VD / "uebersicht_nummern.jpg", OUT / "umriss.jpg")
font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 13)
fsm = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 12)


def zu_bild(x, y):
    return (x - FX) * F + F // 2, (y - FY) * F + F // 2


def viertelrahmen(dr):
    x0, y0 = zu_bild(vib["x"], vib["y"])
    x1, y1 = zu_bild(vib["x"] + vib["breite"], vib["y"] + vib["hoehe"])
    dr.rectangle([x0 - F // 2, y0 - F // 2, x1 - F // 2, y1 - F // 2], outline=(0, 255, 255), width=2)


# Mängelbild
base = Image.open(VD / "uebersicht_roh.jpg").convert("RGB")
W, H = base.size
alle = [(s["id"], p) for s in d["segmente"] for p in s.get("punkte", [])]
zeilen = []
spalten = 1 if H + 18 * (len(alle) + 2) <= 2000 else 2
je = -(-len(alle) // spalten) if alle else 0
leg_h = 18 * (je + 2) if alle else 40
m = Image.new("RGB", (W * spalten, H + leg_h), (25, 25, 25))
m.paste(base, (0, 0))
dr = ImageDraw.Draw(m)
viertelrahmen(dr)
if not alle:
    dr.text((8, H + 10), "keine Mängel", font=font, fill=(255, 255, 255))
for k, (sid, p) in enumerate(alle, 1):
    x, y = zu_bild(*p["xy"])
    dr.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(220, 30, 30), outline=(255, 255, 255))
    dr.text((x, y), str(k), font=font, fill=(255, 255, 255), anchor="mm")
    t = f"{k}: Segment {sid % 100000} – {p['art']}: {p['text']}"
    if len(t) > 150:
        t = t[:147] + "…"
    sp, zl = divmod(k - 1, je)
    dr.text((6 + sp * W, H + 6 + 18 * zl), t, font=fsm, fill=(255, 255, 255))
if spalten == 2:
    dr.text((W + 10, 10), "Mängel dieses Viertels: nummerierte rote Punkte im Bild links,\nBeschriftung unten in zwei Spalten.",
            font=font, fill=(255, 255, 255))
m.save(OUT / "maengel.jpg", quality=90)

# Vorschlagsbild: Klassen frei (grob als Farbe, fein als Text), Grenzen gelb, geplante Änderungen als Marken
FARBE = {"Gehölz": (20, 110, 40), "Grünland": (120, 200, 70), "Garten": (210, 150, 60), "Bebauung": (210, 60, 60),
         "Verkehr": (230, 230, 230), "Schatten": (110, 60, 160), "Feld": (230, 200, 60), "Wasser": (40, 120, 230)}
pal =[(60, 160, 60), (20, 100, 40), (200, 80, 80), (150, 150, 150), (180, 140, 60), (60, 120, 200),
       (120, 80, 160), (230, 200, 60), (90, 90, 90), (200, 120, 200)]
for s in d["segmente"]:
    g = s["kf"][0]
    if g not in FARBE:
        FARBE[g] = pal[len(FARBE) % len(pal)]
crop = tile.crop((FX, FY, FX + FW, FY + FH))
L = lab[FY:FY + FH, FX:FX + FW]
arr = np.asarray(crop).astype(float)
mine = {(s["id"] if s["id"] > 100000 else 400000 + s["id"]): s for s in d["segmente"]}
for sid, s in mine.items():
    mk = L == sid
    arr[mk] = arr[mk] * 0.45 + np.array(FARBE[s["kf"][0]]) * 0.55
img = Image.fromarray(arr.clip(0, 255).astype(np.uint8)).resize((FW * F, FH * F), Image.NEAREST)
Lb = np.kron(L, np.ones((F, F), dtype=np.int64))
e = np.zeros_like(Lb, dtype=bool)
e[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
e[1:, :] |= Lb[1:, :] != Lb[:-1, :]
a2 = np.asarray(img).copy()
a2[e] = (255, 230, 0)
img = Image.fromarray(a2)
leg = 20 * (len(FARBE) // 4 + 2) + 30
v = Image.new("RGB", (W, H + leg), (25, 25, 25))
v.paste(img, (0, 0))
dr = ImageDraw.Draw(v)
viertelrahmen(dr)
for sid, s in mine.items():
    mk = L == sid
    if mk.sum() < 8:
        continue
    dt = ndimage.distance_transform_edt(np.pad(mk, 1))[1:-1, 1:-1]
    yy, xx = np.unravel_index(np.argmax(dt), dt.shape)
    t = f"{sid % 100000} {s['kf'][2]}"
    dr.text((xx * F + F // 2, yy * F + F // 2), t, font=fsm, fill=(255, 255, 255), anchor="mm",
            stroke_width=2, stroke_fill=(0, 0, 0))
for k, (sid, p) in enumerate(alle, 1):
    x, y = zu_bild(*p["xy"])
    dr.rectangle([x - 7, y - 7, x + 7, y + 7], outline=(255, 60, 60), width=2)
    dr.text((x + 9, y - 9), str(k), font=font, fill=(255, 90, 90), stroke_width=2, stroke_fill=(0, 0, 0))
yy = H + 6
xx = 6
for g, c in FARBE.items():
    if g not in {s["kf"][0] for s in d["segmente"]}:
        continue
    dr.rectangle([xx, yy, xx + 14, yy + 14], fill=c)
    dr.text((xx + 18, yy), g, font=fsm, fill=(255, 255, 255))
    xx += 210
    if xx > W - 200:
        xx, yy = 6, yy + 20
yy += 22
dr.text((6, yy), "Farbe = Oberklasse (grob), Text = Nummer und feine Klasse; rote Quadrate = vorgeschlagene Änderung "
        "(Nummer wie im Mängelbild); ohne Marke unverändert.", font=fsm, fill=(255, 255, 255))
v.save(OUT / "vorschlag.jpg", quality=90)
print("gebaut:", len(segs), "Segmente,", sum(1 for s in segs if s["urteil"] == "nicht_sauber"), "nicht sauber,",
      sum(len(s["punkte"]) for s in segs), "Punkte,", sum(1 for s in segs if not s["sicher"]), "unsicher")

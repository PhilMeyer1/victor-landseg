"""Hilfen fuer das Urteil r0c1 (Fassung B): Ansichten, Statistik, Masken -> Polygone."""
import json, sys
import numpy as np, cv2, tifffile
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

H0 = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
LAB = H0 + "/b-kategorien-frei/r0c1/labels.tif"
SEG = H0 + "/b-kategorien-frei/r0c1/segmente.json"
BILD = H0 + "/teilkacheln/r0c1.png"
FONT = "C:/Windows/Fonts/arial.ttf"

def lade():
    lab = tifffile.imread(LAB).astype(np.uint32)
    img = np.array(Image.open(BILD).convert("L"))
    seg = json.load(open(SEG, encoding="utf-8"))
    return lab, img, {s["id"]: s for s in seg["segmente"]}

def grenzen(lab):
    g = np.zeros(lab.shape, bool)
    g[:, 1:] |= lab[:, 1:] != lab[:, :-1]
    g[1:, :] |= lab[1:, :] != lab[:-1, :]
    return g

def ansicht(ziel, x0, y0, w, h, f, lab=None, img=None, ids_text=True, hervor=None, rahmen=None,
            linien=None, titel=None, kontrast=False):
    lab0, img0, _ = lade()
    lab = lab0 if lab is None else lab
    img = img0 if img is None else img
    sub = img[y0:y0+h, x0:x0+w].astype(float)
    if kontrast:
        lo, hi = np.percentile(sub, [1, 99]); sub = np.clip((sub-lo)/(hi-lo+1e-6)*255, 0, 255)
    rgb = np.stack([sub]*3, -1).astype(np.uint8)
    big = cv2.resize(rgb, (w*f, h*f), interpolation=cv2.INTER_NEAREST)
    if lab is not False:
        L = lab[y0:y0+h, x0:x0+w]
        Lb = cv2.resize(L.astype(np.float64), (w*f, h*f), interpolation=cv2.INTER_NEAREST).astype(np.int64)
        g = grenzen(Lb)
        big[g] = (255, 230, 0)
        if hervor:
            for sid in hervor:
                m = Lb == sid
                big[m] = (big[m]*0.6 + np.array([0, 120, 255])*0.4).astype(np.uint8)
    im = Image.fromarray(big); d = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT, 13)
    if rahmen:
        rx0, ry0, rx1, ry1 = rahmen
        d.rectangle([(rx0-x0)*f, (ry0-y0)*f, (rx1-x0)*f, (ry1-y0)*f], outline=(0, 255, 255), width=2)
    if linien:
        for ln in linien:
            pts = [((px-x0)*f+f//2, (py-y0)*f+f//2) for px, py in ln]
            d.line(pts, fill=(255, 0, 255), width=2)
    if lab is not False and ids_text:
        L = lab[y0:y0+h, x0:x0+w]
        for sid in np.unique(L):
            m = L == sid
            if m.sum() < 15: continue
            dt = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
            yy, xx = np.unravel_index(np.argmax(dt), dt.shape)
            t = str(int(sid) % 100000)
            d.text((xx*f+f//2-8, yy*f+f//2-7), t, fill=(255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
    # Gitter-Beschriftung am Rand
    for gx in range((x0//20+1)*20, x0+w, 20):
        d.text(((gx-x0)*f, 1), str(gx), fill=(0, 255, 0), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
    for gy in range((y0//20+1)*20, y0+h, 20):
        d.text((1, (gy-y0)*f), str(gy), fill=(0, 255, 0), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
    if titel:
        d.text((4, h*f-18), titel, fill=(255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
    im.save(ziel, quality=90)

def stat(ids):
    lab, img, seg = lade()
    for sid in ids:
        m = lab == sid
        if not m.any(): print(sid, "weg"); continue
        ys, xs = np.nonzero(m)
        print(sid, seg[sid]["klasse"], "fl", int(m.sum()), "bbox", xs.min(), ys.min(), xs.max(), ys.max(),
              "grau %.0f sd %.0f" % (img[m].mean(), img[m].std()))

def maske_zu_polygonen(maske):
    """Aussenkonturen exakt (ohne Vereinfachung) als Punktlisten."""
    cs, _ = cv2.findContours(maske.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return [c.reshape(-1, 2).tolist() for c in cs]

if __name__ == "__main__":
    stat([int(x) for x in sys.argv[1].split(",")])

KERN = (64, 64, 564, 564)

def zerlegen(sid, t_hell, t_dunkel, sigma=1.2, minfl=40, bereich=None, lab=None, img=None):
    """Kernteil von sid nach Grauton in hell/mittel/dunkel, 4er-Komponenten, kleine Stuecke
    an den Nachbarn mit der laengsten Grenze. Gibt Regionenkarte (0 = nicht betroffen) und Art je Region."""
    if lab is None:
        lab, img, _ = lade()
    kern = np.zeros(lab.shape, bool); kern[KERN[1]:KERN[3], KERN[0]:KERN[2]] = True
    if bereich is not None:
        b = np.zeros(lab.shape, np.uint8); cv2.fillPoly(b, [np.array(bereich, np.int32)], 1); kern &= b.astype(bool)
    m = (lab == sid) & kern
    s = ndimage.gaussian_filter(img.astype(float), sigma)
    art = np.where(s >= t_hell, 3, np.where(s <= t_dunkel, 1, 2))
    art[~m] = 0
    reg = np.zeros(lab.shape, np.int32); n = 0; arten = {}
    for a in (1, 2, 3):
        l, k = ndimage.label(art == a, structure=[[0,1,0],[1,1,1],[0,1,0]])
        for i in range(1, k+1):
            n += 1; reg[l == i] = n; arten[n] = a
    # kleine Stuecke iterativ an Nachbarregion mit laengster Grenze
    while True:
        fl = np.bincount(reg.ravel(), minlength=n+1)
        klein = [r for r in range(1, n+1) if 0 < fl[r] < minfl]
        if not klein: break
        r = min(klein, key=lambda r: fl[r])
        mm = reg == r
        dil = ndimage.binary_dilation(mm, structure=[[0,1,0],[1,1,1],[0,1,0]]) & ~mm
        nb = reg[dil]; nb = nb[nb > 0]
        if len(nb) == 0:
            arten[r] = arten[r]; fl[r] = 10**6; break
        ziel = np.bincount(nb).argmax()
        reg[mm] = ziel
    # Nummern verdichten
    ids = [r for r in np.unique(reg) if r > 0]
    neu = np.zeros_like(reg); na = {}
    for j, r in enumerate(ids, 1):
        neu[reg == r] = j; na[j] = arten[r]
    # Zusammenhang je Region pruefen (nach dem Anhaengen sollte es 4er-zusammenhaengend sein)
    for j in na:
        _, k = ndimage.label(neu == j, structure=[[0,1,0],[1,1,1],[0,1,0]])
        assert k == 1, (j, k)
    return neu, na

def regionen_bild(ziel, reg, arten, x0, y0, w, h, f, titel=None):
    lab, img, _ = lade()
    sub = img[y0:y0+h, x0:x0+w]
    rgb = np.stack([sub]*3, -1).astype(float)
    farbe = {1: (0, 0, 255), 2: (0, 200, 0), 3: (255, 60, 0), 4: (255, 255, 0)}
    R = reg[y0:y0+h, x0:x0+w]
    for j, a in arten.items():
        m = R == j
        rgb[m] = rgb[m]*0.6 + np.array(farbe[a])*0.4
    big = cv2.resize(rgb.astype(np.uint8), (w*f, h*f), interpolation=cv2.INTER_NEAREST)
    Rb = cv2.resize(R.astype(np.float64), (w*f, h*f), interpolation=cv2.INTER_NEAREST).astype(np.int64)
    Lb = cv2.resize(lab[y0:y0+h, x0:x0+w].astype(np.float64), (w*f, h*f), interpolation=cv2.INTER_NEAREST).astype(np.int64)
    big[grenzen(Rb)] = (255, 255, 0); big[grenzen(Lb)] = (255, 255, 255)
    im = Image.fromarray(big); d = ImageDraw.Draw(im); font = ImageFont.truetype(FONT, 13)
    for j in arten:
        m = R == j
        if m.sum() < 10: continue
        dt = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
        yy, xx = np.unravel_index(np.argmax(dt), dt.shape)
        d.text((xx*f, yy*f-6), str(j), fill=(255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
    for gx in range((x0//20+1)*20, x0+w, 20):
        d.text(((gx-x0)*f, 1), str(gx), fill=(0, 255, 0), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
    for gy in range((y0//20+1)*20, y0+h, 20):
        d.text((1, (gy-y0)*f), str(gy), fill=(0, 255, 0), font=font, stroke_width=1, stroke_fill=(0, 0, 0))
    if titel: d.text((4, h*f-18), titel, fill=(255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
    im.save(ziel, quality=90)

def zerlegen_ws(sid, t_hell, t_dunkel, sigma=1.2, minfl=40, ero=(2, 3, 2), minmark=12, bereich=None,
                extra_marken=None):
    """Wie zerlegen, aber Marken aus erodierten Grautonklassen und Wasserscheide auf dem Gradienten:
    Grenzen liegen auf der Bildkante, Saeume (Uebergaenge) fallen an die naechste Klasse.
    extra_marken: Liste (polygon, art) fuer Marken von Hand (z. B. Vorplatz)."""
    from skimage.segmentation import watershed
    lab, img, _ = lade()
    kern = np.zeros(lab.shape, bool); kern[KERN[1]:KERN[3], KERN[0]:KERN[2]] = True
    if bereich is not None:
        b = np.zeros(lab.shape, np.uint8); cv2.fillPoly(b, [np.array(bereich, np.int32)], 1); kern &= b.astype(bool)
    m = (lab == sid) & kern
    s = ndimage.gaussian_filter(img.astype(float), sigma)
    gr = np.hypot(ndimage.sobel(s, 0), ndimage.sobel(s, 1))
    art = np.where(s >= t_hell, 3, np.where(s <= t_dunkel, 1, 2)); art[~m] = 0
    mark = np.zeros(lab.shape, np.int32); arten = {}; n = 0
    st = [[0,1,0],[1,1,1],[0,1,0]]
    for a, r in zip((1, 2, 3), ero):
        e = ndimage.binary_erosion(art == a, structure=st, iterations=r) if r else (art == a)
        l, k = ndimage.label(e, structure=st)
        for i in range(1, k+1):
            if (l == i).sum() >= minmark:
                n += 1; mark[l == i] = n; arten[n] = a
    if extra_marken:
        for poly, a in extra_marken:
            pm = np.zeros(lab.shape, np.uint8); cv2.fillPoly(pm, [np.array(poly, np.int32)], 1)
            pm = pm.astype(bool) & m
            n += 1; mark[pm] = n; arten[n] = a
    reg = watershed(gr, markers=mark, mask=m, connectivity=1)
    # nicht erreichte Inseln (ohne Marke) an Nachbarn
    rest = m & (reg == 0)
    if rest.any():
        l, k = ndimage.label(rest, structure=st)
        for i in range(1, k+1):
            n += 1; reg[l == i] = n; arten[n] = int(np.bincount(art[l == i]).argmax())
    # Zusammenhang: zerfallene Regionen aufteilen
    for j in list(arten):
        l, k = ndimage.label(reg == j, structure=st)
        for i in range(2, k+1):
            n += 1; reg[l == i] = n; arten[n] = arten[j]
    # kleine an Nachbarn mit laengster Grenze
    while True:
        fl = np.bincount(reg.ravel(), minlength=n+1)
        klein = [r for r in arten if 0 < fl[r] < minfl]
        if not klein: break
        r = min(klein, key=lambda r: fl[r])
        mm = reg == r
        dil = ndimage.binary_dilation(mm, structure=st) & ~mm
        nb = reg[dil]; nb = nb[nb > 0]
        if len(nb) == 0: break
        reg[mm] = np.bincount(nb).argmax()
    ids = [r for r in np.unique(reg) if r > 0]
    neu = np.zeros_like(reg); na = {}
    for j, r in enumerate(ids, 1):
        neu[reg == r] = j; na[j] = arten[r]
    for j in na:
        _, k = ndimage.label(neu == j, structure=st)
        assert k == 1, (j, k)
    return neu, na

def gleichartige_vereinen(reg, arten):
    """Benachbarte Regionen gleicher Art zu einer."""
    st = [[0,1,0],[1,1,1],[0,1,0]]
    while True:
        done = True
        for j in sorted(arten):
            if not (reg == j).any(): continue
            mm = reg == j
            dil = ndimage.binary_dilation(mm, structure=st) & ~mm
            nb = set(np.unique(reg[dil]).tolist()) - {0}
            gleich = [k for k in nb if arten.get(k) == arten[j]]
            if gleich:
                for k in gleich: reg[reg == k] = j; del arten[k]
                done = False; break
        if done: break
    ids = sorted(arten); neu = np.zeros_like(reg); na = {}
    for i, j in enumerate(ids, 1):
        neu[reg == j] = i; na[i] = arten[j]
    return neu, na

def plan_schritte(sid, reg, behalten, klasse, lab=None):
    """polygon_zuweisen je Region ausser `behalten`; Reihenfolge: groesste gefuellte Flaeche zuerst."""
    if lab is None: lab, _, _ = lade()
    m = lab == sid
    schritte = []; ordnung = []
    for j in np.unique(reg):
        if j == 0 or j == behalten: continue
        polys = maske_zu_polygonen(reg == j)
        assert len(polys) == 1, (j, len(polys))
        fill = np.zeros(lab.shape, np.uint8); cv2.fillPoly(fill, [np.array(polys[0], np.int32)], 1)
        fill = fill.astype(bool)
        if (fill & ~m).any():
            raise ValueError(f"Region {j}: Polygon greift auf fremde Segmente ({int((fill & ~m).sum())} px)")
        ordnung.append((int(fill.sum()), int(j), polys[0]))
    ordnung.sort(reverse=True)
    for _, j, p in ordnung:
        schritte.append({"op": "polygon_zuweisen", "flaeche": p, "klasse": klasse, "_region": j})
    return schritte

def simulieren(schritte, regs, bearbeiter="sim"):
    """Fuehrt die Schritte auf einer Kopie aus (ohne Speichern) und ordnet Regionen -> IDs zu.
    regs: Liste von (sid, regionskarte). Prueft, dass jede Region genau eine ID traegt."""
    import sys as _s
    _s.path.insert(0, "C:/Users/Phil/Developement/Victor/landseg")
    from landseg.eingriff import Bearbeitung
    from landseg.kategorien import laden as kat_laden
    lab, _, _ = lade()
    seg = json.load(open(SEG, encoding="utf-8"))
    b = Bearbeitung(lab, seg, kat_laden("C:/Users/Phil/Developement/Victor/landseg/kategorien.json"), bearbeiter)
    for s in schritte:
        b.anwenden({k: v for k, v in s.items() if not k.startswith("_")})
    karte = b.karte
    zuordnung = {}
    for sid, reg in regs:
        for j in np.unique(reg):
            if j == 0: continue
            ids = np.unique(karte[reg == j])
            assert len(ids) == 1, (sid, j, ids)
            zuordnung[(sid, int(j))] = int(ids[0])
    return karte, zuordnung, b

VB = H0 + "/viertel/r0c1"
GROB_FARBE = {"Bebaut": (230, 60, 40), "Verkehrsfläche": (200, 200, 200), "Freifläche": (80, 200, 60),
              "Schatten": (40, 60, 200), "Gehölz": (0, 120, 0), "Unklar": (230, 0, 230)}

def _basis(vx, vy, f=3, rand=32):
    lab, img, _ = lade()
    x0, y0, w, h = vx - rand, vy - rand, 250 + 2*rand, 250 + 2*rand
    return lab, img, x0, y0, w, h, f

def _text(d, xy, t, font, farbe=(255, 255, 255)):
    d.text(xy, t, fill=farbe, font=font, stroke_width=2, stroke_fill=(0, 0, 0))

def ergebnisbilder(ordner, vx, vy, eintraege, alle_frei, punkte):
    """roh, umriss, maengel, vorschlag fuer ein Viertel (x vx..vx+249, y vy..vy+249), 3fach mit 32 px Umgebung.
    alle_frei: {id: grob-Name}; punkte: [(nr, x, y, text)]."""
    lab, img, x0, y0, w, h, f = _basis(vx, vy)
    sub = img[y0:y0+h, x0:x0+w]
    rgb = cv2.resize(np.stack([sub]*3, -1), (w*f, h*f), interpolation=cv2.INTER_NEAREST)
    L = lab[y0:y0+h, x0:x0+w]
    Lb = cv2.resize(L.astype(np.float64), (w*f, h*f), interpolation=cv2.INTER_NEAREST).astype(np.int64)
    g = grenzen(Lb)
    font = ImageFont.truetype(FONT, 13); fontk = ImageFont.truetype(FONT, 11)
    rahmen = [(vx-x0)*f, (vy-y0)*f, (vx+250-x0)*f, (vy+250-y0)*f]
    def fertig(arr, name, titel):
        im = Image.fromarray(arr); d = ImageDraw.Draw(im)
        d.rectangle(rahmen, outline=(0, 255, 255), width=2)
        _text(d, (6, h*f-20), titel, font)
        return im, d
    im, d = fertig(rgb.copy(), "roh", "roh: Viertel (cyan) mit 32 px Umgebung, 3fach")
    im.save(ordner + "/roh.jpg", quality=90)
    a = rgb.copy(); a[g] = (255, 230, 0)
    im, d = fertig(a, "umriss", "umriss: alle Segmentgrenzen nach dem Nachsegmentieren, Nummer = ID mod 100000")
    for sid in np.unique(L):
        m = L == sid
        if m.sum() < 12: continue
        dt = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
        yy, xx = np.unravel_index(np.argmax(dt), dt.shape)
        mine = int(sid) in alle_frei
        _text(d, (xx*f-8, yy*f-6), str(int(sid) % 100000), fontk, (255, 255, 255) if mine else (150, 150, 150))
    im.save(ordner + "/umriss.jpg", quality=90)
    # maengel
    a = rgb.copy(); a[g] = (255, 230, 0)
    im, d = fertig(a, "maengel", "")
    if punkte:
        for nr, px, py, t in punkte:
            cx, cy = (px-x0)*f, (py-y0)*f
            d.ellipse([cx-7, cy-7, cx+7, cy+7], fill=(255, 0, 0), outline=(255, 255, 255))
            _text(d, (cx-4 if nr < 10 else cx-7, cy-7), str(nr), fontk)
        # Legende unten anhaengen
        import textwrap
        zeilen = []
        for nr, _, _, t in punkte:
            zeilen += textwrap.wrap(f"{nr}: {t}", 150, subsequent_indent="    ")
        hoehe = 16*len(zeilen)+28
        leg = Image.new("RGB", (im.width, hoehe), (20, 20, 20)); dl = ImageDraw.Draw(leg)
        _text(dl, (6, 4), "Mängel (rote Punkte, Nummer):", font)
        for i, z in enumerate(zeilen):
            dl.text((6, 22+16*i), z, fill=(255, 255, 255), font=fontk)
        neu = Image.new("RGB", (im.width, im.height+hoehe)); neu.paste(im, (0, 0)); neu.paste(leg, (0, im.height)); im = neu
    else:
        _text(d, (rahmen[0]+10, rahmen[1]+10), "keine Mängel", font)
    im.save(ordner + "/maengel.jpg", quality=90)
    # vorschlag: Klassen (grob) als Farbe fuer eigene Segmente (nur im Kern)
    a = rgb.astype(float)
    kk = np.zeros(lab.shape, bool); kk[KERN[1]:KERN[3], KERN[0]:KERN[2]] = True
    kb = cv2.resize(kk[y0:y0+h, x0:x0+w].astype(np.uint8), (w*f, h*f), interpolation=cv2.INTER_NEAREST).astype(bool)
    for sid, gname in alle_frei.items():
        m = (Lb == sid) & kb
        if m.any():
            a[m] = a[m]*0.55 + np.array(GROB_FARBE.get(gname, (255, 255, 255)))*0.45
    a = a.astype(np.uint8); a[g] = (255, 230, 0)
    im, d = fertig(a, "vorschlag", "")
    for sid in alle_frei:
        m = L == sid
        if m.sum() < 12: continue
        dt = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
        yy, xx = np.unravel_index(np.argmax(dt), dt.shape)
        _text(d, (xx*f-8, yy*f-6), str(int(sid) % 100000), fontk)
    leg = Image.new("RGB", (im.width, 40), (20, 20, 20)); dl = ImageDraw.Draw(leg)
    _text(dl, (6, 2), "vorschlag: Grenzen wie gesetzt (nach Nachsegmentieren), Farbe = Klasse grob (Fassung B):", fontk)
    x = 6
    for nm, c in GROB_FARBE.items():
        dl.rectangle([x, 22, x+12, 34], fill=c); dl.text((x+16, 21), nm, fill=(255, 255, 255), font=fontk); x += 120
    neu = Image.new("RGB", (im.width, im.height+40)); neu.paste(im, (0, 0)); neu.paste(leg, (0, im.height))
    neu.save(ordner + "/vorschlag.jpg", quality=90)

def urteil_schreiben(ordner, viertel, eintraege, uebersicht, nah, naht, unsicher, nicht_geprueft, offen,
                     eingriffe, klassen_frei, vx, vy):
    """eintraege: dicts mit id, heute, was, urteil, frei (g,m,f), sicher, punkte [(art, text, x, y, fl)], bilder."""
    lab, img, seg = lade()
    segs = []; pliste = []; nr = 0; frei_grob = {}
    for e in eintraege:
        sid = e["id"]
        pk = []
        for art, text, px, py, fl in e.get("punkte", []):
            nr += 1
            pk.append({"nr": nr, "art": art, "text": text, "flaeche_px": fl})
            pliste.append((nr, px, py, f"{sid % 100000}: {text}"))
        g, m_, fn = e["frei"]
        frei_grob[sid] = g
        segs.append({"id": sid, "klasse_heute": seg[sid]["klasse"] if sid in seg else e.get("heute"),
                     "was_ist_es": e["was"], "urteil": e["urteil"], "klasse_vorschlag": None,
                     "klasse_frei": {"grob": g, "mittel": m_, "fein": fn}, "sicher": e["sicher"],
                     "punkte": pk, "bilder": e["bilder"]})
    ergebnisbilder(ordner, vx, vy, eintraege, frei_grob, pliste)
    eigene = [ordner + "/" + n for n in ("roh.jpg", "umriss.jpg", "maengel.jpg", "vorschlag.jpg")]
    out = {"teilkachel": "r0c1", "viertel": viertel, "bearbeiter": f"urt-b-r0c1-{viertel}",
           "bilder_angesehen": {"uebersicht": uebersicht + eigene, "nah": nah},
           "segmente": segs, "naht": naht, "unsicher": unsicher, "nicht_geprueft": nicht_geprueft,
           "offen": offen, "eingriffe": eingriffe, "klassen_frei": klassen_frei}
    json.dump(out, open(ordner + "/urteil.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return out

KLASSEN = {
 "Bebaut": ("grob", None, "Gebäude; in der Draufsicht scharf begrenzte Dachflächen mit Schattenwurf"),
 "Verkehrsfläche": ("grob", None, "helle, gleichmäßige, bandförmige oder offene Flächen für Verkehr"),
 "Freifläche": ("grob", None, "unbebaute Flächen an Häusern: Hof, Garten, Randstreifen; mittelgrau, unruhig"),
 "Gehölz": ("grob", None, "Bäume und Sträucher: körnig-fleckig, rundliche Kronen mit Eigenschatten"),
 "Schatten": ("grob", None, "sehr dunkle Fläche (Grauwert unter etwa 60), Boden darunter nicht erkennbar"),
 "Unklar": ("grob", None, "Grauton und Form erlauben auf dem Schwarz-Weiß-Scan keine Zuordnung"),
 "Gebäude": ("mittel", "Bebaut", "scharf begrenzte helle bis mittelgraue Dachfläche, Schatten auf der sonnenabgewandten Seite"),
 "Straße": ("mittel", "Verkehrsfläche", "breites helles durchgehendes Band zwischen den Häuserzeilen"),
 "Straßenrand": ("mittel", "Verkehrsfläche", "schmaler Streifen längs der Fahrbahn, Grauton etwas anders als die Fahrbahn"),
 "Platz": ("mittel", "Verkehrsfläche", "helle ebene Fläche ohne Schattenwurf, offen an die Straße angeschlossen"),
 "Hof oder Vorgarten": ("mittel", "Freifläche", "mittelgraue, leicht fleckige Fläche zwischen Hausgiebeln und Straße oder zwischen Häusern"),
 "Garten": ("mittel", "Freifläche", "mittel- bis dunkelgraue, fein gemusterte Fläche hinter den Häusern"),
 "Baum oder Strauch": ("mittel", "Gehölz", "rundliche dunkle Krone mit hellem Rand und eigenem Schatten"),
 "Schlagschatten": ("mittel", "Schatten", "dunkler Streifen auf der Schattenseite eines Gebäudes"),
 "Halbschatten": ("mittel", "Unklar", "mittelgrauer Streifen zwischen heller Dachseite und Schatten: Dachseite im Schatten oder Hof"),
 "Langhaus, Dach Sonnenseite": ("fein", "Gebäude", "langer schmaler heller Streifen quer zur Straße in der Reihe der Streckhöfe"),
 "Querbau an der Straße": ("fein", "Gebäude", "heller Block am Straßenende eines Langhauses, quer gestellt"),
 "Nebengebäude, helles Dach": ("fein", "Gebäude", "kurzer, sehr heller rechteckiger Block mit Schatten daneben"),
 "Wohnhaus, helles Dach": ("fein", "Gebäude", "breiter heller Block mit klarer Traufkante"),
 "Dorfstraße": ("fein", "Straße", "Fahrbahn der Ortsstraße, Belag auf dem Scan nicht bestimmbar"),
 "Randstreifen (Bankett oder Gehweg)": ("fein", "Straßenrand", "heller Streifen neben der Fahrbahn, durch feine Linie abgesetzt"),
 "Vorplatz": ("fein", "Platz", "heller ebener Platz vor den Häusern an der Straße"),
 "Hof oder Vorgarten": None,
 "Strauch am Straßenrand": ("fein", "Baum oder Strauch", "kleiner dunkler Fleck am Fahrbahnrand mit Schatten"),
 "Schatten zwischen Häusern": ("fein", "Schlagschatten", "sehr dunkles Band zwischen zwei Langhäusern"),
 "Dachseite oder Hof": ("fein", "Halbschatten", "mittelgraues Band neben einem hellen Dachstreifen"),
}
KLASSEN["Hof oder Vorgarten"] = ("mittel", "Freifläche", "mittelgraue, leicht fleckige Fläche zwischen Hausgiebeln und Straße oder zwischen Häusern")

def klassen_frei_liste(eintraege, extra=None):
    k = dict(KLASSEN); k.update(extra or {})
    namen = []
    for e in eintraege:
        for n in e["frei"]:
            if n not in namen: namen.append(n)
    # Eltern ergaenzen
    for n in list(namen):
        while n in k and k[n][1] and k[n][1] not in namen:
            namen.append(k[n][1]); n = k[n][1]
    return [{"name": n, "ebene": k[n][0], "eltern": k[n][1], "merkmal": k[n][2]} for n in namen if n in k]

def behalten_waehlen(sid, reg, arten, lab):
    """Region, die die ID behaelt: grenzt an alle Kontextteile (sonst an die meisten), sonst die groesste."""
    st = [[0,1,0],[1,1,1],[0,1,0]]
    kern = np.zeros(lab.shape, bool); kern[64:564, 64:564] = True
    ctx = (lab == sid) & ~kern
    l, k = ndimage.label(ctx, structure=st)
    fl = {j: int((reg == j).sum()) for j in arten}
    if k == 0:
        return max(fl, key=fl.get), 0
    best = None
    for j in arten:
        d = ndimage.binary_dilation(reg == j, structure=st)
        n = sum(1 for i in range(1, k+1) if (d & (l == i)).any())
        key = (n, fl[j])
        if best is None or key > best[0]: best = (key, j)
    return best[1], k - best[0][0]

def regionen_info(sid, reg, arten, zu, img):
    a = {}
    for j in sorted(arten):
        nid = zu[(sid, int(j))]
        m = reg == j; ys, xs = np.nonzero(m)
        dt = ndimage.distance_transform_edt(np.pad(m,1))[1:-1,1:-1]; yy, xx = np.unravel_index(np.argmax(dt), dt.shape)
        a[nid] = dict(von=sid, region=int(j), art=int(arten[j]), fl=int(m.sum()),
                      bbox=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())], punkt=[int(xx),int(yy)],
                      grau=round(float(img[m].mean())), naht_links=bool(xs.min()<=64), naht_rechts=bool(xs.max()>=563),
                      naht_unten=bool(ys.max()>=563))
    return a

def _vier_zus(m):
    _, k = ndimage.label(m, structure=[[0,1,0],[1,1,1],[0,1,0]])
    return k == 1

def plan_schritte2(sid, reg, behalten, klasse, lab=None):
    """Wie plan_schritte; Regionen, deren Aussenkontur fremde Segmente einschliesst, werden an einer
    Geraden durch das fremde Loch in zwei Polygone zerlegt; das zweite geht per Verweis (_ref) an die ID des ersten."""
    if lab is None: lab, _, _ = lade()
    m = lab == sid
    def fill_of(mask):
        polys = maske_zu_polygonen(mask)
        assert len(polys) == 1
        f = np.zeros(lab.shape, np.uint8); cv2.fillPoly(f, [np.array(polys[0], np.int32)], 1)
        return polys[0], f.astype(bool)
    teile = []
    for j in np.unique(reg):
        if j == 0 or j == behalten: continue
        rm = reg == j
        p, f = fill_of(rm)
        fremd = f & ~m
        if not fremd.any():
            teile.append((int(f.sum()), int(j), [p])); continue
        ys, xs = np.nonzero(fremd); cy, cx = int(ys.mean()), int(xs.mean())
        ok = None
        for achse in ("x", "y"):
            for off in (0, -3, 3, -6, 6):
                if achse == "x":
                    A = rm & (np.arange(lab.shape[1])[None, :] < cx + off); B = rm & ~A
                else:
                    A = rm & (np.arange(lab.shape[0])[:, None] < cy + off); B = rm & ~A
                if not (A.sum() >= 10 and B.sum() >= 10 and _vier_zus(A) and _vier_zus(B)): continue
                pa, fa = fill_of(A); pb, fb = fill_of(B)
                if len(pa) < 3 or len(pb) < 3: continue
                if (fa & ~m).any() or (fb & ~m).any(): continue
                ok = [pa, pb]; break
            if ok: break
        if not ok:
            raise ValueError(f"Region {j}: fremdes Loch, keine Zerlegung gefunden")
        teile.append((int(f.sum()), int(j), ok))
    teile.sort(reverse=True)
    schritte = []
    for _, j, polys in teile:
        i0 = len(schritte)
        schritte.append({"op": "polygon_zuweisen", "flaeche": polys[0], "klasse": klasse, "_region": j})
        for p in polys[1:]:
            schritte.append({"op": "polygon_zuweisen", "flaeche": p, "_ref": i0, "_region": j})
    return schritte

def simulieren2(schritte, regs, bearbeiter="sim"):
    """Wie simulieren, loest _ref auf (ID = Ziel des Schritts _ref) und gibt die aufgeloesten Schritte zurueck."""
    import sys as _s
    _s.path.insert(0, "C:/Users/Phil/Developement/Victor/landseg")
    from landseg.eingriff import Bearbeitung
    from landseg.kategorien import laden as kat_laden
    lab, _, _ = lade()
    seg = json.load(open(SEG, encoding="utf-8"))
    b = Bearbeitung(lab, seg, kat_laden("C:/Users/Phil/Developement/Victor/landseg/kategorien.json"), bearbeiter)
    ziele = []; fertig = []
    for s in schritte:
        t = {k: v for k, v in s.items() if not k.startswith("_")}
        if "_ref" in s:
            t["id"] = ziele[s["_ref"]]; t.pop("klasse", None)
        r = b.anwenden(t)
        ziele.append(r.get("ziel")); fertig.append(t)
    karte = b.karte; zuordnung = {}
    for sid, reg in regs:
        for j in np.unique(reg):
            if j == 0: continue
            ids = np.unique(karte[reg == j])
            assert len(ids) == 1, (sid, j, ids)
            zuordnung[(sid, int(j))] = int(ids[0])
    return karte, zuordnung, fertig

KLASSEN.update({
 "Randstreifen": ("mittel", "Freifläche", "schmaler unbefestigter Streifen zwischen Fahrbahn und Häusern"),
 "Randstreifen, dunkel (Bewuchs?)": ("fein", "Randstreifen", "dunkelgrauer Fleck am Fahrbahnrand, wohl Gras oder Gestrüpp"),
 "Weg": ("mittel", "Verkehrsfläche", "schmales helles Band, schmaler als eine Straße"),
 "Gasse": ("fein", "Weg", "schmaler heller Durchgang quer durch einen Häuserblock, Kante auf einer Seite scharf"),
 "Hofweg": ("fein", "Weg", "schmaler heller Streifen innerhalb der Höfe"),
 "Halle oder Scheune, helles Dach": ("fein", "Gebäude", "sehr großes, sehr helles Dach mit klaren Kanten"),
 "Garten, dunkel (Bäume oder Schatten)": ("fein", "Garten", "dunkle fleckige Fläche am Ende der Grundstücke, Bäume und Schatten ineinander"),
 "Garten, fein gemustert": ("fein", "Garten", "große gleichmäßig fein gemusterte Fläche, wohl Beete oder Obstbäume"),
 "Hecke": ("fein", "Baum oder Strauch", "schmales dunkles Band längs einer Grundstücksgrenze"),
 "Gebüsch": ("fein", "Baum oder Strauch", "dunkle, fleckige, unregelmäßige Fläche"),
 "Baum": ("fein", "Baum oder Strauch", "einzelne dunkle rundliche Krone"),
 "Schatten oder Baumgruppe": ("fein", "Schlagschatten", "große, sehr dunkle Fläche ohne Binnenmuster"),
 "Unklar": ("mittel", "Unklar", "Fleck ohne eindeutiges Merkmal"),
 "heller Fleck im Hof": ("fein", "Unklar", "kleiner heller Fleck in einer Hoffläche"),
 "heller runder Fleck": ("fein", "Unklar", "heller rundlicher Fleck ohne Schatten"),
 "Gehölz am Straßenrand": ("fein", "Baum oder Strauch", "dunkle Kronen längs einer Straße"),
 "Baumreihe": ("fein", "Baum oder Strauch", "Reihe dunkler rundlicher Kronen mit Schatten längs eines Weges"),
 "Acker oder Wiese": ("mittel", "Freifläche", "große gleichmäßige Fläche ohne Gebäude"),
})

def klassen_frei_liste(eintraege, extra=None):
    k = dict(KLASSEN); k.update(extra or {})
    namen = []
    for e in eintraege:
        for n in e["frei"]:
            if n not in namen: namen.append(n)
    for n in list(namen):
        while n in k and k[n][1] and k[n][1] not in namen:
            namen.append(k[n][1]); n = k[n][1]
    fehlt = [n for n in namen if n not in k]
    if fehlt: raise ValueError(f"Klassen ohne Beschreibung: {fehlt}")
    return [{"name": n, "ebene": k[n][0], "eltern": k[n][1], "merkmal": k[n][2]} for n in namen]

GEB = ("Bebaut", "Gebäude", "Langhaus, Dach Sonnenseite")
SCH = ("Schatten", "Schlagschatten", "Schatten zwischen Häusern")
HALB = ("Unklar", "Halbschatten", "Dachseite oder Hof")
HOF = ("Freifläche", "Hof oder Vorgarten", "Hof oder Vorgarten")
STR = ("Verkehrsfläche", "Straße", "Dorfstraße")
RAND = ("Verkehrsfläche", "Straßenrand", "Randstreifen (Bankett oder Gehweg)")

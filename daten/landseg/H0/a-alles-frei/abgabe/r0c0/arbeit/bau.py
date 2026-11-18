# Baut aus spec.py die Label-Karte (628 x 628) und Kontrollbilder. Aufruf: python -B bau.py [--snap] [--ausgabe]
import sys, json, importlib
import numpy as np
import cv2
import scipy.ndimage as ndi
from PIL import Image, ImageDraw, ImageFont

ARBEIT = 'C:/Users/Phil/Developement/Victor/daten/landseg/H0/a-alles-frei/abgabe/r0c0/arbeit/'
ABGABE = 'C:/Users/Phil/Developement/Victor/daten/landseg/H0/a-alles-frei/abgabe/r0c0/'
BILD = 'C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c0.png'
H = W = 628
KERN = (64, 64, 564, 564)
S = 8  # Unterabtastung für Rasterung

sys.path.insert(0, ARBEIT)
import spec
import spec2

img = np.array(Image.open(BILD)).astype(float)
if img.ndim == 3:
    img = img[..., 0]


def maske(geo):
    m = np.zeros((H, W), np.uint8)
    art = geo[0]
    if art == 'poly':
        pts = np.round((np.array(geo[1]) + 0.0) * S).astype(np.int32)  # Bildpunktmitte bei x+0.5 -> grob
        cv2.fillPoly(m, [pts], 1, lineType=cv2.LINE_8, shift=3)
    elif art in ('band', 'bandvar'):
        pts = np.round(np.array(geo[1]) * S).astype(np.int32)
        w = int(round(geo[2]))
        cv2.polylines(m, [pts], False, 1, thickness=w, lineType=cv2.LINE_8, shift=3)
    elif art == 'clip':
        m = maske(geo[1]) & maske(geo[2])
    return m.astype(bool)


SCHUETZEN = {'feld_s1', 'feld_s2', 'feld_s3', 'feld_s4', 'feld_s5', 'acker_nw', 'brache_sw', 'mauer_a', 'zaun_a', 'hecke_links', 'hecke_feld', 'feldweg_oben', 'baeume_c', 'rand_c', 'weg_f', 'weg_g', 'b4_weg', 'str_a', 'bankett_a_l', 'rand_a_r', 'str_c', 'str_d', 'str_d2', 'str_e', 'str_h', 'str_c_sued'}


def einrasten(karte):
    """Grenzen auf Bildkanten ziehen: je Superpixel (SLIC) die Mehrheit der gezeichneten Elemente.
    Geschützte Elemente (Linien, Straßen) bleiben bildpunktgleich und wachsen nicht."""
    from skimage.segmentation import slic
    g = ndi.gaussian_filter(img, 1.0)
    g = (g - g.min()) / (g.max() - g.min())
    sp = slic(g, n_segments=H * W // 18, compactness=0.08, channel_axis=None, start_label=1, enforce_connectivity=True)
    schutz = np.zeros(len(spec.E) + 1, bool)
    for i, e in enumerate(spec.E, start=1):
        schutz[i] = e['key'] in SCHUETZEN
    geschuetzt = schutz[karte]
    neu = karte.copy()
    frei = ~geschuetzt
    lab = sp[frei]; val = karte[frei]
    # Mehrheit je Superpixel (nur über freie Bildpunkte)
    order = np.lexsort((val, lab))
    lab_s, val_s = lab[order], val[order]
    paare, cnt = np.unique(np.stack([lab_s, val_s]), axis=1, return_counts=True)
    best = {}
    for (l, v), c in zip(paare.T, cnt):
        if l not in best or c > best[l][1]:
            best[l] = (v, c)
    mehr = np.zeros(sp.max() + 1, np.int32)
    for l, (v, c) in best.items():
        mehr[l] = v
    neu[frei] = mehr[sp[frei]]
    return neu


def baue(snap=False):
    karte = np.zeros((H, W), np.int32)
    for i, e in enumerate(spec.E, start=1):
        karte[maske(e['geo'])] = i
    # Lücken: nächstes Element
    if (karte == 0).any():
        idx = ndi.distance_transform_edt(karte == 0, return_distances=False, return_indices=True)
        karte = karte[idx[0], idx[1]]
    if snap:
        karte = einrasten(karte)
    # Zusammenhang: je Element Teile; kleine Teile (< 25 px) an den Nachbarn mit längster Grenze
    seg = np.zeros((H, W), np.int32)
    meta = []
    nid = 0
    for i, e in enumerate(spec.E, start=1):
        lab, n = ndi.label(karte == i)
        if n == 0:
            continue
        groessen = ndi.sum(np.ones_like(lab), lab, range(1, n + 1))
        reihen = np.argsort(-groessen)
        for rang, k in enumerate(reihen):
            nid += 1
            seg[lab == k + 1] = nid
            meta.append(dict(elem=i - 1, teil=rang, flaeche=int(groessen[k])))
    # kleine Teile verschmelzen
    while True:
        ids, cnt = np.unique(seg, return_counts=True)
        klein = [(c, s) for s, c in zip(ids, cnt) if c < 25 or (meta[s - 1]['teil'] > 0 and c < 80)]
        if not klein:
            break
        klein.sort()
        c, s = klein[0]
        m = seg == s
        rand = ndi.binary_dilation(m, np.ones((3, 3), bool)) & ~m
        nb, nc = np.unique(seg[rand], return_counts=True)
        if len(nb) == 0:
            break
        seg[m] = nb[np.argmax(nc)]
    # neu nummerieren
    ids = np.unique(seg)
    neu = np.zeros(seg.max() + 1, np.uint32)
    neu[ids] = np.arange(1, len(ids) + 1)
    out = neu[seg]
    infos = []
    for alt in ids:
        md = meta[alt - 1]
        e = spec.E[md['elem']]
        ys, xs = np.nonzero(seg == alt)
        im_kern = bool(((xs >= KERN[0]) & (xs < KERN[2]) & (ys >= KERN[1]) & (ys < KERN[3])).any())
        infos.append(dict(id=int(neu[alt]), key=e['key'], klasse=e['klasse'], name=e['name'] + (f' (Teil {md["teil"] + 1})' if md['teil'] else ''),
                          sicher=e['sicher'], grund=e['grund'], im_kern=im_kern, flaeche=int(len(xs)),
                          cx=float(xs.mean()), cy=float(ys.mean())))
    return out, infos


def farben():
    kat = json.load(open(ABGABE + 'kategorien-teil.json', encoding='utf-8'))
    return {k['code']: tuple(int(k['color'][i:i + 2], 16) for i in (1, 3, 5)) for k in kat['classes']}


def ueberlagerung(karte, infos, pfad, x0=0, y0=0, w=W, h=H, s=2, alpha=0.35, nummern=True, legende=False):
    fb = farben()
    sub = img[y0:y0 + h, x0:x0 + w]
    lo, hi = np.percentile(sub, 0.5), np.percentile(sub, 99.5)
    g = np.clip((sub - lo) / (hi - lo) * 255, 0, 255)
    rgb = np.stack([g] * 3, -1)
    L = karte[y0:y0 + h, x0:x0 + w]
    kl = {d['id']: d['klasse'] for d in infos}
    col = np.zeros_like(rgb)
    for d in infos:
        col[L == d['id']] = fb.get(d['klasse'], (255, 0, 255))
    rgb = rgb * (1 - alpha) + col * alpha
    big = np.kron(L, np.ones((s, s), L.dtype))
    rgb = np.kron(rgb, np.ones((s, s, 1)))
    e = np.zeros(big.shape, bool)
    e[:, 1:] |= big[:, 1:] != big[:, :-1]
    e[1:, :] |= big[1:, :] != big[:-1, :]
    rgb[e] = (255, 255, 0)
    im = Image.fromarray(rgb.astype(np.uint8))
    d = ImageDraw.Draw(im)
    # Kern
    kx0, ky0, kx1, ky1 = [(v - o) * s for v, o in zip(KERN, (x0, y0, x0, y0))]
    d.rectangle([kx0, ky0, kx1 - 1, ky1 - 1], outline=(0, 255, 255), width=2)
    f = ImageFont.truetype('arial.ttf', 12)
    if nummern:
        for di in infos:
            m = L == di['id']
            if m.sum() < 30:
                continue
            dt = ndi.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
            yy, xx = np.unravel_index(np.argmax(dt), dt.shape)
            t = str(di['id'])
            d.text((xx * s - 6, yy * s - 6), t, fill=(255, 40, 40), font=f, stroke_width=2, stroke_fill=(255, 255, 255))
    im.save(pfad, quality=90)


if __name__ == '__main__':
    karte, infos = baue('--snap' in sys.argv)
    print('snap', '--snap' in sys.argv)
    np.save(ARBEIT + 'karte.npy', karte)
    json.dump(infos, open(ARBEIT + 'infos.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('Segmente', len(infos), 'im Kern', sum(d['im_kern'] for d in infos))
    ueberlagerung(karte, infos, ARBEIT + 'ov_ganz.jpg')
    for (x, y) in [(0, 0), (300, 0), (0, 300), (300, 300)]:
        ueberlagerung(karte, infos, ARBEIT + f'ov_{x}_{y}.jpg', x, y, 328, 328, 3)

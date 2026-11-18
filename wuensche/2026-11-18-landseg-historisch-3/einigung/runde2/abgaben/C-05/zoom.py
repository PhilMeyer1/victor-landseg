import sys
import numpy as np
from PIL import Image, ImageDraw
import tifffile

D = r"C:/Users/Phil/Developement/Victor/daten/landseg/H0"
OUT = r"C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde2/abgaben/C-05"
KONTEXT = {"r0c0": (-64, -64), "r0c1": (436, -64), "r1c0": (-64, 436), "r1c1": (436, 436)}
KERN = {"r0c0": (0, 0), "r0c1": (500, 0), "r1c0": (0, 500), "r1c1": (500, 500)}

def main():
    name = sys.argv[1]
    x0, y0, x1, y1, f = map(int, sys.argv[2:7])
    segs = sys.argv[7:]  # tk:id
    img = np.array(Image.open(D + "/H0.png").convert("L"))
    crop = img[y0:y1, x0:x1]
    # global id map over crop (cores only)
    gid = np.zeros(crop.shape, dtype=np.int64)
    for tk, (kx, ky) in KERN.items():
        lab = tifffile.imread(D + f"/c-feste-liste/{tk}/labels.tif")
        ox, oy = KONTEXT[tk]
        for yy in range(y0, y1):
            if not (ky <= yy < ky + 500):
                continue
            for xx in range(x0, x1):
                if kx <= xx < kx + 500:
                    gid[yy - y0, xx - x0] = lab[yy - oy, xx - ox] + (0 if True else 0)
    big = Image.fromarray(crop).resize(((x1 - x0) * f, (y1 - y0) * f), Image.NEAREST).convert("RGB")
    over = big.copy()
    dr = ImageDraw.Draw(over)
    cols = [(0, 255, 255), (255, 0, 255), (255, 200, 0), (0, 255, 0)]
    # all segment boundaries thin grey-white
    H, W = gid.shape
    for yy in range(H):
        for xx in range(W):
            v = gid[yy, xx]
            if xx + 1 < W and gid[yy, xx + 1] != v:
                dr.line([((xx + 1) * f, yy * f), ((xx + 1) * f, (yy + 1) * f)], fill=(255, 255, 255))
            if yy + 1 < H and gid[yy + 1, xx] != v:
                dr.line([(xx * f, (yy + 1) * f), ((xx + 1) * f, (yy + 1) * f)], fill=(255, 255, 255))
    for i, s in enumerate(segs):
        tk, sid = s.split(":")
        sid = int(sid)
        kx, ky = KERN[tk]
        m = gid == sid
        # restrict to core of tk
        yy, xx = np.nonzero(m)
        c = cols[i % len(cols)]
        for a, b in zip(yy, xx):
            gx, gy = b + x0, a + y0
            if kx <= gx < kx + 500 and ky <= gy < ky + 500:
                if (a + b) % 2 == 0:
                    dr.rectangle([b * f + 1, a * f + 1, b * f + f - 2, a * f + f - 2], outline=c)
    # core lines
    for v in (500,):
        if x0 <= v < x1:
            dr.line([((v - x0) * f, 0), ((v - x0) * f, H * f)], fill=(255, 255, 0))
        if y0 <= v < y1:
            dr.line([(0, (v - y0) * f), (W * f, (v - y0) * f)], fill=(255, 255, 0))
    for v in (250, 750):
        if x0 <= v < x1:
            dr.line([((v - x0) * f, 0), ((v - x0) * f, H * f)], fill=(255, 120, 0))
        if y0 <= v < y1:
            dr.line([(0, (v - y0) * f), (W * f, (v - y0) * f)], fill=(255, 120, 0))
    out = Image.new("RGB", (big.width * 2 + 10, big.height), (20, 20, 20))
    out.paste(big, (0, 0))
    out.paste(over, (big.width + 10, 0))
    if max(out.size) > 2000:
        s = 2000 / max(out.size)
        out = out.resize((int(out.width * s), int(out.height * s)), Image.LANCZOS)
    out.save(OUT + f"/{name}.jpg", quality=90)
    # print ids present
    u, c = np.unique(gid, return_counts=True)
    print(dict(zip(u.tolist(), c.tolist())))

main()

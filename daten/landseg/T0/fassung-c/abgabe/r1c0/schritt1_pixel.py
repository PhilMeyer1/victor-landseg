"""Schritt 1: Pixel-Klassifikation (Random Forest auf Farbe/Textur) aus von Hand gewählten Trainingsrechtecken.

Grobklassen je Bildpunkt: 0 Gras, 1 beige (trocken/Boden), 2 Gehölz, 3 Bau/Garten-Hartfläche.
Ergebnis: arbeit/pixel.npy (Klasse), arbeit/proba.npy, arbeit/merkmale.npy und ein Kontrollbild.
"""
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from skimage import color
from sklearn.ensemble import RandomForestClassifier

HIER = Path(__file__).parent
A = HIER / "arbeit"
BILD = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/teilkacheln/r1c0.png"

img = np.array(Image.open(BILD).convert("RGB")).astype(np.float64) / 255.0
lab = color.rgb2lab(img)
L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
r, g, bl = img[..., 0], img[..., 1], img[..., 2]
exg = 2 * g - r - bl


def std(x, s):
    m = ndi.gaussian_filter(x, s)
    m2 = ndi.gaussian_filter(x * x, s)
    return np.sqrt(np.maximum(m2 - m * m, 0))


merk = []
for s in (1, 2, 4):
    merk += [ndi.gaussian_filter(L, s), ndi.gaussian_filter(a, s), ndi.gaussian_filter(b, s),
             ndi.gaussian_filter(exg, s)]
merk += [std(L, 1.5), std(L, 3), std(L, 6)]
X = np.stack(merk, -1)
H, W = L.shape

train = {
    0: [(20, 20, 90, 70), (105, 55, 170, 100), (60, 120, 140, 170), (130, 235, 170, 265),
        (240, 15, 300, 60), (520, 20, 600, 60), (60, 100, 120, 115), (470, 160, 495, 190),
        (525, 150, 560, 175)],
    1: [(2, 162, 16, 188), (178, 210, 195, 222), (97, 283, 113, 294), (221, 247, 231, 262),
        (181, 222, 192, 232)],
    2: [(20, 480, 90, 540), (420, 400, 500, 460), (380, 40, 440, 90), (100, 520, 200, 600),
        (170, 410, 240, 470), (480, 240, 560, 300), (200, 120, 230, 160), (330, 500, 450, 600),
        (300, 150, 330, 250), (120, 5, 180, 30), (555, 330, 595, 395), (470, 600, 540, 625),
        (360, 330, 420, 370), (60, 300, 90, 320), (225, 330, 250, 350)],
    3: [(590, 428, 618, 446), (600, 455, 618, 478), (590, 490, 605, 500), (608, 600, 622, 615)],
}
xs, ys = [], []
for k, rects in train.items():
    for x0, y0, x1, y1 in rects:
        xs.append(X[y0:y1, x0:x1].reshape(-1, X.shape[-1]))
        ys.append(np.full((y1 - y0) * (x1 - x0), k))
xs = np.concatenate(xs)
ys = np.concatenate(ys)
rf = RandomForestClassifier(n_estimators=120, max_depth=14, n_jobs=4, random_state=0,
                            class_weight="balanced")
rf.fit(xs, ys)
proba = rf.predict_proba(X.reshape(-1, X.shape[-1])).reshape(H, W, -1)
pix = proba.argmax(-1)
np.save(A / "pixel.npy", pix)
np.save(A / "proba.npy", proba.astype(np.float32))
np.save(A / "L.npy", L.astype(np.float32))

farben = np.array([[120, 220, 80], [240, 200, 140], [0, 90, 30], [255, 0, 255]], np.uint8)
over = (0.5 * (img * 255) + 0.5 * farben[pix]).astype(np.uint8)
Image.fromarray(over).resize((1256, 1256), Image.NEAREST).save(A / "pixel.jpg", quality=88)
print({k: int((pix == k).sum()) for k in range(4)})

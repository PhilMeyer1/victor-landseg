import sys, json
import numpy as np
sys.path.insert(0, 'C:/Users/Phil/Developement/Victor/landseg')
from landseg.dateien import lese_labels
from PIL import Image
L = lese_labels('C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/vorstufe/r0c0/labels.tif')
S = json.load(open('C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/vorstufe/r0c0/segmente.json', encoding='utf-8'))
img = np.asarray(Image.open('C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/teilkacheln/r0c0.png').convert('RGB')).astype(float)
print(L.shape, L.min(), L.max(), len(np.unique(L)))
seg = {s['id']: s for s in S['segmente']}
for i in np.unique(L):
    m = L == i
    ys, xs = np.nonzero(m)
    s = seg.get(int(i), {})
    col = img[m].mean(0)
    print(i, m.sum(), 'cx=%d cy=%d bb=%d,%d-%d,%d' % (xs.mean(), ys.mean(), xs.min(), ys.min(), xs.max(), ys.max()), s.get('klasse'), s.get('instanz', {}).get('text', s.get('herkunft')), s.get('im_kern'), 'rgb=%d,%d,%d' % tuple(col))

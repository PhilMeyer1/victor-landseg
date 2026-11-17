import sys, numpy as np, cv2
sys.path.insert(0, 'C:/Users/Phil/Developement/Victor/landseg')
from landseg.dateien import lese_labels
from PIL import Image
L = lese_labels('C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/vorstufe/r0c0/labels.tif')
img = np.asarray(Image.open('C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/teilkacheln/r0c0.png').convert('RGB')).astype(np.float32)
g = img.mean(2)
dark = (g < 62).astype(np.float32)
k = 21
fr = cv2.blur(dark, (k, k))
mu = cv2.blur(g, (k, k)); sd = np.sqrt(np.maximum(cv2.blur(g*g, (k, k)) - mu*mu, 0))
m = np.isin(L, [100056, 100166])
vis = img.copy()
heat = np.clip(fr*2.5, 0, 1)
col = np.stack([heat*255, (1-heat)*255, np.zeros_like(heat)], 2)
vis[m] = vis[m]*0.4 + col[m]*0.6
for y in range(0, 628, 50):
    cv2.line(vis, (0, y), (627, y), (255, 255, 255), 1); cv2.putText(vis, str(y), (2, y+12), 0, 0.4, (255,255,255), 1)
for x in range(0, 628, 50):
    cv2.line(vis, (x, 0), (x, 627), (255, 255, 255), 1); cv2.putText(vis, str(x), (x+2, 624), 0, 0.4, (255,255,255), 1)
vis = cv2.resize(vis.astype(np.uint8), (1256, 1256), interpolation=cv2.INTER_NEAREST)
Image.fromarray(vis).save('arbeit/textur.jpg', quality=90)
g2 = img.astype(np.uint8).copy()
for y in range(0, 628, 25):
    cv2.line(g2, (0, y), (627, y), (255, 255, 255) if y%50==0 else (180,180,180), 1)
for x in range(0, 628, 25):
    cv2.line(g2, (x, 0), (x, 627), (255, 255, 255) if x%50==0 else (180,180,180), 1)
g2 = cv2.resize(g2, (1256, 1256), interpolation=cv2.INTER_CUBIC)
for y in range(0, 628, 50):
    for x in range(0, 628, 50):
        cv2.putText(g2, f'{x},{y}', (x*2+3, y*2+14), 0, 0.4, (255,255,0), 1)
Image.fromarray(g2).save('arbeit/gitter.jpg', quality=90)

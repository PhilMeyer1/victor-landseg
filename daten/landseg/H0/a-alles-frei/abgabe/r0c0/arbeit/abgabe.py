# Schreibt labels.tif, segmente.json und ergebnis.jpg aus karte.npy / infos.json (nach bau.py --snap)
import json
import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont
import bau

A = bau.ABGABE
karte = np.load(bau.ARBEIT + 'karte.npy').astype(np.uint32)
infos = json.load(open(bau.ARBEIT + 'infos.json', encoding='utf-8'))
kat = json.load(open(A + 'kategorien-teil.json', encoding='utf-8'))
klassen = {k['code']: k for k in kat['classes']}

tifffile.imwrite(A + 'labels.tif', karte, compression='zlib', photometric='minisblack')

segs = []
for d in infos:
    grob = d['klasse'].split('.')[0]
    e = dict(id=d['id'], klasse=d['klasse'], grob=grob, name=d['name'], im_kern=d['im_kern'],
             sicher=bool(d['sicher']), flaeche=d['flaeche'])
    if d['grund']:
        e['grund'] = d['grund']
    segs.append(e)

offen = [
    'Acker gegen Grünland: alle Feldstreifen (3.1) und der Acker nordwestlich von Straße A sind nur nach Streifenform als Acker gedeutet; das Farbbild oder ein Bild aus anderer Jahreszeit entscheidet.',
    'Hofstellen 1.3 (Zeile A, Block B3, Block B4): Dach und Hof sind auf dem Scan nicht getrennt; im Farbbild (rote/graue Dächer gegen Erdhof) lassen sie sich in 1.1.1 und 1.2 teilen.',
    'Dunkle Flächen 9.1/9.2 an den Häusern: Schlagschatten oder dunkle Dachhänge bzw. Baumgruppen; ein Bild mit anderem Sonnenstand oder Farbe entscheidet.',
    'Garten-/Grünflächen 1.4 (Dreieck zwischen den Straßen, Fläche nördlich der Kreuzung): Garten, Wiese oder kleiner Acker nicht trennbar.',
    'Anger 5.1: Belag (Gras, festgetretene Erde) offen; die hellen Kleinobjekte 9.3 können Schuppen oder Haufen sein.',
    'Grenzen der Feldstreifen 3/4/5 sind schwach (helle Raine) und zum Teil geschätzt gezogen.',
    'Naht: Straßen A, C, D, E, Weg F, die Hofzeile A, Block B2/B3/B4 und die Feldstreifen laufen über die Kerngrenzen; die Nachbarkacheln müssen dieselben Linien treffen.',
]
nicht = [
    'Kontextrand (außerhalb des Kerns 64..564) nur grob gezeichnet, nicht fein geprüft.',
    'Einzelne Dachhänge innerhalb der Hofstellen 1.3 nicht weiter zerlegt (Auflösung und Unschärfe des Scans reichen nicht für sichere Grenzen).',
]
json.dump({'schema': 'landseg-segmente/1', 'teilkachel': 'r0c0', 'fassung': 'A (Alles frei)', 'segmente': segs,
           'verlauf': [{'bearbeiter': 'agent-a-r0c0', 'schritt': 'eigene Zeichnung (Polygone in gedrehten Rahmen) + Einrasten an Bildkanten (Superpixel), siehe arbeitsweise.md'}],
           'offen': offen, 'nicht_geprueft': nicht},
          open(A + 'segmente.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# Ergebnisbild mit Legende
bau.ueberlagerung(karte, infos, bau.ARBEIT + 'erg_bild.jpg', 0, 0, 628, 628, 2, alpha=0.38, nummern=True)
im = Image.open(bau.ARBEIT + 'erg_bild.jpg')
Wl = 700
out = Image.new('RGB', (im.width + Wl, im.height), (255, 255, 255))
out.paste(im, (0, 0))
d = ImageDraw.Draw(out)
f = ImageFont.truetype('arial.ttf', 16)
fb = ImageFont.truetype('arialbd.ttf', 17)
x0 = im.width + 14
d.text((x0, 10), 'H0 · Teilkachel r0c0 · Fassung A „Alles frei“', fill=(0, 0, 0), font=fb)
d.text((x0, 34), 'Kern umrandet (türkis), Grenzen gelb, Nummern = Segment-ID', fill=(60, 60, 60), font=f)
y = 66
from collections import Counter
zahl = Counter(s['klasse'] for s in segs)
unsicher = Counter(s['klasse'] for s in segs if not s['sicher'])
for k in kat['classes']:
    code = k['code']
    if code not in zahl and not any(c.startswith(code + '.') for c in zahl):
        continue
    einzug = 18 * (k['level'] - 1)
    col = tuple(int(k['color'][i:i + 2], 16) for i in (1, 3, 5))
    d.rectangle([x0 + einzug, y + 2, x0 + einzug + 18, y + 18], fill=col, outline=(0, 0, 0))
    t = f"{code} {k['name']}"
    if code in zahl:
        t += f"  ({zahl[code]}, davon {unsicher[code]} unsicher)"
    d.text((x0 + einzug + 26, y), t, fill=(0, 0, 0), font=f if code in zahl else fb)
    y += 26
d.text((x0, y + 10), f'{len(segs)} Segmente, {sum(s["im_kern"] for s in segs)} im Kern;', fill=(0, 0, 0), font=f)
d.text((x0, y + 32), f'{sum(not s["sicher"] for s in segs)} mit sicher: false', fill=(0, 0, 0), font=f)
d.text((x0, y + 64), 'Schwarz-Weiß-Scan 1968, ca. 0,45 m je Bildpunkt', fill=(60, 60, 60), font=f)
out.save(A + 'ergebnis.jpg', quality=90)
print(out.size, len(segs), sum(s['im_kern'] for s in segs), sum(not s['sicher'] for s in segs))
print(sorted(zahl.items()))

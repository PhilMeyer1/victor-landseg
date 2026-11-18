p='einzel.py'
s=open(p,encoding='utf-8').read()
s=s.replace('''    h, w = roh.shape
    groß =''','''    h, w = roh.shape
    S = max(2, min(8, 1500 // max(h, w)))
    groß =''')
alt_a=s.index('    pw, ph = w * S, h * S')
alt_b=s.index('    if n in ent:')
neu='''    pw, ph = w * S, h * S
    kopf = 70
    stapeln = pw > 600
    if stapeln:
        orte = [(0, kopf + i * (ph + 30)) for i in range(3)]
        ges = Image.new("RGB", (max(pw, 900), kopf + 3 * (ph + 30) + 10), "white")
    else:
        orte = [(i * (pw + 20), kopf) for i in range(3)]
        ges = Image.new("RGB", (max(3 * pw + 40, 900), ph + kopf + 50), "white")
    for t, (ox, oy) in zip(tafeln, orte):
        ges.paste(t, (ox, oy))
    d = ImageDraw.Draw(ges)
    d.text((5, 5), f"Verstoß {n}: Naht {v['naht']}, Segmente {v['ids'][0]} | {v['ids'][1]}, "
                   f"{v['laenge']} Bildpunkte ab x {ax}, y {ay}", fill="black", font=FONT)
    d.text((5, 27), f"Ausschnitt x {x0}..{x1 - 1}, y {y0}..{y1 - 1}, {S}-fach; cyan = Kerngrenze, gelb = Strecke",
           fill="black", font=FONT)
    for (ox, oy), z in zip(orte, ("Bild (Kontrast verstärkt)", "Grenzen vorher", "Grenzen nachher")):
        d.text((ox + 5, oy - 22), z, fill="black", font=FONT)
    ph = orte[-1][1] + ph - kopf
'''
s=s[:alt_a]+neu+s[alt_b:]
open(p,'w',encoding='utf-8').write(s)

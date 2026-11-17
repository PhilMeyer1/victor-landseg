from pathlib import Path
p=Path("schritt2_segmente.py"); s=p.read_text(encoding="utf-8")
old_codes='''CODES = ["1.1.1", "1.1.2", "1.2", "1.3", "1.4", "1.5", "2.1", "2.2", "3.1", "3.2", "3.3", "4.1",
         "5.1", "5.2"]'''
new_codes='''CODES = ["1.1.1", "1.1.2", "1.1.3", "1.2", "1.3", "1.4", "2.1", "2.2", "2.3", "3.1", "3.2", "4.1",
         "5.1", "5.2"]'''
assert old_codes in s; s=s.replace(old_codes,new_codes)
s=s.replace('k[ACKER & ~G & (beige | bau | gras)] = C["3.3"]','k[ACKER & ~G & (beige | bau | gras)] = C["3.2"]')
s=s.replace('D = holz & (Ls < 16.5) & ~N & frei','D = holz & (Ls < 16.5) & frei')
s=s.replace('''k[wald & ~N] = C["1.1.1"]
k[wald & N] = C["1.2"]
''','''k[wald] = C["1.1.1"]
''')
s=s.replace('''    if a < 150:
        k[m] = C["1.5"]
    elif a <= 2600 and fuell.sum() / (hh * ww) > 0.45:
        k[m] = C["1.3"]
    else:
        k[m] = C["1.4"]''','''    if a < 150:
        k[m] = C["1.4"]
    elif a <= 2600 and fuell.sum() / (hh * ww) > 0.45:
        k[m] = C["1.2"]
    else:
        k[m] = C["1.3"]''')
s=s.replace('''    k[m] = C["3.1"] if L[m].mean() < 55 else C["3.2"]''','''    k[m] = C["3.1"]''')
s=s.replace('''N = zone([(235, 0), (505, 0), (508, 60), (472, 110), (456, 200), (470, 260), (455, 322), (400, 345),
          (338, 348), (328, 300), (252, 250), (238, 150)])  # lockeres Gehölzmosaik
''','')
s=s.replace("binary_opening(","opening(").replace("binary_closing(","closing(").replace("from skimage.morphology import disk, opening, closing","")
s=s.replace("from skimage.morphology import disk, binary_opening, binary_closing","from skimage.morphology import disk, opening, closing")
p.write_text(s,encoding="utf-8")

"""Belege AK7/AK8 aus den Daten einer erzeugten Seite: je Bild und Fassung die Klasse „Garten“ (Code, Farbe,
Eltern), Abstand ihrer Farbe zu allen anderen der Liste (CIELAB) und die Zahl der Segmente im Kern mit Garten
(samt Unterklassen). Aufruf: python seite_garten.py <seite.html> [<seite2.html> …]"""
import json, re, sys
from pathlib import Path

def lab(h):
    def lin(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(int(h[i:i + 2], 16)) for i in (1, 3, 5))
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047; y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    return 116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z))

def suche(o, pfad=""):
    """findet Listen von Klassen (Dicts mit code/name) und Segmentlisten in beliebiger Tiefe"""
    if isinstance(o, dict):
        for k, v in o.items():
            yield from suche(v, f"{pfad}.{k}")
    elif isinstance(o, list):
        if o and isinstance(o[0], dict):
            yield pfad, o
        for i, v in enumerate(o[:50] if not (o and isinstance(o[0], dict)) else []):
            yield from suche(v, f"{pfad}[{i}]")

for html in sys.argv[1:]:
    t = Path(html).read_text(encoding="utf-8")
    a = t.index("window.DATEN = ") + len("window.DATEN = ")
    e = re.compile(r";\r?\n</script>").search(t, a).start()
    daten = json.loads(t[a:e])
    print("==", html, "schema", daten.get("schema"), "Schlüssel", list(daten)[:12])
    bilder = daten.get("bilder") or [daten]
    for b in bilder:
        for f in b["fassungen"]:
            if not f.get("vorhanden", True):
                print(" ", b.get("kennung"), f.get("kennung"), "ohne Daten"); continue
            kl = f.get("kategorien") or f.get("klassen") or daten.get("kategorien")
            if isinstance(kl, dict):
                kl = kl.get("klassen") or kl.get("classes") or list(kl.values())
            garten = [k for k in kl if re.fullmatch(r"Garten(\s*\(.*\))?", str(k.get("name", "")).strip())]
            g = garten[0] if garten else None
            farben = [k.get("farbe") or k.get("color") for k in kl]
            gf = g and (g.get("farbe") or g.get("color"))
            gl = gf and lab(gf[:7])
            dmin = gl and min(sum((p - q) ** 2 for p, q in zip(gl, lab(c[:7]))) ** 0.5 for c in farben if c and c[:7] != gf[:7])
            eltern = g and next((k for k in kl if k.get("code") == (g.get("eltern") or g.get("parent"))), None)
            n = 0
            for tk in (f.get("teilkacheln") or {}).values():
                for s in tk.get("segmente", []):
                    c = str(s.get("klasse", ""))
                    if g and (c == g["code"] or c.startswith(g["code"] + ".")) and s.get("im_kern", True):
                        n += 1
            print(f"  {b.get('kennung')} {f.get('kennung')}: Garten {g and g['code']} „{g and g['name'][:30]}“ Farbe {gf} "
                  f"(kleinster Abstand {dmin and round(dmin, 1)}), unter „{eltern and eltern.get('name')}“, Segmente im Kern {n}")

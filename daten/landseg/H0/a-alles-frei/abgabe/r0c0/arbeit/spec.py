# Eigene Zeichnung der Teilkachel r0c0 (H0), Fassung A. Koordinaten in Bildpunkten der Teilkachel (628 x 628).
# Jedes Element: (schluessel, klasse, name, sicher, grund, geometrie). Spätere Elemente überdecken frühere.
import numpy as np

def frame(o, t, n):
    o = np.array(o, float); t = np.array(t, float); n = np.array(n, float)
    def f(pts):
        return [tuple(o + u * t + v * n) for u, v in pts]
    return f

def rect(u0, u1, v0, v1):
    return [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]

FA = frame((193, 0), (-0.622, 0.783), (0.783, 0.622))      # Häuserzeile an Straße A (u entlang Straße, v quer)
FB2 = frame((400, 15), (0.644, 0.765), (-0.765, 0.644))    # Block B2 an Straße D
FB3 = frame((480, 0), (0.866, 0.5), (-0.5, 0.866))         # Block B3 rechts von Weg F
FF = frame((100, 380), (0.909, -0.417), (0.417, 0.909))    # Feldstreifen (u entlang, v quer)
F4 = frame((440, 240), (0.885, -0.466), (0.466, 0.885))    # Block B4 rechts von Straße C

def P(pts):
    return ('poly', [tuple(map(float, p)) for p in pts])

def B(pts, w):
    return ('band', [tuple(map(float, p)) for p in pts], w)

# Mittellinie Straße C (heller Fahrbahnstreifen), aus Zeilenprofilen
C_MITTE = [(402, 182), (401, 212), (405, 228), (418, 244), (425, 260), (432, 275), (440, 290), (448, 302),
           (459, 320), (475, 350), (485, 370), (493, 400), (504, 420), (512, 440), (521, 460), (534, 480),
           (543, 500), (557, 520), (569, 540), (578, 560), (585, 575)]

def versatz(linie, dx):
    return [(x + dx, y) for x, y in linie]

E = []
def add(k, kl, name, sicher, grund, geo):
    E.append(dict(key=k, klasse=kl, name=name, sicher=sicher, grund=grund, geo=geo))

U_ = 'Hofstelle: Dach und Hof auf dem Scan nicht trennbar'

# ---------------- Grundflächen ----------------
add('acker_nw', '3.1', 'Acker nordwestlich Straße A', False,
    'Ackerstreifen wahrscheinlich (feine Längsstreifen), Grünland auf SW nicht ausschließbar',
    P(FA([(-80, -200), (460, -200), (460, -14), (-80, -14)])))
add('anger', '5.1', 'Anger / offene Freifläche hinter den Höfen', False,
    'unregelmäßig helle Fläche mit Trittspuren; Belag (Gras, Erde) auf SW nicht bestimmbar',
    P([(60, 330), (200, 190), (330, 40), (420, 40), (420, 300), (330, 310), (200, 330), (110, 360), (60, 360)]))
add('brache_sw', '5.2', 'Brache / Weide am Ortsrand', False,
    'helle, fleckige Fläche mit Büschen; Weide, Brache oder Gartenland auf SW nicht trennbar',
    P([(-5, 300), (85, 338), (113, 348), (118, 400), (125, 412), (140, 420), (147, 440), (140, 458), (120, 466),
       (100, 470), (84, 478), (88, 520), (95, 560), (101, 600), (105, 640), (-5, 640)]))

# Garten- und Grünflächen im Ort
add('garten_nord', '1.4', 'Garten-/Grünfläche zwischen Straße D und Weg F', False,
    'gleichmäßig dunkelgraue Fläche; Garten, Wiese oder kleiner Acker nicht trennbar',
    P([(405, -5), (565, -5), (505, 100), (490, 100)]))
add('kontext_oben', '1.3', 'Hofstellen oberhalb Block B2 (nur Kontext)', False, U_, P([(330, -5), (412, -5), (400, 15), (352, 56), (330, 40)]))
add('garten_dreieck', '1.4', 'Dreiecksfläche zwischen Straßen E, D und Block B4', False,
    'gleichmäßig dunkelgraue Fläche; Garten, Wiese oder Acker nicht trennbar',
    P([(405, 190), (455, 135), (498, 100), (540, 135), (575, 163), (563, 173), (430, 243), (412, 236)]))

# Blöcke als Grundfläche (Hofstellen ungetrennt)
PLOTS = [-80, -18, 21, 56, 88, 124, 158, 194, 228, 262, 296, 330, 440]
for i, (a, b) in enumerate(zip(PLOTS, PLOTS[1:])):
    add(f'hof_a{i}', '1.3', f'Hofstelle Zeile A, Parzelle {i}', False, U_, P(FA(rect(a, b, 24, 129 if b < 400 else 90))))
add('mauer_a', '1.5', 'hintere Grenzlinie der Hofzeile A (Mauer oder Hecke, mit Schatten)', False,
    'durchgehende dunkle Linie; Mauer, Zaun oder Hecke nicht unterscheidbar', P(FA(rect(-80, 334, 129, 136))))
add('zaun_a', '1.5', 'Grenzlinie zwischen Parzellen 10 und 11', False, 'schmale dunkle Linie, Mauer oder Zaun',
    P(FA(rect(327, 333, 28, 129))))
add('b2_hof', '1.2', 'Hofraum Block B2', False, 'helle bis mittelgraue offene Fläche zwischen den Häusern; Schuppen nicht auszuschließen',
    P(FB2(rect(-6, 118, -4, 106))))
add('b3_hof', '1.3', 'Hofstellen Block B3 (Rand)', False, U_, P(FB3(rect(68, 220, -60, 72))))
add('b4_hof', '1.3', 'Hofstellen Block B4', False, U_,
    P([(x + 3, y) for x, y in C_MITTE if y >= 243] + [(640, 640), (640, 200), (563, 173), (430, 243)]))

# Feldregion (wird in Streifen geteilt): links Hecke, oben Feldweg, rechts Baumreihe an Straße C, unten Weg H
FELD_OBEN = FF([(14, -28), (60, -33), (120, -38), (200, -40), (228, -35), (232, 18), (330, 22)])
FELD_RECHTS = versatz(C_MITTE[6:], -30)
FELD_LINKS = [(113, 348), (118, 400), (125, 412), (140, 420), (147, 440), (140, 458), (120, 466), (100, 470),
              (84, 478), (88, 520), (95, 560), (101, 600), (105, 640)]
FELD = FELD_OBEN + [p for p in FELD_RECHTS if p[1] > FELD_OBEN[-1][1]] + [(600, 640)] + FELD_LINKS[::-1]
def strip(v0a, v0b, v1a, v1b, u0=-150, u1=360):
    return FF([(u0, v0a), (u1, v0b), (u1, v1b), (u0, v1a)])
add('feld_s1', '3.1', 'Ackerstreifen 1 (oben, heller)', False, 'Streifenparzelle hell; Acker sehr wahrscheinlich, Fruchtart offen',
    ('clip', P(FELD), P(strip(-80, -80, 33, 25))))
add('feld_s2', '3.1', 'Ackerstreifen 2 (breit, dunkel)', False, 'Streifenparzelle; Acker oder Grünland auf SW nicht sicher',
    ('clip', P(FELD), P(strip(33, 25, 152, 148))))
add('feld_s3', '3.1', 'Ackerstreifen 3', False, 'schwache Streifengrenze (heller Rain), Lage geschätzt',
    ('clip', P(FELD), P(strip(152, 148, 196, 193))))
add('feld_s4', '3.1', 'Ackerstreifen 4 (unten links)', False, 'Streifenparzelle; Grenze zu Streifen 3 schwach',
    ('clip', P(FELD), P(strip(196, 193, 400, 400, -150, 205))))
add('feld_s5', '3.1', 'Ackerparzelle 5 (unten rechts, umrandet)', False, 'Parzelle mit dunklem Rand; Acker wahrscheinlich',
    ('clip', P(FELD), P(strip(193, 193, 400, 400, 205, 360))))

# ---------------- Wege und Straßen ----------------
add('bankett_a_l', '2.3', 'Straßenrand links von Straße A', False, 'heller Grünstreifen mit Graben; Bewuchs nicht bestimmbar',
    P(FA(rect(-80, 460, -14, 0))))
add('rand_a_r', '2.3', 'Straßenrand / Vorplatz rechts von Straße A', False, 'mittelgrauer Streifen vor den Höfen; Belag offen',
    P(FA(rect(-80, 460, 12, 24))))
add('str_a', '2.1', 'Straße A (Hauptstraße nach Nordosten)', True, '', P(FA(rect(-80, 460, 0, 12))))
add('feldweg_oben', '2.2', 'Feldweg am oberen Feldrand', False, 'heller Streifen; Weg oder Rain',
    P(FF([(14, -50), (215, -50), (215, -40), (14, -38)])))
add('hecke_feld', '4.2', 'Gebüschreihe am oberen Feldrand', False, 'Reihe dunkler Flecken; Büsche oder Schatten',
    P(FF([(70, -41), (190, -43), (190, -37), (70, -35)])))
add('hecke_links', '4.2', 'Hecke / Feldrain am linken Feldrand', False, 'dunkle Linie mit Büschen; Hecke oder Graben',
    B(FELD_LINKS, 5))
add('str_d', '2.1', 'Straße D (nordwestlicher Teil)', True, '', P(FB2(rect(-60, 125, -21, -4))))
add('weg_f', '2.2', 'Gasse F nach Norden', False, 'heller Streifen, schmaler als die Straßen; Belag offen',
    B([(503, 98), (558, -5)], 13))
add('str_d2', '2.1', 'Straße D (südöstlicher Teil)', True, '', B([(492, 98), (540, 135), (575, 163), (640, 212)], 16))
add('str_e', '2.1', 'Straße E (Verbindung zur Straße C)', True, '', B([(498, 100), (455, 135), (420, 165), (402, 185)], 16))
add('weg_g', '2.2', 'Weg G am Block B2', False, 'heller Streifen entlang Block B2; Weg oder Platzrand', B([(398, 182), (370, 150), (335, 108)], 11))
add('baeume_c', '4.2', 'Baumreihe links an Straße C', False, 'Reihe dunkler runder Flecken; Bäume wahrscheinlich, teils Schatten',
    ('bandvar', versatz(C_MITTE[3:20], -26), 9))
add('rand_c', '2.3', 'Randstreifen links der Straße C', False, 'matter heller Streifen neben der Fahrbahn; Gehweg oder Bankett',
    ('bandvar', versatz(C_MITTE[3:19], -14), 10))
add('str_c', '2.1', 'Straße C (nach Süden)', True, '', ('bandvar', C_MITTE, 15))
add('str_h', '2.1', 'Weg/Straße H am Südrand', False, 'heller Streifen; Straße oder breiter Feldweg', B([(585, 575), (540, 597), (500, 617), (470, 640)], 15))
add('str_c_sued', '2.1', 'Straße C nach Süden (Rand)', False, 'nur im Kontextrand', B([(585, 575), (640, 640)], 15))

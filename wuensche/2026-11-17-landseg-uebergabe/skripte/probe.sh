#!/usr/bin/env bash
# Probe für AK8: Befehle der Anleitung („Einen neuen Ausschnitt rechnen") an einem Probeausschnitt, ohne GPU-Teil.
# Läuft im Übergabe-Projekt; schreibt nur in den Probeordner $PR.
set -u
P=C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0
PR=C:/Users/Phil/AppData/Local/Temp/claude/27e54e3b8399faf6/a2bf01d3-627c-4b06-8b57-51f25ab5229e/scratchpad/probe
PY=C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe
BILD=C:/Users/Phil/Developement/Victor/daten/luftbilder/orthofoto-aktuell/0009626524_100_Orthophoto_aktuell_5236-56.tif
rm -rf "$PR"; mkdir -p "$PR"
cd "$P"
echo "== 1 kacheln"; $PY -B -m landseg kacheln --bild "$BILD" --x 2000 --y 2400 --breite 1000 --hoehe 1000 --kern 500 --rand 64 --name T0 --ziel "$PR/T0"; echo "rc=$?"
for t in r0c0 r0c1 r1c0 r1c1; do cmp -s "$PR/T0/teilkacheln/$t.png" "T0/teilkacheln/$t.png" && echo "$t.png bytegleich" || echo "$t.png ANDERS"; done
cmp -s "$PR/T0/T0.png" T0/T0.png && echo "T0.png bytegleich" || echo "T0.png ANDERS"
echo "== 2 vorstufe (GPU) übersprungen; Ausgang: Karte von C aus dem Projekt"
for t in r0c0 r0c1 r1c0 r1c1; do mkdir -p "$PR/T0/c-feste-liste/$t"; cp "T0/c-feste-liste/$t/labels.tif" "T0/c-feste-liste/$t/segmente.json" "$PR/T0/c-feste-liste/$t/"; done
echo "== 3 pruefen"; $PY -B -m landseg pruefen --labels "$PR/T0/c-feste-liste/r0c0/labels.tif" --segmente "$PR/T0/c-feste-liste/r0c0/segmente.json" --bild "$PR/T0/teilkacheln/r0c0.png"; echo "rc=$?"
echo "== 4 eingriff klasse"; $PY -B -m landseg eingriff --labels "$PR/T0/c-feste-liste/r0c0/labels.tif" --segmente "$PR/T0/c-feste-liste/r0c0/segmente.json" --bearbeiter probe klasse --id 100010 --klasse 1.1.2; echo "rc=$?"
cat > "$PR/T0/c-feste-liste/zusammentragen.json" <<'EOF'
{"schema": "landseg-zusammentragen/1", "manifest": "../manifest.json",
 "einheiten": [{"teilkachel": "r0c0", "labels": "r0c0/labels.tif", "segmente": "r0c0/segmente.json", "runde": 0, "name": "c-r0c0"},
               {"teilkachel": "r0c1", "labels": "r0c1/labels.tif", "segmente": "r0c1/segmente.json", "runde": 0, "name": "c-r0c1"},
               {"teilkachel": "r1c0", "labels": "r1c0/labels.tif", "segmente": "r1c0/segmente.json", "runde": 0, "name": "c-r1c0"},
               {"teilkachel": "r1c1", "labels": "r1c1/labels.tif", "segmente": "r1c1/segmente.json", "runde": 0, "name": "c-r1c1"}],
 "ziel": "zusammen"}
EOF
echo "== 5 zusammentragen C"; $PY -B -m landseg zusammentragen --datei "$PR/T0/c-feste-liste/zusammentragen.json" | tail -3; echo "rc=$?"
echo "== 6 naht C"; $PY -B -m landseg naht --manifest "$PR/T0/manifest.json" --labels "$PR/T0/c-feste-liste/zusammen/labels.tif" | tail -2; echo "rc=$?"
echo "== 7 seite"; $PY -B -m landseg seite --manifest "$PR/T0/manifest.json" --ziel "$PR/T0/T0.html" | tail -2; echo "rc=$?"
echo "== 8 A im Projekt nachrechnen (in den Probeordner)"; $PY -B -m landseg zusammentragen --datei T0/a-alles-frei/zusammentragen.json --kategorien T0/a-alles-frei/kategorien-a.json --ziel "$PR/a-zusammen" | tail -2
cmp -s "$PR/a-zusammen/labels.tif" T0/a-alles-frei/zusammen/labels.tif && echo "A labels.tif bytegleich" || $PY -c "import tifffile,sys;a=tifffile.imread(sys.argv[1]);b=tifffile.imread(sys.argv[2]);print('A labels gleich:',(a==b).all())" "$PR/a-zusammen/labels.tif" T0/a-alles-frei/zusammen/labels.tif
$PY -B -m landseg naht --manifest T0/manifest.json --labels T0/a-alles-frei/zusammen/labels.tif | tail -1
$PY -B -m landseg pruefen --labels T0/a-alles-frei/zusammen/labels.tif --segmente T0/a-alles-frei/zusammen/segmente.json --kategorien T0/a-alles-frei/kategorien-a.json --form 1000x1000 | tail -1
echo "== Werkzeuge"; $PY -B -m landseg --help >/dev/null; echo "help rc=$?"; $PY -I tools/pruefe_kategorien.py T0/a-alles-frei/kategorien-a.json | tail -1; $PY -I tools/pruefe_kategorien.py T0/b-kategorien-frei/kategorien-b.json | tail -1; $PY -I tools/pruefe_kategorien.py T0/c-feste-liste/kategorien-c.json | tail -1
git -C "$P" status --short 2>/dev/null | head -3

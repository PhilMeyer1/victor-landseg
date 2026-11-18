#!/usr/bin/env bash
# Befehlsfolge für den Ausschnitt H0 (Teil 3: grobe Vorstufe, Kopie aus Teil 2; kopien mit Gegenprobe-Kopie c-feste-liste/gegenprobe/r0c0)
# (Scan 1968, x 1500, y 2000, 1000 × 1000, Kern 500, Rand 64).
# Aufruf: bash schritte_h0.sh <schritt>   (kacheln | vorstufe | pruefen | kopien | pruefen-kopien)
# Im Repo-Ordner landseg, ohne -I (sonst findet Python das Paket nicht).
set -u
BASIS="C:/Users/Phil/Developement/Victor"
REPO="$BASIS/landseg"
PY="C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe"
D="$BASIS/wuensche/2026-11-18-landseg-historisch-3"
H0="$BASIS/daten/landseg/H0"
SCAN="$BASIS/daten/luftbilder/historisch/1968105_0014_0228.tif"
KONFIG="$D/vorstufe-h0-grob.json"
TK="r0c0 r0c1 r1c0 r1c1"
cd "$REPO" || exit 2

case "${1:-}" in
  kacheln)
    "$PY" -B -m landseg kacheln --bild "$SCAN" --x 1500 --y 2000 --breite 1000 --hoehe 1000 \
      --kern 500 --rand 64 --name H0 --ziel "$H0"
    ;;
  vorstufe)
    "$PY" -B -m landseg vorstufe --manifest "$H0/manifest.json" --konfig "$KONFIG" "${@:2}"
    ;;
  pruefen)
    rc=0
    for t in $TK; do
      echo "== vorstufe $t"
      "$PY" -B -m landseg pruefen --labels "$H0/vorstufe/$t/labels.tif" \
        --segmente "$H0/vorstufe/$t/segmente.json" --bild "$H0/teilkacheln/$t.png" || rc=1
    done
    exit $rc
    ;;
  kopien)
    for f in b-kategorien-frei c-feste-liste; do
      for t in $TK; do
        mkdir -p "$H0/$f/$t"
        cp -p "$H0/vorstufe/$t/labels.tif" "$H0/vorstufe/$t/segmente.json" "$H0/vorstufe/$t/kandidaten.json" "$H0/$f/$t/"
      done
    done
    mkdir -p "$H0/c-feste-liste/gegenprobe/r0c0"
    cp -p "$H0/vorstufe/r0c0/labels.tif" "$H0/vorstufe/r0c0/segmente.json" "$H0/vorstufe/r0c0/kandidaten.json" "$H0/c-feste-liste/gegenprobe/r0c0/"
    ;;
  pruefen-kopien)
    rc=0
    for f in b-kategorien-frei c-feste-liste; do
      for t in $TK; do
        echo "== $f $t"
        "$PY" -B -m landseg pruefen --labels "$H0/$f/$t/labels.tif" \
          --segmente "$H0/$f/$t/segmente.json" --bild "$H0/teilkacheln/$t.png" || rc=1
      done
    done
    echo "== c-feste-liste gegenprobe r0c0"
    "$PY" -B -m landseg pruefen --labels "$H0/c-feste-liste/gegenprobe/r0c0/labels.tif"       --segmente "$H0/c-feste-liste/gegenprobe/r0c0/segmente.json" --bild "$H0/teilkacheln/r0c0.png" || rc=1
    exit $rc
    ;;
  *)
    echo "Schritt fehlt: kacheln | vorstufe | pruefen | kopien | pruefen-kopien" >&2
    exit 2
    ;;
esac

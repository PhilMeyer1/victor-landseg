from pathlib import Path
p = Path("C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/skripte/schritte_h0.sh")
t = p.read_text(encoding="utf-8")
alt_k = '''        cp -p "$H0/vorstufe/$t/labels.tif" "$H0/vorstufe/$t/segmente.json" "$H0/vorstufe/$t/kandidaten.json" "$H0/$f/$t/"
      done
    done
'''
neu_k = alt_k + '''    mkdir -p "$H0/c-feste-liste/gegenprobe/r0c0"
    cp -p "$H0/vorstufe/r0c0/labels.tif" "$H0/vorstufe/r0c0/segmente.json" "$H0/vorstufe/r0c0/kandidaten.json" "$H0/c-feste-liste/gegenprobe/r0c0/"
'''
assert alt_k in t
t = t.replace(alt_k, neu_k)
alt_p = '''          --segmente "$H0/$f/$t/segmente.json" --bild "$H0/teilkacheln/$t.png" || rc=1
      done
    done
'''
neu_p = alt_p + '''    echo "== c-feste-liste gegenprobe r0c0"
    "$PY" -B -m landseg pruefen --labels "$H0/c-feste-liste/gegenprobe/r0c0/labels.tif" \
      --segmente "$H0/c-feste-liste/gegenprobe/r0c0/segmente.json" --bild "$H0/teilkacheln/r0c0.png" || rc=1
'''
assert alt_p in t
t = t.replace(alt_p, neu_p)
t = t.replace("# Befehlsfolge für den Ausschnitt H0", "# Befehlsfolge für den Ausschnitt H0 (Teil 3: grobe Vorstufe, Kopie aus Teil 2; kopien mit Gegenprobe-Kopie c-feste-liste/gegenprobe/r0c0)\n#")
p.write_text(t, encoding="utf-8", newline="\n")

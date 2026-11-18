"""farben.py seg.json out.json : Klassenfarben-Datei für overlay.py"""
import json, sys
F = {"1": "#bd2835", "1.1": "#eb21ed", "1.1.1": "#e61382", "1.1.2": "#d370f3", "1.1.3": "#ff8c00",
     "1.2": "#f584cd", "1.2.1": "#f0f0a0", "1.2.2": "#d4aee0", "1.2.3": "#ffd27f",
     "1.3": "#3aa0ff", "1.3.1": "#7fc8ff",
     "2": "#9dd161", "2.1": "#3de723", "2.2": "#1d7239", "2.2.1": "#15bc58", "2.2.2": "#0c6c34", "2.3": "#a1df19",
     "9": "#808080", "9.1": "#202060"}
seg = json.load(open(sys.argv[1], encoding="utf-8"))
json.dump({"farben": F, "seg": {k: v["klasse"] for k, v in seg.items()}}, open(sys.argv[2], "w"))

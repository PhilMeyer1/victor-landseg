"""Zählt die Zahlen für die Anleitung aus den Dateien des Übergabe-Projekts."""
import json
import sys
from collections import Counter
from pathlib import Path

T = Path(sys.argv[1]) / "T0"
TK = ["r0c0", "r0c1", "r1c0", "r1c1"]
lies = lambda p: json.loads(Path(p).read_text(encoding="utf-8"))
erg = {}
for f, o, liste in (("A", "a-alles-frei", "kategorien-a.json"), ("B", "b-kategorien-frei", "kategorien-b.json"),
                    ("C", "c-feste-liste", "kategorien-c.json")):
    z = {"tk": {}}
    kat = lies(T / o / liste)
    z["liste"] = {"counts": kat.get("counts"), "klassen": len(kat["classes"]),
                  "je_ebene": dict(Counter(k.get("level", 1) for k in kat["classes"]))}
    klassen_genutzt = set()
    for t in TK:
        seg = lies(T / o / t / "segmente.json")["segmente"]
        kern = [s for s in seg if s.get("im_kern")]
        e = {"segmente": len(seg), "im_kern": len(kern),
             "kern_sicher_nein": sum(1 for s in kern if s.get("sicher") == "nein")}
        klassen_genutzt |= {s.get("klasse") for s in kern}
        u = T / o / "urteil" / t / "urteil.json"
        if u.exists():
            d = lies(u)
            e["urteil"] = {"kernsegmente": d.get("kernsegmente"), "eintraege": d.get("eintraege"), **{
                k: v for k, v in (d.get("zahlen") or {}).items() if k != "je_viertel"}}
            e["urteil_eintraege_nicht_sauber"] = sum(1 for s in d.get("segmente", []) if s.get("sauber") is False)
            pk = Counter()
            for s in d.get("segmente", []):
                for p in s.get("punkte", []) or []:
                    pk[p.get("art") if isinstance(p, dict) else "text"] += 1
            e["punkte_arten"] = dict(pk)
        z["tk"][t] = e
    z["summe"] = {k: sum(z["tk"][t][k] for t in TK) for k in ("segmente", "im_kern", "kern_sicher_nein")}
    if all("urteil" in z["tk"][t] for t in TK):
        z["summe"]["nicht_sauber"] = sum(z["tk"][t]["urteil"].get("nicht_sauber", 0) for t in TK)
        z["summe"]["urteil_sicher_nein"] = sum(z["tk"][t]["urteil"].get("sicher_nein", 0) for t in TK)
        z["summe"]["eintraege"] = sum(z["tk"][t]["urteil"].get("eintraege", 0) for t in TK)
    z["klassen_im_kern_genutzt"] = len(klassen_genutzt)
    erg[f] = z
zs = lies(T / "a-alles-frei" / "zusammen" / "segmente.json")
nj = lies(T / "a-alles-frei" / "zusammen" / "naht.json")
erg["A"]["zusammen"] = {"segmente": len(zs["segmente"]), "naht_keys": list(nj)[:10],
                        "naht_verstoesse": len(nj.get("verstoesse", [])) if isinstance(nj, dict) else None}
erg["beispiel_urteil_segment"] = lies(T / "c-feste-liste" / "urteil" / "r0c0" / "urteil.json")["segmente"][0]
erg["urteil_kopf_c"] = {k: v for k, v in lies(T / "c-feste-liste" / "urteil" / "r0c0" / "urteil.json").items()
                        if k not in ("segmente", "viertel")}
erg["urteil_kopf_b"] = {k: v for k, v in lies(T / "b-kategorien-frei" / "urteil" / "r0c0" / "urteil.json").items()
                        if k not in ("segmente", "viertel")}
erg["segment_a"] = lies(T / "a-alles-frei" / "r0c0" / "segmente.json")["segmente"][0]
erg["segment_c"] = lies(T / "c-feste-liste" / "r0c0" / "segmente.json")["segmente"][0]
print(json.dumps(erg, ensure_ascii=False, indent=1))

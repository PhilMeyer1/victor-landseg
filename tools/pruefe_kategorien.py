"""Validate the category list kategorien.json (standard library only).

Usage: python -I tools/pruefe_kategorien.py kategorien.json

Checks: required fields, unique codes, code/level/parent consistency, every parent present,
level-1 codes 0..6, valid and pairwise distinct colours with a minimum CIELAB distance,
bw values, mapping lists, counts per level and leaves, rules G1..G5 / U1..U5, status notes.
Prints the counts and "ok" (exit 0) or the list of errors (exit 1).
"""

import json
import math
import re
import sys

MIN_DELTA_E = 10.0  # CIE76 distance every pair of class colours must keep
BW_VALUES = {"ja", "eing.", "nein"}
MAPPING_KEYS = ("corine", "clc_plus", "flair", "dkm", "bericht48")
CLASS_FIELDS = ("code", "name", "parent", "level", "color", "bw", "mappings")
RULE_FIELDS = ("id", "kind", "text", "source")
CODE_RE = re.compile(r"^\d+(\.\d+)*$")
COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
RULE_RE = re.compile(r"^([GU])(\d+)$")


def to_lab(hex_color):
    def lin(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (lin(int(hex_color[i:i + 2], 16)) for i in (1, 3, 5))
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116

    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def check(doc):
    errors = []
    classes = doc.get("classes")
    if not isinstance(classes, list) or not classes:
        return ["'classes' missing or empty"], {}

    codes = {}
    for i, k in enumerate(classes):
        where = f"class #{i} ({k.get('code', '?')})"
        missing = [f for f in CLASS_FIELDS if f not in k or (k[f] in ("", None) and f != "parent")]
        if missing:
            errors.append(f"{where}: missing fields {missing}")
            continue
        code = k["code"]
        if not isinstance(code, str) or not CODE_RE.match(code):
            errors.append(f"{where}: invalid code")
            continue
        if code in codes:
            errors.append(f"{where}: duplicate code")
        codes[code] = k
        level = code.count(".") + 1
        if k["level"] != level:
            errors.append(f"{where}: level {k['level']} does not match code (expected {level})")
        expected_parent = None if level == 1 else code.rsplit(".", 1)[0]
        if k["parent"] != expected_parent:
            errors.append(f"{where}: parent {k['parent']!r} does not match code (expected {expected_parent!r})")
        if not isinstance(k["name"], str) or not k["name"].strip():
            errors.append(f"{where}: empty name")
        if not isinstance(k["color"], str) or not COLOR_RE.match(k["color"]):
            errors.append(f"{where}: invalid colour {k['color']!r}")
        if k["bw"] not in BW_VALUES:
            errors.append(f"{where}: bw {k['bw']!r} not in {sorted(BW_VALUES)}")
        m = k["mappings"]
        if not isinstance(m, dict):
            errors.append(f"{where}: mappings is not an object")
        else:
            for key in MAPPING_KEYS:
                if not isinstance(m.get(key), list) or not all(isinstance(v, str) and v for v in m[key]):
                    errors.append(f"{where}: mappings.{key} missing or not a list of strings")

    for code, k in codes.items():
        if k["parent"] is not None and k["parent"] not in codes:
            errors.append(f"class {code}: parent {k['parent']} not present")

    level1 = sorted(c for c, k in codes.items() if k["level"] == 1)
    if level1 != [str(n) for n in range(7)]:
        errors.append(f"level-1 codes are {level1}, expected 0..6")

    # colours: pairwise distinct and at least MIN_DELTA_E apart
    valid = [(c, k["color"].lower()) for c, k in codes.items()
             if isinstance(k["color"], str) and COLOR_RE.match(k["color"])]
    seen = {}
    for c, col in valid:
        if col in seen:
            errors.append(f"colour {col} used by {seen[col]} and {c}")
        seen.setdefault(col, c)
    labs = [(c, to_lab(col)) for c, col in valid]
    closest = None
    for i in range(len(labs)):
        for j in range(i + 1, len(labs)):
            d = math.dist(labs[i][1], labs[j][1])
            if closest is None or d < closest[0]:
                closest = (d, labs[i][0], labs[j][0])
            if d < MIN_DELTA_E:
                errors.append(f"colours of {labs[i][0]} and {labs[j][0]} too close (dE {d:.1f} < {MIN_DELTA_E})")

    parents = {k["parent"] for k in codes.values()}
    counts = {
        "level_1": sum(1 for k in codes.values() if k["level"] == 1),
        "level_2": sum(1 for k in codes.values() if k["level"] == 2),
        "leaves": sum(1 for c in codes if c not in parents),
    }

    rules = doc.get("rules")
    if not isinstance(rules, list) or not rules:
        errors.append("'rules' missing or empty")
        rules = []
    numbers = {"G": [], "U": []}
    for i, r in enumerate(rules):
        missing = [f for f in RULE_FIELDS if not isinstance(r.get(f), str) or not r[f].strip()]
        if missing:
            errors.append(f"rule #{i} ({r.get('id', '?')}): missing fields {missing}")
            continue
        mt = RULE_RE.match(r["id"])
        if not mt:
            errors.append(f"rule #{i}: invalid id {r['id']!r}")
            continue
        numbers[mt.group(1)].append(int(mt.group(2)))
    for prefix, nums in numbers.items():
        if sorted(nums) != list(range(1, len(nums) + 1)):
            errors.append(f"{prefix} rules not numbered 1..n without gaps: {sorted(nums)}")
    counts["rules_g"] = len(numbers["G"])
    counts["rules_u"] = len(numbers["U"])

    declared = doc.get("counts")
    if not isinstance(declared, dict):
        errors.append("'counts' missing")
    else:
        for key, value in counts.items():
            if declared.get(key) != value:
                errors.append(f"count {key}: found {value}, declared {declared.get(key)}")

    status = doc.get("status")
    for key in ("bw", "mappings"):
        if not isinstance(status, dict) or not str(status.get(key, "")).strip():
            errors.append(f"status.{key} (uncertainty note) missing")

    counts["classes"] = len(codes)
    counts["closest"] = closest
    return errors, counts


def main(argv):
    if len(argv) != 2:
        print("usage: pruefe_kategorien.py <kategorien.json>")
        return 2
    try:
        with open(argv[1], encoding="utf-8") as f:
            doc = json.load(f)
    except (OSError, ValueError) as exc:
        print(f"cannot read {argv[1]}: {exc}")
        return 1
    if not isinstance(doc, dict):
        print("top level is not an object")
        return 1
    errors, counts = check(doc)
    if counts:
        print(f"level 1: {counts['level_1']}, level 2: {counts['level_2']}, "
              f"leaves: {counts['leaves']} ({counts['level_1']}/{counts['level_2']}/{counts['leaves']}), "
              f"classes: {counts['classes']}")
        print(f"rules: {counts['rules_g']} G, {counts['rules_u']} U")
        if counts["closest"]:
            d, a, b = counts["closest"]
            print(f"colours: closest pair {a} / {b}, dE {d:.1f} (minimum {MIN_DELTA_E})")
    for e in errors:
        print(f"ERROR: {e}")
    if errors:
        print(f"failed: {len(errors)} error(s)")
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

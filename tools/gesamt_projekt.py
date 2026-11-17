"""Build, check and review the shared project for Victor (standard library only).

Usage (paths in Windows form ``C:/...``):

  python -B tools/gesamt_projekt.py bauen --basis <Victor> --ziel <folder>
  python -B tools/gesamt_projekt.py pruefen [--basis <Victor>] --ziel <folder> [--luftbilder <folder>]
  python -B tools/gesamt_projekt.py durchsicht --ziel <folder> [--basis <Victor>] [--bericht <file.md>]

``bauen`` clones the handover repo (``grundlage``) into ``--ziel`` once, moves its ``T0/`` to
``ergebnisse/`` and drops the old root copy of the tools, brings the repos ``landseg`` and
``unterlagen`` in with their full history (``git subtree``, no squash), mirrors ``wuensche/`` and
``daten/landseg/`` byte for byte and writes README, guide and the description of the original aerial
images. It commits in ``--ziel`` only when something changed (a second run without changes adds no
commit). ``pruefen`` checks completeness against the sources (with ``--basis``), forbidden paths,
file sizes (warning from 50 MB, error from 100 MB, working tree and history), Git LFS, line-ending
settings, the paths named in README.md and, with ``--luftbilder``, the original images by size and
SHA-256. ``durchsicht`` searches every tracked text file for secrets, e-mail addresses, other areas,
internals of the wish system and paths with an account name; each finding needs a rule in the
settings (keep with reason or removed from the copy), otherwise exit 1. Secrets always fail.

Settings: ``einstellungen/gesamt_projekt.json`` (``--einstellungen <file>`` replaces it).
Exit codes: 0 ok, 1 finding or check failed, 2 wrong call or missing source.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STANDARD_EINSTELLUNGEN = REPO / "einstellungen" / "gesamt_projekt.json"
MB = 1024 * 1024
BINAER_ENDUNGEN = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".npz", ".npy", ".gif", ".webp", ".pdf", ".zip"}
BASE64_RE = re.compile(r"data:[^,\s\"']{0,80};base64,[A-Za-z0-9+/=]+")


class Fehler(Exception):
    """Wrong call or missing source: message for the user, exit 2."""


# --------------------------------------------------------------------------- helpers


def einstellungen_laden(pfad: str | Path | None = None) -> dict:
    return json.loads(Path(pfad or STANDARD_EINSTELLUNGEN).read_text(encoding="utf-8"))


def muster_regex(muster: str) -> re.Pattern:
    """Glob relative to a root: ``**`` any depth (also none), ``*`` within one folder, ``?`` one char."""
    teile, i = [], 0
    while i < len(muster):
        if muster.startswith("**/", i):
            teile.append("(?:.*/)?")
            i += 3
        elif muster.startswith("**", i):
            teile.append(".*")
            i += 2
        elif muster[i] == "*":
            teile.append("[^/]*")
            i += 1
        elif muster[i] == "?":
            teile.append("[^/]")
            i += 1
        else:
            teile.append(re.escape(muster[i]))
            i += 1
    return re.compile("^" + "".join(teile) + "$")


def passt(pfad: str, muster: list[str]) -> bool:
    return any(muster_regex(m).match(pfad) for m in muster)


def git(ordner: Path | str, *argumente: str, pruefen: bool = True) -> str:
    lauf = subprocess.run(["git", "-C", str(ordner), "-c", "core.autocrlf=false", *argumente],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")
    if pruefen and lauf.returncode != 0:
        raise Fehler(f"git {' '.join(argumente[:3])} in {ordner}: {(lauf.stderr or lauf.stdout).strip()}")
    return lauf.stdout


def blob_hash(daten: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(daten) + daten).hexdigest()


def baum(ordner: Path, ref: str = "HEAD", unter: str = "") -> dict[str, str]:
    """Tracked files of a commit: path (relative to ``unter``) -> blob hash."""
    ziel = f"{ref}:{unter}" if unter else ref
    if subprocess.run(["git", "-C", str(ordner), "cat-file", "-e", ziel], capture_output=True).returncode:
        return {}
    ausgabe = git(ordner, "ls-tree", "-r", "-z", "--full-tree", ziel)
    dateien = {}
    for eintrag in filter(None, ausgabe.split("\0")):
        kopf, pfad = eintrag.split("\t", 1)
        art, objekt = kopf.split()[1:3]
        if art == "blob":
            dateien[pfad] = objekt
    return dateien


def quelldateien(quelle: Path, ohne: list[str]) -> dict[str, Path]:
    """Files below ``quelle`` (without ``.git`` folders and the patterns in ``ohne``)."""
    dateien = {}
    for wurzel, ordner, namen in os.walk(quelle):
        ordner[:] = sorted(o for o in ordner if o != ".git")
        for name in sorted(namen):
            pfad = Path(wurzel) / name
            rel = pfad.relative_to(quelle).as_posix()
            if not passt(rel, ohne):
                dateien[rel] = pfad
    return dateien


def entfernt_muster(einst: dict) -> list[str]:
    return [m for r in einst["durchsicht"]["regeln"] if r["behandlung"] == "entfernen" for m in r.get("dateien", [])]


def kopien_soll(basis: Path, einst: dict) -> tuple[dict[str, Path], list[str]]:
    """Target path -> source file for all mirrored folders; second value: removed by review."""
    weg = entfernt_muster(einst)
    soll, entfernt = {}, []
    for kopie in einst["kopien"]:
        quelle = basis / kopie["quelle"]
        if not quelle.is_dir():
            raise Fehler(f"Quelle fehlt: {quelle}")
        for rel, pfad in quelldateien(quelle, kopie.get("ohne", [])).items():
            ziel = f"{kopie['ziel']}/{rel}"
            (entfernt.append(ziel) if passt(ziel, weg) else soll.__setitem__(ziel, pfad))
    return soll, sorted(entfernt)


def eigene_datei(rel: str) -> bytes:
    """Template from this repo with LF line endings (a checkout with core.autocrlf may hold CRLF)."""
    return (REPO / rel).read_bytes().replace(b"\r\n", b"\n")


def luftbilder_text(basis: Path, einst: dict) -> str:
    """README of ``daten/luftbilder/`` from the template and the table in ``BASIS/daten/README.md``."""
    lb = einst["luftbilder"]
    text = (basis / lb["quelle"]).read_text(encoding="utf-8")
    if lb["abschnitt"] not in text:
        raise Fehler(f"Abschnitt {lb['abschnitt']!r} fehlt in {basis / lb['quelle']}")
    abschnitt = text.split(lb["abschnitt"], 1)[1].split("\n## ", 1)[0]
    tabelle = "\n".join(z for z in abschnitt.splitlines() if z.startswith("|"))
    if not tabelle:
        raise Fehler(f"keine Tabelle im Abschnitt {lb['abschnitt']!r} von {basis / lb['quelle']}")
    vorlage = eigene_datei(lb["vorlage"]).decode("utf-8")
    return vorlage.replace("<!-- TABELLE -->", tabelle)


def seiten_soll(basis: Path, einst: dict) -> dict[str, bytes]:
    """Generated files of the target: README, guide, luftbilder README, .gitattributes, .gitignore."""
    soll = {ziel: eigene_datei(quelle) for ziel, quelle in einst["seiten"].items()}
    soll[einst["luftbilder"]["ziel"]] = luftbilder_text(basis, einst).encode("utf-8")
    soll[".gitattributes"] = einst["gitattributes"].encode("utf-8")
    soll[".gitignore"] = einst["gitignore"].encode("utf-8")
    return soll


# --------------------------------------------------------------------------- bauen


def schreibe(pfad: Path, daten: bytes) -> bool:
    if pfad.is_file() and pfad.read_bytes() == daten:
        return False
    pfad.parent.mkdir(parents=True, exist_ok=True)
    pfad.write_bytes(daten)
    return True


def sauber(ziel: Path) -> bool:
    return git(ziel, "status", "--porcelain").strip() == ""


def nachricht(betreff: str, titel: str, klartext: str, rumpf: str = "") -> str:
    """Commit message with the plain-language lines ``Klartext-Titel:`` (<= 80) and ``Klartext:`` (<= 250)."""
    if len(titel) > 80 or len(klartext) > 250:
        raise Fehler(f"Klartext zu lang: {titel!r}")
    teile = [betreff] + ([rumpf] if rumpf else []) + [f"Klartext-Titel: {titel}\nKlartext: {klartext}"]
    return "\n\n".join(teile)


def commit(ziel: Path, nachricht: str) -> bool:
    git(ziel, "add", "-A")
    if subprocess.run(["git", "-C", str(ziel), "diff", "--cached", "--quiet"]).returncode == 0:
        return False
    git(ziel, "commit", "-q", "-m", nachricht)
    return True


def bauen(basis: Path, ziel: Path, einst: dict, ausgabe=print) -> list[str]:
    """Create or refresh the target; returns the new commits (one line each)."""
    grundlage = basis / einst["grundlage"]
    for v in einst["verlauf"]:
        if not (basis / v["repo"] / ".git").exists():
            raise Fehler(f"Repo fehlt: {basis / v['repo']}")
    vorher = git(ziel, "rev-parse", "HEAD").strip() if (ziel / ".git").exists() else None
    if vorher is None:
        if ziel.exists() and any(ziel.iterdir()):
            raise Fehler(f"Ziel ist kein Git-Repo und nicht leer: {ziel}")
        if not (grundlage / ".git").exists():
            raise Fehler(f"Grundlage fehlt: {grundlage}")
        ziel.parent.mkdir(parents=True, exist_ok=True)
        lauf = subprocess.run(["git", "-c", "core.autocrlf=false", "clone", "-q", "-c", "core.autocrlf=false",
                               str(grundlage), str(ziel)], capture_output=True, text=True)
        if lauf.returncode:
            raise Fehler(f"git clone: {lauf.stderr.strip()}")
        adresse = git(grundlage, "remote", "get-url", "origin", pruefen=False).strip()
        if adresse:
            git(ziel, "remote", "set-url", "origin", adresse)
        ausgabe(f"geklont: {grundlage} -> {ziel} (origin {adresse or 'ohne'})")
        vorher = git(ziel, "rev-parse", "HEAD").strip()
    git(ziel, "config", "core.autocrlf", "false")
    if not sauber(ziel):
        raise Fehler(f"Ziel hat offene Änderungen, erst committen oder verwerfen: {ziel}")
    seiten = seiten_soll(basis, einst)

    umbau = einst["umbau"]
    inhalt = {Path(p).parts[0] for p in baum(ziel)}
    if umbau["aus"] in inhalt and umbau["nach"] not in inhalt:
        git(ziel, "mv", umbau["aus"], umbau["nach"])
        for eintrag in sorted(inhalt - {umbau["aus"], *umbau["behalten"]}):
            git(ziel, "rm", "-r", "-q", "--", eintrag)
        for name in (".gitattributes", ".gitignore"):
            schreibe(ziel / name, seiten[name])
        commit(ziel, nachricht(
            f"refactor: move handover results to {umbau['nach']}/ and drop the old root copy of the tools",
            f"Ergebnisse der Übergabe in den Ordner {umbau['nach']}/ verschoben",
            "Die Ergebnisse der ersten Übergabe liegen jetzt in einem eigenen Ordner. Die alte Kopie des "
            "Programms ist weg; es kommt gleich mit allen früheren Änderungen zurück.",
            "The tools come back with their full history under the subtree prefixes."))
        ausgabe(f"umgebaut: {umbau['aus']}/ -> {umbau['nach']}/")

    for v in einst["verlauf"]:
        quelle = (basis / v["repo"]).as_posix()
        if v["prefix"] in {Path(p).parts[0] for p in baum(ziel)}:
            git(ziel, "subtree", "pull", "-q", f"--prefix={v['prefix']}", quelle, v["branch"], "-m", nachricht(
                f"chore: update {v['prefix']}/ from {v['repo']} {v['branch']}",
                f"Ordner {v['prefix']}/ auf den neuesten Stand gebracht",
                f"Die neuen Änderungen aus unserem Arbeitsordner {v['repo']} sind übernommen, jede mit ihrer "
                f"eigenen Beschreibung, damit man sie einzeln nachlesen kann."))
        else:
            git(ziel, "subtree", "add", "-q", f"--prefix={v['prefix']}", quelle, v["branch"], "-m", nachricht(
                f"Add '{v['prefix']}/' from {v['repo']} {v['branch']}",
                f"Ordner {v['prefix']}/ mit allen früheren Änderungen übernommen",
                f"Der Inhalt unseres Arbeitsordners {v['repo']} liegt jetzt hier unter {v['prefix']}/, "
                f"samt allen früheren Änderungen, damit jeder Schritt nachvollziehbar bleibt."))
            ausgabe(f"Verlauf übernommen: {v['repo']} -> {v['prefix']}/")

    soll, entfernt = kopien_soll(basis, einst)
    geaendert = 0
    for rel, quelle in soll.items():
        geaendert += schreibe(ziel / rel, quelle.read_bytes())
    verwaltet = tuple(k["ziel"] + "/" for k in einst["kopien"])
    for rel in baum(ziel):
        if rel.startswith(verwaltet) and rel not in soll:
            (ziel / rel).unlink(missing_ok=True)
            geaendert += 1
    for rel, daten in seiten.items():
        geaendert += schreibe(ziel / rel, daten)
    commit(ziel, nachricht(
        "chore: sync wishes, working data and guides from the Victor base folder",
        "Aufträge, Berichte, Arbeitsdaten und Anleitungen aufgefrischt",
        "Die Kopien der Aufträge, Berichte, Arbeitsdaten und Anleitungen sind wieder auf dem Stand "
        "unseres Arbeitsordners."))
    ausgabe(f"Kopien: {len(soll)} Dateien, {geaendert} geändert oder entfernt; laut Durchsicht weggelassen: {len(entfernt)}")
    nachher = git(ziel, "rev-parse", "HEAD").strip()
    if nachher == vorher:
        neu = []
    else:
        bereich = f"{vorher}..{nachher}" if vorher else nachher
        neu = git(ziel, "log", "--oneline", "--first-parent", bereich).splitlines()
    ausgabe(f"neue Commits: {len(neu)}" + "".join(f"\n  {z}" for z in neu))
    return neu


# --------------------------------------------------------------------------- pruefen


def groessen(ziel: Path, warnung_mb: float, grenze_mb: float) -> tuple[list, list, tuple]:
    """Files of the working tree (tracked and not ignored) and blobs of the whole history."""
    eintraege = []
    for rel in filter(None, git(ziel, "ls-files", "-z", "-c", "-o", "--exclude-standard").split("\0")):
        pfad = ziel / rel
        if pfad.is_file():
            eintraege.append((pfad.stat().st_size, rel))
    objekte = git(ziel, "rev-list", "--objects", "--all", pruefen=False)
    if objekte.strip():
        lauf = subprocess.run(["git", "-C", str(ziel), "cat-file",
                               "--batch-check=%(objecttype) %(objectsize) %(rest)"],
                              input=objekte, capture_output=True, text=True, encoding="utf-8", errors="replace")
        for zeile in lauf.stdout.splitlines():
            teile = zeile.split(" ", 2)
            if len(teile) == 3 and teile[0] == "blob":
                eintraege.append((int(teile[1]), f"{teile[2]} (Verlauf)"))
    warnungen = sorted({e for e in eintraege if warnung_mb * MB <= e[0] < grenze_mb * MB}, reverse=True)
    zu_gross = sorted({e for e in eintraege if e[0] >= grenze_mb * MB}, reverse=True)
    groesste = max(eintraege, default=(0, "–"))
    return warnungen, zu_gross, groesste


def readme_pfade(ziel: Path, wurzeln: list[str]) -> tuple[int, list[str]]:
    text = (ziel / "README.md").read_text(encoding="utf-8") if (ziel / "README.md").is_file() else ""
    kandidaten = re.findall(r"`([^`\s]+)`", text) + re.findall(r"\]\(([^)\s]+)\)", text)
    pfade = set()
    for k in kandidaten:
        k = k.split("#", 1)[0].rstrip("/")
        if not k or any(z in k for z in "<>*{}$"):
            continue
        if k.split("/", 1)[0] in wurzeln:
            pfade.add(k)
    return len(pfade), sorted(p for p in pfade if not (ziel / p).exists())


def luftbilder_tabelle(ziel: Path, einst: dict) -> list[tuple[str, int, str]]:
    pfad = ziel / einst["luftbilder"]["ziel"]
    if not pfad.is_file():
        return []
    zeilen = []
    for treffer in re.finditer(r"^\|\s*`([^`]+)`\s*\|\s*(\d+)\s*\|\s*`([0-9a-f]{64})`\s*\|", pfad.read_text(encoding="utf-8"), re.M):
        zeilen.append((treffer.group(1), int(treffer.group(2)), treffer.group(3)))
    return zeilen


def sha256(pfad: Path) -> str:
    h = hashlib.sha256()
    with pfad.open("rb") as datei:
        for stueck in iter(lambda: datei.read(4 * MB), b""):
            h.update(stueck)
    return h.hexdigest()


def luftbilder_pruefen(ziel: Path, ordner: Path, einst: dict) -> tuple[str, bool]:
    tabelle = luftbilder_tabelle(ziel, einst)
    if not tabelle:
        return f"Luftbilder: keine Tabelle in {einst['luftbilder']['ziel']}", False
    fehlt, abweichend = [], []
    for rel, groesse, summe in tabelle:
        pfad = ordner / rel
        if not pfad.is_file():
            fehlt.append(rel)
        elif pfad.stat().st_size != groesse or sha256(pfad) != summe:
            abweichend.append(rel)
    ok = len(tabelle) - len(fehlt) - len(abweichend)
    text = f"Luftbilder: {ok} von {len(tabelle)} passen ({ordner})"
    if fehlt:
        text += "\n  fehlt: " + ", ".join(fehlt)
    if abweichend:
        text += "\n  andere Größe oder Prüfsumme: " + ", ".join(abweichend)
    return text, not (fehlt or abweichend)


def pruefen(ziel: Path, einst: dict, basis: Path | None = None, luftbilder: Path | None = None,
            ausgabe=print) -> int:
    if not (ziel / ".git").exists():
        raise Fehler(f"Ziel ist kein Git-Repo: {ziel}")
    fehler = False
    ist = baum(ziel)

    if basis is not None:
        soll_kopien, entfernt = kopien_soll(basis, einst)
        soll = {rel: blob_hash(p.read_bytes()) for rel, p in soll_kopien.items()}
        soll.update({rel: blob_hash(d) for rel, d in seiten_soll(basis, einst).items()})
        for v in einst["verlauf"]:
            soll.update({f"{v['prefix']}/{rel}": h for rel, h in baum(basis / v["repo"], v["branch"]).items()})
        grundlage = basis / einst["grundlage"]
        ergebnisse = baum(grundlage, "HEAD", einst["umbau"]["aus"])
        soll.update({f"{einst['umbau']['nach']}/{rel}": h for rel, h in ergebnisse.items()})
        fehlend = sorted(set(soll) - set(ist))
        abweichend = sorted(rel for rel in set(soll) & set(ist) if soll[rel] != ist[rel])
        fremd = sorted(set(ist) - set(soll))
        ausgabe(f"Vollständigkeit: fehlend {len(fehlend)}, abweichend {len(abweichend)}, fremd {len(fremd)} "
                f"(geprüft {len(soll)} Dateien; laut Durchsicht weggelassen {len(entfernt)})")
        for name, liste in (("fehlend", fehlend), ("abweichend", abweichend), ("fremd", fremd)):
            for rel in liste[:20]:
                ausgabe(f"  {name}: {rel}")
        fehler |= bool(fehlend or abweichend or fremd)
        weg_da = sorted(rel for rel in entfernt if rel in ist)
        if weg_da:
            ausgabe(f"laut Durchsicht zu entfernen, aber im Ziel: {len(weg_da)}" + "".join(f"\n  {r}" for r in weg_da[:20]))
            fehler = True
        offen = [v["repo"] for v in einst["verlauf"]
                 if git(basis / v["repo"], "status", "--porcelain", "--untracked-files=no").strip()]
        if offen:
            ausgabe("Hinweis: nicht eingecheckte Änderungen in der Quelle (nicht übernommen): " + ", ".join(offen))
    else:
        ausgabe("Vollständigkeit: nicht geprüft (ohne --basis)")

    verboten = sorted(rel for rel in ist if passt(rel, einst["verboten"]) and not passt(rel, einst["erlaubt"]))
    ausgabe(f"Verbotene Pfade: {len(verboten)}" + "".join(f"\n  {r}" for r in verboten[:20]))
    fehler |= bool(verboten)

    g = einst["groesse"]
    warnungen, zu_gross, groesste = groessen(ziel, g["warnung_mb"], g["grenze_mb"])
    ausgabe(f"größte Datei {groesste[0] / MB:.1f} MB ({groesste[1]}); Warnungen: {len(warnungen)}; "
            f"ab {g['grenze_mb']} MB: {len(zu_gross)}")
    for groesse, rel in warnungen:
        ausgabe(f"  Warnung (ab {g['warnung_mb']} MB): {rel} {groesse / MB:.1f} MB")
    for groesse, rel in zu_gross:
        ausgabe(f"  zu groß für GitHub (ab {g['grenze_mb']} MB): {rel} {groesse / MB:.1f} MB")
    fehler |= bool(zu_gross)

    lfs = sorted(rel for rel in ist if rel.endswith(".lfsconfig") or (
        rel.endswith(".gitattributes") and "filter=lfs" in (ziel / rel).read_text(encoding="utf-8", errors="replace")))
    ausgabe("Git-Zusatzspeicher (lfs): " + (", ".join(lfs) if lfs else "keiner"))
    fehler |= bool(lfs)

    attribute = (ziel / ".gitattributes").read_text(encoding="utf-8") if (ziel / ".gitattributes").is_file() else ""
    ohne_umwandlung = bool(re.search(r"^\*\s+-text\s*$", attribute, re.M))
    autocrlf = subprocess.run(["git", "-C", str(ziel), "config", "core.autocrlf"], capture_output=True,
                              text=True).stdout.strip() or "nicht gesetzt"
    ausgabe(f"Zeilenenden: .gitattributes `* -text` {'ja' if ohne_umwandlung else 'NEIN'}; core.autocrlf {autocrlf}")
    fehler |= not ohne_umwandlung and autocrlf != "false"

    anzahl, fehlen = readme_pfade(ziel, einst["readme_wurzeln"])
    if not (ziel / "README.md").is_file():
        ausgabe("README-Pfade: README.md fehlt")
        fehler = True
    elif fehlen:
        ausgabe(f"README-Pfade: {len(fehlen)} von {anzahl} fehlen" + "".join(f"\n  fehlt: {p}" for p in fehlen))
        fehler = True
    else:
        ausgabe(f"README-Pfade: alle vorhanden ({anzahl})")

    if luftbilder is None:
        ausgabe("Luftbilder nicht geprüft (ohne --luftbilder)")
    else:
        text, ok = luftbilder_pruefen(ziel, luftbilder, einst)
        ausgabe(text)
        fehler |= not ok

    ausgabe("Arbeitsstand: " + ("sauber" if sauber(ziel) else "offene Änderungen (git status)"))
    ausgabe("Ergebnis: " + ("Fehler" if fehler else "ok"))
    return 1 if fehler else 0


# --------------------------------------------------------------------------- durchsicht


def ist_text(daten: bytes, rel: str) -> bool:
    return Path(rel).suffix.lower() not in BINAER_ENDUNGEN and b"\0" not in daten[:8192]


def regel_fuer(art: str, rel: str, fund: str, zeile: str, regeln: list[dict]) -> dict | None:
    for regel in regeln:
        if regel["art"] not in (art, "*") or regel["behandlung"] != "behalten":
            continue
        if "dateien" in regel and not passt(rel, regel["dateien"]):
            continue
        if "fund" in regel and not re.fullmatch(regel["fund"], fund):
            continue
        if "zeile" in regel and not re.search(regel["zeile"], zeile):
            continue
        return regel
    return None


def bereiche(nummern: list) -> str:
    """Line numbers as compact ranges: 1, 2, 3, 7 -> ``1–3, 7``; anything else as is."""
    zahlen = sorted({n for n in nummern if isinstance(n, int)})
    teile, i = [], 0
    while i < len(zahlen):
        j = i
        while j + 1 < len(zahlen) and zahlen[j + 1] == zahlen[j] + 1:
            j += 1
        teile.append(str(zahlen[i]) if i == j else f"{zahlen[i]}–{zahlen[j]}")
        i = j + 1
    teile += sorted({str(n) for n in nummern if not isinstance(n, int)})
    return ", ".join(teile)


def funde_in(rel: str, text: str, arten: dict[str, list[re.Pattern]]):
    for nummer, zeile in enumerate(text.splitlines(), 1):
        sauber_zeile = BASE64_RE.sub("data:;base64,…", zeile)
        for art, muster in arten.items():
            gesehen = set()
            for m in muster:
                for treffer in m.finditer(sauber_zeile):
                    if treffer.start() in gesehen:
                        continue
                    gesehen.add(treffer.start())
                    yield nummer, art, treffer.group(0), sauber_zeile


def durchsicht(ziel: Path, einst: dict, basis: Path | None = None, bericht: Path | None = None,
               ausgabe=print) -> int:
    if not (ziel / ".git").exists():
        raise Fehler(f"Ziel ist kein Git-Repo: {ziel}")
    d = einst["durchsicht"]
    arten = {art: [re.compile(m) for m in muster] for art, muster in d["arten"].items()}
    regeln = d["regeln"]
    weg = entfernt_muster(einst)
    zeilen, zaehler, ungeordnet, dateien_mit_fund = [], {}, 0, set()
    for rel in sorted(baum(ziel)):
        pfad = ziel / rel
        if not pfad.is_file():
            continue
        daten = pfad.read_bytes()
        if not ist_text(daten, rel):
            continue
        for nummer, art, fund, zeile in funde_in(rel, daten.decode("utf-8", errors="replace"), arten):
            dateien_mit_fund.add(rel)
            zeigen = "(geschwärzt)" if art == "zugang" else fund[:80]
            if art == "zugang":
                behandlung, grund = "FEHLER", "Zugangsdaten oder Schlüssel dürfen nicht ins Projekt"
            elif passt(rel, weg):
                behandlung, grund = "FEHLER", "laut Regel zu entfernen, aber im Ziel"
            else:
                regel = regel_fuer(art, rel, fund, zeile, regeln)
                behandlung, grund = ("behalten", regel["grund"]) if regel else ("UNGEORDNET", "keine Regel")
            if behandlung != "behalten":
                ungeordnet += 1
            zaehler[(art, behandlung, grund)] = zaehler.get((art, behandlung, grund), 0) + 1
            zeilen.append((rel, nummer, art, zeigen, behandlung, grund))
    entfernt = []
    if basis is not None:
        _, entfernt = kopien_soll(basis, einst)
        for regel in regeln:
            if regel["behandlung"] == "entfernen":
                for rel in entfernt:
                    if passt(rel, regel.get("dateien", [])):
                        zeilen.append((rel, "–", regel["art"], "ganze Datei", "in der Kopie entfernt", regel["grund"]))
                        zaehler[(regel["art"], "in der Kopie entfernt", regel["grund"])] = \
                            zaehler.get((regel["art"], "in der Kopie entfernt", regel["grund"]), 0) + 1

    zusammen = ["| Art | Behandlung | Fundstellen | Grund |", "|---|---|---:|---|"]
    for (art, behandlung, grund), anzahl in sorted(zaehler.items()):
        zusammen.append(f"| {art} | {behandlung} | {anzahl} | {grund} |")
    kopf = (f"Durchsicht {ziel}: {len(zeilen)} Fundstellen in {len(dateien_mit_fund)} Dateien; "
            f"ungeordnet oder Fehler: {ungeordnet}")
    ausgabe(kopf)
    ausgabe("\n".join(zusammen))
    for z in zeilen:
        if z[4] in ("UNGEORDNET", "FEHLER"):
            ausgabe(f"  {z[4]}: {z[0]}:{z[1]} {z[2]} {z[3]}")
    if bericht is not None:
        gruppen: dict[tuple, tuple[list, list]] = {}
        for rel, nummer, art, fund, behandlung, grund in zeilen:
            nummern, funde = gruppen.setdefault((rel, art, behandlung, grund), ([], []))
            nummern.append(nummer)
            if fund not in funde:
                funde.append(fund)
        tabelle = ["| Datei | Zeilen | Art | Fund (Beispiele) | Behandlung | Grund |", "|---|---|---|---|---|---|"]
        for (rel, art, behandlung, grund), (nummern, funde) in gruppen.items():
            beispiele = ", ".join("`" + f.replace("|", "\\|").replace("`", "'") + "`" for f in funde[:3])
            if len(funde) > 3:
                beispiele += f" (+{len(funde) - 3})"
            tabelle.append(f"| `{rel}` | {bereiche(nummern)} | {art} | {beispiele} | {behandlung} | {grund} |")
        bericht.parent.mkdir(parents=True, exist_ok=True)
        bericht.write_text(f"# Durchsicht auf Vertrauliches\n\n{kopf}\n\n## Zusammenfassung\n\n"
                           + "\n".join(zusammen) + "\n\n## Alle Fundstellen\n\n" + "\n".join(tabelle) + "\n",
                           encoding="utf-8", newline="\n")
        ausgabe(f"Bericht: {bericht}")
    return 1 if ungeordnet else 0


# --------------------------------------------------------------------------- Befehlszeile


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="gesamt_projekt.py", description=__doc__.split("\n\n")[0])
    parser.add_argument("--einstellungen", help="eigene Einstellungen statt einstellungen/gesamt_projekt.json")
    befehle = parser.add_subparsers(dest="befehl", required=True)
    b = befehle.add_parser("bauen", help="Gesamt-Ordner anlegen oder aktualisieren (committet dort)")
    b.add_argument("--basis", required=True, help="Basisordner Victor (Quelle)")
    b.add_argument("--ziel", required=True, help="Gesamt-Ordner (Git-Repo)")
    p = befehle.add_parser("pruefen", help="Vollständigkeit, Größen, Pfade im README, Luftbilder")
    p.add_argument("--basis", help="Basisordner Victor; ohne: keine Prüfung der Vollständigkeit")
    p.add_argument("--ziel", required=True)
    p.add_argument("--luftbilder", help="Ordner mit den Original-Luftbildern (Größe und SHA-256)")
    d = befehle.add_parser("durchsicht", help="Suche nach Vertraulichem in allen versionierten Textdateien")
    d.add_argument("--ziel", required=True)
    d.add_argument("--basis", help="Basisordner: auch die in der Kopie entfernten Dateien auflisten")
    d.add_argument("--bericht", help="Markdown-Datei mit allen Fundstellen")
    args = parser.parse_args(argv)
    for strom in (sys.stdout, sys.stderr):
        if hasattr(strom, "reconfigure"):
            strom.reconfigure(encoding="utf-8", errors="replace")
    try:
        einst = einstellungen_laden(args.einstellungen)
        ziel = Path(args.ziel).resolve()
        basis = Path(args.basis).resolve() if getattr(args, "basis", None) else None
        if args.befehl == "bauen":
            bauen(basis, ziel, einst)
            return 0
        if args.befehl == "pruefen":
            return pruefen(ziel, einst, basis, Path(args.luftbilder).resolve() if args.luftbilder else None)
        return durchsicht(ziel, einst, basis, Path(args.bericht).resolve() if args.bericht else None)
    except Fehler as fehler:
        print(f"Fehler: {fehler}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

"""Kostenmessung eines Agent-Laufs aus seinen Transkripten (``python -m landseg messung``).

Quelle ist der Protokollordner eines Workflow-Laufs von Claude Code: je Agent ``agent-<id>.jsonl``
(Transkript) und ``agent-<id>.meta.json`` (``workflowPhase``, ``model``). Gezählt wird je Phase und
für den ganzen Lauf: Agents, Wand-Minuten, Agent-Minuten, Runden (API-Antworten), gelesene Tokens
(Cache-Lesen), neue Tokens (Eingabe + Cache-Schreiben), ausgegebene Tokens, USD, gelesene Bilder und
geschriebene ``.py``-Dateien. Dazu je Fassung die Urteils-Agents (Label ``urteil:<art>:…``, Art ``a``, ``b``,
``c``, ``z`` = Gegenprobe) mit gelesenen Tokens je Agent, um die Aufteilung (ein Agent je Viertel) zu vergleichen.

Zählregeln wie ``kachellauf messung`` im Stitcher und die Kostenauswertung des Plugins ``wunsch``:
Eine API-Antwort steht im Transkript einmal je Inhaltsblock mit derselben ``usage``; sie zählt nur
einmal (Kennung ``message.id``, sonst ``uuid``). Die USD-Zahlen sind ein Rechenwert nach Listenpreis
(``PREIS``), keine Abo-Kosten. Nur Standardbibliothek; die Transkripte werden nur gelesen.
"""

from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path

FORM = "landseg-messung/1"
# Listenpreise in USD je Million Tokens, Stand 2026-10-08 (Tabelle PREIS des Plugins wunsch,
# server/kern_auswertung.py): Eingabe, Cache-Schreiben 5 min, Cache-Schreiben 1 h, Cache-Lesen, Ausgabe.
# Haiku kostet über 100 000 Prompt-Tokens mehr.
PREIS_STAND = "2026-10-08"
PREIS = {
    "opus": (4.0, 5.0, 8.0, 0.20, 20.0),
    "sonnet": (2.0, 2.5, 4.0, 0.10, 10.0),
    "haiku": (0.10, 0.125, 0.20, 0.01, 0.50),
    "haiku-lang": (0.50, 0.625, 1.0, 0.05, 2.50),
    "fable": (10.0, 12.5, 20.0, 0.25, 50.0),
}
BILD_ENDUNGEN = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff")
OHNE_PHASE = "?"
URTEIL_LABEL = re.compile(r"^urteil:([abcz]):")
FASSUNG_NAME = {"a": "A", "b": "B", "c": "C", "z": "Gegenprobe"}


def preis(modell: str | None, prompt: int) -> tuple[float, ...] | None:
    """Preiszeile zum Modellnamen (``opus``, ``claude-opus-…``); None bei unbekanntem Modell."""
    m = (modell or "").lower()
    for familie in ("opus", "sonnet", "fable", "haiku"):
        if familie in m:
            return PREIS["haiku-lang" if familie == "haiku" and prompt > 100_000 else familie]
    return None


def _zeit(wert) -> float | None:
    try:
        return dt.datetime.fromisoformat(str(wert).replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def _meta_lesen(pfad: Path) -> dict:
    try:
        daten = json.loads(pfad.read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        return {}
    return daten if isinstance(daten, dict) else {}


def _zaehle(t: dict, u: dict, modell: str) -> None:
    eingabe, schreiben, lesen, ausgabe = (int(u.get(x) or 0) for x in (
        "input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"))
    cache = u.get("cache_creation") if isinstance(u.get("cache_creation"), dict) else {}
    schreiben_1h = min(schreiben, int(cache.get("ephemeral_1h_input_tokens") or 0))
    t["gelesen"] += lesen
    t["neu"] += eingabe + schreiben
    t["ausgabe"] += ausgabe
    t["runden"] += 1
    p = preis(modell, eingabe + schreiben + lesen)
    if p:
        t["usd"] += (eingabe * p[0] + (schreiben - schreiben_1h) * p[1] + schreiben_1h * p[2]
                     + lesen * p[3] + ausgabe * p[4]) / 1e6


def transkript_lesen(pfad: Path) -> dict:
    """Ein Agent: Phase und Modell aus der ``meta.json`` daneben, Zeiten, Tokens, USD, Bilder, ``.py``."""
    pfad = Path(pfad)
    meta = _meta_lesen(pfad.with_name(pfad.name[:-len(".jsonl")] + ".meta.json"))
    meta_modell = str(meta.get("model") or "")
    t = {"runden": 0, "gelesen": 0, "neu": 0, "ausgabe": 0, "usd": 0.0, "bilder": 0, "py_geschrieben": 0}
    gesehen, werkzeuge, zeiten, modell = set(), set(), [], None
    try:
        zeilen = pfad.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        zeilen = []
    for zeile in zeilen:
        try:
            o = json.loads(zeile)
        except ValueError:
            continue
        if not isinstance(o, dict):
            continue
        z = _zeit(o.get("timestamp"))
        if z:
            zeiten.append(z)
        m = o.get("message") if isinstance(o.get("message"), dict) else {}
        if o.get("type") == "assistant" and isinstance(m.get("content"), list):
            for block in m["content"]:
                if not isinstance(block, dict) or block.get("type") != "tool_use" or block.get("id") in werkzeuge:
                    continue
                werkzeuge.add(block.get("id"))
                eingabe = block.get("input") if isinstance(block.get("input"), dict) else {}
                datei = str(eingabe.get("file_path") or "").lower()
                if block.get("name") == "Read" and datei.endswith(BILD_ENDUNGEN):
                    t["bilder"] += 1
                elif block.get("name") == "Write" and datei.endswith(".py"):
                    t["py_geschrieben"] += 1
        u = m.get("usage")
        schluessel = m.get("id") or o.get("uuid")
        if not isinstance(u, dict) or schluessel in gesehen:
            continue      # eine API-Antwort steht einmal je Inhaltsblock mit derselben usage
        gesehen.add(schluessel)
        eigenes = str(m.get("model") or "")
        if preis(eigenes, 0):
            modell = eigenes
        _zaehle(t, u, eigenes if preis(eigenes, 0) else meta_modell)
    agent = pfad.name[len("agent-"):-len(".jsonl")]
    return {"agent": agent, "label": str(meta.get("description") or agent),
            "phase": str(meta.get("workflowPhase") or OHNE_PHASE), "modell": meta_modell or modell or "",
            "start": min(zeiten) if zeiten else None, "ende": max(zeiten) if zeiten else None, **t}


def agents_lesen(ordner: Path) -> list[dict]:
    """Alle Agents eines Protokollordners (``agent-*.jsonl``), nach Dateiname."""
    ordner = Path(ordner)
    if not ordner.is_dir():
        raise ValueError(f"Protokollordner fehlt: {ordner}")
    pfade = sorted(ordner.glob("agent-*.jsonl"))
    if not pfade:
        raise ValueError(f"keine agent-*.jsonl in {ordner}")
    return [transkript_lesen(p) for p in pfade]


def _zeile(agents: list[dict]) -> dict:
    start = [a["start"] for a in agents if a["start"]]
    ende = [a["ende"] for a in agents if a["ende"]]
    return {
        "agents": len(agents),
        "modell": ", ".join(sorted({a["modell"] for a in agents if a["modell"]})),
        "beginn": _iso(min(start)) if start else None,
        "schluss": _iso(max(ende)) if ende else None,
        "wand_min": round((max(ende) - min(start)) / 60, 1) if start and ende else None,
        "agent_min": round(sum(a["ende"] - a["start"] for a in agents if a["start"] and a["ende"]) / 60, 1),
        **{k: sum(a[k] for a in agents) for k in ("runden", "gelesen", "neu", "ausgabe", "bilder", "py_geschrieben")},
        "usd": round(sum(a["usd"] for a in agents), 2),
    }


def _iso(sekunden: float) -> str:
    return dt.datetime.fromtimestamp(sekunden, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def messung(agents: list[dict], lauf: str = "") -> dict:
    """Je Phase (nach erstem Start) und zusammen; dazu jede Agent-Zeile."""
    je: dict[str, list[dict]] = {}
    for a in agents:
        je.setdefault(a["phase"], []).append(a)
    frueh = lambda xs: min((a["start"] for a in xs if a["start"]), default=float("inf"))
    phasen = {name: _zeile(xs) for name, xs in sorted(je.items(), key=lambda kv: (frueh(kv[1]), kv[0]))}
    urteile: dict[str, list[dict]] = {}
    for a in agents:
        treffer = URTEIL_LABEL.match(a["label"])
        if treffer:
            urteile.setdefault(FASSUNG_NAME[treffer.group(1)], []).append(a)
    fassungen = {}
    for name in FASSUNG_NAME.values():
        if name in urteile:
            z = _zeile(urteile[name])
            z["gelesen_je_agent"] = round(z["gelesen"] / z["agents"])
            fassungen[name] = z
    return {"form": FORM, "lauf": lauf, "preise_stand": PREIS_STAND, "phasen": phasen,
            "zusammen": _zeile(agents), "urteile_je_fassung": fassungen,
            "agents": [{k: (round(v, 4) if k == "usd" else _iso(v) if k in ("start", "ende") and v else v)
                        for k, v in a.items()} for a in agents]}


def _zahl(wert: float | None, stellen: int) -> str:
    return "–" if wert is None else f"{wert:.{stellen}f}".replace(".", ",")


def tabelle(m: dict) -> str:
    """Markdown: Kopf mit Lauf und Preisstand, eine Zeile je Phase, Zeile ``zusammen``."""
    z = ["| Phase | Modell | Agents | Wand (min) | Agent-min | Runden | gelesen (Mio.) | neu (Mio.) "
         "| Ausgabe (Mio.) | USD | Bilder gelesen | .py geschrieben |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for name, r in list(m["phasen"].items()) + [("zusammen", m["zusammen"])]:
        z.append(f"| {name} | {r['modell'] if name != 'zusammen' else ''} | {r['agents']} "
                 f"| {_zahl(r['wand_min'], 1)} | {_zahl(r['agent_min'], 1)} | {r['runden']} "
                 f"| {_zahl(r['gelesen'] / 1e6, 2)} | {_zahl(r['neu'] / 1e6, 2)} | {_zahl(r['ausgabe'] / 1e6, 3)} "
                 f"| {_zahl(r['usd'], 2)} | {r['bilder']} | {r['py_geschrieben']} |")
    fassungen = m.get("urteile_je_fassung") or {}
    if fassungen:
        z += ["", "Urteils-Agents je Fassung (Label `urteil:<art>:…`):", "",
              "| Fassung | Agents | gelesen (Mio.) | gelesen je Agent (Mio.) | Runden | USD | Bilder gelesen |",
              "|---|---|---|---|---|---|---|"]
        for name, r in fassungen.items():
            z.append(f"| {name} | {r['agents']} | {_zahl(r['gelesen'] / 1e6, 2)} | {_zahl(r['gelesen_je_agent'] / 1e6, 2)} "
                     f"| {r['runden']} | {_zahl(r['usd'], 2)} | {r['bilder']} |")
    zeitraum = f" ({m['zusammen']['beginn']} bis {m['zusammen']['schluss']})" if m["zusammen"]["beginn"] else ""
    return (f"# Messung {m['lauf']}\n\n"
            f"USD: Rechenwert nach Listenpreis (Stand {m['preise_stand']}), keine Abo-Kosten. "
            f"Gelesen = Cache-Lesen, neu = Eingabe + Cache-Schreiben; Runden = API-Antworten{zeitraum}.\n\n"
            + "\n".join(z) + "\n")


def messung_befehl(transkripte: str | Path, lauf: str | None = None, ziel: str | Path | None = None) -> dict:
    """Liest den Protokollordner, schreibt ``messung.json`` und ``messung.md`` nach ``ziel`` (wenn gesetzt)."""
    quelle = Path(transkripte)
    name = re.sub(r"[^\w.-]", "_", lauf or quelle.name)
    m = messung(agents_lesen(quelle), name)
    m["quelle"] = str(quelle).replace("\\", "/")
    if ziel is not None:
        z = Path(ziel)
        if z.resolve() == quelle.resolve():
            raise ValueError("--ziel darf nicht der Protokollordner sein (Transkripte nur lesen)")
        z.mkdir(parents=True, exist_ok=True)
        (z / "messung.json").write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        (z / "messung.md").write_text(tabelle(m), encoding="utf-8")
    return m

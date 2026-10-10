#!/usr/bin/env python3
"""Generate the catalogue views from catalog/catalog.json (the single source of truth).

Writes:
  docs/02-architecture/procescatalogus.md   the catalogue as tables, per end-to-end process
  site/data/catalog.json                    the data the prototype reads, with coverage figures
  site/assets/models/proceshuis.svg         L0/L1 process house
  site/assets/models/capability-map.svg     capability map with support heat map and process count
  site/assets/models/otc-waardeketen.svg    L1 order-to-cash as a value chain of its L2 processes
Run: python3 scripts/build_catalog.py
"""
from __future__ import annotations

import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAT = json.loads((ROOT / "catalog/catalog.json").read_text(encoding="utf-8"))
FONT = 'font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif"'
STATUS_LABEL = {"geen-model": "geen model", "draft": "draft", "in-review": "in review", "released": "released", "retired": "retired"}


def active() -> list[dict]:
    return [p for p in CAT["processes"] if p["status"] != "retired"]


def coverage() -> dict:
    procs = active()
    n = len(procs)
    by_status = {s: sum(1 for p in procs if p["status"] == s) for s in CAT["meta"]["statuses"] if s != "retired"}
    per_l1 = {}
    for x in CAT["l1"]:
        ps = [p for p in procs if p["l1"] == x["id"]]
        per_l1[x["id"]] = {"processes": len(ps), "owned": sum(1 for p in ps if p["owner"]),
                           "released": sum(1 for p in ps if p["status"] == "released")}
    return {
        "l2": n,
        "owned": sum(1 for p in procs if p["owner"]),
        "released": by_status["released"],
        "byStatus": by_status,
        "l1WithoutOwner": [x["id"] for x in CAT["l1"] if not x["owner"]],
        "perL1": per_l1,
    }


def markdown(cov: dict) -> str:
    caps = {c["id"]: c["name"] for g in CAT["capabilities"] for c in g["children"]}
    systems = {s["id"]: s["name"] for s in CAT["systems"]}
    out = [
        "# Procescatalogus — Corvent Industries",
        "",
        "> **Gegenereerd** uit [`catalog/catalog.json`](../../catalog/catalog.json) door `scripts/build_catalog.py` — niet met de hand bewerken.",
        "> Wat het is: het register van alle L1- en L2-processen met eigenaar, status, versie, capability, systemen en reviewdatum.",
        "> Voor wie: process architect, analisten, enterprise architectuur, projecten. *Illustrative assumption — not real company data.*",
        "",
        "← [Capability map](capability-map.md) · [Procesboom](procesboom.md) · Volgende: [Modelleerconventie](../03-standards/modelleerconventie.md) →",
        "",
        "## Dekking",
        "",
        f"| Actieve L2-processen | Met eigenaar | Released | In review | Draft | Geen model |",
        "|---:|---:|---:|---:|---:|---:|",
        f"| {cov['l2']} | {cov['owned']} ({round(100 * cov['owned'] / cov['l2'])}%) | {cov['released']} ({round(100 * cov['released'] / cov['l2'])}%) "
        f"| {cov['byStatus']['in-review']} | {cov['byStatus']['draft']} | {cov['byStatus']['geen-model']} |",
        "",
        f"L1 zonder eigenaar: {', '.join(cov['l1WithoutOwner']) or '—'}. De volledige lijst governance-gaten staat in het rapport van "
        "`scripts/check_models.py` (regel C04) en op de [demo](https://phlppgdfry.github.io/manufacturing-process-architecture-case/demo/).",
        "",
    ]
    for l0 in CAT["l0"]:
        out += [f"## {l0['name']}", ""]
        for x in (x for x in CAT["l1"] if x["l0"] == l0["id"]):
            c = cov["perL1"][x["id"]]
            out += [f"### {x['id']} · {x['name']} — {x['nl']}", "",
                    f"Eigenaar L1: **{x['owner'] or 'geen (governance-gat)'}** · {c['processes']} L2 · {c['owned']} met eigenaar · {c['released']} released",
                    "", "| ID | Proces (L2) | Eigenaar | Status | Versie | Capability | Systemen | Review | Opmerking |",
                    "|---|---|---|---|---|---|---|---|---|"]
            for p in (p for p in CAT["processes"] if p["l1"] == x["id"]):
                note = "; ".join(filter(None, [p.get("issue", ""), ("alias: " + ", ".join(p["aliases"])) if p.get("aliases") else ""]))
                model = p.get("model") or ""
                if model.startswith("docs/"):
                    note = (note + "; " if note else "") + f"[model](../../{model})"
                out.append(
                    f"| {p['id']} | {p['name']} | {p['owner'] or '—'} | {STATUS_LABEL[p['status']]} | {p['version'] or '—'} | "
                    f"{', '.join(caps[c] for c in p['capabilities'])} | {', '.join(systems[s] for s in p['systems'])} | {p['review'] or '—'} | {note} |")
            out.append("")
    return "\n".join(out)


def svg_house() -> str:
    w, pad, row_h = 1100, 16, 92
    rows = [("S", "#e8eef5"), ("K", "#dfeee6"), ("O", "#f3efe4")]
    h = 70 + len(rows) * (row_h + 12) + 10
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
         f'aria-label="Proceshuis Corvent: sturende, kern- en ondersteunende processen" {FONT} font-size="13">',
         f'<rect width="{w}" height="{h}" fill="#ffffff"/>',
         f'<path d="M{pad},58 L{w / 2},{pad} L{w - pad},58 z" fill="#1f4e79"/>',
         f'<text x="{w / 2}" y="48" text-anchor="middle" fill="#ffffff" font-weight="700" font-size="15">Corvent Process House — L0 / L1</text>']
    y = 70
    for l0_id, fill in rows:
        l0 = next(x for x in CAT["l0"] if x["id"] == l0_id)
        items = [x for x in CAT["l1"] if x["l0"] == l0_id]
        o.append(f'<rect x="{pad}" y="{y}" width="{w - 2 * pad}" height="{row_h}" rx="8" fill="{fill}" stroke="#c9d1db"/>')
        o.append(f'<text x="{pad + 12}" y="{y + 20}" font-weight="700" fill="#1b2430">{escape(l0["name"])}</text>')
        bw = (w - 2 * pad - 24 - (len(items) - 1) * 10) / len(items)
        for i, x in enumerate(items):
            bx = pad + 12 + i * (bw + 10)
            stroke, dash = ("#a3312a", ' stroke-dasharray="5 3"') if not x["owner"] else ("#3b4652", "")
            o.append(f'<rect x="{bx:.0f}" y="{y + 30}" width="{bw:.0f}" height="50" rx="6" fill="#ffffff" stroke="{stroke}"{dash}/>')
            o.append(f'<text x="{bx + bw / 2:.0f}" y="{y + 51}" text-anchor="middle" font-weight="600" fill="#1b2430">{escape(x["id"])} · {escape(x["name"])}</text>')
            o.append(f'<text x="{bx + bw / 2:.0f}" y="{y + 69}" text-anchor="middle" font-size="11" fill="#5b6675">{escape(x["owner"] or "geen eigenaar")}</text>')
        y += row_h + 12
    o.append("</svg>")
    return "\n".join(o) + "\n"


def svg_capabilities() -> str:
    counts: dict[str, int] = {}
    for p in active():
        for c in p["capabilities"]:
            counts[c] = counts.get(c, 0) + 1
    fills = {"ok": ("#e3f1e9", "#1e7b4f"), "gap": ("#fbf0dc", "#9a5b00"), "missing": ("#f8e1df", "#a3312a")}
    col_w, gap, cell_h, head_h, cols = 190, 12, 46, 34, 6
    groups = CAT["capabilities"]
    rows = [groups[i:i + cols] for i in range(0, len(groups), cols)]
    heights = [head_h + max(len(g["children"]) for g in r) * (cell_h + 6) + 8 for r in rows]
    w = cols * col_w + (cols + 1) * gap
    h = 40 + sum(heights) + gap * len(rows) + 40
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
         f'aria-label="Capability map Corvent met ondersteuning door systemen" {FONT} font-size="12">',
         f'<rect width="{w}" height="{h}" fill="#ffffff"/>',
         f'<text x="{gap}" y="26" font-weight="700" font-size="15" fill="#1b2430">Capability map (L1–L2) — kleur = ondersteuning door systemen, getal = aantal L2-processen</text>']
    y = 40
    for r, rh in zip(rows, heights):
        for i, g in enumerate(r):
            x = gap + i * (col_w + gap)
            o.append(f'<rect x="{x}" y="{y}" width="{col_w}" height="{rh}" rx="8" fill="#f4f6f9" stroke="#c9d1db"/>')
            o.append(f'<text x="{x + 10}" y="{y + 22}" font-weight="700" fill="#1b2430">{escape(g["id"])} {escape(g["name"])}</text>')
            for j, c in enumerate(g["children"]):
                cy = y + head_h + j * (cell_h + 6)
                fill, stroke = fills[c["support"]]
                o.append(f'<rect x="{x + 8}" y="{cy}" width="{col_w - 16}" height="{cell_h}" rx="6" fill="{fill}" stroke="{stroke}"/>')
                o.append(f'<text x="{x + 16}" y="{cy + 19}" font-weight="600" fill="#1b2430">{escape(c["name"])}</text>')
                o.append(f'<text x="{x + 16}" y="{cy + 36}" font-size="11" fill="#5b6675">{escape(c["id"])} · {counts.get(c["id"], 0)} proces(sen)</text>')
        y += rh + gap
    legend = [("ok", "goed ondersteund"), ("gap", "deels / Excel"), ("missing", "niet ondersteund")]
    for i, (k, label) in enumerate(legend):
        fill, stroke = fills[k]
        o.append(f'<rect x="{gap + i * 190}" y="{y + 6}" width="16" height="16" rx="3" fill="{fill}" stroke="{stroke}"/>'
                 f'<text x="{gap + i * 190 + 22}" y="{y + 19}" fill="#1b2430">{label}</text>')
    o.append(f'<text x="{w - gap}" y="{y + 19}" text-anchor="end" font-size="11" fill="#5b6675">Illustrative assumption — not real company data</text>')
    o.append("</svg>")
    return "\n".join(o) + "\n"


def svg_value_chain(l1_id: str) -> str:
    l1 = next(x for x in CAT["l1"] if x["id"] == l1_id)
    procs = [p for p in CAT["processes"] if p["l1"] == l1_id and p["status"] != "retired"]
    bw, bh, tip, gap = 170, 74, 18, 6
    w = len(procs) * (bw + gap) + tip + 32
    h = bh + 110
    colour = {"released": "#1e7b4f", "in-review": "#1f4e79", "draft": "#9a5b00", "geen-model": "#a3312a"}
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
         f'aria-label="{escape(l1["id"])} {escape(l1["name"])} als waardeketen" {FONT} font-size="12">',
         f'<rect width="{w}" height="{h}" fill="#ffffff"/>',
         f'<text x="16" y="24" font-weight="700" font-size="15" fill="#1b2430">{escape(l1["id"])} · {escape(l1["name"])} — {escape(l1["nl"])} (L1 → L2)</text>',
         f'<text x="16" y="44" font-size="12" fill="#5b6675">Eigenaar L1: {escape(l1["owner"] or "geen")} · kleur = status · stippellijn = geen eigenaar</text>']
    for i, p in enumerate(procs):
        x, y = 16 + i * (bw + gap), 58
        notch = tip if i else 0
        d = f"M{x},{y} L{x + bw},{y} L{x + bw + tip},{y + bh / 2} L{x + bw},{y + bh} L{x},{y + bh} L{x + notch},{y + bh / 2} z"
        dash = ' stroke-dasharray="6 3"' if not p["owner"] else ""
        o.append(f'<path d="{d}" fill="#ffffff" stroke="{colour[p["status"]]}" stroke-width="2"{dash}/>')
        o.append(f'<text x="{x + bw / 2 + 6}" y="{y + 26}" text-anchor="middle" font-weight="700" fill="#1b2430">{escape(p["id"])}</text>')
        words, lines, line = p["name"].split(), [], ""
        for word in words:
            if len(line) + len(word) + 1 > 20 and line:
                lines.append(line)
                line = word
            else:
                line = f"{line} {word}".strip()
        lines.append(line)
        for j, text in enumerate(lines[:2]):
            o.append(f'<text x="{x + bw / 2 + 6}" y="{y + 44 + j * 14}" text-anchor="middle" fill="#1b2430">{escape(text)}</text>')
        o.append(f'<text x="{x + bw / 2 + 6}" y="{y + bh + 18}" text-anchor="middle" font-size="11" fill="{colour[p["status"]]}">{STATUS_LABEL[p["status"]]}</text>')
    o.append("</svg>")
    return "\n".join(o) + "\n"


def main() -> None:
    cov = coverage()
    outputs = {
        "docs/02-architecture/procescatalogus.md": markdown(cov) + "\n",
        "site/data/catalog.json": json.dumps({**CAT, "coverage": cov}, ensure_ascii=False, indent=1) + "\n",
        "site/assets/models/proceshuis.svg": svg_house(),
        "site/assets/models/capability-map.svg": svg_capabilities(),
        "site/assets/models/otc-waardeketen.svg": svg_value_chain("OTC"),
    }
    for rel, text in outputs.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(f"wrote {rel}")
    print(f"coverage: {cov['l2']} L2, {cov['owned']} with owner, {cov['released']} released")


if __name__ == "__main__":
    main()

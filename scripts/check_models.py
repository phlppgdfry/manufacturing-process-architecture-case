#!/usr/bin/env python3
"""Check BPMN models and the process catalogue against the Corvent modelling convention.

The toetsbare regels uit docs/03-standards/kwaliteitschecklist.md (R01–R13 voor modellen, C01–C04 voor de catalogus)
staan hier als code. Handmatige regels (M01–M05) blijven bij de reviewer.

Usage:
  python3 scripts/check_models.py                    # check all models + catalogue, print a summary
  python3 scripts/check_models.py --report FILE      # also write the JSON report the site uses
  python3 scripts/check_models.py path/to/model.bpmn # check one model

Exit code 1 when a model that is not a draft (*.draft.bpmn) or the catalogue has an error.
Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog" / "catalog.json"
NS = {"bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL", "bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI"}
B = "{%s}" % NS["bpmn"]

# Palet (R06): alles wat hier niet staat, is niet toegelaten in een Corvent-model.
PALETTE = {
    "startEvent", "endEvent", "intermediateCatchEvent", "intermediateThrowEvent", "boundaryEvent",
    "task", "userTask", "serviceTask", "sendTask", "receiveTask", "manualTask", "businessRuleTask",
    "exclusiveGateway", "parallelGateway", "subProcess", "callActivity",
}
ACTIVITIES = {"task", "userTask", "serviceTask", "sendTask", "receiveTask", "manualTask", "businessRuleTask",
              "subProcess", "callActivity"}
GATEWAYS = {"exclusiveGateway", "parallelGateway", "inclusiveGateway", "complexGateway", "eventBasedGateway"}
FLOW_NODES = PALETTE | GATEWAYS | {"inclusiveGateway", "complexGateway", "eventBasedGateway", "transaction"}
REQUIRED_ATTRS = ("procesId", "niveau", "type", "eigenaar", "versie", "status")
MAX_ACTIVITIES = 20

# Gecontroleerde werkwoordenlijst (R03, C02): naam = object + werkwoord in de infinitief, het werkwoord staat achteraan.
VERBS = set("""
aanmaken aanpassen aanvaarden aanvragen aanwerven afhandelen afsluiten afstemmen afwijzen analyseren annuleren
archiveren beantwoorden behandelen beheren beloven beoordelen bepalen berekenen beslissen bestellen bevestigen bewaken
blokkeren boeken controleren corrigeren doorvoeren escaleren evalueren factureren goedkeuren herbekijken herplannen
heronderhandelen informeren inplannen invoeren keuren melden nakijken onboarden ontvangen ontwikkelen opnemen opslaan
opstellen opvolgen plannen produceren publiceren rapporteren registreren reviewen selecteren stockeren sturen
terugmelden tellen toetsen toewijzen uitleveren uitvoeren uitwerken valideren vastleggen verhelpen verwerken versturen
verwittigen verzamelen verzenden voorstellen vrijgeven wijzigen
""".split())


def load_catalog() -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def name_ok(label: str) -> bool:
    words = label.split()
    return 2 <= len(words) <= 7 and words[-1].lower() in VERBS


def local(tag: str) -> str:
    return tag.split("}", 1)[-1]


def parse_doc(process: ET.Element) -> dict:
    doc = process.find("bpmn:documentation", NS)
    if doc is None or not (doc.text or "").strip():
        return {}
    attrs = {}
    for line in doc.text.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            attrs[key.strip()] = value.strip()
    return attrs


def finding(rule: str, message: str, element: str = "") -> dict:
    return {"rule": rule, "element": element, "message": message}


def check_model(path: Path, catalog: dict) -> dict:
    tree = ET.parse(path)
    root = tree.getroot()
    processes = root.findall("bpmn:process", NS)
    findings: list[dict] = []
    attrs: dict = {}
    roles = set(catalog["roles"]) | {s["name"] for s in catalog["systems"]}
    procs = {p["id"]: p for p in catalog["processes"]}
    di_ids = {s.get("bpmnElement") for s in root.iter() if local(s.tag) in ("BPMNShape", "BPMNEdge")}

    for process in processes:
        attrs = parse_doc(process)
        nodes = {el.get("id"): el for el in process if local(el.tag) in FLOW_NODES}
        names = {nid: (el.get("name") or "").strip() for nid, el in nodes.items()}
        kinds = {nid: local(el.tag) for nid, el in nodes.items()}
        flows = [el for el in process if local(el.tag) == "sequenceFlow"]
        out_flows: dict[str, list[ET.Element]] = {}
        for f in flows:
            out_flows.setdefault(f.get("sourceRef"), []).append(f)
        # boundary events continue the token of their activity
        attached = {nid: el.get("attachedToRef") for nid, el in nodes.items() if kinds[nid] == "boundaryEvent"}

        # R01 — exactly one start event
        starts = [n for n, k in kinds.items() if k == "startEvent"]
        if len(starts) != 1:
            findings.append(finding("R01", f"{len(starts)} startevents; verwacht precies 1"))

        # R02 — every node lies on a path from the start to an end event
        succ = {n: [f.get("targetRef") for f in out_flows.get(n, [])] for n in nodes}
        for b, act in attached.items():
            succ.setdefault(act, []).append(b)
        reach, stack = set(), list(starts)
        while stack:
            n = stack.pop()
            if n in reach:
                continue
            reach.add(n)
            stack += succ.get(n, [])
        pred: dict[str, list[str]] = {}
        for n, targets in succ.items():
            for t in targets:
                pred.setdefault(t, []).append(n)
        ends = [n for n, k in kinds.items() if k == "endEvent"]
        co_reach, stack = set(), list(ends)
        while stack:
            n = stack.pop()
            if n in co_reach:
                continue
            co_reach.add(n)
            stack += pred.get(n, [])
        for n in nodes:
            if n not in reach:
                findings.append(finding("R02", "niet bereikbaar vanaf het startevent", names[n] or n))
            elif n not in co_reach:
                findings.append(finding("R02", "pad eindigt niet in een eindevent (losse draad)", names[n] or n))

        # R03 — activity names: object + infinitive from the verb list, 2–7 words
        for n, k in kinds.items():
            if k in ACTIVITIES and not name_ok(names[n]):
                findings.append(finding("R03", "taaknaam is geen 'object + werkwoord' uit de werkwoordenlijst", names[n] or n))

        # R04 / R05 — diverging gateways: name is a question, outgoing flows are labelled
        for n, k in kinds.items():
            if k in GATEWAYS and k != "parallelGateway" and len(out_flows.get(n, [])) > 1:
                if not names[n].endswith("?"):
                    findings.append(finding("R04", "splitsende gateway heeft geen vraag als naam", names[n] or n))
                unlabelled = [f for f in out_flows[n] if not (f.get("name") or "").strip()]
                if unlabelled:
                    findings.append(finding("R05", f"{len(unlabelled)} uitgaande flow(s) zonder label", names[n] or n))

        # R06 — palette only
        for n, k in kinds.items():
            if k not in PALETTE:
                findings.append(finding("R06", f"element '{k}' staat niet in het palet", names[n] or n))

        # R07 / R11 — every node in a lane; lanes are roles or systems, not people
        in_lane = set()
        for lane in process.iter(B + "lane"):
            in_lane |= {ref.text for ref in lane.findall("bpmn:flowNodeRef", NS)}
            if lane.get("name") not in roles:
                findings.append(finding("R11", "lane is geen rol of systeem uit de rollenlijst", lane.get("name") or lane.get("id")))
        for n in nodes:
            if n not in in_lane:
                findings.append(finding("R07", "element ligt niet in een lane", names[n] or n))

        # R08 — size
        n_act = sum(1 for k in kinds.values() if k in ACTIVITIES)
        if n_act > MAX_ACTIVITIES:
            findings.append(finding("R08", f"{n_act} activiteiten; maximum {MAX_ACTIVITIES} — splits in subprocessen"))

        # R09 — required attributes, consistent with the catalogue
        missing = [a for a in REQUIRED_ATTRS if not attrs.get(a)]
        if missing:
            findings.append(finding("R09", "verplichte attributen ontbreken: " + ", ".join(missing)))
        else:
            proc = procs.get(attrs["procesId"])
            if proc is None:
                findings.append(finding("R09", f"procesId {attrs['procesId']} staat niet in de catalogus"))
            elif attrs["type"] == "as-is":
                if attrs["status"] != "as-is":
                    findings.append(finding("R09", "een as-is-model heeft status 'as-is'"))
            else:
                if attrs["status"] != proc["status"]:
                    findings.append(finding("R09", f"status '{attrs['status']}' ≠ catalogus '{proc['status']}'"))
                if attrs["status"] == "released" and attrs["eigenaar"] != proc.get("owner"):
                    findings.append(finding("R09", f"eigenaar '{attrs['eigenaar']}' ≠ catalogus '{proc.get('owner')}'"))

        # R10 — end events describe a state
        for n in ends:
            if not names[n]:
                findings.append(finding("R10", "eindevent zonder naam", n))

        # R12 — diagram interchange for every element, so the model renders in any tool
        no_di = [n for n in nodes if n not in di_ids] + [f.get("id") for f in flows if f.get("id") not in di_ids]
        if no_di:
            findings.append(finding("R12", f"{len(no_di)} element(en) zonder diagraminformatie"))

        # R13 — a to-be model shows at least one exception path
        if attrs.get("type") == "to-be" and len(ends) < 2 and not attached:
            findings.append(finding("R13", "to-be zonder uitzonderingspad (1 eindevent, geen boundary event)"))

    rel = path.relative_to(ROOT).as_posix()
    return {
        "file": rel,
        "draft": rel.endswith(".draft.bpmn"),
        "procesId": attrs.get("procesId", ""),
        "type": attrs.get("type", ""),
        "title": processes[0].get("name", "") if processes else "",
        "findings": findings,
        "rules": sorted({f["rule"] for f in findings}),
    }


def check_catalog(catalog: dict, today: date) -> dict:
    errors, warnings = [], []
    l1 = {x["id"]: x for x in catalog["l1"]}
    caps = {c["id"] for group in catalog["capabilities"] for c in group["children"]}
    systems = {s["id"] for s in catalog["systems"]}
    seen: dict[str, str] = {}
    for p in catalog["processes"]:
        pid = p["id"]
        # C01 — references exist
        if p["l1"] not in l1:
            errors.append(finding("C01", f"L1 '{p['l1']}' bestaat niet", pid))
        for c in p["capabilities"]:
            if c not in caps:
                errors.append(finding("C01", f"capability '{c}' bestaat niet", pid))
        for s in p["systems"]:
            if s not in systems:
                errors.append(finding("C01", f"systeem '{s}' bestaat niet", pid))
        if p["status"] not in catalog["meta"]["statuses"]:
            errors.append(finding("C01", f"onbekende status '{p['status']}'", pid))
        # C02 — process names follow the naming rule
        if not name_ok(p["name"]):
            errors.append(finding("C02", f"naam '{p['name']}' is geen 'object + werkwoord'", pid))
        # C03 — released means owner, version, review date and model
        if p["status"] == "released":
            for field in ("owner", "version", "review", "model"):
                if not p.get(field):
                    errors.append(finding("C03", f"released zonder {field}", pid))
        if p["status"] == "retired":
            continue
        # C04 — governance gaps (warnings: they are the work list, not a build failure)
        if not p.get("owner"):
            warnings.append(finding("C04", "geen eigenaar", pid))
        if p.get("review") and date.fromisoformat(p["review"]) < today:
            warnings.append(finding("C04", f"reviewdatum {p['review']} verstreken", pid))
        key = p["name"].lower()
        if key in seen:
            warnings.append(finding("C04", f"zelfde naam als {seen[key]}", pid))
        seen[key] = pid
    for x in catalog["l1"]:
        if not x.get("owner"):
            warnings.append(finding("C04", "L1 zonder eigenaar", x["id"]))
    return {"errors": errors, "warnings": warnings}


def model_files() -> list[Path]:
    return sorted(p for p in (ROOT / "docs").rglob("*.bpmn"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("models", nargs="*", type=Path)
    parser.add_argument("--report", type=Path, help="write the JSON report to this file")
    parser.add_argument("--today", default=None, help="reference date for review checks (YYYY-MM-DD)")
    args = parser.parse_args(argv)

    catalog = load_catalog()
    as_of = date.fromisoformat(args.today or catalog["meta"]["asOf"])
    files = [p.resolve() for p in args.models] or model_files()
    results = [check_model(p, catalog) for p in files]
    cat = check_catalog(catalog, as_of)

    failed = False
    for r in results:
        state = "OK  " if not r["findings"] else ("DRAFT" if r["draft"] else "FAIL")
        failed |= bool(r["findings"]) and not r["draft"]
        print(f"{state} {r['file']}  ({len(r['findings'])} bevinding(en){': ' + ', '.join(r['rules']) if r['rules'] else ''})")
        for f in r["findings"]:
            print(f"       {f['rule']}  {f['element'] + ' — ' if f['element'] else ''}{f['message']}")
    print(f"catalogus: {len(cat['errors'])} fout(en), {len(cat['warnings'])} waarschuwing(en)")
    for f in cat["errors"]:
        print(f"  FOUT {f['rule']}  {f['element']} — {f['message']}")
    failed |= bool(cat["errors"])

    if args.report:
        report = {
            "asOf": as_of.isoformat(),
            "convention": "docs/03-standards/kwaliteitschecklist.md",
            "models": results,
            "catalog": cat,
            "summary": {
                "models": len(results),
                "passing": sum(1 for r in results if not r["findings"]),
                "drafts": sum(1 for r in results if r["draft"]),
                "catalogErrors": len(cat["errors"]),
                "catalogWarnings": len(cat["warnings"]),
            },
        }
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Build the process models as BPMN 2.0 XML (with diagram interchange) and SVG.

The models are small Python structures so a change shows up as a readable diff in review.
Each model writes:
  <file>.bpmn                      opens in Camunda Modeler, bpmn.io or any BPMN 2.0 tool
  site/assets/models/<name>.svg    rendered for the site and the Markdown docs
Files ending in .draft.bpmn are work in progress: scripts/check_models.py reports them but they may fail.
Run: python3 scripts/build_models.py
"""
from __future__ import annotations

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANE_H, COL_W, HEADER_W, LEFT_PAD = 130, 158, 34, 30
TASK_W, TASK_H, EVENT, GATE = 118, 66, 36, 50
NS = "https://github.com/phlppgdfry/manufacturing-process-architecture-case"

# Node: (id, kind, lane, column, label). Boundary event: (id, "timerBoundary", attached_task_id, "top" | "bottom", label).
# Flow: (source, target, label[, route]) with route "gap" (default), "vh" (vertical first) or "hv" (horizontal first).

OTC02_AS_IS = {
    "name": "otc-02-as-is",
    "file": "docs/04-reference-model/bpmn/otc-02-as-is.bpmn",
    "title": "OTC-02 Order aanvaarden — as-is (vandaag)",
    "doc": {"procesId": "OTC-02", "niveau": "L3", "type": "as-is", "eigenaar": "Customer service manager",
            "versie": "0.9", "status": "as-is", "gevalideerd": "2026-09-24, workshop met customer service en planning"},
    "lanes": [("cs", "Customer service"), ("am", "Accountmanager"), ("credit", "Credit controller"),
              ("planner", "Planner"), ("erp", "ERP")],
    "nodes": [
        ("start", "messageStart", "cs", 0, "Order ontvangen (mail, telefoon, EDI)"),
        ("t_enter", "userTask", "cs", 1, "Order manueel invoeren"),
        ("g_cfg", "xor", "cs", 2, "Klantspecifieke uitvoering?"),
        ("t_excel", "userTask", "am", 3, "Configuratie in Excel uitwerken"),
        ("t_promise", "userTask", "am", 4, "Leverdatum telefonisch beloven"),
        ("t_confirm", "sendTask", "cs", 5, "Orderbevestiging versturen"),
        ("t_mailcredit", "userTask", "cs", 6, "Kredietcheck per mail aanvragen"),
        ("t_check", "userTask", "credit", 7, "Krediet manueel controleren"),
        ("g_ok", "xor", "credit", 8, "Krediet in orde?"),
        ("t_block", "userTask", "credit", 9, "Order blokkeren en sales verwittigen"),
        ("end_blocked", "end", "credit", 10, "Order geblokkeerd na bevestiging"),
        ("t_release", "serviceTask", "erp", 9, "Order voor planning vrijgeven"),
        ("t_plan", "userTask", "planner", 10, "Order inplannen en datum stil aanpassen"),
        ("end", "end", "planner", 11, "Order ingepland"),
    ],
    "flows": [
        ("start", "t_enter", ""), ("t_enter", "g_cfg", ""), ("g_cfg", "t_excel", "ja", "vh"), ("g_cfg", "t_promise", "nee", "hv"),
        ("t_excel", "t_promise", ""), ("t_promise", "t_confirm", ""), ("t_confirm", "t_mailcredit", ""), ("t_mailcredit", "t_check", ""),
        ("t_check", "g_ok", ""), ("g_ok", "t_release", "ja", "vh"), ("g_ok", "t_block", "nee"), ("t_block", "end_blocked", ""),
        ("t_release", "t_plan", ""), ("t_plan", "end", ""),
    ],
    "pain": {"t_promise": "P1", "t_check": "P2", "t_plan": "P3", "t_confirm": "P4", "t_excel": "P5"},
}

OTC02_TO_BE = {
    "name": "otc-02-to-be",
    "file": "docs/04-reference-model/bpmn/otc-02-to-be.bpmn",
    "title": "OTC-02 Order aanvaarden — to-be v1.0",
    "doc": {"procesId": "OTC-02", "niveau": "L3", "type": "to-be", "eigenaar": "Customer service manager",
            "versie": "1.0", "status": "in-review", "volgt": "OTC-03 Leverdatum bevestigen"},
    "lanes": [("cs", "Customer service"), ("am", "Accountmanager"), ("credit", "Credit controller"), ("erp", "ERP")],
    "nodes": [
        ("start", "messageStart", "cs", 0, "Order ontvangen (portaal, EDI, mail)"),
        ("t_register", "userTask", "cs", 1, "Order registreren en volledigheid controleren"),
        ("g_cfg", "xor", "cs", 2, "Klantspecifieke uitvoering?"),
        ("t_configure", "userTask", "am", 3, "Configuratie in productconfigurator vastleggen"),
        ("t_credit", "serviceTask", "erp", 4, "Kredietlimiet automatisch controleren"),
        ("g_limit", "xor", "erp", 5, "Binnen kredietlimiet?"),
        ("t_review", "userTask", "credit", 6, "Kredietuitzondering beoordelen"),
        ("b_4h", "timerBoundary", "t_review", "top", "4 werkuren zonder beslissing"),
        ("t_inform", "sendTask", "cs", 7, "Klant over wachttijd informeren"),
        ("end_inf", "end", "cs", 8, "Klant geïnformeerd"),
        ("g_approved", "xor", "credit", 7, "Krediet goedgekeurd?"),
        ("t_renegotiate", "userTask", "am", 8, "Betaalvoorwaarden met klant heronderhandelen"),
        ("end_rej", "end", "am", 9, "Order niet aanvaard"),
        ("t_accept", "serviceTask", "erp", 9, "Order aanvaarden en vrijgeven"),
        ("end_ok", "end", "erp", 10, "Order aanvaard (naar OTC-03)"),
    ],
    "flows": [
        ("start", "t_register", ""), ("t_register", "g_cfg", ""), ("g_cfg", "t_configure", "ja", "vh"), ("g_cfg", "t_credit", "nee", "hv"),
        ("t_configure", "t_credit", ""), ("t_credit", "g_limit", ""), ("g_limit", "t_accept", "ja"), ("g_limit", "t_review", "nee", "vh"),
        ("t_review", "g_approved", ""), ("b_4h", "t_inform", "", "vh"), ("t_inform", "end_inf", ""),
        ("g_approved", "t_accept", "ja", "hv"), ("g_approved", "t_renegotiate", "nee", "vh"), ("t_renegotiate", "end_rej", ""),
        ("t_accept", "end_ok", ""),
    ],
    "fixes": {"t_configure": "P5", "t_credit": "P2", "t_accept": "P4", "end_ok": "P1 P3"},
}

OTC03_DRAFT = {
    "name": "otc-03-draft",
    "file": "docs/05-review/bpmn/otc-03.draft.bpmn",
    "title": "Leverdatum (draft analist)",
    "doc": None,  # the draft has no attributes: one of the review findings
    "lanes": [("planner", "Jan (planning)"), ("sales", "Sales"), ("erp", "ERP")],
    "nodes": [
        ("start", "start", "planner", 0, "Order in ERP"),
        ("t1", "userTask", "planner", 1, "Capaciteitscheck"),
        ("g1", "or", "planner", 2, "Check"),
        ("t3", "userTask", "planner", 3, "Datum aanpassen"),
        ("t4", "serviceTask", "erp", 3, "Leverdatum in ERP registreren"),
        ("t2", "userTask", "sales", 4, "Mail naar klant"),
        ("end", "end", "sales", 5, "Klant ingelicht"),
    ],
    "flows": [
        ("start", "t1", ""), ("t1", "g1", ""), ("g1", "t3", ""), ("g1", "t4", ""), ("t4", "t2", ""), ("t2", "end", ""),
    ],
}

OTC03_TO_BE = {
    "name": "otc-03-to-be",
    "file": "docs/05-review/bpmn/otc-03-to-be.bpmn",
    "title": "OTC-03 Leverdatum bevestigen — to-be v1.0 (na review)",
    "doc": {"procesId": "OTC-03", "niveau": "L3", "type": "to-be", "eigenaar": "open (voorstel D-03: Supply chain director)",
            "versie": "1.0", "status": "in-review", "volgt op": "OTC-02 Order aanvaarden", "volgt": "OTC-04 Order uitleveren"},
    "lanes": [("cs", "Customer service"), ("am", "Accountmanager"), ("planner", "Planner"), ("erp", "ERP")],
    "nodes": [
        ("start", "start", "erp", 0, "Order aanvaard (uit OTC-02)"),
        ("t_atp", "serviceTask", "erp", 1, "Haalbare leverdatum voorstellen"),
        ("g_std", "xor", "erp", 2, "Binnen standaard levertermijn?"),
        ("t_assess", "userTask", "planner", 3, "Haalbaarheid met productie afstemmen"),
        ("g_feas", "xor", "planner", 4, "Gevraagde datum haalbaar?"),
        ("t_negotiate", "userTask", "am", 5, "Alternatieve datum met klant afstemmen"),
        ("g_acc", "xor", "am", 6, "Klant akkoord?"),
        ("t_cancel", "userTask", "cs", 7, "Order in overleg annuleren"),
        ("end_cancel", "end", "cs", 8, "Order geannuleerd"),
        ("t_register", "serviceTask", "erp", 8, "Bevestigde leverdatum vastleggen"),
        ("t_send", "sendTask", "cs", 10, "Orderbevestiging met leverdatum versturen"),
        ("end_ok", "end", "cs", 11, "Leverdatum bevestigd (naar OTC-04)"),
    ],
    "flows": [
        ("start", "t_atp", ""), ("t_atp", "g_std", ""), ("g_std", "t_register", "ja"), ("g_std", "t_assess", "nee", "vh"),
        ("t_assess", "g_feas", ""), ("g_feas", "t_register", "ja", "hv"), ("g_feas", "t_negotiate", "nee", "vh"),
        ("t_negotiate", "g_acc", ""), ("g_acc", "t_register", "ja"), ("g_acc", "t_cancel", "nee", "vh"),
        ("t_cancel", "end_cancel", ""), ("t_register", "t_send", ""), ("t_send", "end_ok", ""),
    ],
    "fixes": {"t_atp": "P1", "t_register": "P3", "t_send": "P4"},
}

STE04_CHANGE = {
    "name": "ste-04-proceswijziging",
    "file": "docs/06-governance/bpmn/ste-04-proceswijziging.bpmn",
    "title": "STE-04 Proceswijziging doorvoeren — v1.0",
    "doc": {"procesId": "STE-04", "niveau": "L3", "type": "to-be", "eigenaar": "COO", "versie": "1.0", "status": "released",
            "besluit": "procesraad #1, D-01"},
    "lanes": [("steward", "Process steward"), ("analyst", "Business process analyst"), ("architect", "Process architect"),
              ("owner", "Proceseigenaar"), ("raad", "Procesraad"), ("cat", "Procescatalogus")],
    "nodes": [
        ("start", "start", "steward", 0, "Wijziging nodig (project, audit of verbetering)"),
        ("t_request", "userTask", "steward", 1, "Wijzigingsverzoek registreren"),
        ("t_model", "userTask", "analyst", 2, "Model volgens conventie aanpassen"),
        ("t_check", "serviceTask", "cat", 3, "Model automatisch toetsen"),
        ("g_pass", "xor", "cat", 4, "Alle checks geslaagd?"),
        ("t_review", "userTask", "architect", 5, "Model reviewen"),
        ("g_level", "xor", "architect", 6, "Raakt L1 of een overdracht?"),
        ("t_approve", "userTask", "owner", 7, "Wijziging goedkeuren"),
        ("t_raad", "userTask", "raad", 7, "Wijziging in procesraad beslissen"),
        ("g_ok", "xor", "raad", 8, "Goedgekeurd?"),
        ("end_rej", "end", "raad", 9, "Wijziging afgewezen"),
        ("t_release", "serviceTask", "cat", 9, "Nieuwe versie publiceren"),
        ("end_ok", "end", "cat", 10, "Versie released, vorige versie retired"),
    ],
    "flows": [
        ("start", "t_request", ""), ("t_request", "t_model", ""), ("t_model", "t_check", "", "vh"), ("t_check", "g_pass", ""),
        ("g_pass", "t_review", "ja", "hv"), ("g_pass", "t_model", "nee", "vh"), ("t_review", "g_level", ""),
        ("g_level", "t_raad", "ja", "vh"), ("g_level", "t_approve", "nee", "hv"), ("t_raad", "g_ok", ""),
        ("g_ok", "end_rej", "nee"), ("g_ok", "t_release", "ja", "vh"), ("t_approve", "t_release", ""), ("t_release", "end_ok", ""),
    ],
}

MODELS = [OTC02_AS_IS, OTC02_TO_BE, OTC03_DRAFT, OTC03_TO_BE, STE04_CHANGE]

TAGS = {
    "messageStart": "startEvent", "start": "startEvent", "end": "endEvent", "task": "task", "userTask": "userTask",
    "serviceTask": "serviceTask", "sendTask": "sendTask", "manualTask": "manualTask", "xor": "exclusiveGateway",
    "and": "parallelGateway", "or": "inclusiveGateway", "timerBoundary": "boundaryEvent",
}
EVENTS = {"messageStart", "start", "end", "timerBoundary"}
GATEWAYS = {"xor", "and", "or"}


def size(kind: str) -> tuple[int, int]:
    if kind in EVENTS:
        return EVENT, EVENT
    if kind in GATEWAYS:
        return GATE, GATE
    return TASK_W, TASK_H


def layout(model: dict) -> dict:
    lanes = {lane_id: i for i, (lane_id, _) in enumerate(model["lanes"])}
    boxes = {}
    for node_id, kind, lane, col, _ in model["nodes"]:
        if kind == "timerBoundary":
            continue
        w, h = size(kind)
        cx = HEADER_W + LEFT_PAD + col * COL_W + TASK_W / 2
        cy = lanes[lane] * LANE_H + LANE_H / 2
        boxes[node_id] = (cx - w / 2, cy - h / 2, w, h)
    for node_id, kind, attached, edge, _ in model["nodes"]:
        if kind == "timerBoundary":
            x, y, w, h = boxes[attached]
            cx, cy = x + w * 0.75, (y if edge == "top" else y + h)
            boxes[node_id] = (cx - EVENT / 2, cy - EVENT / 2, EVENT, EVENT)
    return boxes


def waypoints(a: tuple, b: tuple, route: str = "gap") -> list[tuple[float, float]]:
    """Orthogonal routing. 'gap': leave right, turn in the gap between columns. 'vh': leave vertically, enter the target from the side.
    'hv': run along the source lane, enter the target vertically."""
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    acx, acy, bcx, bcy = ax + aw / 2, ay + ah / 2, bx + bw / 2, by + bh / 2
    if abs(acy - bcy) < 1:
        return [(ax + aw, acy), (bx, bcy)] if bcx > acx else [(ax, acy), (bx + bw, bcy)]
    if abs(acx - bcx) < 1:
        return [(acx, ay + ah), (bcx, by)] if bcy > acy else [(acx, ay), (bcx, by + bh)]
    if route == "vh":
        side = bx if bcx > acx else bx + bw
        return [(acx, ay + ah if bcy > acy else ay), (acx, bcy), (side, bcy)]
    if route == "hv":
        return [(ax + aw, acy), (bcx, acy), (bcx, by if bcy > acy else by + bh)]
    gap = bx - (COL_W - TASK_W) / 2 if bcx > acx else bx + bw + (COL_W - TASK_W) / 2
    return [(ax + aw, acy), (gap, acy), (gap, bcy), (bx, bcy)]


def columns(model: dict) -> int:
    return max(n[3] for n in model["nodes"] if n[1] != "timerBoundary") + 1


def bpmn_xml(model: dict, boxes: dict) -> str:
    mid = model["name"].replace("-", "_")
    pid = f"Process_{mid}"
    width = HEADER_W + LEFT_PAD * 2 + columns(model) * COL_W
    height = LANE_H * len(model["lanes"])
    lane_of = {n[0]: n[2] for n in model["nodes"] if n[1] != "timerBoundary"}
    for n in model["nodes"]:
        if n[1] == "timerBoundary":
            lane_of[n[0]] = lane_of[n[2]]
    incoming, outgoing = {}, {}
    for i, (s, t, *_) in enumerate(model["flows"]):
        outgoing.setdefault(s, []).append(f"Flow_{i}")
        incoming.setdefault(t, []).append(f"Flow_{i}")

    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" '
           'xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" '
           'xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" '
           f'id="Defs_{mid}" targetNamespace="{NS}" exporter="build_models.py" exporterVersion="1">',
           f'  <bpmn:collaboration id="Collab_{mid}">',
           f'    <bpmn:participant id="Pool_{mid}" name="{escape(model["title"])}" processRef="{pid}" />',
           '  </bpmn:collaboration>',
           f'  <bpmn:process id="{pid}" name="{escape(model["title"])}" isExecutable="false">']
    if model.get("doc"):
        lines = "\n".join(f"{k}: {v}" for k, v in model["doc"].items())
        out.append(f'    <bpmn:documentation>{escape(lines)}</bpmn:documentation>')
    out.append(f'    <bpmn:laneSet id="LaneSet_{mid}">')
    for lane_id, lane_name in model["lanes"]:
        out.append(f'      <bpmn:lane id="Lane_{lane_id}" name="{escape(lane_name)}">')
        out += [f'        <bpmn:flowNodeRef>{n[0]}</bpmn:flowNodeRef>' for n in model["nodes"] if lane_of[n[0]] == lane_id]
        out.append('      </bpmn:lane>')
    out.append('    </bpmn:laneSet>')
    for node_id, kind, extra, edge, label in model["nodes"]:
        tag = TAGS[kind]
        attrs = f' attachedToRef="{extra}" cancelActivity="false"' if kind == "timerBoundary" else ""
        out.append(f'    <bpmn:{tag} id="{node_id}" name="{escape(label)}"{attrs}>')
        out += [f'      <bpmn:incoming>{f}</bpmn:incoming>' for f in incoming.get(node_id, [])]
        out += [f'      <bpmn:outgoing>{f}</bpmn:outgoing>' for f in outgoing.get(node_id, [])]
        if kind == "messageStart":
            out.append(f'      <bpmn:messageEventDefinition id="Msg_{node_id}" />')
        if kind == "timerBoundary":
            out.append(f'      <bpmn:timerEventDefinition id="Timer_{node_id}" />')
        out.append(f'    </bpmn:{tag}>')
    for i, (s, t, label, *_) in enumerate(model["flows"]):
        name = f' name="{escape(label)}"' if label else ""
        out.append(f'    <bpmn:sequenceFlow id="Flow_{i}"{name} sourceRef="{s}" targetRef="{t}" />')
    out.append('  </bpmn:process>')
    out.append(f'  <bpmndi:BPMNDiagram id="Diagram_{mid}">')
    out.append(f'    <bpmndi:BPMNPlane id="Plane_{mid}" bpmnElement="Collab_{mid}">')
    out.append(f'      <bpmndi:BPMNShape id="Pool_{mid}_di" bpmnElement="Pool_{mid}" isHorizontal="true">')
    out.append(f'        <dc:Bounds x="0" y="0" width="{width}" height="{height}" />')
    out.append('      </bpmndi:BPMNShape>')
    for i, (lane_id, _) in enumerate(model["lanes"]):
        out.append(f'      <bpmndi:BPMNShape id="Lane_{lane_id}_di" bpmnElement="Lane_{lane_id}" isHorizontal="true">')
        out.append(f'        <dc:Bounds x="{HEADER_W}" y="{i * LANE_H}" width="{width - HEADER_W}" height="{LANE_H}" />')
        out.append('      </bpmndi:BPMNShape>')
    for node_id, kind, *_ in model["nodes"]:
        x, y, w, h = boxes[node_id]
        marker = ' isMarkerVisible="true"' if kind == "xor" else ""
        out.append(f'      <bpmndi:BPMNShape id="{node_id}_di" bpmnElement="{node_id}"{marker}>')
        out.append(f'        <dc:Bounds x="{x:.0f}" y="{y:.0f}" width="{w}" height="{h}" />')
        out.append('      </bpmndi:BPMNShape>')
    for i, (s, t, *rest) in enumerate(model["flows"]):
        out.append(f'      <bpmndi:BPMNEdge id="Flow_{i}_di" bpmnElement="Flow_{i}">')
        out += [f'        <di:waypoint x="{x:.0f}" y="{y:.0f}" />' for x, y in waypoints(boxes[s], boxes[t], *rest[1:])]
        out.append('      </bpmndi:BPMNEdge>')
    out += ['    </bpmndi:BPMNPlane>', '  </bpmndi:BPMNDiagram>', '</bpmn:definitions>', '']
    return "\n".join(out)


def wrap(label: str, width: int = 16) -> list[str]:
    words, lines, line = label.split(), [], ""
    for word in words:
        if len(line) + len(word) + 1 > width and line:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    return lines + [line]


def svg(model: dict, boxes: dict) -> str:
    width = HEADER_W + LEFT_PAD * 2 + columns(model) * COL_W + 60
    height = LANE_H * len(model["lanes"])
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-1 -12 {width + 2} {height + 14}" width="{width + 2}" height="{height + 14}" '
         f'role="img" aria-label="{escape(model["title"])}" font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif" font-size="12">',
         '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
         '<path d="M0,0 L10,5 L0,10 z" fill="#3b4652"/></marker></defs>',
         f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff" stroke="#3b4652"/>']
    for i, (_, lane_name) in enumerate(model["lanes"]):
        y = i * LANE_H
        fill = "#f4f6f9" if i % 2 else "#ffffff"
        o.append(f'<rect x="{HEADER_W}" y="{y}" width="{width - HEADER_W}" height="{LANE_H}" fill="{fill}" stroke="#c9d1db"/>')
        lines = wrap(lane_name, 18)
        for j, line in enumerate(lines):
            tx = HEADER_W / 2 + 4 + (j - (len(lines) - 1) / 2) * 13
            o.append(f'<text transform="translate({tx:.0f},{y + LANE_H / 2}) rotate(-90)" text-anchor="middle" font-weight="600" fill="#1b2430">{escape(line)}</text>')
    o.append(f'<line x1="{HEADER_W}" y1="0" x2="{HEADER_W}" y2="{height}" stroke="#3b4652"/>')
    for s, t, label, *route in model["flows"]:
        pts = waypoints(boxes[s], boxes[t], *route)
        d = " ".join(f"{'M' if j == 0 else 'L'}{x:.0f},{y:.0f}" for j, (x, y) in enumerate(pts))
        o.append(f'<path d="{d}" fill="none" stroke="#3b4652" stroke-width="1.3" marker-end="url(#arrow)"/>')
        if label:  # next to the gateway exit, as BPMN tools do
            (x1, y1), (x2, y2) = pts[0], pts[1]
            if abs(y1 - y2) < 1:
                lx, ly = (x1 + 8, y1 - 6) if x2 > x1 else (x1 - 8, y1 - 6)
                anchor = "start" if x2 > x1 else "end"
            else:
                lx, ly, anchor = x1 + 5, (y1 + 16 if y2 > y1 else y1 - 8), "start"
            o.append(f'<text x="{lx:.0f}" y="{ly:.0f}" text-anchor="{anchor}" font-size="11" fill="#5b6675">{escape(label)}</text>')
    marks = {**{k: ("#a3312a", v) for k, v in model.get("pain", {}).items()},
             **{k: ("#1e7b4f", v) for k, v in model.get("fixes", {}).items()}}
    # tasks and gateways first, so boundary events are drawn on top of their task
    ordered = sorted(model["nodes"], key=lambda n: n[1] == "timerBoundary")
    for node_id, kind, _, edge, label in ordered:
        x, y, w, h = boxes[node_id]
        cx, cy = x + w / 2, y + h / 2
        if kind in EVENTS:
            sw = 3 if kind == "end" else 1.5
            o.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{EVENT / 2}" fill="#fff" stroke="#1b2430" stroke-width="{sw}"/>')
            if kind == "timerBoundary":
                o.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{EVENT / 2 - 3}" fill="none" stroke="#1b2430" stroke-dasharray="4 3"/>'
                         f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="8" fill="none" stroke="#1b2430"/>'
                         f'<path d="M{cx:.0f},{cy - 6:.0f} L{cx:.0f},{cy:.0f} L{cx + 4:.0f},{cy + 2:.0f}" fill="none" stroke="#1b2430"/>')
                lines = wrap(label, 16)
                for j, line in enumerate(lines):
                    o.append(f'<text x="{x - 4:.0f}" y="{y + 6 - (len(lines) - 1 - j) * 13:.0f}" text-anchor="end" font-size="11" fill="#5b6675">{escape(line)}</text>')
                continue
            if kind == "messageStart":
                o.append(f'<rect x="{cx - 8:.0f}" y="{cy - 5:.0f}" width="16" height="11" fill="none" stroke="#1b2430"/>'
                         f'<path d="M{cx - 8:.0f},{cy - 5:.0f} L{cx:.0f},{cy + 1:.0f} L{cx + 8:.0f},{cy - 5:.0f}" fill="none" stroke="#1b2430"/>')
            for j, line in enumerate(wrap(label, 18)):
                if kind == "end":
                    o.append(f'<text x="{x + w + 6:.0f}" y="{cy - 2 + j * 13:.0f}" fill="#1b2430">{escape(line)}</text>')
                else:
                    o.append(f'<text x="{cx:.0f}" y="{y + h + 14 + j * 13:.0f}" text-anchor="middle" fill="#1b2430">{escape(line)}</text>')
        elif kind in GATEWAYS:
            o.append(f'<path d="M{cx:.0f},{y:.0f} L{x + w:.0f},{cy:.0f} L{cx:.0f},{y + h:.0f} L{x:.0f},{cy:.0f} z" fill="#fff" stroke="#1b2430" stroke-width="1.5"/>')
            if kind == "xor":
                o.append(f'<path d="M{cx - 8:.0f},{cy - 8:.0f} L{cx + 8:.0f},{cy + 8:.0f} M{cx + 8:.0f},{cy - 8:.0f} L{cx - 8:.0f},{cy + 8:.0f}" stroke="#1b2430" stroke-width="2.5"/>')
            elif kind == "and":
                o.append(f'<path d="M{cx:.0f},{cy - 11:.0f} L{cx:.0f},{cy + 11:.0f} M{cx - 11:.0f},{cy:.0f} L{cx + 11:.0f},{cy:.0f}" stroke="#1b2430" stroke-width="2.5"/>')
            else:
                o.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="10" fill="none" stroke="#1b2430" stroke-width="2.5"/>')
            lines = wrap(label, 14)
            for j, line in enumerate(lines):
                o.append(f'<text x="{cx - 10:.0f}" y="{y - 2 - (len(lines) - 1 - j) * 13:.0f}" text-anchor="end" fill="#1b2430">{escape(line)}</text>')
        else:
            o.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w}" height="{h}" rx="9" fill="#fff" stroke="#1b2430" stroke-width="1.5"/>')
            icon = {"userTask": "user", "serviceTask": "service", "sendTask": "send", "manualTask": "manual"}.get(kind)
            if icon:
                o.append(f'<text x="{x + w - 6:.0f}" y="{y + 13:.0f}" text-anchor="end" font-size="9" fill="#5b6675">{icon}</text>')
            lines = wrap(label, 17)
            small = len(lines) > 3 or max(len(line) for line in lines) > 17
            fs, lh = (10.5, 12) if small else (12, 14)
            for j, line in enumerate(lines):
                o.append(f'<text x="{cx:.0f}" y="{cy + 5 + (j - (len(lines) - 1) / 2) * lh:.0f}" text-anchor="middle" font-size="{fs}" fill="#1b2430">{escape(line)}</text>')
        if node_id in marks:
            colour, text = marks[node_id]
            bw = 8 + 7 * len(text)
            bx, by = (cx, y - 14) if kind in EVENTS else (x + bw / 2 + 4, y - 1)
            o.append(f'<rect x="{bx - bw / 2:.0f}" y="{by - 8:.0f}" width="{bw}" height="16" rx="8" fill="{colour}"/>'
                     f'<text x="{bx:.0f}" y="{by + 4:.0f}" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">{escape(text)}</text>')
    o.append('</svg>')
    return "\n".join(o) + "\n"


def main() -> None:
    for model in MODELS:
        boxes = layout(model)
        bpmn_path = ROOT / model["file"]
        svg_path = ROOT / "site/assets/models" / f"{model['name']}.svg"
        bpmn_path.parent.mkdir(parents=True, exist_ok=True)
        svg_path.parent.mkdir(parents=True, exist_ok=True)
        bpmn_path.write_text(bpmn_xml(model, boxes), encoding="utf-8")
        svg_path.write_text(svg(model, boxes), encoding="utf-8")
        print(f"wrote {bpmn_path.relative_to(ROOT)} and {svg_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

"""Tests for scripts/check_models.py — the automated part of the Corvent modelling convention.

Run: python3 -m unittest discover -s tests
"""
from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_models as cm  # noqa: E402

CATALOG = cm.load_catalog()


def model(body: str, doc: str | None = None, lanes: str = "", di: str | None = None) -> str:
    """Minimal BPMN 2.0 document around a process body."""
    documentation = f"<bpmn:documentation>{doc}</bpmn:documentation>" if doc else ""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
  xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" id="d" targetNamespace="t">
  <bpmn:process id="p" isExecutable="false">{documentation}{lanes}{body}</bpmn:process>
  <bpmndi:BPMNDiagram id="dg"><bpmndi:BPMNPlane id="pl" bpmnElement="p">{di or ""}</bpmndi:BPMNPlane></bpmndi:BPMNDiagram>
</bpmn:definitions>"""


def shapes(*ids: str) -> str:
    return "".join(f'<bpmndi:BPMNShape id="{i}_di" bpmnElement="{i}"/>' for i in ids)


DOC_OTC03 = "procesId: OTC-03\nniveau: L3\ntype: to-be\neigenaar: open\nversie: 1.0\nstatus: in-review"
LANE = '<bpmn:laneSet id="ls"><bpmn:lane id="l" name="Planner">{}</bpmn:lane></bpmn:laneSet>'


def simple(nodes: list[tuple[str, str, str]], flows: list[tuple[str, str, str]], doc: str | None = DOC_OTC03) -> str:
    body = "".join(f'<bpmn:{tag} id="{i}" name="{n}"/>' for i, tag, n in nodes)
    body += "".join(f'<bpmn:sequenceFlow id="f{k}" sourceRef="{s}" targetRef="{t}" name="{lbl}"/>' for k, (s, t, lbl) in enumerate(flows))
    lane = LANE.format("".join(f"<bpmn:flowNodeRef>{i}</bpmn:flowNodeRef>" for i, *_ in nodes))
    return model(body, doc, lane, shapes(*[i for i, *_ in nodes], *[f"f{k}" for k in range(len(flows))]))


def check(xml: str, catalog: dict = CATALOG) -> set[str]:
    with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
        path = Path(tmp) / "m.bpmn"
        path.write_text(xml, encoding="utf-8")
        return set(cm.check_model(path, catalog)["rules"])


GOOD_NODES = [("s", "startEvent", "Order aanvaard"), ("t", "userTask", "Leverdatum bevestigen"),
              ("g", "exclusiveGateway", "Haalbaar?"), ("e1", "endEvent", "Bevestigd"), ("e2", "endEvent", "Geannuleerd")]
GOOD_FLOWS = [("s", "t", ""), ("t", "g", ""), ("g", "e1", "ja"), ("g", "e2", "nee")]


class RepositoryModels(unittest.TestCase):
    """The models in the repository are the reference: they must pass, the analyst draft must not."""

    def test_released_and_review_models_pass(self):
        for path in cm.model_files():
            if path.name.endswith(".draft.bpmn"):
                continue
            with self.subTest(model=path.name):
                self.assertEqual(cm.check_model(path, CATALOG)["findings"], [])

    def test_analyst_draft_fails_on_the_seven_review_rules(self):
        result = cm.check_model(ROOT / "docs/05-review/bpmn/otc-03.draft.bpmn", CATALOG)
        self.assertEqual(result["rules"], ["R02", "R03", "R04", "R05", "R06", "R09", "R11"])
        self.assertEqual(len(result["findings"]), 9)

    def test_catalogue_has_no_errors_and_shows_the_governance_gaps(self):
        cat = cm.check_catalog(CATALOG, date(2026, 10, 10))
        self.assertEqual(cat["errors"], [])
        no_owner = sorted(w["element"] for w in cat["warnings"] if w["message"] == "geen eigenaar")
        self.assertEqual(no_owner, ["DTC-03", "IDP-03", "ITR-01", "ITR-02", "ITR-03", "OTC-03", "PTP-01", "STE-02"])
        self.assertIn("PRP-04", {w["element"] for w in cat["warnings"] if "verstreken" in w["message"]})


class Rules(unittest.TestCase):
    def test_good_minimal_model_passes(self):
        self.assertEqual(check(simple(GOOD_NODES, GOOD_FLOWS)), set())

    def test_r01_two_start_events(self):
        nodes = GOOD_NODES + [("s2", "startEvent", "Tweede start")]
        self.assertIn("R01", check(simple(nodes, GOOD_FLOWS + [("s2", "t", "")])))

    def test_r02_loose_end(self):
        nodes = GOOD_NODES + [("x", "userTask", "Datum aanpassen")]
        self.assertIn("R02", check(simple(nodes, GOOD_FLOWS + [("t", "x", "")])))

    def test_r03_noun_as_task_name(self):
        nodes = [n if n[0] != "t" else ("t", "userTask", "Capaciteitscheck") for n in GOOD_NODES]
        self.assertIn("R03", check(simple(nodes, GOOD_FLOWS)))

    def test_r04_r05_gateway_without_question_and_labels(self):
        nodes = [n if n[0] != "g" else ("g", "exclusiveGateway", "Check") for n in GOOD_NODES]
        flows = [f if f[0] != "g" else (f[0], f[1], "") for f in GOOD_FLOWS]
        self.assertTrue({"R04", "R05"} <= check(simple(nodes, flows)))

    def test_r06_inclusive_gateway_not_in_palette(self):
        nodes = [n if n[0] != "g" else ("g", "inclusiveGateway", "Haalbaar?") for n in GOOD_NODES]
        self.assertIn("R06", check(simple(nodes, GOOD_FLOWS)))

    def test_r08_too_many_activities(self):
        tasks = [(f"t{i}", "userTask", "Order controleren") for i in range(21)]
        nodes = [GOOD_NODES[0], *tasks, ("e1", "endEvent", "Klaar"), ("e2", "endEvent", "Fout")]
        chain = ["s"] + [t[0] for t in tasks] + ["e1"]
        flows = [(a, b, "") for a, b in zip(chain, chain[1:])] + [("t3", "e2", "")]
        self.assertIn("R08", check(simple(nodes, flows)))

    def test_r09_missing_attributes_and_status_mismatch(self):
        self.assertIn("R09", check(simple(GOOD_NODES, GOOD_FLOWS, doc=None)))
        released = DOC_OTC03.replace("in-review", "released")
        self.assertIn("R09", check(simple(GOOD_NODES, GOOD_FLOWS, doc=released)))

    def test_r09_released_owner_must_match_catalogue(self):
        catalog = copy.deepcopy(CATALOG)
        proc = next(p for p in catalog["processes"] if p["id"] == "OTC-03")
        proc.update(status="released", owner="Supply chain director")
        doc = DOC_OTC03.replace("in-review", "released").replace("eigenaar: open", "eigenaar: Sales director")
        self.assertIn("R09", check(simple(GOOD_NODES, GOOD_FLOWS, doc=doc), catalog))

    def test_r11_person_as_lane(self):
        xml = simple(GOOD_NODES, GOOD_FLOWS).replace('name="Planner"', 'name="Jan (planning)"')
        self.assertIn("R11", check(xml))

    def test_r12_missing_diagram_information(self):
        xml = simple(GOOD_NODES, GOOD_FLOWS).replace('<bpmndi:BPMNShape id="t_di" bpmnElement="t"/>', "")
        self.assertIn("R12", check(xml))

    def test_r13_to_be_without_exception_path(self):
        nodes = [n for n in GOOD_NODES if n[0] not in ("g", "e2")]
        self.assertIn("R13", check(simple(nodes, [("s", "t", ""), ("t", "e1", "")])))


class Naming(unittest.TestCase):
    def test_verb_list_in_checklist_matches_the_code(self):
        doc = (ROOT / "docs/03-standards/kwaliteitschecklist.md").read_text(encoding="utf-8")
        section = doc.split("## Werkwoordenlijst", 1)[1].split("##", 1)[0]
        line = next(l for l in section.splitlines() if " · " in l)
        self.assertEqual({w.strip() for w in line.split("·")}, cm.VERBS)

    def test_object_plus_infinitive(self):
        self.assertTrue(cm.name_ok("Leverdatum bevestigen"))
        self.assertTrue(cm.name_ok("Order registreren en volledigheid controleren"))
        self.assertFalse(cm.name_ok("Capaciteitscheck"))
        self.assertFalse(cm.name_ok("Bevestig leverdatum"))
        self.assertFalse(cm.name_ok("Mail naar klant"))


if __name__ == "__main__":
    unittest.main()

# Technical view (architect / BPM-specialist)

> Altijd met businesscontext. *Fictional organisation.*

| Onderwerp | Uitwerking | Waar |
|---|---|---|
| **Bron van waarheid** | `catalog/catalog.json`: L0, L1, L2, capabilities, systemen, rollen; views gegenereerd door `build_catalog.py` | [catalog.json](../../catalog/catalog.json) |
| **Modellen** | BPMN 2.0 XML met diagram interchange, gegenereerd uit reviewbare Python-structuren (`build_models.py`); attributen in `documentation` | [build_models.py](../../scripts/build_models.py) |
| **Conventie als code** | `check_models.py`: R01–R13 op modellen (bereikbaarheid vooruit/achteruit, naamregel met werkwoordenlijst, gateways, palet, lanes uit rollenlijst, attributen vs catalogus, DI, uitzonderingspad) en C01–C04 op de catalogus | [check_models.py](../../scripts/check_models.py) |
| **Tests** | 17 unittests: elke regel met een minimaal falend model; repo-modellen moeten slagen; draft faalt op exact 7 regels; werkwoordenlijst in docs = code | [tests](../../tests/test_check_models.py) |
| **CI** | tests → hergenereren → `git diff --exit-code` → linkcheck | [ci.yml](../../.github/workflows/ci.yml) |
| **Koppeling met EA** | per proces capabilities en systemen; ArchiMate-vertaling (proces realiseert capability, applicatieservice bedient proces) | [proces ↔ applicatie](../../docs/02-architecture/proces-applicatie.md) |
| **Governance in de data** | statussen, eigenaar, reviewdatum; C04 maakt governance-gaten zichtbaar als waarschuwing | [governance](../../docs/06-governance/governance-model.md) |
| **Prototype** | vanilla JS, leest `site/data/*.json`, localStorage, geen externe scripts | [demo.mjs](../../site/assets/demo.mjs) |
| **Exit naar een tool** | BPMN 2.0 importeerbaar; catalogus = tabel | [ADR-001](../../docs/adr/001-catalogus-als-code.md) |

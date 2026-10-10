# Walkthrough van 15 minuten (technisch of panelgesprek)

> Voor een gesprek met een architect, BPM-lead of panel. ⏸ = pauze voor vragen.
> *Independent portfolio case — fictional organisation.*

| Tijd | Onderdeel | Tonen | Kernpunt |
|---|---|---|---|
| 0–2 | Context | [context](../../docs/00-context/README.md) | procesboom zonder gebruik; ERP wacht; zeven stukken rommeligheid |
| 2–4 | Capability map + procesboom | [capability map](../../docs/02-architecture/capability-map.md) | wat vs hoe; leverbelofte rood; capability zonder proces ⏸ |
| 4–6 | Catalogus als code | [catalog.json](../../catalog/catalog.json), [ADR-001](../../docs/adr/001-catalogus-als-code.md) | één bron, gegenereerde views, exitplan naar een tool ⏸ |
| 6–9 | Conventie + check | [conventie](../../docs/03-standards/modelleerconventie.md), [check_models.py](../../scripts/check_models.py), CI | palet (ADR-002), naamregel, R01–R13 vs M01–M05; draft mag falen ⏸ |
| 9–11 | Referentiemodel OTC-02 | [order-to-cash](../../docs/04-reference-model/order-to-cash.md) | pijnpunten P1–P5, non-interrupting timer, leverdatum naar OTC-03 |
| 11–13 | Review + governance | [review](../../docs/05-review/review-otc-03.md), [procesraad](../../docs/06-governance/procesraad.md) | vijf vragen; D-03 met opties; STE-04 haalt eigen checks ⏸ |
| 13–15 | Verbetering + beperkingen | [verbeterportfolio](../../docs/07-improvement/verbeterportfolio.md), [README Limitations](../../README.md#limitations) | Lean verbetert, BPM legt vast; wat niet aangetoond is |

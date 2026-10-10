# Onboarding-kit voor een nieuwe business process analyst

> **Wat:** wat een nieuwe analist de eerste twee weken krijgt, zodat die vanaf het eerste model volgens de standaard werkt.
> **Voor wie:** nieuwe analisten, hun buddy, de process architect.

← [Review OTC-03](review-otc-03.md) · Volgende: [Governance-model](../06-governance/governance-model.md) →

## Week 1 — lezen, kijken, meelopen

| Dag | Wat | Materiaal |
|---|---|---|
| 1 | Proceshuis en catalogus: waar zit wat, wie is eigenaar | [procesboom](../02-architecture/procesboom.md), [catalogus](../02-architecture/procescatalogus.md) |
| 1 | Capability map en het verschil tussen capability en proces | [capability map](../02-architecture/capability-map.md) |
| 2 | Modelleerconventie en checklist (1 uur, met de architect) | [conventie](../03-standards/modelleerconventie.md), [checklist](../03-standards/kwaliteitschecklist.md) |
| 2 | Referentiemodel lezen en drie vragen noteren | [order-to-cash](../04-reference-model/order-to-cash.md) |
| 3 | Een review meelezen, van draft tot herwerkte versie | [review OTC-03](review-otc-03.md) |
| 3–4 | Gemba: een dag meelopen in het eigen domein | — |
| 5 | Governance: wie beslist wat, hoe een wijziging loopt | [governance-model](../06-governance/governance-model.md) |

## Week 2 — eerste model

| Stap | Wat | Check |
|---|---|---|
| 1 | Kies samen met de buddy één L2-proces met status *draft* uit het eigen domein | catalogus |
| 2 | SIPOC opstellen (20 minuten met de eigenaar) | scope helder? |
| 3 | As-is tekenen met de mensen die het werk doen | M05 |
| 4 | `python3 scripts/check_models.py` → alle automatische regels groen | R01–R13 |
| 5 | Review aanvragen; maximaal 5 punten terug | M01–M05 |

## Review-ritme

| Moment | Duur | Wie |
|---|---|---|
| Wekelijks BPM-overleg: blokkades, vragen over de conventie | 30 min | analisten + architect |
| Review per model | ≤ 3 werkdagen doorlooptijd | architect |
| Maandelijks: één model samen herbekijken dat al released is (wat zouden we nu anders doen?) | 45 min | team |

## Wat ik van een nieuwe analist verwacht na 30 dagen

- Eén model in review dat de automatische checks haalt.
- Kan uitleggen waarom het palet geen inclusive gateway bevat.
- Kent de eigenaar van elk L2-proces in het eigen domein.

## Veelgemaakte fouten van nieuwe analisten (en wat ik dan vraag)

| Fout | Vraag |
|---|---|
| alleen het happy path | "Wat gebeurt er als dit misloopt?" |
| afdelingen of personen als lanes | "Welke rol beslist hier?" |
| model start midden in het proces | "Waar komt de input vandaan?" |
| procedure getekend in plaats van praktijk | "Met wie die dit dagelijks doet, heb je het nagelopen?" |

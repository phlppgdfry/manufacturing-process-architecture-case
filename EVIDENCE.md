# Wat deze case aantoont

> Mapping van typische vereisten voor procesrollen (business process architect, process analyst, BPM lead) naar concreet bewijs in deze repository.
> **Getoond / niet geclaimd** scheidt wat deze case aantoont van productie-ervaring die niet geclaimd wordt.
> *Independent portfolio case study based on a fictional organisation. It contains no confidential information from any real employer.*

| Vereiste | Bewijs in deze repository | In 30 seconden te zien | Getoond / niet geclaimd |
|---|---|---|---|
| Eigenaarschap over de procescatalogus | [catalogus](docs/02-architecture/procescatalogus.md) gegenereerd uit [`catalog.json`](catalog/catalog.json): 41 L2-processen, verplichte velden, dekking per L1 | demo stap 2: filter "zonder eigenaar" | getoond: opbouw, velden, werklijst · niet geclaimd: een catalogus beheerd in een echte organisatie |
| Procesarchitectuur op business capabilities en E2E-processen | [capability map](docs/02-architecture/capability-map.md) (35 capabilities, heatmap), [procesboom](docs/02-architecture/procesboom.md) (L0–L4, 10 E2E-processen, overdrachten) | landing page: proceshuis en capability map | getoond: structuur en regels · niet geclaimd: een architectuur onderhandeld met een directie |
| Standaarden voor procesmodellering en -documentatie | [conventie](docs/03-standards/modelleerconventie.md) (palet, naamregel, attributen), [sjabloon](docs/03-standards/documentatiesjabloon.md), [ADR-002](docs/adr/002-bpmn-subset.md) | conventie: §3 palet en §4 naamgeving | getoond: een conventie met verantwoording · niet geclaimd: ingevoerd bij een team |
| Kwaliteit en consistentie van modellen bewaken | [checklist](docs/03-standards/kwaliteitschecklist.md) met 18 regels; 13 als code in [`check_models.py`](scripts/check_models.py), [17 tests](tests/test_check_models.py), in CI | demo stap 4: automatisch rapport | getoond: werkende toetsing van BPMN-bestanden · niet geclaimd: ervaring met Signavio/ARIS/ADONIS |
| BPMN as-is en to-be modelleren | [order-to-cash](docs/04-reference-model/order-to-cash.md): geldige BPMN 2.0 met diagraminformatie, pijnpunten P1–P5, boundary timer, uitzonderingspaden | landing page: as-is ↔ to-be | getoond: modelleren op L1–L3 · niet geclaimd: processen van een echte fabriek gemodelleerd |
| Business process analysts coachen en begeleiden | [review OTC-03](docs/05-review/review-otc-03.md) (5 punten, elk als vraag), [onboarding-kit](docs/05-review/onboarding-analist.md), review-ritme | demo stap 5–6: review en herwerkte versie | getoond: hoe ik zou reviewen en coachen · niet geclaimd: ervaring met het coachen van collega's |
| Procesgovernance: rollen, ownership, besluitvorming | [governance-model](docs/06-governance/governance-model.md) (RACI, statussen, wijzigingsflow als getoetst BPMN-model), [procesraad](docs/06-governance/procesraad.md) (agenda's, beslissingslog, voorstel D-03) | demo stap 7: beslissing D-03 | getoond: ontwerp van governance · niet geclaimd: een procesraad geleid |
| Processen, capabilities, systemen en strategie verbinden | [proces ↔ applicatie](docs/02-architecture/proces-applicatie.md): velden, drie vragen die de koppeling beantwoordt, afspraken met EA | demo: filter op systeem | getoond: de koppeling als data · niet geclaimd: ArchiMate-modellering |
| Procesinzichten → verbeterinitiatieven | [verbeterportfolio](docs/07-improvement/verbeterportfolio.md): 5 initiatieven met proces-ID, KPI, nulmeting, prioriteringsregel | demo stap 9 | getoond: vertaling en prioritering · niet geclaimd: gemeten resultaten (alle cijfers illustratief) |
| Samenwerken met business, IT en management | [one-pager](docs/01-frame/management-one-pager.md), [90-dagenplan](docs/01-frame/90-dagenplan.md), taakverdeling met OpEx en EA | landing page: aanpak | getoond: hoe ik het zou aanpakken · niet geclaimd: stakeholdermanagement in een organisatie van deze grootte |
| Lean Six Sigma (pluspunt) | [SIPOC en DMAIC-schets](docs/07-improvement/sipoc-dmaic-i02.md) met BPM in de Control-fase | — | getoond: de begrippen correct gebruikt · niet geclaimd: belt-certificering of een uitgevoerd DMAIC-project |

Deze case toont hoe ik denk en werk in een procesrol. Ze vervangt geen productie-ervaring in een organisatie; daarom staat bij elke rij wat niet geclaimd wordt.

## Gerelateerd werk

- [Shipment exception management — business analysis](https://github.com/phlppgdfry/shipment-exception-management-business-analysis): BPMN as-is/to-be, event storming, business case (logistiek)
- [Short-sea booking — functional analysis](https://github.com/phlppgdfry/shortsea-booking-functional-analysis): beslistabellen, state machine, interfaces

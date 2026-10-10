# Corvent Process House — procesarchitectuur die gebruikt wordt

**Procescatalogus, modelleerstandaard en governance + referentiemodel order-to-cash**

> Van een procesboom in PowerPoint naar een beheerde procescatalogus met eigenaars, één modelleerstandaard die automatisch getoetst wordt, en een eerste referentiemodel voor order-to-cash.

> *Independent portfolio case study based on a fictional organisation (Corvent Industries). It contains no confidential information from any real employer or the hiring company. All figures are illustrative assumptions — not real company data.*

**[Live site](https://phlppgdfry.github.io/manufacturing-process-architecture-case/)** · **[Start here](START-HERE.md)** · **[Evidence](EVIDENCE.md)** · **[Case study](CASE_STUDY.md)** · **[2-minute demo](https://phlppgdfry.github.io/manufacturing-process-architecture-case/demo/?tour)**

## De journey

```text
Frame         90-dagenplan, management one-pager, maturiteitsscan
   ↓
Structure     capability map → procesboom L0–L2 → catalogus met eigenaar, status, capability, systemen
   ↓
Standardise   modelleerconventie + checklist (18 regels, 13 automatisch getoetst in CI)
   ↓
Model         referentiemodel order-to-cash: L1 → L3, as-is en to-be, met overdrachten en uitzonderingen
   ↓
Review        draft van een analist → 9 bevindingen → 5 feedbackpunten → herwerkte versie, 0 bevindingen
   ↓
Govern        rollen, RACI, procesraad, wijzigingsflow (zelf een gemodelleerd en getoetst proces)
   ↓
Improve       verbeterportfolio gekoppeld aan proces-ID en KPI; DMAIC-schets met BPM in de Control-fase
```

## Het probleem

Corvent Industries, een fictieve maakindustrie van ±950 medewerkers, heeft net een procesarchitectuur op capabilities en end-to-end processen laten tekenen. Niemand gebruikt die: 8 van de 41 L2-processen hebben geen eigenaar, slechts 8 hebben een vrijgegeven model, vier analisten tekenen elk anders, en over zes weken wil het ERP-project vrijgegeven to-be-processen.

## Wat ik deed

- **Gestructureerd** in plaats van hertekend: een [capability map](docs/02-architecture/capability-map.md) naast de bestaande [procesboom](docs/02-architecture/procesboom.md), en een [procescatalogus](docs/02-architecture/procescatalogus.md) met verplichte velden, gegenereerd uit één [JSON-bron](catalog/catalog.json).
- **Een standaard vastgelegd** die kort genoeg is om gevolgd te worden: [modelleerconventie](docs/03-standards/modelleerconventie.md) en [checklist](docs/03-standards/kwaliteitschecklist.md), met een [automatische check](scripts/check_models.py) en [tests](tests/test_check_models.py) in CI.
- **Zelf gemodelleerd**: [order-to-cash L1 → L3](docs/04-reference-model/order-to-cash.md), as-is met vijf genummerde pijnpunten, en een to-be met een non-interrupting timer en drie uitzonderingspaden.
- **Gecoacht** via een [review van een analistenmodel](docs/05-review/review-otc-03.md): maximaal vijf punten, elk als vraag; de herwerkte versie haalt alle checks.
- **Governance ingericht**: [rollen, RACI en wijzigingsflow](docs/06-governance/governance-model.md), en een [procesraad](docs/06-governance/procesraad.md) die het eigenaarsconflict over de leverdatum beslist.
- **Inzichten vertaald** naar een [verbeterportfolio](docs/07-improvement/verbeterportfolio.md) met KPI's en nulmetingen.

## Wat deze case aantoont

| Vereiste in procesrollen | Bewijs |
|---|---|
| Procescatalogus beheren | [catalogus](docs/02-architecture/procescatalogus.md) · [demo](https://phlppgdfry.github.io/manufacturing-process-architecture-case/demo/?tour) |
| Procesarchitectuur op capabilities en E2E-processen | [capability map](docs/02-architecture/capability-map.md) · [procesboom](docs/02-architecture/procesboom.md) |
| Standaarden voor modellering en documentatie | [conventie](docs/03-standards/modelleerconventie.md) · [sjabloon](docs/03-standards/documentatiesjabloon.md) |
| Kwaliteit en consistentie bewaken | [checklist](docs/03-standards/kwaliteitschecklist.md) · [check in CI](scripts/check_models.py) |
| BPMN as-is en to-be modelleren | [order-to-cash](docs/04-reference-model/order-to-cash.md) |
| Analisten coachen | [review OTC-03](docs/05-review/review-otc-03.md) · [onboarding-kit](docs/05-review/onboarding-analist.md) |
| Procesgovernance | [governance-model](docs/06-governance/governance-model.md) · [procesraad](docs/06-governance/procesraad.md) |
| Processen, capabilities, systemen en strategie verbinden | [proces ↔ applicatie](docs/02-architecture/proces-applicatie.md) |
| Inzichten → verbeterinitiatieven | [verbeterportfolio](docs/07-improvement/verbeterportfolio.md) |

Volledige mapping, inclusief wat deze case *niet* claimt: [EVIDENCE.md](EVIDENCE.md).

## Repository

| Map | Inhoud |
|---|---|
| `catalog/` | `catalog.json`: de bron van waarheid (L0, L1, L2, capabilities, systemen, rollen) |
| `docs/00-context/` | organisatie, probleem, scope, rommeligheid, aannames |
| `docs/01-frame/` | 90-dagenplan, management one-pager, maturiteitsscan |
| `docs/02-architecture/` | capability map, procesboom, proces ↔ applicatie, catalogus (gegenereerd) |
| `docs/03-standards/` | modelleerconventie, kwaliteitschecklist, documentatiesjabloon |
| `docs/04-reference-model/` | order-to-cash, BPMN as-is en to-be |
| `docs/05-review/` | review van een analistenmodel, onboarding-kit |
| `docs/06-governance/` | governance-model, procesraad, wijzigingsflow (BPMN) |
| `docs/07-improvement/` | verbeterportfolio, SIPOC/DMAIC-schets |
| `docs/adr/` | ontwerpbeslissingen |
| `scripts/` | `build_models.py` (BPMN + SVG), `build_catalog.py` (views), `check_models.py` (conventie als code), `check-links.py` |
| `tests/` | tests van de modelregels |
| `site/` | GitHub Pages: landing page, prototype met rondleiding, lenzen per rol |
| `application-kit/` | samenvatting, demo-script, deck-outline |

## How to run and verify

Alleen Python 3 (standaardbibliotheek), geen installatie.

```bash
git clone https://github.com/phlppgdfry/manufacturing-process-architecture-case && cd manufacturing-process-architecture-case
python3 -m unittest discover -s tests                                 # 17 tests van de modelregels
python3 scripts/check_models.py                                       # alle modellen + catalogus: 4 × OK, 1 draft met 9 bevindingen
python3 scripts/build_models.py && python3 scripts/build_catalog.py   # modellen en views opnieuw genereren
git diff --exit-code                                                  # niets veranderd = gegenereerde bestanden zijn actueel
python3 -m http.server -d site 8000                                   # site en demo op http://localhost:8000
```

Dezelfde stappen draaien bij elke push in [GitHub Actions](.github/workflows/ci.yml). De BPMN-bestanden openen in [bpmn.io](https://demo.bpmn.io/) of Camunda Modeler.

**Demo laadt niet?** Screenshots: [catalogus](docs/screenshots/demo-catalogus.png) · [review](docs/screenshots/demo-review.png) · [procesraad](docs/screenshots/demo-procesraad.png) · [landing page](docs/screenshots/landing.png).

## Sources, data and licences

- **Data:** volledig fictief en zelf opgesteld (Corvent Industries bestaat niet). Alle aantallen, KPI's en nulmetingen zijn *illustrative assumptions*. Geen gegevens van een werkgever of een echte organisatie.
- **Standaarden en kaders** (alleen als referentie, niets gekopieerd): BPMN 2.0.2 ([OMG](https://www.omg.org/spec/BPMN/2.0.2/)), TOGAF business architecture ([The Open Group](https://www.opengroup.org/togaf)), ArchiMate 3 ([The Open Group](https://pubs.opengroup.org/architecture/archimate3-doc/)), APQC Process Classification Framework (genoemd als referentiekader), Lean Six Sigma / DMAIC ([IASSC](https://www.iassc.org/)).
- **Afhankelijkheden:** geen. Python-standaardbibliotheek; de site is plain HTML/CSS/JS zonder externe scripts (Mermaid-diagrammen in de Markdown worden door GitHub gerenderd).
- **Licentie:** code (scripts, tests, site) onder MIT, documentatie en diagrammen onder CC BY 4.0. Zie [LICENSE](LICENSE).
- **Werkwijze:** uitgewerkt met AI-ondersteuning; keuzes, verantwoording en beperkingen staan in de ADR's en hieronder.

## Limitations

- **Fictief en zonder stakeholders.** Interviews, workshops, procesraden en de review zijn uitgeschreven scenario's, geen verslagen van echte gesprekken.
- **Gesimuleerd in de demo:** de beslissing van de procesraad, de release van OTC-03 en de update van het modelattribuut. **Echt:** de catalogusdata, de BPMN-modellen en het checkrapport uit `check_models.py`.
- **Niet aangetoond:** procesmanagement in een echte organisatie, gemeten resultaten, werken met een procesrepository-tool (de modellen zijn wel standaard BPMN 2.0 en importeerbaar).
- **Bewust beperkt:** L3 alleen voor order-to-cash en de wijzigingsflow; geen L4-werkinstructies, geen process mining (zie [ADR-003](docs/adr/003-breed-ondiep-eerst.md)).
- **Capability map** is afgeleid uit de bestaande procesarchitectuur, niet gevalideerd in een workshop met enterprise architectuur.

## Realisme en aannames

Alle cijfers zijn *illustrative assumptions*. De rommeligheid is bewust: overlap in de bestaande procesboom, een eigenaarsconflict tussen sales en planning, een ervaren analist met een eigen stijl, een ERP-project dat niet wacht, en geen budget voor een tool. Zie [context](docs/00-context/README.md#realistische-rommeligheid).

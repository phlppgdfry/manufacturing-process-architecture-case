# 90-dagenplan van de process architect

> **Wat:** hoe ik de eerste 90 dagen aanpak, en waarom in deze volgorde.
> **Voor wie:** COO (sponsor), hoofd enterprise architectuur, de analisten.
> *Illustrative assumption — not real company data.*

← [Context](../00-context/README.md) · Volgende: [Management one-pager](management-one-pager.md) →

## Uitgangspunt

De procesarchitectuur is net getekend. Ik teken hem dus niet opnieuw. Ik zorg dat hij gebruikt wordt: één catalogus, één manier van modelleren, en voor elk proces iemand die beslist. Het ERP-project is de eerste klant: dat bepaalt waar ik de diepte in ga ([ADR-003](../adr/003-breed-ondiep-eerst.md)).

## Dag 0–30: begrijpen en vertrouwen winnen

| Wat | Met wie | Resultaat |
|---|---|---|
| 1-op-1 met elke analist: wat werkt, wat frustreert, welke stijl en waarom | 4 analisten | lijst met gewoontes die we behouden (bv. pijnpunten nummeren) |
| 1-op-1 met elke L1-eigenaar en de COO | 9 directeurs, COO | verwachtingen, de 3 grootste procesproblemen per domein |
| Afstemming met enterprise architectuur | 2 architecten | afspraak over de koppeling proces ↔ capability ↔ applicatie |
| Afstemming met operational excellence | Lean-lead | taakverdeling: zij verbeteren, de catalogus legt vast ([governance](../06-governance/governance-model.md)) |
| 10 bestaande modellen lezen | — | patronen (geen fouten) in een tabel; input voor de conventie |
| Gemba: een halve dag in elk domein meelopen | customer service, planning, magazijn | het verschil tussen procedure en praktijk |
| Maturiteitsscan per domein | analisten | [startpunt](maturiteitsscan.md) |

## Dag 31–60: het kader

| Wat | Resultaat | Bewijs in deze case |
|---|---|---|
| Catalogusvelden afspreken met EA | ID, naam, niveau, eigenaar, status, versie, capability, systemen, reviewdatum | [catalogus](../02-architecture/procescatalogus.md), [ADR-001](../adr/001-catalogus-als-code.md) |
| Capability map naast de procesboom leggen | elke L2 wijst naar een capability; gaten zichtbaar | [capability map](../02-architecture/capability-map.md) |
| Modelleerconventie v1 samen met de analisten | 3 pagina's, BPMN-palet per niveau, naamregel | [conventie](../03-standards/modelleerconventie.md), [ADR-002](../adr/002-bpmn-subset.md) |
| Checklist van 18 regels, waarvan 13 automatisch | objectieve review | [checklist](../03-standards/kwaliteitschecklist.md), `scripts/check_models.py` |
| Test op 3 bestaande modellen | conventie bijgesteld vóór de release | [review OTC-03](../05-review/review-otc-03.md) |
| Procesraad #1 | eerste beslissingen: wijzigingsflow (D-01), klachten onder ITR (D-02) | [procesraad](../06-governance/procesraad.md) |

## Dag 61–90: het eerste bewijs

| Wat | Resultaat | Bewijs |
|---|---|---|
| Referentiemodel order-to-cash, L1 → L3 | as-is en to-be voor OTC-02, met overdrachten en uitzonderingen | [order-to-cash](../04-reference-model/order-to-cash.md) |
| Eerste review van een analistenmodel volgens de nieuwe standaard | OTC-03 van 9 bevindingen naar 0 | [review](../05-review/review-otc-03.md) |
| Eigenaarsconflict leverdatum voorleggen | voorstel D-03 voor procesraad #2 | [procesraad](../06-governance/procesraad.md) |
| Verbeterportfolio | 5 initiatieven met proces-ID, KPI en nulmeting | [verbeterportfolio](../07-improvement/verbeterportfolio.md) |
| Onboarding-kit voor nieuwe analisten | zelfde standaard vanaf dag 1 | [onboarding](../05-review/onboarding-analist.md) |

## Wat ik na 90 dagen wil kunnen tonen

| Indicator | Dag 0 | Doel dag 90 | Doel 12 maanden |
|---|---:|---:|---:|
| L2-processen met eigenaar | 33 / 41 | 39 / 41 | 41 / 41 |
| L2 released in de catalogus | 8 / 41 | 12 / 41 | 30 / 41 |
| Modellen die de automatische check halen (in repo) | — | 100% van wat in review gaat | 100% |
| Doorlooptijd review (indienen → feedback) | onbekend | ≤ 3 werkdagen | ≤ 2 werkdagen |
| Procesraad gehouden met minstens 1 beslissing | 0 | 2 | maandelijks |

## Risico's

| Risico | Kans | Impact | Mitigatie |
|---|---|---|---|
| Directeurs zien eigenaarschap als extra administratie | hoog | hoog | eigenaar beslist; steward houdt bij; procesraad max. 60 min |
| Conventie voelt als controle | middel | hoog | samen opgesteld; automatische check zodat de review over inhoud gaat |
| ERP-project wacht niet | hoog | middel | OTC eerst; wat het ERP-project nodig heeft, krijgt voorrang |
| Lean-team voelt zich gepasseerd | middel | middel | duidelijke rolverdeling in de RACI; gezamenlijk verbeterportfolio |

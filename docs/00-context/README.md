# Context — Corvent Industries

> **Wat:** de fictieve organisatie, het probleem, de scope en de aannames van deze case.
> **Voor wie:** iedereen die de case leest; begin hier.
> *Independent portfolio case study based on a fictional organisation. It contains no confidential information from any real employer or the hiring company. Alle cijfers: illustrative assumption — not real company data.*

Volgende: [90-dagenplan](../01-frame/90-dagenplan.md) →

## De organisatie

| Kenmerk | Waarde |
|---|---|
| Wat | Vlaamse maakindustrie: ventilatie-units en luchtbehandelingscomponenten voor utiliteitsbouw, deels op maat (configure-to-order) |
| Grootte | ±950 medewerkers |
| Locaties | 2 productiesites, 1 distributiecentrum, verkoopkantoren in België, Frankrijk en Nederland |
| Domeinen | operations, supply chain, commercial, HR, finance |
| Systemen | ERP, MES, WMS, CRM (met productconfigurator), PLM, QMS, CMMS, HRIS, BI, EDI — en Excel-lijsten waar een systeem tekortschiet |
| Sponsor | COO, programma "Corvent Process House" |
| Teams | enterprise architectuur (2), operational excellence / Lean (3), business process analysts (4, waarvan 2 nieuw), ERP-projectteam |

## Waarom nu

In 2025 tekende een consultant samen met het management een **procesarchitectuur op basis van business capabilities en end-to-end processen**: 3 lagen (sturend, kern, ondersteunend) en 10 end-to-end processen. Die staat in een PowerPoint. In Q1 2027 start een **ERP-upgrade** met fit-to-standard-workshops, en die hebben per proces een eigenaar en een vrijgegeven to-be-model nodig.

De COO wil één proceshuis vóór die workshops. Een process architect wordt aangesteld. Deze case beschrijft zijn of haar eerste 90 dagen.

## Wat de architect aantreft

| Bevinding (dag 1–30) | Gevolg |
|---|---|
| De procesboom bestaat (L0–L1), L2 is half ingevuld, niemand gebruikt hem | projecten tekenen hun eigen processen |
| 41 actieve L2-processen; 8 zonder eigenaar, en het hele L1-proces issue-to-resolution heeft geen eigenaar | niemand beslist over wijzigingen of overdrachten |
| 8 van de 41 L2-processen hebben een vrijgegeven model; 7 daarvan staan in oude formaten (Visio, PowerPoint, Word) | het ERP-team krijgt tegenstrijdige versies |
| Vier analisten, vier modelleerstijlen | reviews gaan over smaak; modellen zijn niet te vergelijken |
| "Klachten behandelen" staat zowel onder order-to-cash als onder issue-to-resolution | dubbel werk, onduidelijke eigenaar |
| Sales belooft leverdatums, planning wijzigt ze stil | late leveringen; customer service vangt de klachten op |
| Het Lean-team werkt met value stream maps en eigen procesbeschrijvingen | twee "waarheden" over hetzelfde proces |

## Scope

**Binnen scope**
1. **Proceshuis laten leven:** capability map, procescatalogus L0–L2 met verplichte velden, modelleerconventie, kwaliteitschecklist met automatische check, governance met procesraad en wijzigingsflow.
2. **Eerste referentiemodel:** order-to-cash, L1 → L3, met as-is en to-be voor *Order aanvaarden* (OTC-02) en een review van het analistenmodel *Leverdatum bevestigen* (OTC-03).

**Buiten scope** (bewust)
- tool-selectie voor een procesrepository (zie [ADR-001](../adr/001-catalogus-als-code.md));
- L4-werkinstructies;
- process mining (later, op basis van ERP-logs);
- de ERP-configuratie zelf.

## Realistische rommeligheid

| # | Wat | Waar zichtbaar |
|---|---|---|
| R1 | Overlap in de consultant-boom (klachten onder twee L1-processen) | [procesraad D-02](../06-governance/procesraad.md), catalogus OTC-07 |
| R2 | Vier modelleerstijlen; een ervaren analist wil zijn eigen stijl houden | [review](../05-review/review-otc-03.md), [onboarding-kit](../05-review/onboarding-analist.md) |
| R3 | Eigenaarsconflict sales ↔ planning over de bevestigde leverdatum | [as-is](../04-reference-model/order-to-cash.md), [procesraad D-03](../06-governance/procesraad.md) |
| R4 | Het ERP-project wil to-be-modellen binnen 6 weken | [90-dagenplan](../01-frame/90-dagenplan.md), [ADR-003](../adr/003-breed-ondiep-eerst.md) |
| R5 | Het Lean-team werkt met eigen beschrijvingen | [governance-model](../06-governance/governance-model.md), [verbeterportfolio](../07-improvement/verbeterportfolio.md) |
| R6 | Andere namen in ERP-documentatie dan in de procesboom ("Orderintake" vs "Order aanvaarden") | catalogusveld `aliases` |
| R7 | Geen budget voor een procesrepository-tool dit jaar | [ADR-001](../adr/001-catalogus-als-code.md) |

## Aannames

- Alle aantallen, KPI's en nulmetingen zijn *illustrative assumptions*.
- Functietitels zijn generiek; er komen geen echte personen in voor. Lanes en eigenaars zijn rollen.
- Systemen hebben geen merknaam: de case gaat over procesarchitectuur, niet over een pakket.

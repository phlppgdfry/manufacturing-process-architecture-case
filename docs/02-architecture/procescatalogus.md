# Procescatalogus — Corvent Industries

> **Gegenereerd** uit [`catalog/catalog.json`](../../catalog/catalog.json) door `scripts/build_catalog.py` — niet met de hand bewerken.
> Wat het is: het register van alle L1- en L2-processen met eigenaar, status, versie, capability, systemen en reviewdatum.
> Voor wie: process architect, analisten, enterprise architectuur, projecten. *Illustrative assumption — not real company data.*

← [Capability map](capability-map.md) · [Procesboom](procesboom.md) · Volgende: [Modelleerconventie](../03-standards/modelleerconventie.md) →

## Dekking

| Actieve L2-processen | Met eigenaar | Released | In review | Draft | Geen model |
|---:|---:|---:|---:|---:|---:|
| 41 | 33 (80%) | 8 (20%) | 2 | 20 | 11 |

L1 zonder eigenaar: ITR. De volledige lijst governance-gaten staat in het rapport van `scripts/check_models.py` (regel C04) en op de [demo](https://phlppgdfry.github.io/manufacturing-process-architecture-case/demo/).

## Sturende processen

### STE · Strategy-to-execution — Van strategie naar uitvoering

Eigenaar L1: **CEO** · 4 L2 · 3 met eigenaar · 1 released

| ID | Proces (L2) | Eigenaar | Status | Versie | Capability | Systemen | Review | Opmerking |
|---|---|---|---|---|---|---|---|---|
| STE-01 | Strategie en jaarplan bepalen | CEO | draft | 0.3 | Strategieplanning | Excel-lijsten | — |  |
| STE-02 | Verbeterportfolio sturen | — | geen model | — | Portfoliomanagement | Excel-lijsten | — |  |
| STE-03 | Prestaties opvolgen | COO | draft | 0.2 | Prestatiemanagement | BI | — |  |
| STE-04 | Proceswijziging doorvoeren | COO | released | 1.0 | Procesmanagement | Procesrepository | 2027-04-30 | [model](../../docs/06-governance/bpmn/ste-04-proceswijziging.bpmn) |

### DTC · Detect-to-correct — Kwaliteit borgen en afwijkingen corrigeren

Eigenaar L1: **Quality director** · 4 L2 · 3 met eigenaar · 1 released

| ID | Proces (L2) | Eigenaar | Status | Versie | Capability | Systemen | Review | Opmerking |
|---|---|---|---|---|---|---|---|---|
| DTC-01 | Inkomende goederen keuren | Quality manager | draft | 0.5 | Kwaliteitscontrole, Goederenontvangst | QMS, ERP | — |  |
| DTC-02 | Non-conformiteit behandelen | Quality manager | released | 2.0 | Non-conformiteitenbeheer | QMS | 2027-02-28 |  |
| DTC-03 | Corrigerende maatregelen opvolgen | — | geen model | — | Non-conformiteitenbeheer | QMS, Excel-lijsten | — |  |
| DTC-04 | Interne audit uitvoeren | Quality director | geen model | — | Auditbeheer | Excel-lijsten | — |  |

## Kernprocessen

### IDP · Idea-to-product — Van idee tot vrijgegeven product

Eigenaar L1: **R&D director** · 3 L2 · 2 met eigenaar · 0 released

| ID | Proces (L2) | Eigenaar | Status | Versie | Capability | Systemen | Review | Opmerking |
|---|---|---|---|---|---|---|---|---|
| IDP-01 | Productidee beoordelen | R&D director | geen model | — | Productontwikkeling | PLM | — |  |
| IDP-02 | Product ontwikkelen en vrijgeven | R&D director | draft | 0.4 | Productontwikkeling, Productdatabeheer | PLM | — |  |
| IDP-03 | Engineering change doorvoeren | — | draft | 0.1 | Engineering changes | PLM, ERP | — |  |

### OTC · Order-to-cash — Van klantorder tot ontvangen betaling

Eigenaar L1: **Commercial director** · 6 L2 · 5 met eigenaar · 0 released

| ID | Proces (L2) | Eigenaar | Status | Versie | Capability | Systemen | Review | Opmerking |
|---|---|---|---|---|---|---|---|---|
| OTC-01 | Offerte opstellen | Sales director | draft | 0.6 | Offertebeheer | CRM | — |  |
| OTC-02 | Order aanvaarden | Customer service manager | in review | 1.0 | Orderbeheer, Krediet en debiteuren | ERP, CRM, EDI | — | alias: Orderintake (ERP-documentatie); [model](../../docs/04-reference-model/bpmn/otc-02-to-be.bpmn) |
| OTC-03 | Leverdatum bevestigen | — | in review | 1.0 | Leverbelofte, Capaciteitsplanning | ERP | — | Eigenaarsconflict sales ↔ planning: voorstel D-03 voor procesraad #2; [model](../../docs/05-review/bpmn/otc-03-to-be.bpmn) |
| OTC-04 | Order uitleveren | Logistics manager | draft | 0.7 | Verzending | WMS, ERP | — |  |
| OTC-05 | Klant factureren | Finance manager | draft | 0.5 | Krediet en debiteuren | ERP, EDI | — |  |
| OTC-06 | Betaling opvolgen | Credit manager | draft | 0.4 | Krediet en debiteuren | ERP | — |  |
| OTC-07 | Klachten behandelen | — | retired | 0.2 | Klantenservice | CRM | — | Dubbel met ITR-01; procesraad #1 besliste D-02: enkel onder ITR-01 beheren; alias: zie ITR-01 |

### PTP · Plan-to-produce — Van vraagplan tot geproduceerd eindproduct

Eigenaar L1: **Supply chain director** · 6 L2 · 5 met eigenaar · 1 released

| ID | Proces (L2) | Eigenaar | Status | Versie | Capability | Systemen | Review | Opmerking |
|---|---|---|---|---|---|---|---|---|
| PTP-01 | Vraag en aanbod afstemmen | — | geen model | — | Vraagplanning | Excel-lijsten, BI | — | alias: S&OP |
| PTP-02 | Materialen plannen | Planning manager | draft | 0.8 | Materiaalplanning | ERP | — | alias: MRP-run |
| PTP-03 | Productieorder plannen en vrijgeven | Planning manager | draft | 0.6 | Capaciteitsplanning | ERP, MES | — |  |
| PTP-04 | Produceren en terugmelden | Plant manager | released | 1.1 | Productie-uitvoering, Productieterugmelding | MES, ERP | 2027-01-31 |  |
| PTP-05 | Eindproduct keuren en stockeren | Plant manager | draft | 0.3 | Kwaliteitscontrole, Voorraadbeheer | MES, WMS | — |  |
| PTP-06 | Voorraad tellen en corrigeren | Logistics manager | draft | 0.5 | Voorraadbeheer | WMS, ERP | — |  |

### PRP · Procure-to-pay — Van behoefte tot betaalde leverancier

Eigenaar L1: **Purchasing director** · 5 L2 · 5 met eigenaar · 2 released

| ID | Proces (L2) | Eigenaar | Status | Versie | Capability | Systemen | Review | Opmerking |
|---|---|---|---|---|---|---|---|---|
| PRP-01 | Leverancier selecteren | Purchasing director | draft | 0.4 | Leveranciersbeheer | Excel-lijsten | — |  |
| PRP-02 | Materiaal bestellen | Purchasing manager | released | 1.3 | Bestelbeheer | ERP, EDI | 2027-03-31 |  |
| PRP-03 | Goederen ontvangen | Logistics manager | draft | 0.9 | Goederenontvangst | WMS, ERP | — |  |
| PRP-04 | Leveranciersfactuur verwerken | Finance manager | released | 1.0 | Crediteurenbeheer | ERP, EDI | 2026-09-30 |  |
| PRP-05 | Leveranciersprestaties evalueren | Purchasing manager | geen model | — | Leveranciersbeheer | BI, Excel-lijsten | — |  |

### ITR · Issue-to-resolution — Van klacht of servicevraag tot oplossing

Eigenaar L1: **geen (governance-gat)** · 3 L2 · 0 met eigenaar · 0 released

| ID | Proces (L2) | Eigenaar | Status | Versie | Capability | Systemen | Review | Opmerking |
|---|---|---|---|---|---|---|---|---|
| ITR-01 | Klachten behandelen | — | draft | 0.3 | Klantenservice, Non-conformiteitenbeheer | CRM, QMS | — | alias: vroeger ook OTC-07 |
| ITR-02 | Service-interventie uitvoeren | — | geen model | — | Klantenservice | CRM | — |  |
| ITR-03 | Retour verwerken | — | geen model | — | Klantenservice, Goederenontvangst | WMS, ERP | — |  |

## Ondersteunende processen

### PTM · Plan-to-maintain — Installaties beschikbaar houden

Eigenaar L1: **Technical director** · 3 L2 · 3 met eigenaar · 1 released

| ID | Proces (L2) | Eigenaar | Status | Versie | Capability | Systemen | Review | Opmerking |
|---|---|---|---|---|---|---|---|---|
| PTM-01 | Preventief onderhoud plannen | Maintenance manager | draft | 0.6 | Onderhoudsplanning | CMMS | — |  |
| PTM-02 | Storing verhelpen | Maintenance manager | released | 1.2 | Storingsbeheer | CMMS, MES | 2027-05-31 |  |
| PTM-03 | Wisselstukken beheren | Maintenance manager | geen model | — | Wisselstukbeheer | CMMS, Excel-lijsten | — |  |

### HTR · Hire-to-retire — Van vacature tot vertrek

Eigenaar L1: **HR director** · 4 L2 · 4 met eigenaar · 1 released

| ID | Proces (L2) | Eigenaar | Status | Versie | Capability | Systemen | Review | Opmerking |
|---|---|---|---|---|---|---|---|---|
| HTR-01 | Medewerker aanwerven | HR manager | draft | 0.7 | Werving | HRIS | — |  |
| HTR-02 | Medewerker onboarden | HR manager | released | 1.1 | Personeelsadministratie | HRIS | 2027-06-30 |  |
| HTR-03 | Prestaties en ontwikkeling opvolgen | HR director | geen model | — | Talentontwikkeling | HRIS | — |  |
| HTR-04 | Medewerker uitstroom afhandelen | HR manager | geen model | — | Personeelsadministratie | HRIS | — |  |

### RTR · Record-to-report — Van boeking tot rapport

Eigenaar L1: **CFO** · 3 L2 · 3 met eigenaar · 1 released

| ID | Proces (L2) | Eigenaar | Status | Versie | Capability | Systemen | Review | Opmerking |
|---|---|---|---|---|---|---|---|---|
| RTR-01 | Maand afsluiten | Finance manager | released | 1.4 | Financiële rapportering | ERP, BI | 2027-01-31 |  |
| RTR-02 | Kostprijs berekenen | Controller | draft | 0.5 | Kostprijsbeheer | ERP, Excel-lijsten | — |  |
| RTR-03 | Rapport aan directie opstellen | CFO | draft | 0.4 | Financiële rapportering, Prestatiemanagement | BI | — |  |


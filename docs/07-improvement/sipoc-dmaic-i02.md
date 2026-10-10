# SIPOC en DMAIC-schets voor I-02 — haalbare leverdatum

> **Wat:** hoe een verbeterinitiatief uit het portfolio aansluit op Lean Six Sigma-taal, en waar BPM in die cyclus zit.
> **Voor wie:** OpEx-lead, eigenaar OTC-03, procesraad.
> *Schets, geen uitgevoerd project. Alle cijfers: illustrative assumption — not real company data.*

← [Verbeterportfolio](verbeterportfolio.md) · Terug naar het begin: [Context](../00-context/README.md)

## SIPOC — OTC-03 Leverdatum bevestigen

| Suppliers | Inputs | Process | Outputs | Customers |
|---|---|---|---|---|
| OTC-02 (customer service), planning, productie | aanvaarde order met gevraagde datum, capaciteit, materiaalbeschikbaarheid | 1. haalbare datum voorstellen · 2. standaardtermijn toetsen · 3. haalbaarheid afstemmen · 4. alternatief met klant afstemmen · 5. datum vastleggen en bevestigen | bevestigde leverdatum, orderbevestiging | klant, PTP-03 (productieplanning), OTC-04 (uitlevering) |

## DMAIC-schets

| Fase | Vraag | Voor I-02 | Wie |
|---|---|---|---|
| **Define** | Wat is het probleem, voor wie, hoe meten we het? | Klanten krijgen laat of onbetrouwbaar een leverdatum. CTQ: datum binnen 4 werkuren, en die datum wordt gehaald | eigenaar OTC-03, OpEx |
| **Measure** | Hoe groot is het nu? | 42% bevestigd binnen 4 werkuren; OTIF 78%; 23% van de bevestigde datums wordt nadien gewijzigd | OpEx, op basis van ERP-tijdstempels |
| **Analyze** | Waarom? | 5 whys: datum beloofd zonder capaciteit → geen ondersteuning in ERP (C3.4) → niemand eigenaar van de belofte → conflict sales ↔ planning nooit beslist | OpEx + analist; BPM levert as-is en pijnpunten |
| **Improve** | Wat veranderen we? | eigenaar beslist (D-03); ERP stelt haalbare datum voor; afwijkingen naar planner en accountmanager; pilot op één productlijn | ERP-project, eigenaar |
| **Control** | Hoe blijft het zo? | **to-be v1.0 released in de catalogus**, KPI op de procespagina, reviewdatum, maandelijkse KPI in de procesraad | **BPM-team**, eigenaar |

## Waar BPM het verschil maakt

Een bekend risico van verbeterprojecten is dat het resultaat wegzakt zodra het project afgesloten is. Bij Corvent is de Control-fase gekoppeld aan de catalogus:

- de verbetering is pas klaar als het to-be-model *released* is (via [STE-04](../06-governance/governance-model.md#wijzigingsflow));
- de KPI staat op de procespagina, met eigenaar;
- de reviewdatum dwingt een herbekijking na 12 maanden af.

## Rolverdeling

De schets gebruikt de Lean Six Sigma-structuur ([DMAIC](https://www.iassc.org/)) als gemeenschappelijke taal met operational excellence. In deze rolverdeling leidt OpEx het verbeterproject; BPM levert de as-is en de pijnpunten aan het begin en zorgt aan het einde voor de vastlegging.

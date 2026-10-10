# Proces ↔ capability ↔ applicatie

> **Wat:** hoe de procescatalogus aansluit op de enterprise architectuur: per proces de capability en de systemen, en wat dat oplevert voor projecten.
> **Voor wie:** collega-architecten (EA), ERP-projectleider.
> *Illustrative assumption — not real company data.*

← [Procesboom](procesboom.md) · Volgende: [Procescatalogus](procescatalogus.md) →

## De koppeling in één beeld

```mermaid
flowchart LR
  subgraph Strategie
    D1[Doel: OTIF naar 92%]
  end
  subgraph Business
    C[Capability C3.4<br/>Leverbelofte]
    P[Proces OTC-03<br/>Leverdatum bevestigen]
  end
  subgraph Applicaties
    ERP[ERP<br/>order, capaciteit]
  end
  D1 --> C
  C -- wordt uitgevoerd door --> P
  ERP -- ondersteunt --> P
  ERP -. ondersteunt C3.4 niet<br/>(geen ATP/CTP) .-> C
```

In ArchiMate-termen: het businessproces *Leverdatum bevestigen* realiseert de capability *Leverbelofte* en wordt bediend door een applicatieservice van het ERP. Ik teken de ArchiMate-views niet zelf: dat doet EA. De catalogus levert de relaties aan ([ArchiMate 3](https://pubs.opengroup.org/architecture/archimate3-doc/)).

## Velden in de catalogus die EA gebruikt

| Veld | Betekenis | Wie onderhoudt |
|---|---|---|
| `capabilities` | welke capabilities het proces uitvoert | process architect, met EA afgestemd |
| `systems` | welke systemen het proces ondersteunen (incl. Excel-lijsten) | analist, gecontroleerd door EA |
| `aliases` | andere namen voor hetzelfde proces (bv. in ERP-documentatie) | analist |
| `model` | waar het L3-model staat | analist |

## Wat de koppeling oplevert: drie vragen die nu in één query beantwoord worden

**1. Wat raakt de ERP-upgrade?** Alle processen met `ERP` in `systems`: 17 van de 41 L2-processen, verspreid over 7 van de 10 L1-processen. Voor elk daarvan zijn eigenaar en status bekend, dus het ERP-project weet wie het voor welke fit-to-standard-workshop moet uitnodigen.

**2. Waar zit schaduw-IT?** Processen met `Excel-lijsten` in `systems`: STE-01, STE-02, DTC-03, DTC-04, PTP-01, PRP-01, PRP-05, PTM-03, RTR-02. Dat zijn kandidaten voor de roadmap, maar alleen als de capability ook rood of oranje staat.

**3. Welke capability heeft geen proces of geen systeem?** C1.1 *Marktbewerking* (geen proces) en C3.4 *Leverbelofte* (geen systeemondersteuning).

De lijsten hierboven komen rechtstreeks uit [`catalog/catalog.json`](../../catalog/catalog.json). Op de [demo](https://phlppgdfry.github.io/manufacturing-process-architecture-case/demo/) kan je filteren op systeem.

## Afspraken met EA

| Afspraak | Waarom |
|---|---|
| De capability map is van EA, de procescatalogus van de process architect | elk één eigenaar; afstemming in het architectuuroverleg |
| Een nieuw L2-proces zonder capability gaat niet in review | de koppeling mag niet achteraf komen |
| Systeemnamen in de catalogus volgen het applicatieregister van EA | één naam per systeem |

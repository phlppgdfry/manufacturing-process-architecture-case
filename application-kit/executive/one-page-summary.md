# Corvent Process House — samenvatting op één pagina

> *Independent portfolio case study based on a fictional organisation. It contains no confidential information from any real employer or the hiring company.*
> Live: [phlppgdfry.github.io/manufacturing-process-architecture-case](https://phlppgdfry.github.io/manufacturing-process-architecture-case/) · Demo: [rondleiding van 2 minuten](https://phlppgdfry.github.io/manufacturing-process-architecture-case/demo/?tour)

## Uitdaging

Een fictieve maakindustrie (±950 medewerkers) liet een procesarchitectuur tekenen op capabilities en end-to-end processen. Niemand gebruikt die: 8 van de 41 processen hebben geen eigenaar, slechts 8 hebben een vrijgegeven model, vier analisten tekenen elk anders, en over zes weken wil het ERP-project vrijgegeven to-be-processen.

## Aanpak

Frame → Structure → Standardise → Model → Review → Govern → Improve. De bestaande architectuur blijft de basis; ze wordt beheerd, getoetst en gebruikt.

## Wat ik opleverde

1. **Procescatalogus** uit één bron: 41 L2-processen met eigenaar, status, capability, systemen en reviewdatum.
2. **Capability map** met heatmap naast de procesboom; koppeling proces ↔ applicatie voor enterprise architectuur.
3. **Modelleerconventie** (3 pagina's) en **checklist van 18 regels**, waarvan 13 automatisch getoetst in CI met 17 tests.
4. **Referentiemodel order-to-cash** L1 → L3: as-is met 5 pijnpunten, to-be met uitzonderingen en een non-interrupting timer.
5. **Review van een analistenmodel**: van 9 bevindingen naar 0, met 5 feedbackpunten als vragen.
6. **Governance**: RACI, statussen, procesraad met beslissingslog, en een wijzigingsflow die zelf een getoetst proces is.

## Oplossing in één beeld

```text
catalog.json ──► catalogus, proceshuis, capability map, site
BPMN 2.0     ──► check_models.py (R01–R13) ──► CI ──► rapport per model
procesraad   ──► beslissing ──► status released ──► verbeterportfolio
```

## Impact (doelen)

| Indicator | Start | 12 maanden |
|---|---:|---:|
| L2 met eigenaar | 33 / 41 | 41 / 41 |
| L2 vrijgegeven | 8 / 41 | 30 / 41 |
| Orders bevestigd binnen 4 werkuren | 42% | 85% |

*Illustrative assumptions — not real company data.*

## Rolfit

| Vereiste in procesrollen | Bewijs |
|---|---|
| Procescatalogus beheren | catalogus + dekking + werklijst |
| Procesarchitectuur op capabilities en E2E | capability map, procesboom, overdrachten |
| Standaarden voor modellering en documentatie | conventie, sjabloon, ADR's |
| Kwaliteit en consistentie bewaken | checklist, check in CI |
| BPMN as-is/to-be | order-to-cash |
| Analisten coachen | review OTC-03, onboarding-kit |
| Procesgovernance | RACI, procesraad, wijzigingsflow |
| Inzicht → verbetering | verbeterportfolio met KPI's |

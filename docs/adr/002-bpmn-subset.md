# ADR-002 — Een beperkt BPMN-palet in plaats van de volledige standaard

> Status: aanvaard · Datum: dag 45 · Beslissers: process architect, met de vier analisten

← [ADR-index](README.md)

## Context

BPMN 2.0 kent meer dan honderd elementen. De vier bestaande modelleerstijlen gebruikten samen 23 verschillende elementtypes, waaronder inclusive gateways en escalatie-events die lezers verschillend interpreteerden. De lezers zijn vooral key users en het ERP-team, geen BPMN-specialisten.

## Opties

| Optie | Voor | Tegen |
|---|---|---|
| A. Alles toelaten | maximale expressiviteit | modellen niet vergelijkbaar, discussies over semantiek |
| B. Alleen taken, exclusieve gateways, start/eind | eenvoudig | geen deadlines of parallel werk te tonen; uitzonderingen verdwijnen |
| C. **±15 elementen: events incl. timer/bericht/fout-boundary, taaktypes, exclusieve en parallelle gateway, subproces** | dekt wat Corvent nodig heeft, inclusief deadlines en uitzonderingen | soms een omweg nodig (inclusive → meerdere exclusieve) |

## Beslissing

Optie C, vastgelegd in de [modelleerconventie](../03-standards/modelleerconventie.md#3-het-bpmn-palet-l3) en automatisch getoetst (regel R06). Dit komt overeen met de geest van de "descriptive" en "analytic" conformance-subklassen in BPMN 2.0 ([OMG](https://www.omg.org/spec/BPMN/2.0.2/)), aangepast aan Corvent.

## Gevolgen

- Inclusive gateways worden herschreven ([voorbeeld OTC-03](../05-review/review-otc-03.md)).
- Uitbreiding van het palet kan via de wijzigingsflow, na een test op drie modellen.

# ADR-003 — Breed en ondiep eerst; diep alleen waar een project of pijnpunt het vraagt

> Status: aanvaard · Datum: dag 30 · Beslissers: process architect, COO

← [ADR-index](README.md)

## Context

Management vroeg "alle processen gedocumenteerd tegen het einde van het jaar". Het ERP-project wil binnen zes weken to-be-modellen voor order-to-cash. Er zijn vier analisten.

## Opties

| Optie | Voor | Tegen |
|---|---|---|
| A. Alle processen tot L3 uitwerken, domein per domein | volledig | 41 L3-modellen × ±5 dagen = ruim een jaar; het ERP-project wacht niet; modellen verouderen voor ze klaar zijn |
| B. **Alle L1/L2 in de catalogus met eigenaar en status (breed); L3 alleen voor OTC en waar een pijnpunt of project zit (diep)** | snel een volledig overzicht; diepte waar ze waarde heeft | sommige domeinen blijven maanden op L2 |
| C. Alleen OTC, rest later | snelst voor het ERP-project | geen organisatiebreed kader; elke analist blijft in zijn domein |

## Beslissing

Optie B. Doel 12 maanden: alle L2 met eigenaar, 30 van de 41 released. Volgorde voor L3: OTC (ERP-project) → PTP (S&OP zonder eigenaar) → ITR (geen L1-eigenaar) → rest op vraag.

## Gevolgen

- De catalogus toont eerlijk *geen model* of *draft*; dat is geen falen maar de werklijst.
- "Alles documenteren" wordt een dekkingsdoel in de governance, geen project.

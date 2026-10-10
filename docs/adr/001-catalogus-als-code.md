# ADR-001 — Procescatalogus en modellen als bestanden in git, geen repository-tool in jaar 1

> Status: aanvaard · Datum: dag 35 · Beslissers: process architect, hoofd EA, COO (budget)

← [ADR-index](README.md)

## Context

Er is dit jaar geen budget voor een procesrepository-tool (Signavio, ARIS, ADONIS, BIC …). De modellen staan nu in vier formaten op verschillende plaatsen. Het ERP-project heeft binnen zes weken één bron nodig.

## Opties

| Optie | Voor | Tegen |
|---|---|---|
| A. Wachten op budget en dan een tool kiezen | volwaardige repository, workflow, rechten | maanden zonder bron; het ERP-project wacht niet |
| B. SharePoint-lijst + Visio | bekend bij gebruikers | geen toetsing, Visio is geen open BPMN-formaat, versiebeheer zwak |
| C. **Catalogus als JSON + BPMN 2.0-bestanden in git, views gegenereerd, checks in CI** | gratis, versiebeheer en review ingebouwd, open standaard, automatische toetsing | minder gebruiksvriendelijk voor niet-technische bewerkers; geen grafische editor in de repo |

## Beslissing

Optie C. De catalogus (`catalog/catalog.json`) is de bron. Markdown-tabellen, SVG's en de site worden gegenereerd. BPMN-modellen zijn standaard BPMN 2.0 XML met diagraminformatie, gemaakt met eender welke editor (bpmn.io, Camunda Modeler, of gegenereerd).

## Gevolgen

- Wijzigingen lopen via pull requests; dat is meteen het auditspoor van de [wijzigingsflow](../06-governance/governance-model.md#wijzigingsflow).
- Business-gebruikers lezen via de site, niet in git. Stewards melden wijzigingen; analisten voeren ze door.
- **Exit:** BPMN 2.0 is importeerbaar in elke repository-tool. De catalogus is een eenvoudige tabel. Een migratie later kost dagen, geen maanden.
- Herbekijken bij meer dan ±100 L3-modellen of meer dan 6 actieve bewerkers.

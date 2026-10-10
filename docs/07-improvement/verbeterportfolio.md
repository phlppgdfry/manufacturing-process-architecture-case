# Verbeterportfolio — van procesinzicht naar initiatief

> **Wat:** de verbeterinitiatieven die uit de eerste 90 dagen kwamen, elk gekoppeld aan een proces-ID, een pijnpunt, een KPI met nulmeting en een eigenaar.
> **Voor wie:** procesraad (prioriteren), proceseigenaars, operational excellence.
> *Alle cijfers: illustrative assumption — not real company data.*

← [Procesraad](../06-governance/procesraad.md) · Volgende: [SIPOC en DMAIC voor I-02](sipoc-dmaic-i02.md) →

## Portfolio

| ID | Initiatief | Proces | Pijnpunt | KPI | Nulmeting | Doel | Eigenaar | Uitvoering | Inspanning | Prioriteit |
|---|---|---|---|---|---:|---:|---|---|---|---:|
| I-01 | Automatische kredietcheck onder de limiet | OTC-02 | P2 | % orders met manuele kredietcheck | 31% | ≤ 10% | Credit manager | ERP-project | M | 1 |
| I-02 | Haalbare leverdatum voorstellen (capaciteitscheck) | OTC-03 | P1, P3 | % orders bevestigd binnen 4 werkuren | 42% | 85% | Supply chain director (na D-03) | ERP-project + OpEx | L | 1 |
| I-03 | Productconfigurator in plaats van Excel | OTC-02 | P5 | % maatorders met overtypfout | 6% | ≤ 1% | Sales director | CRM-team | M | 2 |
| I-04 | Eigenaars en released modellen voor ITR | ITR-01..03 | geen eigenaar | L2 met eigenaar in ITR | 0 / 3 | 3 / 3 | COO (D-05) | BPM-team | S | 2 |
| I-05 | CAPA-opvolging uit Excel naar QMS | DTC-03 | schaduw-IT | CAPA's afgesloten binnen termijn | 55% | 85% | Quality director | QMS-beheer | M | 3 |

## Hoe ik prioriteer

Niet op "wie het luidst roept", maar met drie vragen die de procesraad in 15 minuten kan beantwoorden:

| Vraag | Score |
|---|---|
| Raakt het een E2E-KPI die de directie volgt (OTIF, doorlooptijd, cash)? | 0–3 |
| Heeft het proces een eigenaar die het wil? | 0 of 2 (zonder eigenaar: eerst eigenaar) |
| Is het nodig voor een lopend project (ERP)? | 0–2 |

Inspanning (S/M/L) breekt een gelijkspel. I-02 is groot, maar scoort maximaal op KPI en project; daarom krijgt het prioriteit 1, op voorwaarde dat D-03 eerst beslist wordt.

## Taakverdeling met operational excellence

| Stap | BPM-team | OpEx-team |
|---|---|---|
| Inzicht: waar zit het probleem? | catalogus, as-is, pijnpunten | gemba, data, VSM |
| Verbeteren | — | DMAIC of kaizen ([voorbeeld I-02](sipoc-dmaic-i02.md)) |
| Vastleggen | nieuwe to-be-versie, released via [STE-04](../06-governance/governance-model.md#wijzigingsflow) | levert het verbeterde proces en de nieuwe KPI-waarde aan |
| Borgen | reviewdatum, KPI op de procespagina | opvolging op de werkvloer |

Zo werken BPM en Lean naast elkaar: Lean verbetert, BPM zorgt dat de verbetering de nieuwe standaard wordt en niet na zes maanden weer wegzakt.

## Wat niet in het portfolio staat (en waarom)

- **"Alle processen documenteren tegen eind van het jaar":** geen verbetering, en niet haalbaar. Wordt een dekkingsdoel in de governance (30/41 released na 12 maanden).
- **Een procesrepository-tool:** geen budget dit jaar ([ADR-001](../adr/001-catalogus-als-code.md)). Herbekijken als er meer dan ±100 L3-modellen zijn.
- **Process mining:** waardevol voor OTC na de ERP-upgrade, als de tijdstempels betrouwbaar zijn. Nu zou het de oude chaos meten.

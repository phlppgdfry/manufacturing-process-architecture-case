# Kwaliteitschecklist voor procesmodellen en de catalogus

> **Wat:** de toetsbare regels achter de [modelleerconventie](modelleerconventie.md). Een review verwijst naar regel-ID's, niet naar smaak.
> **Voor wie:** analisten (zelfcontrole vóór review), process architect (review), de CI-pipeline.
> **Automatisch:** `python3 scripts/check_models.py` controleert R01–R13 en C01–C04. Het draait bij elke push in GitHub Actions, en het rapport staat op de [demo](https://phlppgdfry.github.io/manufacturing-process-architecture-case/demo/#review).

← [Modelleerconventie](modelleerconventie.md) · Volgende: [Documentatiesjabloon](documentatiesjabloon.md) →

## Modellen — automatisch (13)

| ID | Regel | Waarom |
|---|---|---|
| R01 | Precies één startevent per proces | één trigger = één proces; twee triggers = twee processen of een ontbrekende gateway |
| R02 | Elk element ligt op een pad van start naar een eindevent | losse draden zijn vergeten uitzonderingen |
| R03 | Taaknamen: object + werkwoord (infinitief uit de werkwoordenlijst), 2–7 woorden | leesbaar, sorteerbaar, consistent met de catalogus |
| R04 | Een splitsende gateway heeft een vraag als naam (eindigt op "?") | de lezer moet zien wat er beslist wordt |
| R05 | Uitgaande flows van een splitsende gateway hebben een label | het antwoord op de vraag |
| R06 | Alleen elementen uit het palet | elementen die lezers verkeerd interpreteren, staan er niet in |
| R07 | Elk element ligt in een lane | wie doet het? |
| R08 | Maximaal 20 activiteiten per diagram | groter = subprocessen |
| R09 | Verplichte attributen aanwezig; procesId bestaat in de catalogus; status gelijk aan de catalogus; bij released ook dezelfde eigenaar | het model en de catalogus spreken elkaar niet tegen |
| R10 | Eindevents hebben een naam (de toestand) | wat is het resultaat? |
| R11 | Lanes zijn rollen of systemen uit de rollenlijst, geen personen of afdelingen | eigenaarschap hangt aan een rol; personen wisselen |
| R12 | Elk element heeft diagraminformatie (DI) | het model rendert in elke BPMN-tool |
| R13 | Een to-be heeft minstens één uitzonderingspad (≥ 2 eindevents of een boundary event) | alleen een happy path = niet af |

## Modellen — door de reviewer (5)

| ID | Regel | Vraag die de reviewer stelt |
|---|---|---|
| M01 | Het detailniveau past bij de lezer | "Voor wie is dit model, en welke beslissing helpt het nemen?" |
| M02 | Overdrachten naar andere processen zijn expliciet | "Waar komt de input vandaan, waar gaat het resultaat naartoe, en wie is eigenaar van die overdracht?" |
| M03 | As-is: pijnpunten genummerd; to-be toont welk pijnpunt waar opgelost wordt | "Welke taak lost P2 op?" |
| M04 | Beslissingen zitten in een taak of business rule, niet verstopt in een gateway | "Wie beslist dit, op basis van welke regel?" |
| M05 | Het model klopt met de praktijk | "Met wie die het werk doet, heb je dit gevalideerd?" |

Waarom deze vijf niet automatisch: ze gaan over betekenis en context. Een script kan een gateway-naam controleren, maar niet of de beslissing bij de juiste rol ligt.

## Catalogus — automatisch (4)

| ID | Regel | Ernst |
|---|---|---|
| C01 | Elke verwijzing bestaat: L1, capability, systeem, status | fout — build faalt |
| C02 | Procesnamen volgen de naamregel (zoals R03) | fout |
| C03 | Released = eigenaar, versie, reviewdatum en model ingevuld | fout |
| C04 | Geen eigenaar, reviewdatum verstreken, dubbele naam, L1 zonder eigenaar | waarschuwing — dat is de werklijst, geen reden om de build te laten falen |

## Hoe een review loopt

1. De analist draait de check lokaal of ziet het resultaat in de pull request. Alleen modellen zonder bevindingen gaan in review; werkversies heten `*.draft.bpmn`.
2. De architect reviewt M01–M05 en geeft **maximaal 5 punten** per ronde, elk met regel-ID en een vraag in plaats van een oplossing. Zie het [voorbeeld](../05-review/review-otc-03.md).
3. Na twee rondes zonder akkoord volgt een gesprek van 30 minuten, geen derde schriftelijke ronde.

## Werkwoordenlijst

Gecontroleerde lijst (R03, C02). Ontbreekt er een werkwoord, stel het dan voor in het BPM-overleg; het komt erbij als het een activiteit beschrijft en geen resultaat.

aanmaken · aanpassen · aanvaarden · aanvragen · aanwerven · afhandelen · afsluiten · afstemmen · afwijzen · analyseren · annuleren · archiveren · beantwoorden · behandelen · beheren · beloven · beoordelen · bepalen · berekenen · beslissen · bestellen · bevestigen · bewaken · blokkeren · boeken · controleren · corrigeren · doorvoeren · escaleren · evalueren · factureren · goedkeuren · herbekijken · herplannen · heronderhandelen · informeren · inplannen · invoeren · keuren · melden · nakijken · onboarden · ontvangen · ontwikkelen · opnemen · opslaan · opstellen · opvolgen · plannen · produceren · publiceren · rapporteren · registreren · reviewen · selecteren · stockeren · sturen · terugmelden · tellen · toetsen · toewijzen · uitleveren · uitvoeren · uitwerken · valideren · vastleggen · verhelpen · verwerken · versturen · verwittigen · verzamelen · verzenden · voorstellen · vrijgeven · wijzigen

## Lokaal draaien

```bash
python3 scripts/check_models.py                 # alle modellen + catalogus
python3 scripts/check_models.py pad/naar/model.bpmn
python3 -m unittest discover -s tests           # de tests van de regels zelf
```

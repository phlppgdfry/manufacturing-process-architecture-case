# Modelleerconventie v1.0

> **Wat:** hoe iedereen bij Corvent processen tekent en beschrijft. Drie pagina's, met goed/fout-voorbeelden. De toetsbare regels staan in de [kwaliteitschecklist](kwaliteitschecklist.md); 13 daarvan controleert `scripts/check_models.py` automatisch.
> **Voor wie:** business process analysts, process stewards, key users die modellen lezen.
> **Status:** v1.0, opgesteld met de vier analisten, getest op drie bestaande modellen, goedgekeurd in procesraad #1.

← [Procescatalogus](../02-architecture/procescatalogus.md) · Volgende: [Kwaliteitschecklist](kwaliteitschecklist.md) →

## 1. Waarom een conventie

Een model is pas bruikbaar als iemand anders het kan lezen, vergelijken en aanpassen zonder de maker te bellen. Met vier stijlen lukt dat niet. Deze conventie is bewust kort: liever een kleine set die iedereen volgt dan een handboek dat niemand leest.

## 2. Per niveau: notatie en lezer

| Niveau | Notatie | Toegelaten | Niet doen |
|---|---|---|---|
| L1 | waardeketen (chevrons), gegenereerd uit de catalogus | — | geen BPMN voor management |
| L2 | catalogusregel; SIPOC als de scope onduidelijk is | — | geen verloop op L2 |
| L3 | BPMN 2.0, één pool, lanes = rollen of systemen | het palet hieronder | geen werkinstructies (dat is L4) |

## 3. Het BPMN-palet (L3)

BPMN 2.0 heeft meer dan honderd elementen ([OMG BPMN 2.0.2](https://www.omg.org/spec/BPMN/2.0.2/)). Corvent gebruikt er ±15. Waarom deze set: zie [ADR-002](../adr/002-bpmn-subset.md).

| Groep | Toegelaten | Wanneer |
|---|---|---|
| Events | start, eind, tussentijds (timer, bericht), boundary (timer, bericht, fout) | start = trigger; eind = toestand; boundary = deadline of fout tijdens een taak |
| Activiteiten | task, user, service, send, receive, manual, business rule, subproces, call activity | type = wie of wat het werk doet |
| Gateways | exclusief (X), parallel (+) | X = één pad, + = alle paden |
| Verbindingen | sequence flow; message flow alleen tussen pools | — |

**Niet toegelaten:** inclusive (O), complex en event-based gateways, transacties, compensatie, escalatie-events. Die zijn correct BPMN, maar de meeste lezers interpreteren ze verkeerd. Een inclusive gateway vervang je door een exclusieve gateway per voorwaarde, of door een parallelle gateway met condities op de paden.

## 4. Naamgeving

| Element | Regel | Goed | Fout |
|---|---|---|---|
| Proces (L2) en taak | **object + werkwoord (infinitief)**, 2–7 woorden, werkwoord uit de [werkwoordenlijst](kwaliteitschecklist.md#werkwoordenlijst) | *Leverdatum bevestigen*, *Krediet manueel controleren* | *Capaciteitscheck*, *Mail naar klant*, *Bevestig leverdatum* |
| Gateway (splitsend) | een vraag, eindigt op "?" | *Binnen kredietlimiet?* | *Check*, *Krediet* |
| Uitgaande flows van een gateway | het antwoord | *ja* / *nee*, *standaard* / *op maat* | leeg |
| Startevent | de trigger | *Order ontvangen (portaal, EDI, mail)* | *Start* |
| Eindevent | de toestand na afloop, met overdracht als die er is | *Order aanvaard (naar OTC-03)* | *Einde*, leeg |
| Lane | rol of systeem uit de rollenlijst in de catalogus | *Planner*, *ERP* | *Jan (planning)*, *Sales* |

Waarom "object + werkwoord" en niet "werkwoord + object": zo lezen catalogus en modellen gelijk ("Order aanvaarden"), en sorteert een lijst op het object.

## 5. Verplichte attributen

Elk L3-model heeft in de procesdocumentatie (BPMN `documentation`, dus leesbaar in elke tool):

```text
procesId: OTC-03
niveau: L3
type: to-be            (as-is | to-be)
eigenaar: Supply chain director
versie: 1.0
status: in-review      (= status in de catalogus; as-is-modellen hebben status "as-is")
volgt op: OTC-02 Order aanvaarden     (optioneel: overdrachten)
volgt: OTC-04 Order uitleveren
```

Het procesId moet in de catalogus bestaan. Een released model heeft dezelfde eigenaar als de catalogus.

## 6. Inhoudelijke regels

1. **Elk pad eindigt.** Geen losse draden. Wat gebeurt er als het misloopt? Dat pad hoort erbij.
2. **Een to-be toont minstens één uitzondering**: een tweede eindevent of een boundary event. Een model met alleen een happy path is niet af.
3. **Beslissingen zijn zichtbaar.** De gateway stelt de vraag, maar een taak (of business rule task) neemt de beslissing. Een gateway beslist niets.
4. **Maximaal 20 activiteiten per diagram.** Is het groter, splits dan in subprocessen.
5. **Overdrachten expliciet.** Start- en eindevents noemen het proces-ID waarvan je komt of waarnaar je gaat.
6. **As-is: pijnpunten genummerd** (P1, P2 …) als rode badge; de to-be toont welke taak welk pijnpunt oplost (groene badge). Dit komt van een van de analisten en is overgenomen omdat het traceerbaarheid gratis maakt.
7. **Teken wat er gebeurt, niet wat de procedure zegt.** Valideer een as-is met minstens één persoon die het werk doet.

## 7. Bestanden

| Wat | Waar | Formaat |
|---|---|---|
| L3-model | `docs/<map>/bpmn/<procesId>-<type>.bpmn` | BPMN 2.0 XML met diagraminformatie, opent in Camunda Modeler, bpmn.io en elke repository-tool |
| Werkversie | `*.draft.bpmn` | mag de checks nog niet halen, gaat niet in review |
| Render | `site/assets/models/*.svg` | gegenereerd |
| Beschrijving | Markdown volgens het [documentatiesjabloon](documentatiesjabloon.md) | — |

## 8. Wijzigen van deze conventie

Een voorstel tot wijziging gaat via de [wijzigingsflow](../06-governance/governance-model.md#wijzigingsflow) met de process architect als eigenaar. Kleine verduidelijkingen kunnen meteen. Een nieuwe regel geldt pas na een test op drie bestaande modellen.

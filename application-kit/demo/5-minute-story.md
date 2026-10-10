# Verhaal van 5 minuten

> Gesproken toelichting zonder slides. Natuurlijke spreektaal; niet voorlezen. Bij elke beat staat wat je kan tonen als er een scherm is.
> *Independent portfolio case — fictional organisation. Cijfers: illustrative assumptions.*

| Tijd | Beat | Wat ik zeg (kern) | Tonen |
|---|---|---|---|
| 0:00–0:30 | Het probleem | "Corvent heeft een procesboom, maar geen proceshuis. Niemand gebruikt hem: acht processen zonder eigenaar, vier analisten die elk anders tekenen, en over zes weken vraagt het ERP-project welke versie de juiste is." | landing page, uitdaging |
| 0:30–1:15 | Hoe ik begon | "Ik heb niets hertekend. De architectuur was net goedgekeurd. Ik sprak met elke analist en elke eigenaar, las tien modellen en liep een halve dag mee. De grootste problemen zaten tussen afdelingen, niet erin." | [90-dagenplan](../../docs/01-frame/90-dagenplan.md) |
| 1:15–2:00 | Structuur | "Naast de procesboom kwam een capability map. Die toonde meteen het pijnpunt: leverbelofte staat rood. Daaronder een catalogus uit één bron, met verplichte velden: eigenaar, status, capability, systemen, reviewdatum." | demo stap 1–3 |
| 2:00–2:45 | Standaard | "Drie pagina's conventie, samen met de analisten opgesteld. Achttien regels, waarvan dertien een script controleert bij elke push. Dan gaat de review over inhoud: voor wie is dit model, waar zijn de overdrachten?" | [checklist](../../docs/03-standards/kwaliteitschecklist.md), demo stap 4 |
| 2:45–3:30 | Modelleren en coachen | "Ik modelleerde order-to-cash zelf: vijf pijnpunten in de as-is, in de to-be per pijnpunt de oplossing. Een analist leverde de leverdatum aan: negen bevindingen. Ik gaf vijf vragen terug, en zijn herwerkte versie is beter dan wat ik zelf had." | demo stap 5–6 |
| 3:30–4:15 | Governance | "Wat een model niet kan oplossen, gaat naar de procesraad: wie is eigenaar van de leverdatum? Drie opties, één aanbeveling. De wijzigingsflow is zelf een proces in de catalogus en haalt zijn eigen checks." | demo stap 7–8 |
| 4:15–5:00 | Waarde en ik | "Het doel na een jaar: elk proces een eigenaar, 30 van de 41 vrijgegeven, en het ERP-project werkt vanuit één bron. Wat dit over mij zegt: ik breng structuur zonder alles opnieuw te doen, ik maak standaarden toetsbaar en ik leg conflicten bij wie erover moet beslissen." | demo stap 9–10 |

## Vragen die vaak volgen

- *"Waarom geen tool?"* → geen budget, en BPMN 2.0 is importeerbaar: [ADR-001](../../docs/adr/001-catalogus-als-code.md).
- *"Waarom geen inclusive gateway?"* → bijna iedereen leest hem anders: [ADR-002](../../docs/adr/002-bpmn-subset.md).
- *"Waarom niet alles tot L3?"* → breed en ondiep eerst: [ADR-003](../../docs/adr/003-breed-ondiep-eerst.md).

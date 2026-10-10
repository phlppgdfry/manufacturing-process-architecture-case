# Corvent Process House — case study

> *Independent portfolio case study based on a fictional organisation. It contains no confidential information from any real employer or the hiring company. All figures are illustrative assumptions — not real company data.*
> Het volledige verhaal in één document (±10 minuten). Details staan in de gelinkte documenten.

## 1. De situatie

Corvent Industries maakt ventilatie-units en luchtbehandelingscomponenten, deels op maat. Het bedrijf telt ±950 medewerkers, twee productiesites en een distributiecentrum. In 2025 liet het een procesarchitectuur tekenen op basis van business capabilities en end-to-end processen: drie lagen en tien E2E-processen, van order-to-cash tot hire-to-retire.

Een jaar later wordt die architectuur niet gebruikt. Bij de start van de nieuwe process architect:

- 41 actieve L2-processen, waarvan **8 zonder eigenaar**; het hele L1-proces issue-to-resolution heeft geen eigenaar;
- **8 processen met een vrijgegeven model**, 7 daarvan in oude formaten;
- **vier analisten, vier modelleerstijlen**;
- een **ERP-upgrade** die over zes weken met fit-to-standard-workshops begint en vrijgegeven to-be-processen nodig heeft.

[Context en scope →](docs/00-context/README.md)

## 2. Hoe ik begon: niet hertekenen

De verleiding is om een nieuwe procesboom te tekenen. Dat doe ik niet: de architectuur is net goedgekeurd, en wie hem opnieuw tekent, verliest het vertrouwen van wie hem gemaakt heeft. Ik begon met gesprekken: met elke analist, elke L1-eigenaar, enterprise architectuur en operational excellence. Ik las tien bestaande modellen en noteerde patronen, geen fouten. En ik liep een halve dag mee in customer service, planning en het magazijn.

Twee dingen vielen op. De goede gewoontes zaten verspreid: één analist nummerde pijnpunten in elk model, een ander hield systeemtaken netjes apart. En de grootste problemen zaten niet in een afdeling, maar **tussen** afdelingen. Het duidelijkste voorbeeld: sales belooft leverdatums, planning wijzigt ze, en niemand is eigenaar van de belofte.

[90-dagenplan →](docs/01-frame/90-dagenplan.md) · [Maturiteitsscan →](docs/01-frame/maturiteitsscan.md)

## 3. Structuur: capabilities, procesboom, catalogus

Ik legde een **capability map** naast de procesboom: 35 capabilities, met een heatmap van hoe goed systemen ze ondersteunen. Daaruit kwamen meteen gesprekspunten. *Leverbelofte* wordt door geen systeem ondersteund. *Marktbewerking* heeft geen enkel proces. *Klantenservice* wordt door drie processen uitgevoerd, maar het L1-proces erboven heeft geen eigenaar.

De **procescatalogus** werd één JSON-bestand met verplichte velden: ID, naam, eigenaar, status, versie, capability, systemen, reviewdatum, model en aliassen. Tabellen, diagrammen en de site worden eruit gegenereerd. Zo bestaat er één bron, en is elke wijziging zichtbaar als een diff. Er was geen budget voor een repository-tool. Omdat de modellen standaard BPMN 2.0 zijn, blijft een overstap later eenvoudig ([ADR-001](docs/adr/001-catalogus-als-code.md)).

Ik koos bewust voor **breed en ondiep**: alle L1- en L2-processen met eigenaar en status, en diepte (L3) alleen waar het ERP-project of een pijnpunt erom vraagt ([ADR-003](docs/adr/003-breed-ondiep-eerst.md)).

[Capability map →](docs/02-architecture/capability-map.md) · [Procesboom →](docs/02-architecture/procesboom.md) · [Catalogus →](docs/02-architecture/procescatalogus.md) · [Proces ↔ applicatie →](docs/02-architecture/proces-applicatie.md)

## 4. Een standaard die gevolgd kan worden

De modelleerconventie telt drie pagina's. Ze legt vast welke notatie op welk niveau, een BPMN-palet van ±15 elementen (geen inclusive gateways: die leest bijna iedereen anders), één naamregel (object + werkwoord, zoals in de catalogus) en verplichte attributen in elk model.

De conventie stelde ik op met de analisten. De regel over genummerde pijnpunten komt van een van hen.

Daaronder ligt een **checklist van 18 regels**. Dertien daarvan controleert een script automatisch bij elke push: één startevent, geen losse draden, gateways als vraag, alleen het palet, lanes als rollen, attributen consistent met de catalogus, minstens één uitzonderingspad in een to-be. De vijf andere zijn vragen voor de reviewer: voor wie is dit model, waar zijn de overdrachten, met wie is het gevalideerd?

Het effect: de review gaat over inhoud, niet over vorm.

[Conventie →](docs/03-standards/modelleerconventie.md) · [Checklist →](docs/03-standards/kwaliteitschecklist.md) · [ADR-002 →](docs/adr/002-bpmn-subset.md)

## 5. Zelf modelleren: order-to-cash

Het eerste referentiemodel is **OTC-02 Order aanvaarden**, van L1 (waardeketen) tot L3 (BPMN).

De **as-is** heeft vijf genummerde pijnpunten. De leverdatum wordt beloofd zonder capaciteitscheck (P1). De kredietcheck gaat per mail (P2). De planner wijzigt datums stil (P3). De bevestiging vertrekt vóór het kredietakkoord (P4). Configuraties op maat worden in Excel uitgewerkt (P5).

De **to-be** lost ze op met een productconfigurator, een automatische kredietcheck waarbij alleen uitzonderingen bij de credit controller komen, en een vaste volgorde: aanvaarden vóór bevestigen. Een non-interrupting timer zorgt dat de klant na vier werkuren geïnformeerd wordt terwijl de kredietbeslissing doorloopt. De leverdatum verhuist naar het volgende proces, OTC-03, met één eigenaar.

[Referentiemodel →](docs/04-reference-model/order-to-cash.md)

## 6. Coachen: een review van een analistenmodel

Een ervaren analist levert een draft van **OTC-03 Leverdatum bevestigen** aan. Het automatische rapport geeft 9 bevindingen op 7 regels: een losse draad, een inclusive gateway, lanes met een persoonsnaam, geen attributen.

De naamgeving en de labels lost de analist zelf op met de checklist. Mijn feedback telt **vijf punten, elk als vraag**: wat gebeurt er als de datum niet haalbaar is? Welke rol beslist? Waar start het proces echt?

Het gesprek legde bloot wat geen model kan oplossen: niemand is eigenaar van de bevestigde leverdatum. Dat werd een voorstel voor de procesraad. De analist stelde zelf een betere oplossing voor dan ik had: het ERP stelt een haalbare datum voor, en de planner komt alleen bij afwijkingen in beeld. De herwerkte versie haalt alle checks.

[Review →](docs/05-review/review-otc-03.md) · [Onboarding-kit →](docs/05-review/onboarding-analist.md)

## 7. Governance: wie beslist

Rollen, een RACI waarin niemand overal R én A is, en een procesraad van 60 minuten per maand die altijd minstens één beslissing neemt. De **wijzigingsflow** is zelf een proces in de catalogus (STE-04): gemodelleerd volgens de conventie, door de checks gehaald en vrijgegeven in de eerste procesraad.

Die eerste raad besliste ook over de overlap in de oude procesboom: klachten vallen voortaan alleen onder issue-to-resolution. De tweede raad krijgt het voorstel over de leverdatum. Daarin staan drie opties en een aanbeveling: de Supply chain director wordt eigenaar, standaardgevallen gaan automatisch, en sales blijft het gezicht naar de klant.

[Governance-model →](docs/06-governance/governance-model.md) · [Procesraad →](docs/06-governance/procesraad.md)

## 8. Van inzicht naar verbetering

Vijf initiatieven, elk met proces-ID, pijnpunt, KPI en nulmeting, eigenaar en prioriteit op basis van drie vragen: raakt het een E2E-KPI, is er een eigenaar, is het nodig voor een lopend project?

Operational excellence leidt de verbeterprojecten. BPM zorgt dat de verbetering als nieuwe versie in de catalogus landt, zodat ze niet wegzakt.

[Verbeterportfolio →](docs/07-improvement/verbeterportfolio.md) · [SIPOC/DMAIC →](docs/07-improvement/sipoc-dmaic-i02.md)

## 9. Wat het oplevert (doelen, illustratief)

| Indicator | Start | 90 dagen | 12 maanden |
|---|---:|---:|---:|
| L2 met eigenaar | 33 / 41 | 39 / 41 | 41 / 41 |
| L2 released | 8 / 41 | 12 / 41 | 30 / 41 |
| Modellen in review die de checks halen | — | 100% | 100% |
| Orders bevestigd binnen 4 werkuren | 42% | — | 85% |

## 10. Wat ik anders zou doen met meer tijd of in een echte organisatie

- **Process mining** op order-to-cash na de ERP-upgrade, om het echte verloop naast het model te leggen.
- **Een repository-tool** zodra er meer dan ±100 L3-modellen zijn. De BPMN-bestanden en de catalogus migreren dan zonder verlies.
- **De capability map met EA valideren** in een workshop met de L1-eigenaars, in plaats van ze op basis van de bestaande architectuur af te leiden.
- **Het referentiemodel in een fit-to-standard-workshop testen** voor het released wordt.

## 11. Wat dit over mijn manier van werken zegt

Ik breng structuur zonder alles opnieuw te tekenen. Ik maak standaarden toetsbaar, zodat de review over inhoud gaat. Ik modelleer zelf, met de uitzonderingen erbij. En ik leg conflicten bij wie erover moet beslissen in plaats van ze in een diagram te verstoppen.

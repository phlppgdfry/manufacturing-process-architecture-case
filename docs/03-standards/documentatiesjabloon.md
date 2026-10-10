# Documentatiesjabloon per proces

> **Wat:** de vaste opbouw van de beschrijving bij een L2/L3-proces, zodat elke procespagina op dezelfde plek dezelfde informatie geeft.
> **Voor wie:** analisten die een proces documenteren; iedereen die er een zoekt.

← [Kwaliteitschecklist](kwaliteitschecklist.md) · Volgende: [Referentiemodel order-to-cash](../04-reference-model/order-to-cash.md) →

## Sjabloon

```markdown
# <procesId> <Procesnaam> — <as-is | to-be> v<versie>

> Eigenaar: <rol> · Status: <status> · Review: <datum> · Capability: <ID naam> · Systemen: <…>
> Volgt op: <procesId> · Volgt: <procesId>

## Doel en resultaat
Eén zin: waarom bestaat dit proces, wat is het resultaat.

## Afbakening (SIPOC)
| Suppliers | Inputs | Process (5–7 stappen) | Outputs | Customers |

## Model
![<procesId>](<pad naar svg>) · BPMN-bestand: <pad>

## Rollen
| Rol (lane) | Doet | Beslist |

## Uitzonderingen
| Uitzondering | Waar in het model | Afhandeling |

## Regels en drempels
| Regel | Waarde | Eigenaar van de regel |

## KPI's
| KPI | Definitie | Nulmeting | Doel | Bron |

## Pijnpunten (as-is) / oplossingen (to-be)
| ID | Pijnpunt | Opgelost door (taak in to-be) |

## Open punten en beslissingen
| ID | Vraag | Wie beslist | Status |

## Wijzigingshistoriek
| Versie | Datum | Wijziging | Goedgekeurd door |
```

## Waarom deze volgorde

- **Doel en afbakening eerst**: een lezer moet in 20 seconden weten of dit het proces is dat hij zoekt.
- **Uitzonderingen en regels apart**: daar zit wat een ERP-consultant of developer nodig heeft, en het is het eerste wat in een tekst verdwijnt.
- **KPI's bij het proces, niet in een apart rapport**: de eigenaar ziet ze op dezelfde pagina als het model.

Uitgewerkt voorbeeld: [order-to-cash](../04-reference-model/order-to-cash.md).

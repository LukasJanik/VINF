# VINF Projekt 2020
## Zadanie projektu
- F3: Artists, awards, tracks + vyhľadávanie (Python/Hadoop):
    - Spracovanie a identifikovanie entít a vzťahov medzi nimi
    - Vyhľadávanie nad entitami vrátane vzťahov

### Dátová reprezentácia
Program ukladá a pracuje nad dátami v slovníku (data), kde kľúčom je entita a hodnotou je slovník s dátami k danej entite (kľúč je ID entity). Tento prístup umožňuje jednoducho zisťovať, či už existuje objekt pre danú entitu a taktiež jednoduché vytváranie prepojení medzi objektami s tým, že vykonané zmeny sú viditeľné z ktoréhokoľvek prepojenia. Nateraz uvažujeme s nasledujúcimi entitami:

- Artist
- Album
- Award
- Track
- Recording
- Genre
- Edit

### Postup spracovania
**1.prechod súboru**:
- získanie ID entít, ktoré nás zaujímajú (overenie zhody s hľadaným výrazom pomocou regex-u a následné získanie hodnoty ID)

**2.prechod súboru**:

- získavanie dát pre jednotlivé entity (zistenie v ktorom slovníku sa nachádza získané ID a následne spracovanie podľa príslušnej entity)
- pri získavaní dát rozlišujeme 2 prípady: object buď predstavuje konkrétnu hodnotu (získame danú hodnotu), alebo referenciu na ďalší objekt (vytvoríme daný objekt a uložíme jeho referenciu do príslušného slovníka a aj do aktuálne spracovavaného objektu)
- získava sa pre všetky spomínané entity okrem Award a Genre

**3.prechod súboru**:
- získavanie dát pre Award a Genre (opäť zistenie v ktorom slovníku sa nachádza získané ID a následné spracovanie podľa príslušnej entity)

**Dôvod pre odloženie získavania dát pre Award na posledný beh**:
- existujú inštancie pre Award, ktoré sa nevzťahujú k entite Artist (garancia, že získavame dáta už len o tých relevantných)
- na zisťovanie či ide o správny Award (vzťahujúci sa k Artist-ovi) a získavanie dát sa vzťahuje už vyššie spomínaný problém (možnosť preskočenia dôležitých informácií)

### Ukladanie spracovaných dát
- spracované dáta ukladáme do jedného súboru po jednotlivých entitách (jedna entita = jeden riadok)
- na serializáciu sa využíva jsonpickle


### Štruktúra programu
- main.py - predstavuje hlavný program, ktorý realizuje čítanie súboru a volá pomocné metódy pre parsovanie
- models.py - obsahuje modely pre jednotlivé entity
- parsers.py - obsahuje metódy pre parsovanie jednotlivých entít a získavanie hodnôt
- helpers.py - obsahuje metódy pre inicializáciu slovníkov a ich ukladanie do “jsonu”
- patterns.py a constants.py - obsahujú regulárne výrazy a konštanty

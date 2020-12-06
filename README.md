# VINF Projekt 2020
## Zadanie projektu
- **F3: Artists, awards, tracks + vyhľadávanie (Python/Hadoop)**:
    - Spracovanie a identifikovanie entít a vzťahov medzi nimi
    - Vyhľadávanie nad entitami vrátane vzťahov

## Obsah repozitára
Repozitár obsahuje zdrojový kód k jednotlivým fázam realizácie spracovania freebase dát:
 - **single_node_data_parsing**: obsahuje zdrojový kód pre spracovanie dát na jednom nóde (bez uvažovania Hadoop clustera)
 - **hadoop_data_parsing**: obsahuje zdrojový kód pre spracovanie dát na Hadoop clusteri s rozdelením na 3 joby (samostatný adresár pre každý job): 
    - **1st_file_pass**
    - **2nd_file_pass**
    - **3rd_file_pass**
    - Každý job obsahuje príslušný **mapper** a **reducer**
- **cluster_data_processing**: obsahuje zdrojový kód pre finálne spracovanie dát získaných z parsovania na Hadoop clusteri:
    - **filtrovanie prázdnych riadkov** (za prázdny riadok sa považuje riadok, ktorý neobsahuje ani *name* ani *description*)
    - **modely** pre jednotlivé entity a vytvorenie finálnych objektov do vyhľadávania    
    - **rozdelenie dát** podľa jednotlivých entít a vytvorenie zoznamov pre následné načítanie vo finálnom spájaní/normalizovaní
    - **normalizácia dát** pre spojenie objektov jednotlivých entít súvisiacich s artistom do finálneho objektu artistu
- **elasticsearch** pre indexovanie a realizáciu samotného vyhľadávania:
    - docker-compose pre vytvorenie elasticsearch clustera v dockeri
    - index s mappingom a analyzérmi
    - naplnenie elasticsearchu dátami
    - vyhľadávanie

## Spracovanie na jednom node (single_node_data_parsing)
- pre spustenie tejto časti je potrebné mať:
    - Python >= 3.8
    - jsonpickle
    - dostupný dump file freebasu (cesta k súboru je nastavovaná premennou file v scripte `main.py`)
- spracovanie sa spustí jednoducho spustením scriptu `main.py`

## Spracovanie na Hadoop clusteri (hadoop_data_parsing)
- **pre spustenie tejto časti je potrebné mať**:
    - Python >= 2.7
    - jsonpickle
    - Hadoop cluster
    - dump súbor freebasu 
- **postup spracovania**:
    - Nakopírovať do hadoopu adresár *hadoop_data_parsing*
    - Spustiť **prvý job**: 
        - `hadoop jar /usr/local/hadoop-2.9.2/share/hadoop/tools/lib/hadoop-streaming-2.9.2.jar -files hadoop_data_parsing/1st_pass/mapper.py,hadoop_data_parsing/1st_pass/reducer.py -mapper mapper.py -reducer reducer.py -input ./freebase -output output_pass_1`
    - Výsledok behu nakopírovať do hadoop_data_parsing/2nd_pass a pomenovať ho ako input 
    - Spustiť **druhý job**: 
        - `hadoop jar /usr/local/hadoop-2.9.2/share/hadoop/tools/lib/hadoop-streaming-2.9.2.jar -files hadoop_data_parsing/2nd_pass/mapper.py,hadoop_data_parsing/2nd_pass/reducer.py,hadoop_data_parsing/2nd_pass/input -mapper mapper.py -reducer reducer.py -input ./freebase -output output_pass_2`
    - Skopírovať a prefiltrovať výstup z druhého jobu: `.... | grep '.*\"entity_type\": \"award_honor\"' > hadoop_data_parsing/3rd_pass/input`
    - Spustiť **tretí job**: 
        - `hadoop jar /usr/local/hadoop-2.9.2/share/hadoop/tools/lib/hadoop-streaming-2.9.2.jar -files hadoop_data_parsing/3rd_pass/mapper.py,hadoop_data_parsing/3rd_pass/reducer.py,hadoop_data_parsing/3rd_pass/input -mapper mapper.py -reducer reducer.py -input ./freebase -output output_pass_3`

## Finálne spracovanie dát z clustera (cluster_data_processing)
- **pre spustenie tejto časti je potrebné mať**:
    - Python >= 2.7
    - jsonpickle
    - výsledky parsovania z Hadoop-u (výsledok 2. a 3. jobu)
- **postup spracovania**:
    - vyfiltrovať prázdne riadky:
        - `cat output_2 | python filter_empty_rows.py > filtered_output_2` 
        - `cat output_3 | python filter_empty_rows.py > filtered_output_3`
    - vytvoriť adresáre `filtered_output` a `final_output`
    - spustiť script `split_data.py` a následne script `normalize_data.py`

## Elasticsearch
- **pre spustenie tejto časti je potrebné mať**:
    - Python >= 2.7
    - elasticsearch (client pre Python)
    - Docker
- **postup spracovania**:
    - spustiť docker-compose up v adresári `elasticsearch`:
        - vykoná vytvorenie a spustenie elasticsearch clustera s 3 nodmi
    - po spustení clustera:
        - **vytvoriť index s mappingom a analyzérmi**: 
            - poslať `PUT` request na `localhost:9200/music/` cez klienta (napr. Insomnia alebo Postman) s obsahom súboru `music_mapping_with_analyzers.json`
        - spustiť script `json_extraction.py`, ktorý realizuje naplnenie elasticsearch-u dátami z predošlého spracovania

## Klient pre vyhľadávanie
- klient pre vyhľadávanie je realizovaný prostredníctvom CLI
- **umožňuje**:
    - **zápis query priamo v konzole**
        - pre jednotlivé časti query sú určené prepínače (napr. `-a` pre AND, `-o` pre OR) formát pre query je nasledovný: -prepínač atribút = hodnota? (viaceré atribúty pre jeden prepínač sú oddelené “;”)
        - podporované queries = `AND`, `OR`, `Range`, `fulltext` (query_string - podporuje taktiež OR, AND, …), `skórovanie výsledkov` na základe zvoleného atribútu: `no_of_albums | no_of_awards_won | no_of_tracks (default)`
    - **čítanie query zo súboru**
    - **nastavovanie výstupu**:
        - zoznam atribútov, ktoré majú byť na výstupe
        - limitovanie počtu výsledkov
    - **zobrazovanie**:
        - formatovaných výsledkov
        - štatistík

![alt text](http://luky.janik-online.sk/CLI_client.png)
![alt text](http://luky.janik-online.sk/sample_result.png)
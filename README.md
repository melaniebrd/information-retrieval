# Information Retrieval

Search engine for school project in IS3013AA (RI-W) at Centrale Supelec

### Table of contents: 
+ **[1. Getting Started](#1-getting-started)**
    + **[1.1 Prerequisites](#11-prerequisites)**
    + **[1.2 Build the linguistic treatment](#12-build-the-linguistic-treatment)**
    + **[1.3 Build the index](#13-build-the-index)**
    + **[1.4 Query search](#14-query-search)**
+ **[2. Rapport](#2-rapport-in-french)**
    + **[2.1 Traitements Linguistics](#21-traitements-linguistics)**
    + **[2.2 Création de l'index inversé](#22-création-de-lindex-inversé)**
    + **[2.3 Modèles de recherche](#23-modèles-de-recherche)**
        + **[Modèle booléen](#modèle-booléen)**
        + **[Modèle vectoriel](#modèle-vectoriel)**
    + **[2.4 Performances](#24-performances)**
    + **[2.5 Conclusion](#25-conclusion)**
+ **[3. Authors](#3-authors)**
+ **[4. License](#4-license)**

## 1. Getting started

### 1.1 Prerequisites

What things you need to install the software :
* Python3
* virtualenv

Run the script below to create your virtual env:
```
virtualenv ENV
```

Run the script below to activate your virtual env:
```
source ENV/bin/activate
```

Run the script below to download the requirements with pip:
```
pip3 install -r requirements.txt
```

Run the script below to deactivate your virtual env:
```
deactivate
```

Add the CACM and CS276 data collection in the `data/` folder :
- [data/CACM]()
..* [cacm.all]()
..* [common_words]()
..* [qrels.text]()
..* [query.text]()
- [data/CS276]()
..* [pa1-data/0/...]()


### 1.2 Build the linguistic treatment

Use the [main_linguistic_treatment.py](main_linguistic_treatment.py) file to trigger the collections' terms tokenization.

You can add the following arguments:
* `-l <c>` : to get the linguistic treatment of the cacm or cs276 collection
* `-f <c>` : to get the linguistic treatment with vocabulary frequencies, of the cacm or cs276 collection
* `-h <c>` : to get heap parameters from the linguistic treatment for the cacm or cs276 collection
* `-g <c>` : to get the graph representation from the linguistic treatment of cacm or cs276

Example for cacm:
```
python3 main_linguistic_treatment.py -l cacm
```
Example for cs276:
```
python3 main_linguistic_treatment.py -l cs276
```

### 1.3 Build the index

Use the [main_index.py](main_index.py) file to build the collection's index.

You can add the following arguments:
* `-b <c>` : to build the collection's index and then save it into the folder [indexes/](indexes/)
* `-g <c>` : to get the collection's index from the [indexes/](indexes/) folder

Example for cacm:
```
python3 main_index.py -b cacm
```
Example for cs276:
```
python3 main_index.py -b cs276
```

### 1.4 Query search

Use the [main_search.py](main_search.py) file to search informations in the collections.

You can add the following arguments:
* `-bool <c>` : to do a boolean search in the collection c
* `-vect <c>` : to do a vectorial search in the collection c (cacm or cs276)
In both cases, you must have the indexes already saved in the [indexes/](indexes/) folder. To build them, use the following code ```python3 main_index.py -b cacm```

Example for cacm with the boolean search:
```
python3 main_search.py -bool cacm
```
Example for cs276 with the vectorial search:
```
python3 main_search.py -vect cs276
```
Here is how the interaction with the search engine appears for the boolean search:
```
##### Welcome to the CS Search Engine #####

# To type a request, use the following syntax :
# 'NOT (term1 OR term2) AND (term3 OR term4) AND NOT (term5 OR term6)'

# Type your request :
Algorithm AND Programming AND (Style OR Algebra)

# Results : 3 files found

# Showing 1 to 3 of 3 files

- DOC ID 3137 (points : 6): A Mathematical Programming Updating Method Using Modified Givens Transformations and Applied to LP Problems
- DOC ID 1913 (points : 5): Matrix Scaling by Integer Programming (Algorithm 348 [F1])
- DOC ID 1869 (points : 3): Some Techniques for Using Pseudorandom Numbers in Computer Simulation

################################################################################

# Do you want to type a new request ? y/n

```

## 2. Rapport (in French)

### 2.1 Traitements Linguistics

Les fichiers correspondants au traitement linguistique des deux collections (CACM et CS276) dont les suivants:
- [main_linguistic_treatment.py](main_linguistic_treatment.py) : permet de lancer le traitement linguistique en ligne de commande
- [linguistic_treatment.py](linguistic_treatment.py) : permet de construire les tokens ainsi que le vocabulaire (avec ou sans term_frequency) pour chacune des deux collections.

Voici les résultats de la tokenisation de CACM et CS276 :

| Collection    |   CACM  |    CS276    |
|---------------|---------|-------------|
| Tokens        | 222 373 |  25 498 340 |
| Vocabulary    |   8 976 |     346 650 |
| Half tokens   | 111 186 |  12 749 170 |
| Half vocab    |   6 393 |     177 266 |
| Heap param k  |  21.641 |    0.023639 |
| Heap param b  | 0.48958 |     0.96756 |
| Voc (1Million)|  18 738 |      15 100 |

#### Graphes fréquence (f) vs rang (r) :
- CACM :
![alt text](images/cacm_freq_vs_rank.png "CACM frequence (f) vs rang (r)")
- CS276 :
![alt text](images/cs276_freq_vs_rank.png "CS276 frequence (f) vs rang (r)")

#### Graphes logarithme de la fréquence (log(f)) vs logarithme du rang (log(r)) :
- CACM :
![alt text](images/cacm_log_freq_vs_log_rank.png "CACM Logarithme de la frequence vs Logarithme du rang")
- CS276 :
![alt text](images/cs276_log_freq_vs_log_rank.png "CS276 Logarithme de la frequence vs Logarithme du rang")


### 2.2 Création de l'index inversé

#### Choix d'implémentation et stratégie utilisée
Pour représenter un index (CACM ou CS276), j'ai choisi d'implémenter une classe Index dont allait hérité les deux classes CACMIndex et CS276Index.

Chaque classe possède les propriétés suivantes :
```
self.collection_name = collection_name
self.doc_ids = {}     # { doc_id : doc } : dictionnaire de (document_id, document)
self.term_ids = {}    # { term_id : term } : dictionnaire de (terme, terme_id)
self.index = {}       # { term_id : [(doc_id_0, freq_0), ..., (doc_id_10, freq_10)] } : liste de postings pour chaque terme_id
```

La collection CACM a été considérée comme un seul bloc, en revanche, pour CS276, j'ai considéré chaque sous répertoire du dossier pa1-data comme un bloc.

La création de l'index de CACM se déroule ainsi:
- Création du dictionnaire de (terme, terme_id) à partir du traitement linguistique fait précédemment : `self.term_ids`
- Parcours de tous les documents :
..* Attribution d'un document_id
..* Ajout dans l'index `self.index` du tuple (document_id, frequency)  pour tous les term_id présents dans le document
- Sauvegarde de l'index, et des dictionnaires de (document_id, document) et (terme, terme_id) dans [indexes/cacm/](indexes/cacm/)

La création de l'index CS276 se déroule de la façon suivante :
- Création du dictionnaire de (terme, terme_id) à partir du traitement linguistique fait précédemment : `self.term_ids`
- Parcours de tous les blocs (10 en tout) :
..* Création de l'index de ce bloc (même méthode que pour CACM)
..* Sauvegarde de cet index dans le dossier [indexes/cs276/temporary/](indexes/cs276/temporary/)
- Fusion des index des 10 blocs enregistrés dans le dossier [indexes/cs276/temporary/](indexes/cs276/temporary/)
..* Fusion de deux index, par exemple: `index_0.txt` et `index_1.txt`
..* Sauvegarde temporaire de l'index fusionné : `index_01.txt`
..* Recommencer jusqu'à ce qu'il n'y ait plus qu'un seul index.
- Sauvegarde de l'index final dans le dossier [indexes/cs276/](indexes/cs276/)
- Le dictionnaire de (document_id, document) est mis à jour régulièrement et sauvegardé à la fin dans le même dossier

#### Performances
Les performances détaillées de création des deux index (CACM et CS276) sont enregistrées ici:
- [results/cacm_cProfile.txt](results/cacm_cProfile.txt)
- [results/cs276_cProfile.txt](results/cs276_cProfile.txt)

| Collection | Durée de création | Taille de l'index |
|------------|-------------------|-------------------|
|    CACM    |     1.779 seconds |             1.1 Mo|
|    CS276   |   129.393 seconds |            79.4 Mo|


### 2.3 Modèles de recherche

#### Modèle Booléen

#### Modèle Vectoriel

### 2.4 Performances
Évaluation pour la collection CACM

### 2.5 Conclusion
Une conclusion (améliorations possibles, ...)







## Authors
* Melanie Berard

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
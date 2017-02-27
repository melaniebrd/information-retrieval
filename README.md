# Information Retrieval

Search engine for school project in IS3013AA (RI-W) at Centrale Supelec

## Getting started

### Prerequisites

What things you need to install the software :
* Python3
* virtualenv

Run the script below to download the requirements with pip:
```
pip3 install -r requirements.txt
```

### Build the linguistic treatment (tokenisation)

Use the [main_linguistic_treatment.py](main_linguistic_treatment.py) file to trigger the collections tokenization.

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

### Build the index

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

### Search queries

Use the [main_search.py](main_search.py) file to search informations in the collections.

You can add the following arguments:
* `-bool <c>` : to do a boolean search in the collection c
* `-vect <c>` : to do a vectorial search in the collection c (cacm or cs276)
In both cases, you must have the indexes already saved in the [indexes/](indexes/) folder. To build them, use the following code ```python3 main_index.py -b cacm```

Example for cacm:
```
python3 main_search.py -bool cacm
```
Example for cs276:
```
python3 main_search.py -vect cs276
```
Here is how the interaction with the search engine appears:
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
...
```

## Authors
* Melanie Berard

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
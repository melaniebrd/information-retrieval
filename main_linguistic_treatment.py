from linguistic_treatment import LinguisticTreatment, CACMLinguisticTreatment, CS276LinguisticTreatment
from settings import CACM, CS276

from math import floor
import time
import sys


def build_liguistic_treatment(collection_name, build_frequencies=False, heap_parameters=False):
    if collection_name == CACM:
        linguistic_treatment = CACMLinguisticTreatment(build_frequencies=build_frequencies)
    else:
        linguistic_treatment = CS276LinguisticTreatment(build_frequencies=build_frequencies)
    print("Size of the token list : %s" % linguistic_treatment.get_tokens_size())
    print("Size of the vocabulary list : %s" % linguistic_treatment.get_vocabulary_size())
    if build_frequencies:
        linguistic_treatment.print_ranks()
    if heap_parameters:
        (k,b) = linguistic_treatment.get_heap_parameters()
        print("Heap's law parameters : k = %s | b = %s" % (k,b))
        t = pow(10, 6)
        voc_size = floor(k * pow(t, b))
        print("Estimated vocabulary size for 10^6 tokens : %s" % voc_size)


def help():
    print("Usage: ./main_linguistic_treatment.py <arguments>")
    print("  -l <c>       to get the linguistic treatment of the cacm or cs276 (c)")
    print("  -f <c>       to get the linguistic treatment with vocabulary frequencies, of the cacm or cs276 (c)")
    print("  -h <c>       to get heap parameters from the linguistic treatment of the cacm or cs276 (c)")
    print("  -g <c>       to get the graph representation from the linguistic treatment of cacm or cs276 (c)")


if __name__ == "__main__" :
    collection_name = str(sys.argv[2]) if len(sys.argv) > 2 else None
    if collection_name not in [CACM, CS276]:
        help()
    elif len(sys.argv) == 3 and sys.argv[1] == "-l":
        build_liguistic_treatment(collection_name)
    elif len(sys.argv) == 3 and sys.argv[1] == "-f":
        build_liguistic_treatment(collection_name, build_frequencies=True)
    elif len(sys.argv) == 3 and sys.argv[1] == "-h":
        build_liguistic_treatment(collection_name, heap_parameters=True)
    elif len(sys.argv) == 3 and sys.argv[1] == "-g":
        build_liguistic_treatment(collection_name)
    else:
        help()

from search import BooleanSearch, VectorialSearch
from settings import CACM, CS276

import sys


def search(collection_name, search_type):
    if search_type == "bool":
        search = BooleanSearch(collection_name)
    else:
        search = VectorialSearch(collection_name)
    print_separation(120)
    print("#" * 5 + " Welcome to the CS Search Engine " + "#" * 5 + "\n")
    new_request = True
    while new_request:
        search_for_request(search)
        print_separation(80)
        print("# Do you want to type a new request ? y/n")
        new_request = read_line() == 'y'
        print_separation(80)
    print("Goodbye :)\n")

def search_for_request(search):
    print("# To type a request, use the following syntax :")
    print("# 'NOT (term1 OR term2) AND (term3 OR term4) AND NOT (term5 OR term6)'\n")
    print("# Type your request :")
    text_request = read_line()
    result, frequencies = search.search(text_request)
    plural = "s" if len(result) > 1 else ""
    print("\n# Result%s : %s file%s found" % (plural, len(result), plural))
    print_more = True
    index = 0
    while print_more and (index == 0 or index < len(result)) and len(result) > 0:
        max_index = min(len(result) - 1, index + 10 - 1)
        print("\n# Showing %s to %s of %s files\n" % (index + 1, max_index + 1, len(result)))
        for doc_id in result[index:max_index + 1]:
            print("- DOC ID %s (points : %s): %s" % (doc_id, frequencies[doc_id], search.index.doc_ids[doc_id]))
        if max_index == index + 10 - 1:
            print("# Print more ? y/n")
            print_more = (read_line() == 'y')
        index += 10

def print_separation(length):
    print("\n"+ "#" * length + "\n")

def read_line():
    user_input = sys.stdin.readline()
    user_input = str(user_input)
    user_input = user_input.replace("\n", "")
    return user_input

def help():
    print("Usage: ./main_search.py <arguments>")
    print("  -bool <c>         to do a boolean search in the collection c (cacm or cs276)")
    print("  -vect <c>         to do a vectorial search in the collection c (cacm or cs276)")


if __name__ == "__main__":
    collection_name = str(sys.argv[2]) if len(sys.argv) > 2 else None
    if collection_name not in [CACM, CS276]:
        help()
    elif len(sys.argv) == 3 and sys.argv[1] == "-bool":
        search(collection_name, search_type="bool")
    elif len(sys.argv) == 3 and sys.argv[1] == "-vect":
        search(collection_name, search_type="vect")
    else:
        help()
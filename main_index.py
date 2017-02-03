from index import CACMIndex, CS276Index
from settings import CACM, CS276

import sys

def build_index(collection_name, build_dictionaries=False):
    if collection_name == CACM:
        index = CACMIndex(build_dictionaries=build_dictionaries)
    else:
        index = CS276Index(build_dictionaries=build_dictionaries)
    if build_dictionaries:
        index.save_all()
    else:
        print("Doc IDs length : %s" % len(index.doc_ids))
        print("Term IDs length : %s" % len(index.term_ids))
        print("Index length : %s" % len(index.index))


def help():
    print("Usage: ./main_index.py <arguments>")
    print("  -b <c>         to build the collection c index (c == cacm or c == cs276)")
    print("  -g <c>         to get the collection c index (c == cacm or c == cs276)")


if __name__ == "__main__":
    collection_name = str(sys.argv[2]) if len(sys.argv) > 2 else None
    if collection_name not in [CACM, CS276]:
        help()
    elif len(sys.argv) == 3 and sys.argv[1] == "-b":
        build_index(collection_name, build_dictionaries=True)
    elif len(sys.argv) == 3 and sys.argv[1] == "-g":
        build_index(collection_name)
    else:
        help()

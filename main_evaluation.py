from evaluation import Evaluation

import sys


def get_evaluation(build_dictionaries=False):
    evaluation = Evaluation(build_dictionaries=build_dictionaries)
    evaluation.precision_recall()


def help():
    print("Usage: ./main_evaluation.py <arguments>")
    print("  -g           to get the precision and recall graph for cacm")
    print("  -gb          to get the precision and recall graph for cacm and build all the index")


if __name__ == "__main__" :
    if len(sys.argv) > 1 and sys.argv[1] == "-g":
        get_evaluation()
    elif len(sys.argv) > 1 and sys.argv[1] == "-gb":
        get_evaluation(build_dictionaries=True)
    else:
        help()
from evaluation import Evaluation

import sys


def get_evaluation(evaluation_type, build_dictionaries=False):
    evaluation = Evaluation(build_dictionaries=build_dictionaries)
    if evaluation_type == "-g":
        evaluation.show_precision_recall()
    elif evaluation_type == "-m":
        map_value = evaluation.mean_average_precision()
        print("MAP : %s" % map_value)


def help():
    print("Usage: ./main_evaluation.py <arguments>")
    print("  -g           to get the precision and recall graph for cacm")
    print("  -gb          to get the precision and recall graph for cacm and build all the index")
    print("  -m           to get the MAP (Mean Average Precision) value for cacm")

if __name__ == "__main__" :
    if len(sys.argv) > 1 and sys.argv[1] == "-g":
        get_evaluation("-g")
    elif len(sys.argv) > 1 and sys.argv[1] == "-gb":
        get_evaluation("-g", build_dictionaries=True)
    elif len(sys.argv) > 1 and sys.argv[1] == "-m":
        get_evaluation("-m")
    else:
        help()
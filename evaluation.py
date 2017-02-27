from graph_representation import show
from index import CACMIndex
from search import VectorialSearch
from settings import CACM, CACM_QUERY_PATH, CACM_QUERY_RESULT_PATH, INITIAL_MARKER, QUERY_MARKER, PREFIX


class Evaluation(object):
    """
    This class is used only by CACM for the moment
    """

    def __init__(self, build_dictionaries=False):
        self.index = CACMIndex(build_dictionaries=build_dictionaries)
        self.search = VectorialSearch(CACM)

    def precision_recall(self):
        queries = self.upload_queries()
        results = self.upload_correct_results()
        for query_id in queries:
            if query_id in results:
                doc_ids, frequencies = self.search.search(queries[query_id])
                precisions, recalls = [], []
                # i is the current index of the doc_ids list
                i = 0
                # Current number of correct doc_ids found
                correct_doc_ids = 0
                while (len(recalls) < len(results[query_id]) and i < len(doc_ids)):
                    if doc_ids[i] in results[query_id]:
                        # Update the number of current doc found
                        correct_doc_ids += 1
                        # Add the precision and recall values to the precisions and recalls lists 
                        precision = round(float(correct_doc_ids)/(i+1), 4)
                        recall = round(float(correct_doc_ids)/len(results[query_id]), 4)
                        precisions.append(precision)
                        recalls.append(recall)
                    i += 1
            show(recalls, "Recalls in %", precisions, "Precision in %")

    def upload_queries(self):
        queries = {}
        with open(CACM_QUERY_PATH, 'r') as content_file:
            line = content_file.readline()
            while line:
                if line.startswith(PREFIX + INITIAL_MARKER):
                    query_id = int(line.lstrip(PREFIX + INITIAL_MARKER + " "))
                    line = content_file.readline()
                    if not line.startswith(PREFIX + QUERY_MARKER):
                        raise SyntaxError
                    line = content_file.readline()
                    line = line[1:]
                    query = ""
                    while not line.startswith(PREFIX):
                        line = line.replace('\n', ' ')
                        query += line
                        line = content_file.readline()
                    queries[query_id] = query
                line = content_file.readline()
        return queries

    def upload_correct_results(self):
        results = {}
        with open(CACM_QUERY_RESULT_PATH, 'r') as content_file:
            line = content_file.readline()
            while line:
                line = line.split()
                query_id = int(line[0])
                query_doc_id = int(line[1]) - 1      # -1 because my document indexation starts at 0 (instead of 1)
                if query_id not in results:
                    results[query_id] = []
                results[query_id].append(query_doc_id)
                line = content_file.readline()
        return results
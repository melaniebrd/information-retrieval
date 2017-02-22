from index import CACMIndex, CS276Index
from settings import CACM, CS276

from re import split
from string import lower, lstrip


class Search(object):

    def __init__(self, collection_name, build_dictionaries=False):
        self.collection_name = collection_name
        if self.collection_name == CACM:
            # By default, build_dictionay will be false because we can get the 
            # indexes from the indexes/../index.txt files
            self.index = CACMIndex(build_dictionaries=build_dictionaries)
        else:
            # Same here with build_dictionary
            self.index = CS276Index(build_dictionaries=build_dictionaries)


    def search(self):
        pass


class BooleanSearch(Search):
    AND = "and"
    OR = "or"
    NOT = "not"

    def search(self, text_request):
        """
        In order to process the search, the text_request must be written with a 
        Conjonctive Normal Form. For example if we call x1, x2, ..., xn the 
        searched terms, the request will look like this:
        NOT (x1 OR x2) AND (x3 OR x4 OR x5) AND NOT (x6 OR .. OR xn)
        :param text_request: a string representing the request
        """
        text_request = lower(text_request)
        positive_clauses, negative_clauses = self.convert_request(text_request)
        positive_postings, positive_frequencies = self.get_postings(positive_clauses)
        negative_postings, negative_frequencies = self.get_postings(negative_clauses)
        result = positive_postings - negative_postings
        result, frequencies = self.order_result_by_frequencies(result, positive_frequencies)
        return result, frequencies

    def convert_request(self, text_request):
        """
        Convert string request to array :
        "NOT (x1 OR x2) AND (x3 OR x4 OR x5) AND NOT (x6 OR .. OR xn)"
        to the array [NOT, (x1, x2), (x3, x4, x5), NOT, (x6, ..., xn)]
        :param text_request: a string representing the request 
        """
        request = split(" %s " % self.AND, text_request)
        negative_clauses = []
        positive_clauses = []
        # request = ['NOT (x1 OR x2)', '(x3 OR x4 OR x5)', 'NOT (x6 OR .. OR xn)']
        for clause in request:
            if clause.startswith(self.NOT):
                clause = lstrip(clause, "%s " % self.NOT)
                clause = self.format_clause(clause)
                negative_clauses.append(clause)
            else:
                clause = self.format_clause(clause)
                positive_clauses.append(clause)
        return positive_clauses, negative_clauses

    def format_clause(self, clause):
        """
        :param clause: string representing a clause, for example "(x1 OR x2 OR x3)"
        """
        clause = clause.replace("(", "")
        clause = clause.replace(")", "")
        clause = split(" %s | " % self.OR, clause)
        return clause

    def get_postings(self, clauses):
        frequencies = {}
        merged_postings = None if len(clauses) > 0 else set()
        for clause in clauses:
            # For each term of the clause, get the list of doc_id where the term appear,
            # and add it to the "postings" array
            postings = set()
            for term in clause:
                if term in self.index.term_ids:
                    postings = postings | set([doc_tuple[0] for doc_tuple in self.index.index[self.index.term_ids[term]]])
                    for doc_tuple in self.index.index[self.index.term_ids[term]]:
                        if doc_tuple[0] not in frequencies:
                            frequencies[doc_tuple[0]] = 0
                        frequencies[doc_tuple[0]] += doc_tuple[1]
            if merged_postings == None:
                merged_postings = postings
            elif len(postings) != 0:
                merged_postings = merged_postings & postings
        return merged_postings, frequencies

    def order_result_by_frequencies(self, result, frequencies):
        filtered_frequencies = {doc_id : frequencies[doc_id] for doc_id in result}
        result = sorted(filtered_frequencies, key=filtered_frequencies.get)
        result.reverse()
        return result, filtered_frequencies


class VectorialSearch():
    TF_IDF = "tf-idf"                       # TF-IDF
    NORM_TF_IDF = "norm-tf-idf"             # Normalized TF-IDF
    NORM_FREQ = "norm-freq"                 # Normalized Frequency

    def __init__(self, collection_name, weight_method, build_dictionaries=False):
        if weight_method in [TF_IDF, NORM_TF_IDF, NORM_FREQ]:
            self.weight_method = weight_method
        else:
            self.weight_method = TF_IDF
        super(VectorialSearch, self).__init__(collection_name=collection_name, build_dictionaries=build_dictionaries)


    def search(self, text_request):
        """
        In order to process the search, the text_request is transformed into a request_vector
        in the space of dimension n, with n = the length of terms saved in the index.
        """
        return result, frequencies

    def get_vector(self, request):
        pass
from index import CACMIndex, CS276Index
from settings import CACM, CS276

from collections import Counter
from math import log
from re import split


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


    def search(self, text_request):
        """
        ::param text_request: the request as the user entered it
        ::output result,frequencies:
        """
        pass

    def get_postings(self, request):
        """
        Returns : "result, frequencies" or "result, similitudes"
        result : [doc_id_1, doc_id_2, doc_id_3, ...] ordered by frequency or similitude
        similitudes or frequencies = {doc_id_1: 0.70, doc_id_2: 0.56, doc_id_3: 0.98}
        """
        pass

    def order_result_by_frequencies_or_similitudes(self, result, frequencies):
        filtered_frequencies = {doc_id : frequencies[doc_id] for doc_id in result}
        result = sorted(filtered_frequencies, key=filtered_frequencies.get)
        result.reverse()
        return result, filtered_frequencies


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
        text_request = text_request.lower()
        positive_clauses, negative_clauses = self.convert_request(text_request)
        positive_postings, positive_frequencies = self.get_postings(positive_clauses)
        negative_postings, negative_frequencies = self.get_postings(negative_clauses)
        result = positive_postings - negative_postings
        result, frequencies = self.order_result_by_frequencies_or_similitudes(result, positive_frequencies)
        # frequencies = {doc_id: frequency}
        # result = [doc_id_1, doc_id_2, ...]
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
                clause = clause.lstrip("%s " % self.NOT)
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


class VectorialSearch(Search):
    TF_IDF = "tf-idf"                       # TF-IDF
    NORM_TF_IDF = "norm-tf-idf"             # Normalized TF-IDF
    NORM_FREQ = "norm-freq"                 # Normalized Frequency

    def __init__(self, collection_name, weight_method=TF_IDF, build_dictionaries=False):
        if weight_method in [self.TF_IDF, self.NORM_TF_IDF, self.NORM_FREQ]:
            self.weight_method = weight_method
        else:
            self.weight_method = self.TF_IDF
        super(VectorialSearch, self).__init__(collection_name=collection_name, build_dictionaries=build_dictionaries)


    def search(self, text_request):
        """
        In order to process the search, the text_request is transformed into the list of terms ids request_term_ids
        in the space of dimension n, with n = the length of terms saved in the index.
        """
        request_term_ids = self.get_request_term_ids(text_request)
        result, similitudes = self.get_postings(request_term_ids)
        result, similitudes = self.order_result_by_frequencies_or_similitudes(result, similitudes)
        return result, similitudes

    def get_request_term_ids(self, request):
        """
        Transform the request into a list of term_ids request = [q1, q2, ...]
        """
        request = request.lower()
        request_term_ids = [self.index.term_ids[term] for term in split('\W+', request) if not term.isdigit() and term in self.index.term_ids]
        return request_term_ids

    def get_postings(self, request_term_ids):
        doc_ids = set()
        df = {}
        if request_term_ids == []:
            return [], {}
        for term_id in request_term_ids:
            doc_ids = doc_ids | set([doc_tuple[0] for doc_tuple in self.index.index[term_id]])
        # Calculate the df list
        N = float(len(doc_ids))
        for term_id in request_term_ids:
            df[term_id] = round(float(len(self.index.index[term_id]))/N, 4)
        # Calculate the tf dictionary
        tf = {}
        for term_id in request_term_ids:
            for doc_tuple in self.index.index[term_id]:
                tf[(term_id, doc_tuple[0])] = doc_tuple[1]
        # Calculate the weights from tf, df and N
        # weights : key = (term_id, doc_id), value = weight of the term term_id in the doc doc_id
        weights = {}
        for term_id in request_term_ids:
            for doc_id in doc_ids:
                if (term_id, doc_id) in tf:
                    term_frequency = tf[(term_id, doc_id)]
                    if self.weight_method == self.TF_IDF:
                        weights[(term_id, doc_id)] = self.get_tf_idf_weight(term_frequency, N, df[term_id])
                else:
                    weights[(term_id, doc_id)] = 0
        query_weights = {}
        request_term_ids_counter = Counter(request_term_ids)
        for term_id in request_term_ids_counter:
            query_weights[term_id] = round(float(request_term_ids_counter[term_id])/float(len(request_term_ids)), 4)
        similitudes = self.get_similitudes(weights, request_term_ids, query_weights, doc_ids)
        return doc_ids, similitudes

    def get_similitudes(self, weights, request_term_ids, query_weights, doc_ids):
        query_norm = sum([pow(query_weights[term_id], 2) for term_id in request_term_ids])
        similitudes = {}
        for doc_id in doc_ids:
            #doc_norm = sum([pow(weights[(term_id, doc_id)], 2) for term_id in request_term_ids])
            doc_norm = 1
            numerator_sim = 0
            for term_id in request_term_ids:
                numerator_sim += query_weights[term_id] * weights[(term_id, doc_id)]
            similitudes[doc_id] = round(float(numerator_sim)/float(doc_norm * query_norm), 4)
        return similitudes

    def get_tf_idf_weight(self, tf, N, dft):
        """
        Returns the weight with the TF-IDF method
        """
        return (1 + log(tf, 10)) * log(N/dft, 10)



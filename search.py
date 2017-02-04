from index import CACMIndex, CS276Index
from settings import CACM, CS276

from re import split
from string import lower, lstrip


class BooleanSearch():
    AND = "and"
    OR = "or"
    NOT = "not"

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
        In order to process the search, the text_request must be written with a 
        Conjonctive Normal Form. For example if we call x1, x2, ..., xn the 
        searched terms, the request will look like this:
        NOT (x1 OR x2) AND (x3 OR x4 OR x5) AND NOT (x6 OR .. OR xn)
        :param text_request: a string representing the request
        """
        text_request = lower(text_request)
        positive_clauses, negative_clauses = self.convert_request(text_request)
        positive_postings = self.get_postings(positive_clauses)
        negative_postings = self.get_postings(negative_clauses)
        result = positive_postings - negative_postings
        return result

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
        merged_postings = None if len(clauses) > 0 else set()
        for clause in clauses:
            # For each term of the clause, get the list of doc_id where the term appear,
            # and add it to the "postings" array
            postings = set()
            for term in clause:
                if term in self.index.term_ids:
                    postings = postings | set(self.index.index[self.index.term_ids[term]])
            if merged_postings == None:
                merged_postings = postings
            else:
                merged_postings = merged_postings & postings
        return merged_postings



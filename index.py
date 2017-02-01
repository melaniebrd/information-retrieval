from linguistic_treatment import CACMLinguisticTreatment
from settings import CACM, CACM_PATH, CS276, DOC_IDS_PATH, INDEX_PATH, \
     PREFIX, INITIAL_MARKER, TERM_IDS_PATH, TITLE_MARKER


class Index(object):

    def __init__(self, collection_name, build_dictionaries=False):
        self.collection_name = collection_name
        self.doc_ids = {}     # { doc_id : doc }
        self.term_ids = {}    # { term_id : term }
        self.index = {}       # { term_id : [doc_id_0, ..., doc_id_10] }
        # We can either build the dictionaries or get the last one saved
        if build_dictionaries:
            self.doc_ids = self.build_doc_ids()
            self.term_ids = self.build_term_ids()
            self.index = self.build_index()
        else:
            self.doc_ids = self.get_doc_ids()
            self.term_ids = self.get_term_ids()
            self.index = self.get_index()

    def build_doc_ids(self):
        """
        Builds a dictionary of (doc_id, doc)
        """
        pass

    def build_term_ids(self):
        """
        Builds a dictionary of (term_id, term)
        """
        pass

    def build_index(self):
        """
        Builds the reversed index dictionary with the following : (key, value) = (term_id, [doc_id_0, ..., doc_id_n])  
        """
        pass

    def get_path(self, file_name):
        return 'indexes/%s/%s.txt' % (self.collection_name, file_name)

    def save_doc_ids(self):
        path = self.get_path(DOC_IDS_PATH)
        with open(path, 'w') as file:
            file.write("# %s doc ids\n" % self.collection_name)
            for doc_id in self.doc_ids.keys():
                file.write("%s : %s\n" % (doc_id, self.doc_ids[doc_id]))

    def save_term_ids(self):
        path = self.get_path(TERM_IDS_PATH)
        with open(path, 'w') as file:
            file.write("# %s term ids\n" % self.collection_name)
            for term_id in self.term_ids.keys():
                file.write("%s : %s\n" % (term_id, self.term_ids[term_id]))

    def save_index(self):
        path = self.get_path(INDEX_PATH)
        with open(path, 'w') as file:
            file.write("# %s index\n" % self.collection_name)
            for key in self.index.keys():
                file.write("%s : %s\n" % (key, ", ".join(map(str, self.index[key]))))

    def save_all(self):
        if len(self.doc_ids) > 0:
            self.save_doc_ids()
            print("Document IDs saved")
        if len(self.term_ids) > 0:
            self.save_term_ids()
            print("Term IDs saved")
        if self.index is not None and len(self.index) > 0:
            self.save_index()
            print("Index saved")

    def get_doc_ids(self):
        doc_ids = {}
        path = self.get_path(DOC_IDS_PATH)
        with open(path, 'r') as file:
            line = file.readline()
            while line:
                if not line.startswith("#"):
                    doc_id = int(line[0:line.index(':')])
                    doc = line[line.index(':') + 1:]
                    doc_ids[doc_id] = doc
                line = file.readline()
        return doc_ids

    def get_term_ids(self):
        term_ids = {}
        path = self.get_path(TERM_IDS_PATH)
        with open(path, 'r') as file:
            line = file.readline()
            while line:
                if not line.startswith("#"):
                    term_id = int(line[0:line.index(':')])
                    # + 1 because there is a space after ":"
                    term = str(line[line.index(':') + 1:])
                    term_ids[term_id] = term
                line = file.readline()
        return term_ids

    def get_index(self):
        index = {}
        path = self.get_path(INDEX_PATH)
        with open(path, 'r') as file:
            line = file.readline()
            while line:
                if not line.startswith("#"):
                    term_id = int(line[0:line.index(':')])
                    # + 1 because there is a space after ":"
                    docs_list = line[line.index(':') + 1:]
                    docs_list = map(int, docs_list.split(', '))
                    index[term_id] = docs_list
                line = file.readline()
        return index


class CACMIndex(Index):

    def __init__(self, build_dictionaries=False):
        self.linguistic_treatment = CACMLinguisticTreatment()
        super(CACMIndex, self).__init__(collection_name=CACM, build_dictionaries=build_dictionaries)

    def starts_with_id(self, line):
        return line.startswith(PREFIX + INITIAL_MARKER)

    def starts_with_title(self, line):
        return line.startswith(PREFIX + TITLE_MARKER)

    def starts_with_any_marker(self, line):
        return line.startswith(PREFIX)

    def build_doc_ids(self):
        """
        Builds a dictionary of (doc_id, doc)
        """
        doc_count = 0
        doc_ids = {}
        with open(CACM_PATH, 'r') as content_file:
            line = content_file.readline()
            while line:
                if self.starts_with_id(line):
                    # Go to next line to get the title
                    line = content_file.readline()
                    if not self.starts_with_title(line):
                        raise SyntaxError
                    line = content_file.readline()
                    title = ""
                    while not self.starts_with_any_marker(line):
                        title += line.replace('\n', ' ')
                        line = content_file.readline()
                    doc_ids[doc_count] = title
                    doc_count += 1
                else:
                    line = content_file.readline()
        return doc_ids

    def build_term_ids(self):
        """
        Builds a dictionary of (term_id, term)
        """
        term_ids = {}
        self.linguistic_treatment.vocabulary
        for i in range(self.linguistic_treatment.get_vocabulary_size()):
            term_ids[i] = self.linguistic_treatment.vocabulary[i]
        return term_ids

    def build_index(self):
        """
        Builds the reversed index dictionary with the following : (key, value) = (term_id, [doc_id_0, ..., doc_id_n])
        """
        pass


class CS276Index(Index):

    def __init__(self, build_dictionaries=False):
        self.linguistic_treatment = CACMLinguisticTreatment()
        super(CACMIndex, self).__init__(collection_name=CS276, build_dictionaries=build_dictionaries)

    def build_doc_ids(self):
        """
        Builds a dictionary of (doc, doc_id)
        """
        pass

    def build_term_ids(self):
        """
        Builds a dictionary of (term_id, term)
        """
        pass

    def build_index(self):
        """
        Builds the reversed index dictionary with the following : (key, value) = (term_id, [doc_id_0, ..., doc_id_n])
        """
        pass


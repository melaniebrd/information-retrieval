from linguistic_treatment import CACMLinguisticTreatment
from settings import DOC_IDS_PATH, TERM_IDS_PATH, INDEX_PATH


class Index(object):

    def __init__(self, collection_name, build_dictionaries=False):
        self.collection_name = collection_name
        self.doc_ids = {}     # { doc_id : doc }
        self.term_ids = {}    # { term_id : term }
        self.index = {}       # { term_id : [doc_id_0, ..., doc_id_10] }
        # We can either build the dictionaries or get the last one saved
        if build_dictionaries:
            self.doc_ids = self.build_doc_ids()
            self.term_ids = self.term_ids()
            self.index = self.build_index()
        else:
            self.doc_ids = self.get_doc_ids()
            self.term_ids = self.get_ids()
            self.index = self.get_index()


    def build_doc_ids(self):
        """
        Builds a dictionary of (doc, doc_id)
        """
        pass

    def build_term_ids(self):
        """
        Builds a dictionary of (term, term_id)
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
            file.write("# %s doc ids" % self.collection_name)
            for doc_id in self.doc_ids.keys():
                file.write("%s : %s\n" % (doc_id, self.index[doc_id]))

    def save_term_ids(self):
        path = self.get_path(TERM_IDS_PATH)
        with open(path, 'w') as file:
            file.write("# %s term ids" % self.collection_name)
            for term_id in self.term_ids.keys():
                file.write("%s : %s\n" % (term_id, self.index[term_id]))

    def save_index(self):
        path = self.get_path(INDEX_PATH)
        with open(path, 'w') as file:
            file.write("# %s index" % self.collection_name)
            for key in self.index.keys():
                file.write("%s : %s\n" % (key, ", ".join(map(str, self.index[key]))))

    def get_doc_ids(self):
        path = self.get_path(DOC_IDS_PATH)
        with open(path, 'r') as file:
            line = file.readline()
            while line:
                if not line.startswith("#"):
                    doc_id = int(line[0:line.index(':')])
                    doc = int(line[line.index(':') + 1:])
                    self.doc_ids[doc_id] = doc
                line = file.readline()

    def get_term_ids(self):
        path = self.get_path(TERM_IDS_PATH)
        with open(path, 'r') as file:
            line = file.readline()
            while line:
                if not line.startswith("#"):
                    term_id = int(line[0:line.index(':')])
                    # + 1 because there is a space after ":"
                    term = str(line[line.index(':') + 1:])
                    self.term_ids[term_id] = term
                line = file.readline()

    def get_index(self):
        path = self.get_path(INDEX_PATH)
        with open(path, 'r') as file:
            line = file.readline()
            while line:
                if not line.startswith("#"):
                    term_id = int(line[0:line.index(':')])
                    # + 1 because there is a space after ":"
                    docs_list = line[line.index(':') + 1:]
                    docs_list = map(int, docs_list.split(', '))
                    self.index[term_id] = docs_list
                line = file.readline()


class CACMIndex(Index):

    def __init__(self, build_dictionaries=False):
        super(CACMIndex, self).__init__(collection_name=CACM, build_dictionaries)
        self.count = 0

    def build_doc_ids(self):
        """
        Builds a dictionary of (doc, doc_id)
        """

        pass

    def build_term_ids(self):
        linguistic_treatment = CACMLinguisticTreatment()
        pass

    def build_index(self):
        """
        Builds the reversed index dictionary with the following : (key, value) = (term_id, [doc_id_0, ..., doc_id_n])  
        """
        pass






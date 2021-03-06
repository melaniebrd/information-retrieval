from linguistic_treatment import CACMLinguisticTreatment
from settings import CACM, CACM_PATH, CS276, CS276_PATH, DOC_IDS_PATH, INDEX_PATH, \
     PREFIX, INITIAL_MARKER, TERM_IDS_PATH, TITLE_MARKER

from collections import Counter
from copy import copy
from itertools import zip_longest
import os


class Index(object):

    def __init__(self, collection_name, build_dictionaries=False):
        self.collection_name = collection_name
        self.doc_ids = {}     # { doc_id : doc }
        self.term_ids = {}    # { term_id : term }
        self.index = {}       # { term_id : [[(doc_id_0, freq_0), ..., (doc_id_10, freq_10)]] }
        # We can either build the dictionaries or get the last one saved
        if build_dictionaries:
            self.term_ids = self.build_term_ids()
            # The function build_index fill the index dynamically
            self.build_index()
        else:
            self.doc_ids = self.get_doc_ids()
            self.term_ids = self.get_term_ids()
            self.index = self.get_index()

    def build_term_ids(self):
        """
        Builds a dictionary of (term, term_id)
        """
        term_ids = {}
        self.linguistic_treatment.vocabulary
        for i in range(self.linguistic_treatment.get_vocabulary_size()):
            if self.linguistic_treatment.vocabulary[i] != "":
                term_ids[self.linguistic_treatment.vocabulary[i]] = i
            #self.print_position(i, 1000, 8976)
        return term_ids

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
            for doc_id in self.doc_ids:
                file.write("%s : %s\n" % (doc_id, self.doc_ids[doc_id]))
                #self.print_position(doc_id, 1000, 3203)

    def save_term_ids(self):
        count = 0
        path = self.get_path(TERM_IDS_PATH)
        with open(path, 'w') as file:
            file.write("# %s term ids\n" % self.collection_name)
            for term in self.term_ids:
                file.write("%s : %s\n" % (term, self.term_ids[term]))
                #self.print_position(count, 1000, 8976)
                count += 1

    def save_index(self):
        if self.collection_name == CACM:
            count = 0
            path = self.get_path(INDEX_PATH)
            with open(path, 'w') as file:
                file.write("# %s index\n" % self.collection_name)
                for key in self.index:
                    file.write("%s : %s\n" % (key, " - ".join(map(str, self.index[key]))))
                    #self.print_position(count, 500, 8976)
                    count += 1

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
                    # From 0 to line.rindex(':') - 1 because there is a space
                    # before the first ":"
                    separation_index = line.index(':')
                    doc_id = int(line[0:separation_index - 1])
                    separation_index += 1
                    while line[separation_index] == " ":
                        separation_index += 1
                    doc = str(line[separation_index:])
                    doc = doc.replace("\n", "")
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
                    # From 0 to line.rindex(':') - 1 because there is a space
                    # before the last ":"
                    term = str(line[0:line.rindex(':') - 1])
                    # + 1 because there is a space after ":"
                    term_id = int(line[line.rindex(':') + 1:])
                    term_ids[term] = term_id
                line = file.readline()
        return term_ids

    def get_index(self):
        index = {}
        path = self.get_path(INDEX_PATH)
        with open(path, 'r') as file:
            line = file.readline()
            while line:
                if not line.startswith("#"):
                    term_id = int(line[0:line.rindex(':')])
                    # + 1 because there is a space after ":"
                    docs_list = line[line.rindex(':') + 1:]
                    docs_list = docs_list.split(' - ')
                    for i in range(len(docs_list)):
                        doc_tuple = docs_list[i]
                        doc_tuple = doc_tuple.replace("(", "")
                        doc_tuple = doc_tuple.replace(")", "")
                        doc_tuple = doc_tuple.split(", ")
                        docs_list[i] = (int(doc_tuple[0]), int(doc_tuple[1]))
                    index[term_id] = docs_list
                line = file.readline()
        return index

    def fill_index(self, doc_id, terms, index):
        terms_with_counters = Counter(terms)
        for term in terms_with_counters:
            if term in self.term_ids:
                term_frequency = terms_with_counters[term]
                if self.term_ids[term] not in index:
                    index[self.term_ids[term]] = [(doc_id, term_frequency)]
                else:
                    index[self.term_ids[term]].append((doc_id, term_frequency))
        return index


    def print_position(self, current, modulo, maximum):
        if current % modulo == 0:
            print("%s / %s" % (current, maximum))


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

    def build_index(self):
        """
        Builds the reversed index dictionary with the following : (key, value) = (term_id, [doc_id_0, ..., doc_id_n])
        """
        doc_count = 0
        with open(CACM_PATH, 'r') as content_file:
            line = content_file.readline()
            while line:
                if self.starts_with_id(line):
                    # We have a new document from CACM, for wich we must build the list of terms and save the doc_id
                    terms = []
                    title = ""
                    line = content_file.readline()
                    if not self.starts_with_title(line):
                        raise SyntaxError
                    line = content_file.readline()
                    while not self.starts_with_any_marker(line):
                        title += line.replace('\n', ' ')
                        terms += self.linguistic_treatment.tokenize_by_line(line)
                        line = content_file.readline()
                    while line and not self.starts_with_id(line):
                        if not self.starts_with_any_marker(line):
                            terms += self.linguistic_treatment.tokenize_by_line(line)
                        line = content_file.readline()
                    # We arrived at the end of this document.
                    # We must now save the new doc_id in self.doc_ids and add, for each term of the doc, the doc_id to the index
                    doc_id = doc_count
                    self.doc_ids[doc_id] = title
                    self.index = self.fill_index(doc_id, terms, self.index)
                    doc_count += 1
                    self.print_position(doc_count, 1000, 3203)
                else:
                    line = content_file.readline()


class CS276Index(Index):

    def __init__(self, build_dictionaries=False):
        self.doc_id_count = 0
        self.linguistic_treatment = CACMLinguisticTreatment()
        super(CS276Index, self).__init__(collection_name=CS276, build_dictionaries=build_dictionaries)

    def get_file_path(self, folder_name, filename):
        return CS276_PATH + '/' + folder_name + '/' + filename

    def get_folder_path(self, folder_name):
        return os.getcwd() + '/' + CS276_PATH + '/' + folder_name

    def get_tmp_path(self, file_name):
        return 'indexes/%s/temporary/%s.txt' % (self.collection_name, file_name)

    def build_index(self):
        folder_count = 1
        print("Step 1 : create one index per block")
        for folder_name in os.listdir(os.getcwd() + '/' + CS276_PATH):
            if folder_name != ".DS_Store":
                print("%s %s %s %s" % ("####" * folder_count, "    " * (10 - folder_count), folder_count * 10, '%'))
                folder_count += 1
                tmp_index = self.build_block_index(folder_name)
                self.save_tmp_index(folder_name, tmp_index)
        self.merge_indexes()

    def build_block_index(self, folder_name):
        tmp_index = {}
        for filename in os.listdir(self.get_folder_path(folder_name)):
            doc_id = self.create_new_doc_id(folder_name, filename)
            terms = []
            with open(self.get_file_path(folder_name, filename), 'r') as content_file:
                # Get the terms from the doc
                line = content_file.readline()
                while line:
                    line = line.split()
                    terms += line
                    line = content_file.readline()
            tmp_index = self.fill_index(doc_id, terms, tmp_index)
        return tmp_index

    def create_new_doc_id(self, folder_name, filename):
        doc_id = self.doc_id_count
        self.doc_ids[doc_id] = self.get_file_path(folder_name, filename)
        # Update doc_id_count value
        self.doc_id_count += 1
        return doc_id

    def save_tmp_index(self, folder_name, tmp_index, final_index=False):
        folder_count = 0
        if final_index:
            path = self.get_path(INDEX_PATH)
        else:
            path = self.get_tmp_path(INDEX_PATH + "_" + folder_name)
        with open(path, 'w') as file:
            file.write("# %s tmp index %s\n" % (self.collection_name, folder_count))
            for key in tmp_index:
                file.write("%s : %s\n" % (key, " - ".join(map(str, tmp_index[key]))))
                folder_count += 1

    def merge_indexes(self):
        folder_names = os.listdir(os.getcwd() + '/' + CS276_PATH)
        folder_names.remove(".DS_Store")
        print("\nStep 2 : Merge all the block indexes")
        step_count = 1
        while len(folder_names) > 1:
            final_index = (len(folder_names) == 2)
            new_folder_names = copy(folder_names)
            for name_1, name_2 in self.pairwise(folder_names):
                if (name_2 != "-"):
                    index_1 = self.get_tmp_index(name_1)
                    index_2 = self.get_tmp_index(name_2)
                    merged_index = self.merge_index_dictionaries(index_1, index_2)
                    # Delete the txt indexes : index_1 and index_2
                    os.remove(os.getcwd() + '/' + self.get_tmp_path(INDEX_PATH + "_" + name_1))
                    os.remove(os.getcwd() + '/' + self.get_tmp_path(INDEX_PATH + "_" + name_2))
                    # Save the newly merged_index into temporary/index_12.txt
                    self.save_tmp_index(name_1 + name_2, merged_index, final_index=final_index)
                    # Remove the name_1, name_2 from folder_names and add the new name
                    new_folder_names.remove(name_1)
                    new_folder_names.remove(name_2)
                    new_folder_names.append(name_1 + name_2)
            folder_names = copy(new_folder_names)
            # In order to let the user know where we are in the process
            print("%s %s %s %s" % ("####" * step_count, "    " * (5 - step_count), step_count * 20, '%'))
            step_count += 1

    def pairwise(self, folder_names):
        pair = iter(folder_names)
        return zip_longest(pair, pair, fillvalue='-')

    def get_tmp_index(self, folder_name):
        index = {}
        path = self.get_tmp_path(INDEX_PATH + "_" + folder_name)
        with open(path, 'r') as file:
            line = file.readline()
            while line:
                if not line.startswith("#"):
                    term_id = int(line[0:line.rindex(':')])
                    # + 1 because there is a space after ":"
                    docs_list = line[line.rindex(':') + 1:]
                    docs_list = docs_list.split(' - ')
                    for i in range(len(docs_list)):
                        doc_tuple = docs_list[i]
                        doc_tuple = doc_tuple.replace("(", "")
                        doc_tuple = doc_tuple.replace(")", "")
                        doc_tuple = doc_tuple.split(", ")
                        docs_list[i] = (int(doc_tuple[0]), int(doc_tuple[1]))
                    index[term_id] = docs_list
                line = file.readline()
        return index

    def merge_index_dictionaries(self, index_1, index_2):
        for key in index_2:
            if key not in index_1:
                index_1[key] = index_2[key]
            else:
                index_1[key] = sorted(index_1[key] + (index_2[key]))
        return index_1

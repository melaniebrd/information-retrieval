from settings import CACM, CACM_PATH, CS276, CS276_PATH, MARKERS_TO_CHECK, MARKERS, PREFIX

from math import floor, log
from string import lower, punctuation
import os
import re


class LinguisticTreatment(object):

    def __init__(self, collection_name, build_frequencies=False):
        self.collection_name = collection_name
        self.tokens = self.tokenize()
        self.vocabulary = self.build_vocabulary_list()
        self.vocabulary_with_frequencies = {}
        if build_frequencies:
            self.vocabulary_with_frequencies = self.build_vocabulary_with_frequency()

    def get_tokens_size(self):
        return len(self.tokens)

    def get_vocabulary_size(self):
        return len(self.vocabulary)

    def tokenize(self):
        """
        Builds the list of tokens
        """
        pass

    def build_vocabulary_list(self):
        """
        Returns the size of the vocabulary, without counting the stop-words
        """
        tokens = self.remove_duplication()
        common_words = self.get_common_words()
        voc_list = list(set(tokens) - set(common_words) - set([""]))
        return sorted(voc_list)

    def build_vocabulary_with_frequency(self):
        self.remove_common_words()
        voc_with_frequency = {}
        # Alphabeticaly sorted
        self.tokens = sorted(self.tokens)
        voc_with_frequency[self.tokens[0]] = 1
        for i in range(1, len(self.tokens)):
            if self.tokens[i] == self.tokens[i - 1]:
                voc_with_frequency[self.tokens[i]] += 1
            else:
                voc_with_frequency[self.tokens[i]] = 1
        return voc_with_frequency

    def remove_duplication(self):
        return list(set(self.tokens))

    def get_common_words(self):
        with open('Data/CACM/common_words', 'r') as content_file:
            common_words = content_file.readlines()
            common_words = [word.rstrip('\n') for word in common_words]
        return common_words

    def remove_common_words(self):
        common_words = self.get_common_words()
        self.tokens = [token for token in self.tokens if token not in common_words]

    def get_ranks(self):
        ranks = sorted(self.vocabulary_with_frequencies, key=self.vocabulary_with_frequencies.get, reverse=True)
        return ranks

    def print_ranks(self):
        ranks = self.get_ranks()
        for term in ranks:
            print('%s | freq : %s | rank : %s' % (term, self.vocabulary_with_frequencies[term], ranks.index(term)))

    def get_heap_parameters(self):
        """
        Heap's law is number_of_voc = k * (number_of_tok)^b
        Find the k and b parameters 
        """
        tokens = self.tokens[:len(self.tokens)/2]
        tokens = list(set(tokens))
        common_words = self.get_common_words()
        vocabulary = list(set(tokens) - set(common_words))
        (k, b) = (0, 0)
        try :
            token_size, half_token_size = float(self.get_tokens_size()), float(self.get_tokens_size()/2)
            vocabulary_size, half_vocabulary_size = float(self.get_vocabulary_size()), len(vocabulary)
            b = log(vocabulary_size/half_vocabulary_size)/log(token_size/half_token_size)
            k = (vocabulary_size + half_vocabulary_size)/float(pow(token_size, b) + pow(half_token_size, b))
        except ValueError:
            print("Oups you're trying to get the log of 0")
        except ZeroDivisionError:
            print("Oups you're trying to divide by zero")
        return (k, b)


class CACMLinguisticTreatment(LinguisticTreatment):

    def __init__(self, build_frequencies=False):
        super(CACMLinguisticTreatment, self).__init__(CACM, build_frequencies=build_frequencies)

    def tokenize(self):
        tokens = []
        """
        Give the number of Token in the Collection.
        Spaces and ponctuation (non alphabetic char) divide token.
        """
        with open(CACM_PATH, 'r') as content_file:
            line = content_file.readline()
            while line:
                if self.line_to_analyse(line):
                    # Go to next line because this line is .I, .T, .W or .K
                    line = content_file.readline()
                    while line and self.line_to_read(line):
                        line_words = self.tokenize_by_line(line)
                        tokens += line_words
                        line = content_file.readline()
                else:
                    while line and not self.line_to_analyse(line):
                        line = content_file.readline()
        return tokens

    # Unused right now
    def tokenize_with_nltk(self, line):
        return nltk.word_tokenize(line)

    def tokenize_by_line(self, line):
        # Lower all the letters
        line = lower(line)
        # Get an array of words
        line_words = [word for word in re.split('\W+', line) if not word.isdigit()]
        return line_words

    def line_to_analyse(self, line):
        for marker in MARKERS_TO_CHECK:
            if line.startswith(PREFIX + marker):
                return True
        return False

    def line_to_read(self, line):
        return not line.startswith(PREFIX)


class CS276LinguisticTreatment(LinguisticTreatment):

    def __init__(self, build_frequencies=False):
        super(CS276LinguisticTreatment, self).__init__(CS276, build_frequencies=build_frequencies)

    def tokenize(self):
        tokens = []
        """
        Give the number of Token in the Collection.
        Spaces and ponctuation (non alphabetic char) divide token.
        """
        folder_count = 1
        print("CS276 Tokenize")
        for folder_name in os.listdir(os.getcwd() + '/' + CS276_PATH):
            print("%s %s %s %s" % ("####" * folder_count, "    " * (10 - folder_count), folder_count * 10, '%'))
            folder_count += 1
            for filename in os.listdir(os.getcwd() + '/' + CS276_PATH + '/' + folder_name):
                with open(CS276_PATH + '/' + folder_name + '/' + filename, 'r') as content_file:
                    line = content_file.readline()
                    while line:
                        line = line.split()
                        tokens += line
                        line = content_file.readline()
        return tokens

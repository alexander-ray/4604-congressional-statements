import string
import nltk
import json
import os

from scraper import Scraper

class Feature_Processor:
    # Removing odd punctuation added by BS
    # BS adds \n and #, quite a bit
    # Leaves other punctuation
    @staticmethod
    def remove_punctuation(s):
        return s.replace('\n', ' ').replace('\r', '').replace('"', '').replace('#', '')

    # https: // stackoverflow.com / questions / 43742956 / fast - named - entity - removal - with-nltk
    @staticmethod
    def _tokens_to_string(tokens):
        return "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in tokens]).strip()

    # https: // stackoverflow.com / questions / 43742956 / fast - named - entity - removal - with-nltk
    # Named entity replacement with NLTK
    def remove_named_entities(self, s):
        # Tokenize
        tokens = nltk.word_tokenize(s)
        # Chunk, binary (e.g. Named Entity or Not Named Entity)
        chunked = nltk.ne_chunk(nltk.pos_tag(tokens), binary=True)

        # If type == nltk.Tree, named entity subtree (replace with ENTITY)
        # Otherwise, use word
        tokens = [leaf[0] if type(leaf) != nltk.Tree else "ENTITY" for leaf in chunked]

        ret = self._tokens_to_string(tokens)
        return ret

    def get_features(self, base_url, num, base_file):
        # Check if base_file exists
        # If not, create it
        if not os.path.isfile(base_file + '_train.txt'):
            scrape = Scraper()
            scrape.get_entries_driver(base_url, num, base_file)

        # Open relevant files, return training and test lists
        with open(base_file + '_train.txt', 'r', encoding="ascii") as fin:
            train = json.load(fin)
        with open(base_file + '_test.txt', 'r', encoding="ascii") as fin:
            test = json.load(fin)

        return train, test



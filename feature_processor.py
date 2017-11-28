import string
import nltk
from collections import Counter
import json


from scraper import Scraper

class Feature_Processor:
    def _remove_punctuation(self, s):
        translator = str.maketrans('', '', string.punctuation)
        return s.translate(translator)

    #https: // stackoverflow.com / questions / 43742956 / fast - named - entity - removal - with-nltk
    def _remove_named_entities(self, s):
        tokens = nltk.word_tokenize(s)
        cs = nltk.pos_tag(tokens)
        tokens = [word for word, tag in cs if tag != 'NNP']
        return tokens

    # From 4604 HW 4
    def _n_grams(self, tokens, n):
        output = []
        for i in range(n - 1, len(tokens)):
            ngram = ' '.join(tokens[i - n + 1:i + 1])
            output.append(ngram)
        return output

    def _convert_to_count(self, l):
        return Counter(l)

    def get_features(self, base_url, num):
        scrape = Scraper()
        first = scrape.get_entries_driver(base_url, num)[0]
        #return self._remove_punctuation(first["text"])

        tmp = self._remove_named_entities(self._remove_punctuation(first["text"]))
        tmp.extend(self._n_grams(tmp, 2))
        tmp.extend(self._n_grams(tmp, 3))

        with open("test.txt", 'w') as fout:
            json.dump(Counter(tmp), fout)

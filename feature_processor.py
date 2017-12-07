import string
import nltk
import json
import os

from scraper import Scraper

class Feature_Processor:
    def remove_punctuation(self, s):
        translator = str.maketrans('', '', string.punctuation)
        return s.translate(translator)

    #https: // stackoverflow.com / questions / 43742956 / fast - named - entity - removal - with-nltk
    def remove_named_entities(self, s):
        tokens = nltk.word_tokenize(s)
        cs = nltk.pos_tag(tokens)
        tokens = [word for word, tag in cs if tag != 'NNP']
        return tokens

    # From 4604 HW 4
    def n_grams(self, tokens, n):
        output = []
        for i in range(n - 1, len(tokens)):
            ngram = ' '.join(tokens[i - n + 1:i + 1])
            output.append(ngram)
        return output

    def get_features(self, base_url, num, base_file):
        if not os.path.isfile(base_file + '_train.txt'):
            scrape = Scraper()
            train = []
            test = []
            tmp = scrape.get_entries_driver(base_url, num)
            print(tmp)
            for i, e in enumerate(tmp):
                if i % 10 == 0:
                    test.append([e['party'], e['text']])
                else:
                    train.append([e['party'], e['text']])
            with open(base_file + '_train.txt', 'w') as fout:
                json.dump(train, fout)
            with open(base_file + '_test.txt', 'w') as fout:
                json.dump(test, fout)

        train = []
        test = []
        with open(base_file + '_train.txt', 'r') as fin:
            train = json.load(fin)
        with open(base_file + '_test.txt', 'r') as fin:
            test = json.load(fin)

        return train, test
        #return self._remove_punctuation(first["text"])

        #tmp = self._remove_named_entities(self._remove_punctuation(first["text"]))
        #tmp.extend(self._n_grams(tmp, 2))
        #tmp.extend(self._n_grams(tmp, 3))

        #v = CountVectorizer(stop_words='english', analyzer='word')



from feature_processor import Feature_Processor
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import SGDClassifier
import numpy as np
from nltk.corpus import stopwords

def main():
    fp = Feature_Processor()
    train, test = fp.get_features('https://projects.propublica.org/represent/statements?page=', 20, 'test')

    stops = set(stopwords.words("english"))

    for e in train:
        tmp = fp.remove_named_entities(fp.remove_punctuation(e[1]))
        tmp.extend(fp.n_grams(tmp, 2))
        tmp.extend(fp.n_grams(tmp, 3))
        tmp = [word for word in tmp if word not in stops]
        e[1] = Counter(tmp)
    for e in test:
        tmp = fp.remove_named_entities(fp.remove_punctuation(e[1]))
        tmp.extend(fp.n_grams(tmp, 2))
        tmp.extend(fp.n_grams(tmp, 3))
        tmp = [word for word in tmp if word not in stops]
        e[1] = Counter(tmp)

    vect = DictVectorizer()
    X_train = vect.fit_transform(e[1] for e in train)
    Y_train = [e[0][0] for e in train]

    feature_names = np.asarray(vect.get_feature_names())

    X_test = vect.fit(e[1] for e in test)

    classifier = SGDClassifier(loss='log', max_iter=1000, tol=1.0e-12, random_state=123)
    classifier.fit(X_train, Y_train)

    args = np.argsort(classifier.coef_[0])
    for a in args[0:20]:
        print(" %s: %0.4f" % (feature_names[a], classifier.coef_[0][a]))

    args = np.argsort(classifier.coef_[0])
    for a in args[:-20]:
        print(" %s: %0.4f" % (feature_names[a], classifier.coef_[0][a]))

if __name__ == '__main__':
    main()
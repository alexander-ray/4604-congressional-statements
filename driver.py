from feature_processor import Feature_Processor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.linear_model import SGDClassifier
import numpy as np
from plotting import Plotting


# Code to get vector of topic scores for each party
def get_topic_vectors(train, topics):
    r_topics = []
    d_topics = []
    for d, t in zip(train, topics):
        if d['party'] == 'D':
            d_topics.append(t)
        else:
            r_topics.append(t)

    r = np.average(r_topics, axis=0)
    d = np.average(d_topics, axis=0)
    return r, d

#http://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html#sphx-glr-auto-examples-applications-plot-topics-extraction-with-nmf-lda-py
# Scikit learn LDA example
def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()


# Print features, code from class HW
def print_features(features, feature_names):
    args = np.argsort(features)
    for a in args[0:100]:
        print(" %s: %0.4f" % (feature_names[a], features[a]))

    args = np.argsort(features)
    for a in args[-100:]:
        print(" %s: %0.4f" % (feature_names[a], features[a]))


# Logistic regression driver function
def log_reg(train, test):
    # Setup
    vect = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), lowercase=False)
    X_train = vect.fit_transform(e['text'] for e in train)
    Y_train = [e['party'] for e in train]

    X_test = vect.transform(e['text'] for e in test)
    Y_test = [e['party'] for e in test]

    base_classifier = SGDClassifier(loss='log', random_state=123, tol=1e-12, max_iter=1000, alpha=0.0001)
    feature_names = np.asarray(vect.get_feature_names())

    # GRID SEARCH CODE
    #params = [{'alpha': [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0]}]

    #gs_classifier = GridSearchCV(base_classifier, params, return_train_score=True, scoring='accuracy')
    #gs_classifier.fit(X_train, Y_train)

    #print("Best parameter settings:", gs_classifier.best_params_)
    #print("Validation accuracy: %0.6f" % gs_classifier.best_score_)

    # Plot results
    #Plotting.plot_double(params[0]['alpha'], gs_classifier.cv_results_['mean_train_score'], gs_classifier.cv_results_['mean_test_score'],
    #                     "Alpha", "Accuracy", "Alpha vs Accuracy Logistic Regression", "Avg Train Acc", "Avg Test Acc")

    # BASE CLASSIFIER CODE
    base_classifier.fit(X_train, Y_train)
    print("Log Reg Testing accuracy: %0.6f" % accuracy_score(Y_test, base_classifier.predict(X_test)))
    print_features(base_classifier.coef_[0], feature_names)


# Linear SVM driver function
def linear_svm(train, test):
    # Setup
    vect = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), lowercase=False)
    X_train = vect.fit_transform(e['text'] for e in train)
    Y_train = [e['party'] for e in train]

    X_test = vect.transform(e['text'] for e in test)
    Y_test = [e['party'] for e in test]

    base_classifier = SGDClassifier(random_state=123, tol=1e-12, max_iter=1000, alpha=0.0001)
    feature_names = np.asarray(vect.get_feature_names())

    # GRID SEARCH CODE
    #params = [{'alpha': [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0]}]

    #gs_classifier = GridSearchCV(base_classifier, params, return_train_score=True, scoring='accuracy')
    #gs_classifier.fit(X_train, Y_train)

    #print("Best parameter settings:", gs_classifier.best_params_)
    #print("Validation accuracy: %0.6f" % gs_classifier.best_score_)

    #Plotting.plot_double(params[0]['alpha'], gs_classifier.cv_results_['mean_train_score'],
    #                     gs_classifier.cv_results_['mean_test_score'], "Alpha", "Accuracy",
    #                     "Alpha vs Accuracy Linear SVM", "Avg Train Acc", "Avg Test Acc")

    # BASE CLASSIFIER CODE
    base_classifier.fit(X_train, Y_train)
    print("SVM Testing accuracy: %0.6f" % accuracy_score(Y_test, base_classifier.predict(X_test)))
    print_features(base_classifier.coef_[0], feature_names)


# LDA driver function
# Useful: https://stackoverflow.com/questions/45145368/python-scikit-learn-get-documents-per-topic-in-lda
def lda(train, n_components):
    # Can't use Tfidf vectorizer with tf-idf
    vect = CountVectorizer(lowercase=False, analyzer='word', stop_words='english', max_df=0.3)
    tf = vect.fit_transform(e['text'] for e in train)

    lda = LatentDirichletAllocation(n_components=n_components, max_iter=5,
                              learning_method='online',
                              learning_offset=50.,
                              random_state=123)

    lda.fit(tf)
    tf_feature_names = vect.get_feature_names()
    print_top_words(lda, tf_feature_names, 20)

    topics = lda.transform(tf)
    r, d = get_topic_vectors(train, topics)
    labels = ("Education", "VA", "Security", "Agenda", "Military", "Internet", "Econ")
    legend = ("R", "D")
    Plotting.bar_chart(r, d, labels, 'Topic Scores', 'Republican and Democrat Topic Score Averages', legend)


def main():
    fp = Feature_Processor()
    # 'er' for entity-removed dataset
    # 'new' for normal dataset
    train, test = fp.get_features('https://projects.propublica.org/represent/statements?page=', 1200, 'er')

    # SPACE FOR DRIVER FUNCTION CALLS
    lda(train, 7)


if __name__ == '__main__':
    main()
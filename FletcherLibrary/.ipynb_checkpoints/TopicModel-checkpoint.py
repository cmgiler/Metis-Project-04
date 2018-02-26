__author__ = 'cmgiler'

from scipy.sparse import coo_matrix
from sklearn.feature_extraction.text import CountVectorizer
from IPython.display import clear_output
from . import TextAnalysis as TA

def GetCountVect(content_list):
    print("Regenerating Content List")
    content_list = [' '.join(TA.TokenizeData(content)) for content in content_list]
    count_vectorizer = CountVectorizer(stop_words='english', 
                                       token_pattern="\\b[a-z][a-z]+\\b")
    clear_output(wait=True)
    print("Fitting Vectorizer...")
    count_vectorizer.fit(content_list)
    clear_output(wait=True)
    print("Generating Counts...")
    counts = count_vectorizer.transform(content_list).transpose()
    clear_output(wait=True)
    num_words, num_entries = counts.shape
    print("Number of Entries: %d" % num_entries)
    print("Number of Words: %d" % num_words)
    return counts, count_vectorizer

def GetTfIdfCountVect(content_list):
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer(stop_words="english",
                                 token_pattern="\\b[a-z][a-z]+\\b")
    clear_output(wait=True)
    print("Fitting Vectorizer...")
    vectorizer.fit(content_list)
    clear_output(wait=True)
    print("Generating Vectors...")
    doc_vectors = vectorizer.transform(content_list).transpose()
    num_words, num_entries = doc_vectors.shape
    print("Number of Entries: %d" % num_entries)
    print("Number of Words: %d" % num_words)
    return doc_vectors, vectorizer

def LDA(counts, count_vectorizer, num_topics):
    from gensim import corpora, models, similarities, matutils
    id2word = dict((v, k) for k, v in count_vectorizer.vocabulary_.items())
    corpus = matutils.Sparse2Corpus(counts)
    lda = models.LdaModel(corpus=corpus, num_topics=num_topics, id2word=id2word, passes=10)
    return lda

def NMF(counts, count_vectorizer, num_topics):
    from sklearn.decomposition import NMF
    import numpy as np
    id2word = dict((v, k) for k, v \
                   in count_vectorizer.vocabulary_.items())
    nmf = NMF(n_components=num_topics)
    model = nmf.fit(counts.toarray().T)
    return model

def GetTopWords(model, n, count_vectorizer=None):
    if model.__str__().startswith('LdaModel'):
        # LDA Model Type
        id2word = model.id2word
        top_n_words = []
        for doc in model.get_topics():
            sorted_idx = doc.argsort()[::-1]
            top_n_idx = sorted_idx[:n]
            top_n_words.append([id2word[i] for i in top_n_idx])
        return top_n_words
    if model.__str__().startswith('NMF'):
        if not count_vectorizer:
            print("Error: Count Vectorizer must be included for NMF")
            return None
        id2word = dict((v, k) for k, v \
                       in count_vectorizer.vocabulary_.items())
        top_n_words = []
        for topic_idx, topic in enumerate(model.components_):
            top_n_words.append([id2word[i] for i \
                                in topic.argsort()][::-1][:n])

        return top_n_words
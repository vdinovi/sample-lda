import pdb
import os.path
from pprint import pprint
import pickle

from stop_words import get_stop_words
import enchant
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
from gensim.models import KeyedVectors

os.environ["PYRO_SERIALIZERS_ACCEPTED"] = 'pickle'
os.environ["PYRO_SERIALIZER"] = 'pickle'

def clean_data(filename):
    docs = [line.lower().split() for line in open(filename)]
    # Filter out english words
    en_check = enchant.Dict('en_US')
    for i, doc in enumerate(docs):
        docs[i] = [word for word in doc if en_check.check(word)]

    # Filter out stop words
    en_stop = get_stop_words('en')
    for i, doc in enumerate(docs):
        docs[i] = [word for word in doc if word not in en_stop]

    # Simplify words (stemming)
    p_stemmer = PorterStemmer()
    for i, doc in enumerate(docs):
        docs[i] = [p_stemmer.stem(word) for word in doc]

    with open('{}.pickle'.format(filename), 'wb') as f:
        pickle.dump(docs, f)

def process_docs(file):
    print("cleaning data...")
    clean_data(file)

process_docs('master.txt')
with open('master.txt.pickle', 'rb') as f:
    print("loading data...")
    docs = pickle.load(f)

    # assign ids for each word and collect stats
    dictionary = corpora.Dictionary(docs)
    # create corpus
    corpus = [dictionary.doc2bow(doc) for doc in docs]
    tfidf = models.TfidfModel(corpus)
    # perform tfidf
    tfcorpus = [tfidf[x] for x in corpus]
    print("running lda...")
    # apply the lda model
    ldamodel = models.ldamodel.LdaModel(tfcorpus, num_topics=100, id2word=dictionary, passes=100, distributed=True)
    print("LDA RESULTS\n")
    pprint(ldamodel.print_topics(num_topics=25, num_words=5))
    ldamodel.save('lda_model.lda')

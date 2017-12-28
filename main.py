import pdb
import os.path
from pprint import pprint
import pickle

from stop_words import get_stop_words
import enchant
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models

def clean_data():
    docs = [line.lower().split() for line in open('data.txt')]
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

    with open('clean_data.pickle', 'wb') as f:
        pickle.dump(docs, f)

if not os.path.isfile('clean_data.pickle'):
    print("cleaning data...")
    clean_data()

with open('clean_data.pickle', 'rb') as f:
    print("loading data...")
    docs = pickle.load(f)


# assign ids for each word and collect stats
dictionary = corpora.Dictionary(docs)
# create corpus
corpus = [dictionary.doc2bow(doc) for doc in docs]

# apply the lda model
print("running lda...")
ldamodel = models.ldamodel.LdaModel(corpus, num_topics=8, id2word=dictionary, passes=100)
print("LDA RESULTS\n")
pprint(ldamodel.print_topics(num_topics=8, num_words=3))

pdb.set_trace()
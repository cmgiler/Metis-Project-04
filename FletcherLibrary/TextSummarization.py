from . import MongoQuery as MQ
from . import TopicModel as TM
import pickle

def PredictTopic(content_list, name='reuters'):
	with open(name+'_categories.pkl', 'rb') as pkl:
	    category_names = pickle.load(pkl)
	with open(name+'_count_vectorizer_tfidf.pkl', 'rb') as pkl:
	    count_vectorizer = pickle.load(pkl)
	with open(name+'_counts_tfidf.pkl', 'rb') as pkl:
	    counts = pickle.load(pkl)
	with open(name+'_NMF.pkl', 'rb') as pkl:
	    model = pickle.load(pkl)

	topics = []
	confidence = []

	return count_vectorizer, counts

	x = count_vectorizer.transform(content_list)

	W = model.transform(x.toarray().T)[0]

	topics = [category_names[w.argmax()] for w in W]
	confidence = [w.max()/w.sum() for w in W]

	return topics, confidence
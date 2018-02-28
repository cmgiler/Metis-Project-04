from . import MongoQuery as MQ
from . import TopicModel as TM
import datetime as dt
from collections import Counter
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

	x = count_vectorizer.transform(content_list)

	W = model.transform(x.toarray())

	topics = [category_names[w.argmax()] for w in W]
	confidence = [w.max()/w.sum() for w in W]

	return topics, confidence

def FetchDataInDateRange(collection_name, start_date_str, end_date_str):
    collection = MQ.GetMongoCollection('blog_data', collection_name)
    start = dt.datetime.strptime(start_date_str, 
                                 '%B %d, %Y').replace(hour=0, 
                                                      minute=0, 
                                                      second=0)
    end = dt.datetime.strptime(end_date_str, 
                               '%B %d, %Y').replace(hour=23, 
                                                    minute=59, 
                                                    second=59)
    data = []
    for d in collection.find({'datetime': {'$gt': start, '$lt': end}}):
        if 'topic' in d.keys() and d['topic'] != '':            
            data.append(d)
    return data

def GetCategoryCounts(collection_name, start_date_str, end_date_str):
    data = FetchDataInDateRange(collection_name, start_date, end_date)
    return Counter([d['topic'] for d in data])
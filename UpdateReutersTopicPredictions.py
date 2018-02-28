from FletcherLibrary import MongoQuery as MQ
from FletcherLibrary import TopicModel as TM
from FletcherLibrary import TextSummarization as TS

collection = MQ.GetMongoCollection('blog_data', 'reuters_all')

_ids = [_id['_id'] for _id in collection.find({},{'_id':1})]

for i, _id in enumerate(_ids):
    try:
        content = collection.find_one({'_id': _id}, {'_id':0, 'content':1, 'title':1})
        title = content['title']
        content = content['content']
    except:
        continue
    try:
        topic, confidence = TS.PredictTopic([content])
    except:
        print("ERROR ERROR ERROR")
        print(content)
        break
    topic = topic[0]
    confidence = confidence[0]
    collection.update_one({'_id': _id},
                          {'$set': {'topic': topic,
                                    'topic_confidence': confidence}})
    if i%25 == 0:
        print('(%d/%d) %s\nTopic: %s (%0.2f%% Confidence)' % (i+1, len(_ids), title, topic.upper(), confidence*100.))
        print('-----')
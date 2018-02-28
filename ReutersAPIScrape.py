from FletcherLibrary import MongoQuery as MQ
newsapi = MQ.NewsAPIConnect()

import datetime as dt
start_date = dt.datetime(2018,1,1)
end_date = dt.datetime(2018,2,27)
articles = MQ.GetArticlesInRange(newsapi, 'reuters', 
                                 '"https://www.reuters.com"',
                                 start_date, end_date, 'en')

articles = MQ.add_article_content(articles)

collection = MQ.GetMongoCollection('blog_data', 'reuters_all')

collection.drop()
collection.insert_many(articles)
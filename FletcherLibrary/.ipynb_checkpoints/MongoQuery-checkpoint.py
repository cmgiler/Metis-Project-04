__author__ = 'cmgiler'

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import datetime as dt
from IPython.display import clear_output

def GetMongoCollection(db_name, collection_name):
    from pymongo import MongoClient
    client = MongoClient()
    db = client[db_name]
    return db[collection_name]

def GetCollectionNames(db_name):
    from pymongo import MongoClient
    client = MongoClient()
    db = client[db_name]
    return db.collection_names()

def GetFields(collection):
    field_names = set()
    for item in collection.find():
        [field_names.add(x) for x in item.keys()]
    return field_names

def FetchData(collection, return_fields, filter={}):
    projection = {'_id': 0}
    for field in return_fields:
        projection[field] = 1
    data = collection.find(filter, projection)
    data_array = []
    for item in data:
        item_array = []
        for field in return_fields:
            item_array.append(item[field])
        data_array.append(item)
    df = pd.DataFrame(data_array, columns=return_fields)
    if 'date' in return_fields:
        df['date'] = pd.to_datetime(df['date'])
    return df

def NewsAPIConnect():
    from newsapi import NewsApiClient
    API_KEY = 'e4d78b49d7c24afa86eb59b318cb04a8'
    newsapi = NewsApiClient(API_KEY)
    return newsapi

def CreateMongoNewsDatabase(db='blog_data', collection='reuters_all', data=[]):
    collection = GetMongoCollection(db, collection)
    collection.insert_many(data)

def GetArticlesInRange(newsapi, sources, domains, start_date, end_date, language):
    start = start_date
    end = end_date
    delta = end-start
    date_range = []
    for i in range(delta.days+1):
        date_range.append((start+dt.timedelta(days=i)))
    articles = []
    for date in date_range:
        articles += fetch_articles(newsapi, sources, domains, date, language)
    return articles

def fetch_articles(newsapi, sources, domains, date, language):
    date_str = date.strftime('%Y-%m-%d')
    all_articles = newsapi.get_everything(q='',
                                          sources=sources,
                                          domains=domains,
                                          from_parameter=date_str,
                                          to=date_str,
                                          language='en',
                                          sort_by='date',
                                          page=1,
                                          page_size=1)
    articles = []
    print(date)
    for i in range(1, int(np.ceil(all_articles['totalResults']/100.)+1)):
        new_articles = newsapi.get_everything(q='',
                                              sources=sources,
                                              domains=domains,
                                              from_parameter=date_str,
                                              to=date_str,
                                              language='en',
                                              sort_by='date',
                                              page=i,
                                              page_size=100)
        new_articles = new_articles['articles']
        for article in new_articles:
            articles.append({
                'url': article['url'],
                'author': article['author'],
                'title': article['title'],
                'date': article['publishedAt']
            })
    return articles

def get_article_text(url):
    soup = BeautifulSoup(requests.get(url).text)
    return ''.join([x.text for x in soup.find(name='div', attrs={'class': 'StandardArticleBody_body_1gnLA'}).find_all(name='p')][:-1])

def add_article_content(articles):
    for i, article in enumerate(articles):
        clear_output(wait=True)
        print("(%d/%d) %s" % (i+1, len(articles), article['title']))
        try:
            articles[i]['content'] = get_article_text(article['url'])
        except:
            continue
    return articles

def add_articles_to_mongo():
    pass
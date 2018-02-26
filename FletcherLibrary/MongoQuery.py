__author__ = 'cmgiler'

import pandas as pd

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
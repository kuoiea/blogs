import pymongo

CONNECTION_STRING = "mongodb://localhost:27017/"  # replace it with your settings
CONNECTION = pymongo.MongoClient(CONNECTION_STRING)
DATABASE = CONNECTION.myblogs


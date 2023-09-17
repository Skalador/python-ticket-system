import pymongo
from config import CONNECTION_STRING
from logger import logger
from tickets import tickets_cache

client = pymongo.MongoClient(CONNECTION_STRING)
db = client['pythondb']
collection = db['tickets']


def populate_db():
    db_names = client.list_database_names()
    python_db_exists = False
    for db in db_names:
        logger.debug("Following db exists: " + db)
        if db == 'pythondb':
            python_db_exists = True

    if python_db_exists:
        logger.debug("pythondb exists, no population needed!")
    else:
        result = collection.insert_many(tickets_cache)
        logger.debug(result)

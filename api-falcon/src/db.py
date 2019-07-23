import os
from mongoengine import connect

# MONGO CONFIG
mongo_db = os.environ.get("MONGO_DB", "rcn")
mongo_host = os.environ.get("MONGO_HOST", "mongo")

connection = connect(db=mongo_db, host=mongo_host)

import os
from mongoengine import connect
import os

connection = connect(db=os.environ.get("MONGO_DB"), host=os.environ.get("MONGO_HOST"))

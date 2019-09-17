from mongoengine import connect
import os


connection = connect(db='rcn', host=os.environ['MONGO_HOST'])

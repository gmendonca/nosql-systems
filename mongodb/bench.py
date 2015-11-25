from pymongo import MongoClient
import string
import random

def string_generator(size=10, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

client = MongoClient("localhost", 27017)

db = client.database

db.key_pair.create_index("key")
db.key_pair.create_index("value")

operations = 10

for i in range(operations):

    db.key_pair.insert_one({"key": i, "value": string_generator(90)})

for i in range(operations):
    item = db.key_pair.find_one({"key": i})
    print item

for item in db.key_pair.find():
    db.key_pair.remove({"key": item["key"]})

from pymongo import MongoClient
import string
import random
import time
import timeit

def string_generator(size=10, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

client = MongoClient("localhost", 27017)

db = client.database

db.key_pair.create_index("key")
db.key_pair.create_index("value")

operations = 1000


print "Starting timer..."
startTotal = timeit.default_timer()
start_time = timeit.default_timer()
for i in range(operations):
    db.key_pair.insert_one({"key": string_generator(10), "value": string_generator(90)})
start = time.time()
print "Insert Time: ",time.time() - start
print "Insert Time: ",timeit.default_timer() - start_time
for i in range(operations):
    db.key_pair.find_one({"key": string_generator(10)})
start = time.time()
print "Lookup Time: ",time.time() - start
for item in db.key_pair.find():
    db.key_pair.remove({"key": item["key"]})
print "Delete Time: ",time.time() - start
print "Overall Time: ",time.time() - startTotal

from pymongo import MongoClient
import string
import random
import time
import timeit
import sys

def string_generator(size=10, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

client = MongoClient("172.31.32.209", 27017)

db = client.database

#db.key_pair.create_index("key")
db.key_pair.create_index("value")

operations = 1000
if len(sys.argv) > 0:
    operations =  int(sys.argv[1])
print "Number of operations:", operations


print "Starting timer..."
startTotal = start = time.time()
for i in range(operations):
    db.key_pair.insert_one({"_id": string_generator(10), "value": string_generator(90)})
print "Insert Time:",time.time() - start,"seconds"
start = time.time()
for i in range(operations):
    db.key_pair.find_one({"_id": string_generator(10)})
print "Lookup Time:",time.time() - start,"seconds"
start = time.time()
for item in db.key_pair.find():
    db.key_pair.remove({"_id": item["_id"]})
print "Delete Time:",time.time() - start,"seconds"
print "Overall Time:",time.time() - startTotal,"seconds"

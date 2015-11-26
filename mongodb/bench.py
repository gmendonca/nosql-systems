import pymongo
import string
import random
import time
import timeit
import sys

def string_generator(size=10, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

host = "localhost"
port = 27017

operations = 1000

if (len(sys.argv) >= 2 and len(sys.argv) <= 4):
    operations =  int(sys.argv[1])
    if(len(sys.argv) >= 3):
        host = sys.argv[2]
    if(len(sys.argv) == 4):
        port = int(sys.argv[3])
else:
    print "Usage: python",sys.argv[0],"[number_operations] [host] [port]"
    exit()

print "Number of operations:",operations
print "Host:","\""+host + ":" + str(port)+"\""

client = pymongo.MongoClient(host, port)

db = client.database

db.key_pair.create_index([("_id", pymongo.HASHED)])
db.key_pair.create_index("value")


print "Starting timer..."
startTotal = start = time.time()
for i in range(operations):
    db.key_pair.insert_one({"_id": host+str(port)+str(i), "value": string_generator(90)})
print "Insert Time:",time.time() - start,"seconds"
start = time.time()
for i in range(operations):
    db.key_pair.find_one({"_id": host+str(port)+str(i)})
    #print db.key_pair.find_one({"_id": host+str(port)+str(i)})
print "Lookup Time:",time.time() - start,"seconds"
start = time.time()
for item in db.key_pair.find():
    #print item
    db.key_pair.remove({"_id": item["_id"]})
print "Delete Time:",time.time() - start,"seconds"
print "Overall Time:",time.time() - startTotal,"seconds"

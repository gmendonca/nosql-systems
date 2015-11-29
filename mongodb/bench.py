import pymongo
import string
import random
import time
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

print "Starting timer..."
startTotal = start = time.time()

key_pair_values= {}
for i in range(operations):
    key_pair_values[string_generator(10)] = string_generator(90)

for key in key_pair_values:
    db.key_pair.insert_one({"_id":  key, "value": key_pair_values[key]})
print "Insert Time:",time.time() - start,"seconds"

start = time.time()
for key in key_pair_values:
    db.key_pair.find_one({"_id": key})
    #print db.key_pair.find_one({"_id": host+str(port)+str(i)})
print "Lookup Time:",time.time() - start,"seconds"

start = time.time()
for key in key_pair_values:
    db.key_pair.remove({"_id": key})
print "Delete Time:",time.time() - start,"seconds"

print "Overall Time:",time.time() - startTotal,"seconds"

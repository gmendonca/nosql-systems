from rediscluster import StrictRedisCluster
import string
import random
import time
import sys

def string_generator(size=10, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

if (len(sys.argv) == 1):
    operations =  1000
elif (len(sys.argv) == 2):
    operations =  int(sys.argv[1])
else:
    print "Usage: python",sys.argv[0],"[number_operations]"
    exit()

print "Number of operations:",operations

with open('cluster') as f:
    lines = f.readlines()

startup_nodes = []
for ip in lines:
    startup_nodes.append({"host": ip[:-1], "port": "6379"})

rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)

print "Starting timer..."
startTotal = start = time.time()

key_pair_values= {}
for i in range(operations):
    key_pair_values[string_generator(10)] = string_generator(90)

for key in key_pair_values:
    rc.set(key, key_pair_values[key])
print "Insert Time:",time.time() - start,"seconds"

start = time.time()
for key in key_pair_values:
    rc.get(key)
print "Lookup Time:",time.time() - start,"seconds"

start = time.time()
for key in key_pair_values:
    rc.delete(key)
print "Delete Time:",time.time() - start,"seconds"

print "Overall Time:",time.time() - startTotal,"seconds"

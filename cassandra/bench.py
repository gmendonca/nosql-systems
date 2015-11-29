from cassandra.cluster import Cluster
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

cluster = Cluster(lines)

session = cluster.connect()

session.execute("""
CREATE KEYSPACE IF NOT EXISTS data
WITH replication = {'class':'SimpleStrategy', 'replication_factor':1}
""")

session.set_keyspace("data")

session.execute("""
CREATE TABLE IF NOT EXISTS key_pair (
   key text PRIMARY KEY,
   value text)
""")

print "Starting timer..."
startTotal = start = time.time()

key_pair_values= {}
for i in range(operations):
    key_pair_values[string_generator(10)] = string_generator(90)

for key in key_pair_values:
    session.execute("INSERT INTO key_pair (key, value) VALUES (\'"
    + key + "\', \'"
    + key_pair_values[key] + "\')")
print "Insert Time:",time.time() - start,"seconds"

start = time.time()
for key in key_pair_values:
    result = session.execute("SELECT key, value FROM key_pair WHERE key = \'" + key+ "\'")
    #print result
print "Lookup Time:",time.time() - start,"seconds"

start = time.time()
for key in key_pair_values:
    session.execute("DELETE FROM key_pair WHERE key = \'"+ key + "\'")
    #print i.key,i.value
print "Delete Time:",time.time() - start,"seconds"

print "Overall Time:",time.time() - startTotal,"seconds"

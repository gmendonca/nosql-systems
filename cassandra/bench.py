from cassandra.cluster import Cluster
import string
import random

def string_generator(size=10, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

operations = 100

cluster = Cluster()
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


for i in range(operations):
    session.execute("INSERT INTO key_pair (key, value) VALUES (\'"
    + string_generator(10) + "\', \'"
    + string_generator(90) + "\')")

for i in range(operations):



result = session.execute("select * from key_pair ")
for i in result:
    session.execute("DELETE FROM key_pair WHERE key = \'"+ i.key + "\'")
    print result.key, result.value

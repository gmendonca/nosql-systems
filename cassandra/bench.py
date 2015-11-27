from cassandra.cluster import Cluster
import string
import random

def string_generator(size=10, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


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

session.execute("insert into key_pair (key, value) values (\'"
+ string_generator(10) + "\', \'"
+ string_generator(90) + "\')")

result = session.execute("select * from key_pair ")[0]
print result.key, result.value

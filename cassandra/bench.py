from cassandra.cluster import Cluster


def string_generator(size=10, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


cluster = Cluster()
session = cluster.connect()

session.execute("""
CREATE KEYSPACE data
WITH replication = {'class':'SimpleStrategy'}
""")

session.set_keyspace("data")

session.execute("""
CREATE TABLE key_pair (
   key text PRIMARY KEY,
   value text)
""")


session.execute("insert into key_pair (key, value) values ("
+ string_generator(10) + ", " + string_generator(90) + ")")

result = session.execute("select * from key_pair ")[0]
print result.firstname, result.age

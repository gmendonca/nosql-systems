import pymongo
import sys


host = "localhost"
port = 27017

if (len(sys.argv) >= 2 and len(sys.argv) <= 3):
    host = sys.argv[1]
    if(len(sys.argv) >= 3):
        port = int(sys.argv[2])
else:
    print "Usage: python",sys.argv[0],"[host] [port]"
    exit()

client = pymongo.MongoClient(host, port)

db = client.database

db.key_pair.create_index([("_id", pymongo.HASHED)])
db.key_pair.create_index("value")

with open('cluster') as f:
    lines = f.readlines()

for ip in lines:
    address = ip[:-1] + ":27017"
    db.command("addShard", address)

db.command("enableSharding", "database")
db.command("shardCollection", "database.key-pair", key={ "_id": "hashed" })

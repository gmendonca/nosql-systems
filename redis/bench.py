from rediscluster import StrictRedisCluster
import string
import random
import time
import sys

def string_generator(size=10, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

startup_nodes = [{"host": "127.0.0.1", "port": "7000"}]


rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)

rc.set("foo", "bar")
rc.get("foo")
rc.delete("foo")

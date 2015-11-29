#Redis

[Reference](http://redis.io/topics/cluster-tutorial)

[Reference](https://github.com/Grokzen/redis-py-cluster)

## Installation

```bash
$ sudo apt-get install gcc g++ make
$ wget http://download.redis.io/releases/redis-3.0.5.tar.gz
$ tar xzf redis-3.0.5.tar.gz
$ cd redis-3.0.5
$ make
```

If it fails: [Reference](http://iamjavakid.blogspot.com/2015/04/install-redis-300-in-ubuntu-14042-server.html)
```bash
$ cd deps
$ make jemalloc
$ make hiredis lua jemalloc linenoise
```

The test it:
```bash
$ make test
```

If it fails:

```bash
$ sudo apt-get install tcl
```

To run the server:

```bash
$ cd redis-3.0.5
$ ./src/redis-server redis.conf
```

## Python Client

```bash
$ sudo apt-get install python-pip python-dev build-essential
$ sudo pip install --upgrade pip
$ sudo pip install --upgrade virtualenv

$ sudo pip install redis-py-cluster
```

## Creating hosts and seeds file

```bash
$ ec2-describe-instances --filter "instance-type=m3.medium" | awk '{print $2}' | grep "52\." > hosts

$ ec2-describe-instances --filter "instance-type=m3.medium" | awk '{print $2}' | grep "172\." > cluster
```

# Cluster

```bash
$ sudo apt-get install ruby
$ sudo gem install redis
```

```bash
pscp -v -t 0 -h hosts -l ubuntu -x "-o StrictHostKeyChecking=no -i guzz-macbook.pem" redis.conf /home/ubuntu/redis-3.0.5/
```

```bash
$ pssh -v -t 0 -h hosts -l ubuntu  -x "-o StrictHostKeyChecking=no -i guzz-macbook.pem" -P './redis-3.0.5/src/redis-server redis-3.0.5/redis.conf &'
```

Restart:
```bash
$ pssh -v -t 0 -h hosts -l ubuntu  -x "-o StrictHostKeyChecking=no -i guzz-macbook.pem" -P 'sudo reboot'
```

``` bash
./src/redis-trib.rb create --replicas 0 172.31.1.220:6379 \
172.31.9.213:6379 172.31.15.7:6379 172.31.11.189:6379 172.31.8.68:6379 \
172.31.10.107:6379 172.31.13.239:6379 172.31.13.238:6379 172.31.12.23:6379 \
172.31.12.1:6379 172.31.5.143:6379 172.31.3.223:6379 172.31.15.13:6379 \
172.31.1.111:6379 172.31.8.111:6379 172.31.11.24:6379
```

## Benchamrking

```bash
pscp -v -t 0 -h hosts -l ubuntu -x "-o StrictHostKeyChecking=no -i guzz-macbook.pem" cluster /home/ubuntu

pscp -v -t 0 -h hosts -l ubuntu -x "-o StrictHostKeyChecking=no -i guzz-macbook.pem" bench.py /home/ubuntu

$ pssh -v -t 0 -h hosts -l ubuntu  -x "-o StrictHostKeyChecking=no -i guzz-macbook.pem" -P 'python bench.py 100000'
```

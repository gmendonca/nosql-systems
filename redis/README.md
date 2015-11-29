# Installation

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

# Python Client

```bash
$ sudo apt-get install python-pip python-dev build-essential
$ sudo pip install --upgrade pip
$ sudo pip install --upgrade virtualenv

$ sudo pip install redis-py-cluster
```

## Creating hosts and seeds file

```bash
$ ec2-describe-instances --filter "instance-type=m3.medium" | awk '{print $2}' | grep "52\." hosts

$ ec2-describe-instances --filter "instance-type=m3.medium" | awk '{print $2}' | grep "172\." > cluster
```

# Cluster

```bash
$ sudo apt-get install ruby
$ sudo gem install redis
```

``` bash
./src/redis-trib.rb create --replicas 0 127.0.0.1:7000 127.0.0.1:7001 \
127.0.0.1:7002 127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005
```

## Benchmarking

```bash
$ pssh -v -t 0 -h hosts -l ubuntu  -x "-o StrictHostKeyChecking=no -i guzz-macbook.pem" -P './redis-3.0.5/src/redis-server redis-3.0.5/redis.conf'
```

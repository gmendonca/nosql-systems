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

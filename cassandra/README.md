## Installing Java

```bash
$ sudo apt-get update
$ sudo apt-get install openjdk-7-jdk

$ sudo update-alternatives --config java
$ vim ~/.bashrc
```

Set the JAVA_HOME like this:

```bash
$ vim ~/.bashrc


#JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64/jre
export PATH=$JAVA_HOME/bin:$PATH
```

## Installing Cassandra

[Reference](http://docs.datastax.com/en/cassandra/2.2/cassandra/install/installDeb.html)
```bash
$ echo "deb http://debian.datastax.com/community stable main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list

$ curl -L https://debian.datastax.com/debian/repo_key | sudo apt-key add -

$ sudo apt-get update


$ sudo apt-get install dsc22=2.2.3-1 cassandra=2.2.3
$ sudo apt-get install cassandra-tools ## Optional utilities
```


To start:
```bash
$ sudo service cassandra start
```

To stop:
```bash
sudo service cassandra stop
sudo rm -rf /var/lib/cassandra/data/system/*
```
## Troubleshooting:
[Reference](https://www.digitalocean.com/community/tutorials/how-to-install-cassandra-and-run-a-single-node-cluster-on-ubuntu-14-04)

If ```sudo service cassandra status``` gives you this error:

```bash
could not access pidfile for Cassandra
```

Then:

```bash
$ sudo nano +60 /etc/init.d/cassandra
```

This line:
```/etc/init.d/cassandra
CMD_PATT="cassandra.+CassandraDaemon"
```

should be like this:
```/etc/init.d/cassandra

CMD_PATT="cassandra"
```

After that, restart you node.

## Installing pip and cassandra-driver:

```bash
$ sudo apt-get install python-pip python-dev build-essential
$ sudo pip install --upgrade pip
$ sudo pip install --upgrade virtualenv

$ sudo pip install cassandra-driver
```

## Limits configuration
[Reference](http://docs.datastax.com/en/cassandra/2.0/cassandra/install/installRecommendSettings.html)

Add line to ```/etc/sysctl.conf```:
```
vm.max_map_count = 131072
```

Configuration for file ```/etc/security/limits.d/cassandra.conf```:

```
cassandra - memlock unlimited
cassandra - nofile 100000
cassandra - nproc 32768
cassandra - as unlimited
```

## Setting up a Cluster

In this part it's necessary [Parallel SSH](https://code.google.com/p/parallel-ssh/)

```bash
$ pssh -v -t 0 -h hosts -l ubuntu  -x "-o StrictHostKeyChecking=no -i guzz-macbook.pem" -P sudo service cassandra stop

$ pssh -v -t 0 -h hosts -l ubuntu -h hosts -l ubuntu  -x "-o StrictHostKeyChecking=no -i guzz-macbook.pem" -P sudo rm -rf /var/lib/cassandra/data/system/*

$ pscp -v -t 0 -h hosts -l ubuntu -x "-o StrictHostKeyChecking=no -i guzz-macbook.pem" cassandra.yaml /home/ubuntu

$ pscp -v -t 0 -h hosts -l ubuntu -x "-o StrictHostKeyChecking=no -i guzz-macbook.pem" cassandra-rackdc.properties /home/ubuntu

$ pssh -v -t 0 -h hosts -l ubuntu -h hosts -l ubuntu  -x "-o StrictHostKeyChecking=no -i guzz-macbook.pem" -P sudo cp cassandra.yaml /etc/cassandra/cassandra.yaml

$ pssh -v -t 0 -h hosts -l ubuntu -h hosts -l ubuntu  -x "-o StrictHostKeyChecking=no -i guzz-macbook.pem" -P sudo cp cassandra-rackdc.properties /etc/cassandra/cassandra-rackdc.properties

$ pssh -v -t 0 -h hosts -l ubuntu  -x "-o StrictHostKeyChecking=no -i guzz-macbook.pem" -P sudo service cassandra start

$ pscp -v -t 0 -h hosts -l ubuntu -x "-o StrictHostKeyChecking=no -i guzz-macbook.pem" bench.py /home/ubuntu

$ pssh -v -t 0 -h hosts -l ubuntu  -x "-o StrictHostKeyChecking=no -i guzz-macbook.pem" -P python bench.py

```

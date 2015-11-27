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
export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64/jre/bin/java
```
or like this:

```bash
$ echo "export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64/jre/bin/java" >> ~/.bashrc
```


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

# Spike

Spike is a simple Distributed Hashtable using Java sockets and Java inbuilt Hashtable for store key-value pairs.

[Reference](https://github.com/gmendonca/distributed-hash-table)

Icon - explosion by Magicon from the Noun Project

## Configure

There is a [JSON file](https://code.google.com/p/json-simple/) in the system. The prebuilt configuration is 8 servers running in localhost,
from ports 13000 to 13007. If you need to run in a different situation, you have to change the values
there. It's a simple array of strings using the format "address:port".

## Build - Ant

For the Ant option, there is three options to run the program: as a client with an user
interface, and for doing benchmarking there is two approaches, one open and closing the socket
per task and the another one leaving the socket open all the time. The second approach is way
faster, but I leave it there for evaluation purposes.

For this project, I used a JSON as the config file, if is not on the `lib/` folder, you have to download the [JSON.simple](https://code.google.com/p/json-simple/) and put the jar file and put it there. For the Maven,
is already on the Maven dependencies, so you don't need to worry about it.

After that, you can run the following commands to build your system:

```sh
$ ant clean
$ ant compile
$ ant jar
```

## How to use

Run the jar files like this:
```sh
java -jar build/Client.jar <PeerId> <Address> <Port>

java -jar build/RemoteClient.jar <Id> <Number of operations>

java -jar build/RemoteServer.jar <Id>
```

The options for both option are explained above:

* Id - It should be a number starting from 0 and going until the limit of
the number of Peers provided in the config file. Keep in mind, that there isn't
any sort of verification here. So in order to use the program, keep it fair.

* Address - Should be localhost or an valid ip address.

* Port - A valid port number for the provided address.

* Number Operations - Number of Put, Get and Del operations to run in each client.

P.S.: The number of server will be the number provided in the config file.
And the operations will Put, Get, and Del from all of them depending on the key value.

## Nodes

### Dependencies

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

```bash
$ sudo apt-get install ant
```

### Installing Spike

```bash
$ sudo apt-get install git
$ git clone https://github.com/gmendonca/spike.git
$ cd spike
$ mkdir lib bin
$ cd lib
$ wget https://json-simple.googlecode.com/files/json-simple-1.1.1.jar

$ ant compile & ant jar
```

## Creating hosts and seeds file

```bash
$ ec2-describe-instances --filter "instance-type=m3.medium" | awk '{print $2}' | grep "52\." > hosts

ec2-describe-instances --filter "instance-type=m3.medium" | awk '{print $2}' | grep "172\." > cluster
```

## Benchmarking

```bash
pscp -v -t 0 -h hosts -h seeds -l ubuntu -x "-o StrictHostKeyChecking=no -i guzz-macbook.pem" config.json /home/ubuntu

$ pssh -v -t 0 -h hosts -l ubuntu  -x "-o StrictHostKeyChecking=no -i guzz-macbook.pem" -P 'java -jar spike/build/RemoteServer.jar $PSSH_NODENUM'

$ pssh -v -t 0 -h hosts -l ubuntu  -x "-o StrictHostKeyChecking=no -i guzz-macbook.pem" -P 'java -jar spike/build/Remote Server.jar $PSSH_NODENUM 100000'
```

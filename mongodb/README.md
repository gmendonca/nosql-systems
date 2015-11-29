# MongoDB

[Reference](http://docs.aws.amazon.com/AWSEC2/latest/CommandLineReference/set-up-ec2-cli-linux.html)

```vim
export EC2_HOME="/opt/ec2-api-tools"
export AWS_ACCESS_KEY="lalala"
export AWS_SECRET_KEY="lululu"
export EC2_URL="https://ec2.us-west-2.amazonaws.com/"
```

```bash
ec2-run-instances ami-5189a661 -t t2.micro -g sg-cc7010a9 -k key-pair-name -b "/dev/xvdf=:200:false:io1:1000" -b "/dev/xvdg=:25:false:io1:250" -b "/dev/xvdh=:10:false:io1:100"
```

```bash
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
$ echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
$ sudo apt-get update
$ sudo apt-get install mongodb-org
```

[Reference](https://docs.mongodb.org/ecosystem/platforms/amazon-ec2/)
```bash
$ sudo mkdir /data /log /journal

$ sudo mkfs.ext4 /dev/xvdf
$ sudo mkfs.ext4 /dev/xvdg
$ sudo mkfs.ext4 /dev/xvdh

$ echo '/dev/xvdf /data ext4 defaults,auto,noatime,noexec 0 0
/dev/xvdg /journal ext4 defaults,auto,noatime,noexec 0 0
/dev/xvdh /log ext4 defaults,auto,noatime,noexec 0 0' | sudo tee -a /etc/fstab

$ sudo mount /data
$ sudo mount /journal
$ sudo mount /log

$ sudo chown mongodb:mongodb /data /journal /log

$ sudo ln -s /journal /data/journal
```

Edit file ```/etc/mongodb.conf```:
```text
# Where and how to store data.
storage:
  dbPath: /data
  journal:
    enabled: true

# where to write logging data.
systemLog:
  destination: file
  logAppend: true
  path: /log/mongod.log
```

Comment this line ```bindIp: 127.0.0.1``` on file ```/etc/mongod.conf``` if it's a cluster:
```text
# network interfaces
net:
  port: 27017
  #bindIp: 127.0.0.1
```

Changes to ulimit for MongoDB:
```bash
$ sudo vim /etc/security/limits.conf
* soft nofile 64000
* hard nofile 64000
* soft nproc 32000
* hard nproc 32000

$ sudo vim /etc/security/limits.d/90-nproc.conf
* soft nproc 32000
* hard nproc 32000
```

Read-ahead changes for MongoDB:
```bash
$ sudo blockdev --setra 32 /dev/xvdf
$ sudo blockdev --setra 32 /dev/xvdg
$ sudo blockdev --setra 32 /dev/xvdh
```
To make it persistent across system boot:
```bash
$ echo 'ACTION=="add", KERNEL=="xvdf", ATTR{bdi/read_ahead_kb}="16"' | sudo tee -a /etc/udev/rules.d/85-ebs.rule
```

To start MongoDB:
```bash
$ sudo service mongod start
```

In Ubuntu by default mongod start at run level, to change this behaviour edit ```sudo vim /etc/init/mongod.conf``` and comment this line:

```text
#start on runlevel [2345]
```

Installing pip and pymongo:
```bash
$ sudo apt-get install python-pip python-dev build-essential
$ sudo pip install --upgrade pip
$ sudo pip install --upgrade virtualenv

$ sudo pip install pymongo
```

## Creating hosts filter
```bash
$ ec2-describe-instances --filter "instance-type=m3.medium" | awk '{print $2}' | grep "52\." > hosts

$ ec2-describe-instances --filter "instance-type=m3.medium" | awk '{print $2}' | grep "172\." > cluster
```

Remember to remove your config server from both lists. And double check the files this is not a guarantee.

# Deploying a shard cluster

```bash
$ sudo mkdir /data/configdb
$ sudo mkdir /data/configdb2
$ sudo mkdir /data/configdb3

$ sudo mongod --configsvr --dbpath /data/configdb --port 27019 &
$ sudo mongod --configsvr --dbpath /data/configdb2 --port 27020 &
$ sudo mongod --configsvr --dbpath /data/configdb3 --port 27021 &
```

Since I am using all the three config-servers in the same node:
```bash
$ sudo mongos --configdb 172.31.3.246:27019,172.31.3.246:27020,172.31.3.246:27021
```

Now, for the client part:
```bash
$ mongo --host 172.31.3.246 --port 27017
```

```mongos
mongos> sh.addShard( "172.31.3.254:27017" )
mongos> sh.addShard( "172.31.3.253:27017" )
mongos> sh.addShard( "172.31.3.252:27017" )
mongos> sh.addShard( "172.31.3.251:27017" )
mongos> sh.addShard( "172.31.3.255:27017" )
mongos> sh.addShard( "172.31.3.245:27017" )
mongos> sh.addShard( "172.31.3.244:27017" )
mongos> sh.addShard( "172.31.4.4:27017" )
mongos> sh.addShard( "172.31.3.250:27017" )
mongos> sh.addShard( "172.31.3.249:27017" )
mongos> sh.addShard( "172.31.3.248:27017" )
mongos> sh.addShard( "172.31.3.247:27017" )
mongos> sh.addShard( "172.31.4.1:27017" )
mongos> sh.addShard( "172.31.4.0:27017" )
mongos> sh.addShard( "172.31.4.3:27017" )
mongos> sh.addShard( "172.31.4.2:27017" )


mongos> sh.enableSharding("database")
mongos> sh.shardCollection("database.key-pair",{ "_id": "hashed" })

```

or

use the python ```sharding.py``` file ( not working properly ):

```bash
$ scp -i guzz-macbook.pem sharding.py ubuntu@52.35.2.111:/home/ubuntu


$ scp -i guzz-macbook.pem cluster ubuntu@52.35.2.111:/home/ubuntu
```

## Benchmarking

In this part it's necessary [Parallel SSH](https://code.google.com/p/parallel-ssh/)

```bash
$ pssh -v -t 0 -h hosts -l ubuntu  -x "-o StrictHostKeyChecking=no -i guzz-macbook.pem" -P 'sudo service mongod start'

$ pscp -v -t 0 -h hosts -l ubuntu -x "-o StrictHostKeyChecking=no -i guzz-macbook.pem" bench.py /home/ubuntu

$ pssh -v -t 0 -h hosts -l ubuntu  -x "-o StrictHostKeyChecking=no -i guzz-macbook.pem" -P 'python bench.py 100000 172.31.3.246 27017'

```

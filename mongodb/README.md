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

Comment this line ```bindIp: 127.0.0.1``` on file ```/etc/mongodb.conf``` if it's a cluster:
```text
# network interfaces
net:
  port: 27017
  #bindIp: 127.0.0.1
```

Changes to ulimit for MongoDB:
```bash
$ sudo nano /etc/security/limits.conf
* soft nofile 64000
* hard nofile 64000
* soft nproc 32000
* hard nproc 32000

$ sudo nano /etc/security/limits.d/90-nproc.conf
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

To make it start automatically at boot:
```bash
$ sudo chkconfig mongod on
```

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
$ sudo mongos --configdb 172.31.11.46:27019,172.31.11.46:27020,172.31.11.46:27021
```

 mongo --host 172.31.32.209 --port 27017

 mongos> sh.addShard( "172.31.2.87:27017" )
 mongos> sh.addShard( "172.31.1.239:27017" )
 mongos> sh.addShard( "172.31.8.17:27017" )
 mongos> sh.addShard( "172.31.5.144:27017" )

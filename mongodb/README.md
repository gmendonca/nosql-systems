

http://docs.aws.amazon.com/AWSEC2/latest/CommandLineReference/set-up-ec2-cli-linux.html
export EC2_HOME="/opt/ec2-api-tools"
export AWS_ACCESS_KEY="lalala"
export AWS_SECRET_KEY="lululu"
export EC2_URL="https://ec2.us-west-2.amazonaws.com/"

```bash
ec2-run-instances ami-5189a661 -t t2.micro -g sg-cc7010a9 -k key-pair-name -b "/dev/xvdf=:200:false:io1:1000" -b "/dev/xvdg=:25:false:io1:250" -b "/dev/xvdh=:10:false:io1:100"
```

```bash
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
$ echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
$ sudo apt-get update
$ apt-get install mongodb-org
```

```bash
sudo pip install pymongo
```

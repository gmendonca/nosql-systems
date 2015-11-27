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

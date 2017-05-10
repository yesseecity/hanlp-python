# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* hanLP為 [hankcs](https://github.com/hankcs/HanLP) 所開發的中文NLP，這邊用python改寫成 api server 

* Version: 0.3.0


### How do I get set up? ###

* 用 git clone --depth 1 複製此專案

* 安裝 python3 及相關 pip套件
```
pip3 install pyyaml
```

* 安裝 java:8
ubuntu:16.10 安裝指令如下

```
apt-get install software-properties-common 
add-apt-repository ppa:webupd8team/java -y 
apt-get update 
apt-get install oracle-java8-installer -y
```

* 安裝 JPype1

```
wget https://pypi.python.org/packages/d2/c2/cda0e4ae97037ace419704b4ebb7584ed73ef420137ff2b79c64e1682c43/JPype1-0.6.2.tar.gz
tar -xvzf JPype1-0.6.2.tar.gz
cd JPype1-0.6.2
python3 setup.py install
```
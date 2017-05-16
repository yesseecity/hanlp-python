# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* hanLP為 [hankcs](https://github.com/hankcs/HanLP) 所開發的中文NLP，這邊用python改寫成 api 


### How do I get set up? ###
* 用 git clone --depth 1 複製此專案
* 快速建置環境

```
docker build -t cosmos:1.0.0 ./
```
- - - -

* 用 git clone --depth 1 複製此專案

* 安裝 python3 及相關 pip套件
```
apt-get update;
apt-get install python3 python3-pip -y;
pip3 install pyyaml

```

* 安裝 java:8
ubuntu:16.10 安裝指令如下

```
apt-get install software-properties-common -y
add-apt-repository ppa:webupd8team/java 
apt-get update 
apt-get install oracle-java8-installer -y
```

* 安裝 JPype

```
wget https://pypi.python.org/packages/d2/c2/cda0e4ae97037ace419704b4ebb7584ed73ef420137ff2b79c64e1682c43/JPype1-0.6.2.tar.gz
tar -xvzf JPype1-0.6.2.tar.gz
cd JPype1-0.6.2
python3 setup.py install
```

* 測試

```
python3 example.py
```

* 修改環境語言(如果測試檔無法順利顯示結果)

```
locale-gen zh_TW.UTF-8
echo 'export LC_ALL=zh_TW.UTF-8' >> ~/.bashrc
echo 'export LANG=zh_TW.UTF-8' >> ~/.bashrc
echo 'export LANGUAGE=zh_TW.UTF-8' >> ~/.bashrc
source ~/.bashrc
```
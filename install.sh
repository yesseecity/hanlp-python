#!/bin/bash
## INSTALLNATION

## ================ 變換語系
sudo locale-gen zh_TW.UTF-8
sudo update-locale LANG=zh_TW.UTF-8

echo 'export LC_ALL=zh_TW.UTF-8' >> ~/.bashrc
echo 'export LANG=zh_TW.UTF-8' >> ~/.bashrc
echo 'export LANGUAGE=zh_TW.UTF-8' >> ~/.bashrc

source ~/.bashrc

## ================ INSTALL python3
sudo apt-get update;
sudo apt-get install python3 python3-pip -y;
sudo pip3 install pyyaml

## ================ INSTALL java:8
sudo apt-get install software-properties-common -y
' ' | sudo add-apt-repository ppa:webupd8team/java

sudo apt-get update
sudo apt-get install oracle-java8-installer -y

## ================ INSTALL JPype
cd ~
wget https://pypi.python.org/packages/d2/c2/cda0e4ae97037ace419704b4ebb7584ed73ef420137ff2b79c64e1682c43/JPype1-0.6.2.tar.gz
tar -xvzf JPype1-0.6.2.tar.gz
cd JPype1-0.6.2

sudo python3 setup.py install
cd ..
rm -r JPype1-0.6.2
rm JPype1-0.6.2.tar.gz


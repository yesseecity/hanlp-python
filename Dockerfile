# cosmos
#
#
# Version: 1.0.0

FROM java:8

MAINTAINER Tid at tid@breaktime.com.tw

# Install python3
RUN apt-get update \
    && apt-get install apt-utils g++ python3 python3-dev python3-pip python3-mock -y \
    && pip3 install pyyaml 

# Install JPype
RUN cd ~/ \
    && apt-get install wget -y \
    && wget https://pypi.python.org/packages/d2/c2/cda0e4ae97037ace419704b4ebb7584ed73ef420137ff2b79c64e1682c43/JPype1-0.6.2.tar.gz \
    && tar -xvzf JPype1-0.6.2.tar.gz \
    && cd JPype1-0.6.2 \
    && python3 setup.py install \
    && cd ~ \
    && rm -r ./*

# Set Environment Language to 'zh_TW.UTF-8'
RUN locale-gen zh_TW.UTF-8 \
    && update-locale LANG=zh_TW.UTF-8 \
    && echo 'export LC_ALL=zh_TW.UTF-8' >> ~/.bashrc \
    && echo 'export LANG=zh_TW.UTF-8' >> ~/.bashrc \
    && echo 'export LANGUAGE=zh_TW.UTF-8' >> ~/.bashrc \
    && source ~/.bashrc

RUN cd / \
    && mkdir cosmos

COPY . /cosmos

WORKDIR /cosmos
# Use ubuntu as parent image
FROM ubuntu:trusty

RUN apt-get update && apt-get install -y build-essential vim python-dev python3-dev python-pip python3-pip capnproto && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /src

# Copy the current directory contents into the container at /src
ADD . /src

RUN pip3 install -r requirements.txt
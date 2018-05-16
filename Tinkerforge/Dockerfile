FROM debian:jessie
MAINTAINER Dominik Ebert <dominik.ebert@zuehlke.com>

ARG app_dir=/var/tinkerforge

RUN apt-get update && apt-get install -y \
  git \
  mosquitto \
  mosquitto-clients \
  python3 \
  python3-pip \
  wget \
  && rm -rf /var/lib/apt/lists/*
  
RUN mkdir -p ${app_dir}

RUN mkdir -p ${app_dir}/mqttProxy
WORKDIR ${app_dir}/mqttProxy
RUN wget https://raw.githubusercontent.com/Tinkerforge/brick-mqtt-proxy/master/brick-mqtt-proxy.py

RUN pip3 install tinkerforge
RUN pip3 install paho-mqtt

CMD ["/bin/bash"]

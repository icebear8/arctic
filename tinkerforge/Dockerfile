FROM alpine:3.7
MAINTAINER Dominik Ebert <dominik.ebert@zuehlke.com>

ARG app_dir=/var/tinkerforge/
ENV app_launcher=${app_dir}/launchScript.sh

RUN apk update && apk add --no-cache \
  git \
  mosquitto \
  mosquitto-clients \
  python3 \
  wget

RUN python3 -m ensurepip

# Install tinkerforge mqtt proxy dependencies
RUN pip3 install tinkerforge
RUN pip3 install paho-mqtt
  
RUN mkdir -p ${app_dir}

# Install tinkerforge MQTT proxy
RUN mkdir -p ${app_dir}/mqttProxy
WORKDIR ${app_dir}/mqttProxy
RUN wget https://raw.githubusercontent.com/Tinkerforge/brick-mqtt-proxy/master/brick-mqtt-proxy.py

# Copy launcher script
COPY resources/tinkerforge/* ${app_dir}/
RUN chmod +x ${app_launcher}

VOLUME /var/tinkerforge/config

CMD ["sh", "/var/tinkerforge/launchScript.sh"]

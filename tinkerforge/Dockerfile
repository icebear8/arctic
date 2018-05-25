FROM alpine:3.7
MAINTAINER Dominik Ebert <dominik.ebert@zuehlke.com>

ENV APP_DIR=/opt/tinkermqtt
ENV CONFIG_DIR=${APP_DIR}/config
ENV APP_LAUNCHER=${APP_DIR}/launchScript.sh

RUN apk update && apk add --no-cache \
  python3 \
  wget

RUN python3 -m ensurepip

# Install tinkerforge mqtt proxy dependencies
RUN pip3 install tinkerforge
RUN pip3 install paho-mqtt
  
RUN mkdir -p ${APP_DIR}

# Install tinkerforge MQTT proxy
RUN mkdir -p ${APP_DIR}/mqttProxy
WORKDIR ${APP_DIR}/mqttProxy
RUN wget https://raw.githubusercontent.com/Tinkerforge/brick-mqtt-proxy/master/brick-mqtt-proxy.py

# Copy launcher script
COPY resources/* ${APP_DIR}
RUN chmod +x ${APP_LAUNCHER}

VOLUME ${CONFIG_DIR}

ENTRYPOINT ["sh", "-c"]

CMD ["sh ${APP_LAUNCHER}"]

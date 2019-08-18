ARG BASE_IMG_VERSION=3.10.1
FROM alpine:${BASE_IMG_VERSION}
MAINTAINER Ponder Bear <ponder.bear@protonmail.com>

# User definition
ARG USER=Ahab
ARG GROUP=Ahab
ARG UID=1000
ARG GID=1000

# Application settings
ARG MQTT_PROXY_VERSION=2_0_6
ENV APP_DIR=/opt/tinkermqtt
ENV SERVICE_ARGS='--help'

RUN apk update && apk add --no-cache \
  python3 \
  && apk del --purge

# Create user
RUN addgroup -g ${GID} ${GROUP} \
  && adduser -u ${UID} -G ${GROUP} -D ${USER}

# Install tinkerforge mqtt proxy dependencies
RUN python3 -m ensurepip
RUN pip3 install paho-mqtt

# Install tinkerforge MQTT proxy
RUN mkdir -p ${APP_DIR}
COPY /resources/tinkerforge_mqtt_${MQTT_PROXY_VERSION} ${APP_DIR}/tinkerforge_mqtt

USER ${USER}
WORKDIR ${APP_DIR}

ENTRYPOINT ["sh", "-c"]
CMD ["python3 tinkerforge_mqtt ${SERVICE_ARGS}"]

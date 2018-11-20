FROM alpine:3.8
MAINTAINER Cheshire Lynx <cheshire.lynx@protonmail.com>

ARG USER=Ahab
ARG GROUP=Ahab
ARG UID=1000
ARG GID=1000

# Bubble upnp server app settings
ARG BUBBLE_RESOURCE_DIR=/resources/bubble
ARG BUBBLE_APPLICATION_REPO=BubbleUPnPServer-distrib.zip
ARG BUBBLE_SERVER_VERSION=v0.9-update30
ENV BUBBLE_APP_DIR=/opt/bubbleupnpserver
ENV BUBBLE_SERVICE_ARGS="-nologfile -logLevel SEVERE -disableAutoUpdate"

RUN apk update && apk add --no-cache \
  ffmpeg \
  openjdk8-jre \
  sox \
  unzip \
  wget
  
# Create user
RUN addgroup -g ${GID} ${GROUP} \
    && adduser -u ${UID} -G ${GROUP} -D ${USER}

# Add bubble application launcher
COPY ${BUBBLE_RESOURCE_DIR}/${BUBBLE_APPLICATION_REPO} /tmp/
RUN mkdir -p ${BUBBLE_APP_DIR} \
    && unzip /tmp/${BUBBLE_APPLICATION_REPO} -d ${BUBBLE_APP_DIR} \
    && rm /tmp/${BUBBLE_APPLICATION_REPO}

COPY ${BUBBLE_RESOURCE_DIR}/BubbleUPnPServer-${BUBBLE_SERVER_VERSION}.jar /${BUBBLE_APP_DIR}/BubbleUPnPServer.jar

RUN chown -R ${USER}:${GROUP} ${BUBBLE_APP_DIR}
RUN chmod -R +x ${BUBBLE_APP_DIR}
USER ${USER}

EXPOSE 58050/tcp
#EXPOSE 58051/tcp 1900/udp

ENTRYPOINT ["sh", "-c"]
CMD ["${BUBBLE_APP_DIR}/launch.sh ${BUBBLE_SERVICE_ARGS}"]

FROM alpine:3.8
MAINTAINER Cheshire Lynx <cheshire.lynx@protonmail.com>

ARG USER=Ahab
ARG GROUP=Ahab
ARG UID=1000
ARG GID=1000

ARG APPLICATION_REPO=BubbleUPnPServer-distrib.zip
ARG SERVER_VERSION=v0.9-update30
ENV APP_DIR=/opt/bubbleupnpserver
ENV SERVICE_ARGS="-nologfile -logLevel SEVERE -disableAutoUpdate"


RUN apk update && apk add --no-cache \
  ffmpeg \
  openjdk8-jre \
  sox \
  unzip \
  wget
  
# Create user
RUN addgroup -g ${GID} ${GROUP} \
    && adduser -u ${UID} -G ${GROUP} -D ${USER}

# Add application launcher
COPY /resources/${APPLICATION_REPO} /tmp/
RUN mkdir -p ${APP_DIR} \
    && unzip /tmp/${APPLICATION_REPO} -d ${APP_DIR} \
    && rm /tmp/${APPLICATION_REPO}

COPY /resources/BubbleUPnPServer-${SERVER_VERSION}.jar /${APP_DIR}/BubbleUPnPServer.jar

RUN chown -R ${USER}:${GROUP} ${APP_DIR}
RUN chmod -R +x ${APP_DIR}
USER ${USER}

EXPOSE 58050/tcp
#EXPOSE 58051/tcp 1900/udp

ENTRYPOINT ["sh", "-c"]
CMD ["${APP_DIR}/launch.sh ${SERVICE_ARGS}"]

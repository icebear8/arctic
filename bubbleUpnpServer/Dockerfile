FROM alpine:3.7
MAINTAINER Dominik Ebert <dominik.ebert@zuehlke.com>

ARG USER=boxer
ARG GROUP=boxer
ARG UID=1000
ARG GID=1000

ARG APPLICATION_REPO=BubbleUPnPServer-distrib-2018-09.zip
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

# Add application
COPY /resources/${APPLICATION_REPO} /tmp/
RUN mkdir -p ${APP_DIR} \
    && unzip /tmp/${APPLICATION_REPO} -d ${APP_DIR} \
    && rm /tmp/${APPLICATION_REPO}

RUN chmod -R +x ${APP_DIR}

EXPOSE 58050/tcp
#EXPOSE 58051/tcp 1900/udp

ENTRYPOINT ["sh", "-c"]

CMD ["${APP_DIR}/launch.sh ${SERVICE_ARGS}"]

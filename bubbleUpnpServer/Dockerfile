FROM alpine:3.10.3

MAINTAINER Ponder Bear <ponder.bear@protonmail.com>

ARG USER=Ahab
ARG GROUP=Ahab
ARG UID=1000
ARG GID=1000

# Bubble upnp server app settings
ARG BUBBLE_RESOURCE_DIR=/resources/bubble
ARG BUBBLE_LAUNCHER=${BUBBLE_RESOURCE_DIR}/launcher
ARG BUBBLE_SERVER_VERSION=v0.9-update37
ENV BUBBLE_APP_DIR=/opt/bubbleupnpserver
ENV BUBBLE_APP_LAUNCHER=${BUBBLE_APP_DIR}/launch.sh
ENV BUBBLE_SERVICE_ARGS="-nologfile -logLevel SEVERE -disableAutoUpdate"

# Supporting rest service
ARG REST_RESOURCE_DIR=/resources/restService
ENV REST_APP_DIR=/opt/restservice
ENV REST_APP_PORT=58052

RUN apk update && apk add --no-cache \
  ffmpeg \
  openjdk8-jre \
  python3 \
  sox \
  && apk del --purge

RUN pip3 install flask

# Create user
RUN addgroup -g ${GID} ${GROUP} \
    && adduser -u ${UID} -G ${GROUP} -D ${USER}

# Add bubble application launcher
RUN mkdir -p ${BUBBLE_APP_DIR}
COPY ${BUBBLE_LAUNCHER} ${BUBBLE_APP_DIR}
COPY ${BUBBLE_RESOURCE_DIR}/BubbleUPnPServer-${BUBBLE_SERVER_VERSION}.jar /${BUBBLE_APP_DIR}/BubbleUPnPServer.jar

RUN chown -R ${USER}:${GROUP} ${BUBBLE_APP_DIR}
RUN chmod -R +x ${BUBBLE_APP_DIR}

# Add rest service to the image
COPY ${REST_RESOURCE_DIR}/* ${REST_APP_DIR}/
RUN chown -R ${USER} ${REST_APP_DIR}

USER ${USER}
# Bubble upnp server port
EXPOSE 58050/tcp
# Rest service port
EXPOSE ${REST_APP_PORT}

ENTRYPOINT ["sh", "-c"]
CMD ["python3 ${REST_APP_DIR}/RestService.py ${REST_APP_PORT} ${BUBBLE_APP_LAUNCHER} ${BUBBLE_SERVICE_ARGS}"]

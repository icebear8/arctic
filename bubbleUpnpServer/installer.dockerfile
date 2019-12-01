FROM alpine:latest

# Installer settings
ARG BUBBLE_DOWNLOAD_LINK=https://bubblesoftapps.com/bubbleupnpserver/BubbleUPnPServer-distrib.zip
ARG BUBBLE_APPLICATION_REPO=BubbleUPnPServer-distrib.zip
ARG BUBBLE_SERVER_VERSION=v0.9-update37
ARG BUBBLE_APP_DIR=/opt/bubbleupnpserver
ARG BUBBLE_APP_LAUNCHER=${BUBBLE_APP_DIR}/launch.sh
ENV BUBBLE_DOWNLOAD_DIR=/tmp/bubble

RUN apk update && apk add --no-cache \
  ffmpeg \
  openjdk8-jre \
  python3 \
  sox \
  unzip \
  wget \
  && apk del --purge

RUN pip3 install flask

# Add bubble application launcher from web
RUN wget ${BUBBLE_DOWNLOAD_LINK} -P ${BUBBLE_DOWNLOAD_DIR}
RUN mkdir -p ${BUBBLE_APP_DIR} \
    && unzip ${BUBBLE_DOWNLOAD_DIR}/${BUBBLE_APPLICATION_REPO} -d ${BUBBLE_DOWNLOAD_DIR}/launcher \
    && unzip ${BUBBLE_DOWNLOAD_DIR}/${BUBBLE_APPLICATION_REPO} -d ${BUBBLE_APP_DIR} \
    && rm ${BUBBLE_DOWNLOAD_DIR}/${BUBBLE_APPLICATION_REPO}

# Run script to download latest version,
# kill after start and copy new version to the resource dir
RUN sh ${BUBBLE_APP_LAUNCHER} & \
    sleep 10 \
    && kill $!

RUN cp ${BUBBLE_APP_DIR}/BubbleUPnPServer.jar ${BUBBLE_DOWNLOAD_DIR}/BubbleUPnPServer-${BUBBLE_SERVER_VERSION}.jar

VOLUME /mnt/bubble

ENTRYPOINT ["sh", "-c"]
CMD ["cp -r ${BUBBLE_DOWNLOAD_DIR}/* /mnt/bubble"]

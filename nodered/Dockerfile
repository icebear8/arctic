ARG USER=Ahab
ARG GROUP=Ahab
ARG UID=1000
ARG GID=1000
ARG REPO_DIR=/opt/repo
ARG DOWNLOAD_DIR=/tmp/download

ARG BASE_IMG_VERSION=3.11.2-r1-onbuild

# Nodered downloader
From alpine:latest as downloader

# Common arguments must be repeated but kept empty to be accepted
ARG DOWNLOAD_DIR

ARG NODERED_VERSION=1.0.3
ARG TMP_DOWNLOAD_DIR=/tmp/nred

RUN mkdir -p ${TMP_DOWNLOAD_DIR} \
  && mkdir ${DOWNLOAD_DIR}

RUN wget https://github.com/node-red/node-red/releases/download/${NODERED_VERSION}/node-red-${NODERED_VERSION}.zip -P ${TMP_DOWNLOAD_DIR}
RUN unzip ${TMP_DOWNLOAD_DIR}/node-red-${NODERED_VERSION}.zip -d ${DOWNLOAD_DIR}


FROM icebear8/gitrepoutils:${BASE_IMG_VERSION}
MAINTAINER Ponder Bear <ponder.bear@protonmail.com>

# Common arguments must be repeated but kept empty to be accepted
ARG REPO_DIR
ARG DOWNLOAD_DIR

# APP_INSTALL_DIR: Node-red zip creates a 'node-red' folder => /opt/node-red
ENV APP_RUNTIME_DIR=/srv/nodered
ARG APP_INSTALL_DIR=/opt

# Application tools and helpers
ENV APP_UTILS_DIR=/opt/utils/app
ENV APP_LAUNCHER=${APP_UTILS_DIR}/launcher.sh

# Default arguments for service execution
ENV SERVICE_ARGS="--userDir ${APP_RUNTIME_DIR}"

RUN apk update && apk add --no-cache \
  nodejs \
  nodejs-npm \
  && apk del --purge

# Install node-red
RUN mkdir -p ${APP_INSTALL_DIR}
COPY --from=downloader ${DOWNLOAD_DIR}/ ${APP_INSTALL_DIR}
WORKDIR ${APP_INSTALL_DIR}/node-red
RUN npm install -g --unsafe-perm --production || true
WORKDIR /

# Prepare the directory for the application data and configuration
# Copy the default settings as well
RUN mkdir -p ${APP_RUNTIME_DIR}
COPY ./resources/settings.js ${APP_RUNTIME_DIR}

# Prepare launcher utilities
RUN mkdir -p ${APP_UTILS_DIR}
COPY /utils/* ${APP_UTILS_DIR}/

# Fix access rights
RUN chmod -R 755 ${APP_UTILS_DIR}/*.sh
RUN chown -R ${USER}:${GROUP} ${APP_RUNTIME_DIR}

USER ${USER}
EXPOSE 1880
VOLUME ${APP_RUNTIME_DIR}

ENTRYPOINT ["sh", "-c"]
CMD ["sh ${APP_LAUNCHER}"]

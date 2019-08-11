FROM icebear8/gitrepoutils:3.10.0-r1

MAINTAINER Ponder Bear <ponder.bear@protonmail.com>

ARG USER=Ahab
ARG GROUP=Ahab
ARG uid=1000
ARG gid=1000

ARG NODERED_VERSION=0.20.7
# APP_INSTALL_DIR: Node-red zip creates a 'node-red' folder => /opt/node-red
ARG APP_INSTALL_DIR=/opt/
ENV APP_RUNTIME_DIR=/srv/nodered

# Application tools and helpers
ENV APP_UTILS_DIR=/opt/utils/app
ENV APP_LAUNCHER=${APP_UTILS_DIR}/launcher.sh

# Default arguments for service execution
ENV SERVICE_ARGS="--userDir ${APP_RUNTIME_DIR}"

RUN apk update && apk add --no-cache \
  nodejs \
  nodejs-npm \
  && apk del --purge

RUN addgroup -g ${gid} ${GROUP} && \
    adduser -u ${uid} -G ${GROUP} -D ${USER}

# Prepare access to git config and key files
RUN ln -s ${GIT_CONFIG_DIR}/.ssh/ /home/${USER}/.ssh \
  && ln -s ${GIT_CONFIG_DIR}/.gitconfig /home/${USER}/.gitconfig

# Install node-red
ARG TMP_DOWNLOAD_DIR=/tmp/nred
RUN mkdir -p ${TMP_DOWNLOAD_DIR} \
    && mkdir -p ${APP_INSTALL_DIR} \
    && wget https://github.com/node-red/node-red/releases/download/${NODERED_VERSION}/node-red-${NODERED_VERSION}.zip -P ${TMP_DOWNLOAD_DIR} \
    && unzip ${TMP_DOWNLOAD_DIR}/node-red-${NODERED_VERSION}.zip -d ${APP_INSTALL_DIR} \
    && cd ${APP_INSTALL_DIR}/node-red \
    && npm install -g --unsafe-perm --production \
    && cd / \
    && rm -rf ${TMP_DOWNLOAD_DIR}

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
RUN chown -R ${USER}:${GROUP} ${GIT_CONFIG_DIR}

USER ${USER}

# Port and data settings
EXPOSE 1880
VOLUME ${APP_RUNTIME_DIR}
VOLUME ${GIT_CONFIG_DIR}

ENTRYPOINT ["sh", "-c"]
CMD ["sh ${APP_LAUNCHER}"]

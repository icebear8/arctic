# Node Red

FROM icebear8/gitrepoutils:latest
MAINTAINER Cheshire Lynx <cheshire.lynx@protonmail.com>

ARG USER=Ahab
ARG GROUP=Ahab
ARG uid=1000
ARG gid=1000

ENV DATA_DIR=/data

# Launcher
ENV APP_UTILS_DIR=/opt/utils/app
ENV APP_LAUNCHER=${APP_UTILS_DIR}/launcher.sh

# Default arguments for service execution
ENV SERVICE_ARGS="--userDir ${DATA_DIR}"

RUN apk update && apk add --no-cache \
  nodejs \
  nodejs-npm \
  && apk del --purge
  
RUN addgroup -g ${gid} ${GROUP} && \
    adduser -u ${uid} -G ${GROUP} -D ${USER}
    
# Prepare access to git config and key files
RUN ln -s ${GIT_USER_ACCESS_DIR}/.ssh/ /home/${USER}/.ssh \
  && ln -s ${GIT_USER_ACCESS_DIR}/.gitconfig /home/${USER}/.gitconfig
  
# Install node-red
RUN npm install -g --unsafe-perm node-red@0.19.5
  
# Directory for storing the data
RUN mkdir -p ${DATA_DIR}
# Default settings
COPY ./resources/settings.js ${DATA_DIR}

# Prepare launcher utilities
RUN mkdir -p ${APP_UTILS_DIR}
COPY /utils/* ${APP_UTILS_DIR}/

# Fix access rights
RUN chmod -R 755 ${APP_UTILS_DIR}/*.sh
RUN chown -R ${USER}:${GROUP} ${DATA_DIR}
RUN chown -R ${USER}:${GROUP} ${GIT_USER_ACCESS_DIR}

USER ${USER}

# Port and data settings
EXPOSE 1880
VOLUME ${DATA_DIR}

ENTRYPOINT ["sh", "-c"]
CMD ["sh ${APP_LAUNCHER}"]

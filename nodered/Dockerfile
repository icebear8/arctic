# Node Red

FROM icebear8/gitrepoutils:3.8-r2
MAINTAINER Cheshire Lynx <cheshire.lynx@protonmail.com>

ARG USER=Ahab
ARG GROUP=Ahab
ARG uid=1000
ARG gid=1000

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
RUN npm install -g --unsafe-perm node-red@0.19.5
  
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

FROM alpine:3.7

MAINTAINER Cheshire Lynx <cheshire.lynx@protonmail.com>

# User
ARG USER=Ahab
ARG GROUP=Ahab
ARG UID=1000
ARG GID=1000

# Application and content
ARG CONTENT_DIR=/var/www
ARG CONFIG_DIR=/etc/nginx/sites-enabled

# Launcher
ENV APP_UTILS_DIR=/opt/utils/app
ENV APP_LAUNCHER=${APP_UTILS_DIR}/launcher.sh

# Repo utilities
ENV REPO_URL=
ENV REPO_DIR=/opt/repo
ENV CONTENT_REPO_DIR=${REPO_DIR}/nginx/www
ENV CONFIG_REPO_DIR=${REPO_DIR}/nginx/config
ENV GIT_UTILS_DIR=/opt/utils/git

RUN apk update &&\
  apk add --no-cache \
  git \
  logrotate \
  openssh-client \
  openssh-keygen \
  nginx

# Create user
RUN addgroup -g ${GID} ${GROUP} \
    && adduser -u ${UID} -G ${GROUP} -D ${USER}
    
# Prepare git remote repo access
RUN git clone --depth 1 https://github.com/icebear8/gitRepoUtils.git ${GIT_UTILS_DIR}
RUN mkdir -p /home/${USER}/.ssh/ \
  && touch /home/${USER}/.ssh/known_hosts \
  && cat /opt/utils/git/resources/known_hostsGithub >> /home/${USER}/.ssh/known_hosts
  
# Prepare utilities
RUN mkdir -p ${APP_UTILS_DIR}
COPY /utils/* ${APP_UTILS_DIR}/

COPY ./resources/nginx.conf /etc/nginx/nginx.conf

# Prepare repo directories and symlinks to the application directory
RUN mkdir -p ${REPO_DIR} \
  && mkdir -p ${CONFIG_REPO_DIR} \
  && ln -s ${CONFIG_REPO_DIR} ${CONFIG_DIR} \
  && mkdir -p ${CONTENT_REPO_DIR} \
  && rm -rf ${CONTENT_DIR} \
  && ln -s ${CONFIG_REPO_DIR} ${CONTENT_DIR}

COPY ./resources/config/* ${CONFIG_REPO_DIR}
COPY ./resources/www/* ${CONTENT_REPO_DIR}

RUN touch /var/run/nginx.pid

RUN chmod -R 755 ${APP_UTILS_DIR}/*.sh
RUN chmod -R 755 ${GIT_UTILS_DIR}/*.sh
RUN chown -R ${USER}:${GROUP} /home/${USER}
RUN chown -R ${USER}:${GROUP} ${REPO_DIR}
RUN chown -R ${USER}:${GROUP} ${CONTENT_DIR}
RUN chown -R ${USER}:${GROUP} /var/log/nginx
RUN chown -R ${USER}:${GROUP} /var/lib/nginx
RUN chown -R ${USER}:${GROUP} /var/run/nginx.pid
RUN chown -Rh ${USER}:${GROUP} /var/lib/nginx

USER ${USER}
EXPOSE 8080

WORKDIR ${REPO_DIR}    
VOLUME ${REPO_DIR}

ENTRYPOINT ["sh", "-c"]
CMD ["sh ${APP_LAUNCHER}"]

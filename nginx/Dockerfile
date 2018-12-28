# Nginx

FROM icebear8/gitrepoutils:3.8-r2
MAINTAINER Cheshire Lynx <cheshire.lynx@protonmail.com>

# User
ARG USER=Ahab
ARG GROUP=Ahab
ARG UID=1000
ARG GID=1000

# Helper tools and scripts for the application
ENV APP_UTILS_DIR=/opt/utils/app
ENV APP_LAUNCHER=${APP_UTILS_DIR}/launcher.sh

# Application configuration and content
ARG CONTENT_DIR=/var/www
ARG CONFIG_DIR=/etc/nginx/sites-enabled

# Configuration and content location in the repository
ENV CONFIG_REPO_DIR=${REPO_DIR}/nginx/config
ENV CONTENT_REPO_DIR=${REPO_DIR}/nginx/www

RUN apk update \
  && apk add --no-cache \
  nginx \
  && apk del --purge

# Create user
RUN addgroup -g ${GID} ${GROUP} \
    && adduser -u ${UID} -G ${GROUP} -D ${USER}
    
# Sym links to git configuration for the container user
RUN ln -s ${GIT_CONFIG_DIR}/.ssh/ /home/${USER}/.ssh \
  && ln -s ${GIT_CONFIG_DIR}/.gitconfig /home/${USER}/.gitconfig
    
# Prepare application tools and helper scripts
RUN mkdir -p ${APP_UTILS_DIR}
COPY /utils/* ${APP_UTILS_DIR}/

# Prepare repo directories and symlinks to the application directory
RUN mkdir -p ${CONFIG_REPO_DIR} \
  && ln -s ${CONFIG_REPO_DIR} ${CONFIG_DIR} \
  && rm -rf ${CONTENT_DIR} \
  && mkdir -p ${CONTENT_REPO_DIR} \
  && ln -s ${CONTENT_REPO_DIR} ${CONTENT_DIR}

# Prepare nginx settings
# Copy initial default settings as well (not from git repo)
COPY ./resources/nginx.conf /etc/nginx/nginx.conf
COPY ./resources/config/* ${CONFIG_REPO_DIR}
COPY ./resources/www/* ${CONTENT_REPO_DIR}
RUN touch /var/run/nginx.pid

# Fix access rights
RUN chmod -R 755 ${APP_UTILS_DIR}/*.sh
RUN chown -R ${USER}:${GROUP} ${GIT_CONFIG_DIR}
RUN chown -R ${USER}:${GROUP} ${REPO_DIR}
RUN chown -R ${USER}:${GROUP} ${CONTENT_DIR}
RUN chown -R ${USER}:${GROUP} /var/log/nginx
RUN chown -R ${USER}:${GROUP} /var/lib/nginx
RUN chown -R ${USER}:${GROUP} /var/run/nginx.pid
RUN chown -Rh ${USER}:${GROUP} /var/lib/nginx

WORKDIR ${REPO_DIR}

VOLUME ${GIT_CONFIG_DIR}
VOLUME ${REPO_DIR}

USER ${USER}
EXPOSE 8080

ENTRYPOINT ["sh", "-c"]
CMD ["sh ${APP_LAUNCHER}"]

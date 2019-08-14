# User
ARG USER=Ahab
ARG GROUP=Ahab
ARG UID=1000
ARG GID=1000
ARG REPO_DIR=/opt/repo

ARG BASE_IMG_VERSION=3.10.1-r2-onbuild
FROM icebear8/gitrepoutils:${BASE_IMG_VERSION}

MAINTAINER Ponder Bear <ponder.bear@protonmail.com>

# User access
ENV USER=${USER}
ENV GROUP=${GROUP}

# Helper tools and scripts for the application
ENV APP_UTILS_DIR=/opt/utils/app
ENV APP_LAUNCHER=${APP_UTILS_DIR}/launcher.sh

# Application configuration and content
ENV NGX_CONTENT_DIR=/var/www
ENV NGX_CONFIG_DIR=/etc/nginx/sites-enabled

# Configuration and content location in the repository
ENV NGX_CONFIG_REPO_DIR=${REPO_DIR}/nginx/config
ENV NGX_CONTENT_REPO_DIR=${REPO_DIR}/nginx/www

RUN apk update && apk add --no-cache \
  nginx=1.16.1-r0 \
  && apk del --purge

# Prepare application tools and helper scripts
RUN mkdir -p ${APP_UTILS_DIR}
COPY /utils/* ${APP_UTILS_DIR}/

# Prepare repo directories and symlinks to the application directory
RUN mkdir -p ${NGX_CONFIG_REPO_DIR} \
  && ln -s ${NGX_CONFIG_REPO_DIR} ${NGX_CONFIG_DIR} \
  && rm -rf ${NGX_CONTENT_DIR} \
  && mkdir -p ${NGX_CONTENT_REPO_DIR} \
  && ln -s ${NGX_CONTENT_REPO_DIR} ${NGX_CONTENT_DIR}

# Prepare nginx settings
# Copy initial default settings as well (not from git repo)
COPY ./resources/nginx.conf /etc/nginx/nginx.conf
COPY ./resources/config/* ${NGX_CONFIG_REPO_DIR}
COPY ./resources/www/* ${NGX_CONTENT_REPO_DIR}
RUN touch /var/run/nginx.pid

# Fix access rights
RUN chmod -R 755 ${APP_UTILS_DIR}/*.sh
RUN chown -R ${USER}:${GROUP} ${REPO_DIR}
RUN chown -R ${USER}:${GROUP} ${NGX_CONTENT_DIR}
RUN chown -R ${USER}:${GROUP} /var/log/nginx \
  && chown -R ${USER}:${GROUP} /var/lib/nginx \
  && chown -R ${USER}:${GROUP} /var/run/nginx.pid \
  && chown -Rh ${USER}:${GROUP} /var/lib/nginx

WORKDIR ${REPO_DIR}
VOLUME ${REPO_DIR}
USER ${USER}
EXPOSE 8080

ENTRYPOINT ["sh", "-c"]
CMD ["sh ${APP_LAUNCHER}"]

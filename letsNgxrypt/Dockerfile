ARG BASE_IMG_VERSION=1.16.0-r4
FROM icebear8/nginx:${BASE_IMG_VERSION}

MAINTAINER <ponder.bear@protonmail.com>

# User already created and switched in base image
USER root

# LETSENCRYPT directories
ENV CERTIFICATE_DIR=/srv/certificates
ENV LETSENCRYPT_MAIL=foo@bar.com
ENV LETSENCRYPT_DOMAINS=example.com
ENV LETSENCRYPT_SERVER=https://acme-staging-v02.api.letsencrypt.org/directory
ENV LETSENCRYPT_CHALLANGE=http
ENV LETSENCRYPT_PORT=8080
ENV LETSENCRYPT_GLOBAL_OPTIONS=

# General setup
## User is already setup in base image

# Copy helper tools
COPY /utils/* ${APP_UTILS_DIR}/

# NGINX
## Setting up the basic Nginx configuration is done in the base image
## Copy initial nginx default settings as well (not from git repo)
COPY ./resources/nginx.conf /etc/nginx/nginx.conf
#COPY ./resources/config/* ${NGX_CONFIG_REPO_DIR}

# LETSENCRYPT, LEGO
COPY ./resources/lego_v2.6.0_linux_386/lego /usr/bin/lego
RUN chmod +x /usr/bin/lego

## Directories and access
RUN mkdir -p ${CERTIFICATE_DIR} \
  && chown -R ${USER}:${GROUP} ${CERTIFICATE_DIR}

# General system config
WORKDIR ${REPO_DIR}
VOLUME ${CERTIFICATE_DIR}

USER ${USER}
EXPOSE ${LETSENCRYPT_PORT}

ENTRYPOINT ["sh", "-c"]
CMD ["sh ${APP_LAUNCHER}"]

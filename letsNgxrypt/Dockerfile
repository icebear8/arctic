ARG CPU_ARCH
ARG BASE_IMG_VERSION=1.16.1-r1

ARG DOWNLOAD_DIR=/tmp/download
ARG SUPERCRONIC_BIN=supercronic
ARG LEGO_BIN=lego
ARG CPU_TARGET_ARCH=386

# Supercronic downloader
From alpine:latest as supercronic-downloader

ARG CPU_TARGET_ARCH
ARG DOWNLOAD_DIR
ARG SUPERCRONIC_BIN
ARG SUPERCRONIC_VERSION=v0.1.9
ARG SUPERCRONIC_TMP_BIN=supercronic-linux-${CPU_TARGET_ARCH}

RUN apk update && apk add --no-cache \
  curl \
  && apk del --purge

RUN mkdir -p /tmp/verifyer \
  && echo "echo '5ddf8ea26b56d4a7ff6faecdd8966610d5cb9d85  ${DOWNLOAD_DIR}/${SUPERCRONIC_TMP_BIN}' | sha1sum -c -" > /tmp/verifyer/amd64 \
  && echo "echo 'e0126b0102b9f388ecd55714358e3ad60d0cebdb  ${DOWNLOAD_DIR}/${SUPERCRONIC_TMP_BIN}' | sha1sum -c -" > /tmp/verifyer/386 \
  && echo "echo '47481c3341bc3a1ae91a728e0cc63c8e6d3791ad  ${DOWNLOAD_DIR}/${SUPERCRONIC_TMP_BIN}' | sha1sum -c -" > /tmp/verifyer/arm \
  && echo "echo 'e2714c43e7781bf1579c85aa61259245f56dbba1  ${DOWNLOAD_DIR}/${SUPERCRONIC_TMP_BIN}' | sha1sum -c -" > /tmp/verifyer/arm64

RUN mkdir -p ${DOWNLOAD_DIR}
WORKDIR ${DOWNLOAD_DIR}

RUN curl -fsSLO https://github.com/aptible/supercronic/releases/download/${SUPERCRONIC_VERSION}/${SUPERCRONIC_TMP_BIN} \
 && sh /tmp/verifyer/${CPU_TARGET_ARCH} \
 && mv ${SUPERCRONIC_TMP_BIN} ${SUPERCRONIC_BIN} \
 && chmod +x ${SUPERCRONIC_BIN}

# Lego downloader
From alpine:latest as lego-downloader

ARG CPU_TARGET_ARCH
ARG DOWNLOAD_DIR=/tmp/download
ARG LEGO_BIN
ARG LEGO_VERSION=v2.6.0
ARG LEGO_TMP_BIN=lego_${LEGO_VERSION}_linux_${CPU_TARGET_ARCH}.tar.gz

RUN apk update && apk add --no-cache \
  curl \
  tar \
  && apk del --purge

RUN mkdir -p ${DOWNLOAD_DIR}
WORKDIR ${DOWNLOAD_DIR}

RUN curl -fsSLO https://github.com/go-acme/lego/releases/download/${LEGO_VERSION}/${LEGO_TMP_BIN}
RUN tar -zxvf ${LEGO_TMP_BIN} \
  && chmod +x ${LEGO_BIN}


# Productive image
FROM icebear8/nginx:${BASE_IMG_VERSION}${CPU_ARCH}
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

ENV CRONTAB_DIR=/srv/supercronic
ENV CRONTAB_FILE_PATH=${CRONTAB_DIR}/superCronicTab

# General setup
## User is already setup in base image

ARG DOWNLOAD_DIR
ARG SUPERCRONIC_BIN
ARG LEGO_BIN

# Install Supersonic
COPY --from=supercronic-downloader ${DOWNLOAD_DIR}/${SUPERCRONIC_BIN} "/usr/bin/${SUPERCRONIC_BIN}"
RUN mkdir -p ${CRONTAB_DIR} \
  && touch ${CRONTAB_FILE_PATH} \
  && chown -R ${USER}:${GROUP} ${CRONTAB_DIR}

# Copy helper tools
COPY /utils/* ${APP_UTILS_DIR}/

# NGINX
## Setting up the basic Nginx configuration is done in the base image
## Copy initial nginx default settings as well (not from git repo)
COPY ./resources/nginx.conf /etc/nginx/nginx.conf

# LETSENCRYPT, LEGO
COPY --from=lego-downloader ${DOWNLOAD_DIR}/${LEGO_BIN} "/usr/bin/${LEGO_BIN}"
RUN chown ${USER}:${GROUP} /usr/bin/${LEGO_BIN}

## Directories and access
RUN mkdir -p ${CERTIFICATE_DIR} \
&& chown -R ${USER}:${GROUP} ${CERTIFICATE_DIR}

RUN chmod -R 755 ${APP_UTILS_DIR}/*.sh

# General system config
WORKDIR ${REPO_DIR}
VOLUME ${CERTIFICATE_DIR}

USER ${USER}
EXPOSE ${LETSENCRYPT_PORT}

ENTRYPOINT ["sh", "-c"]
CMD ["sh ${APP_LAUNCHER}"]

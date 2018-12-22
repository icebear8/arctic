FROM alpine:3.8

MAINTAINER Cheshire Lynx <cheshire.lynx@protonmail.com>

# User settings
ARG USER=Ahab
ARG GROUP=Ahab
ARG UID=1000
ARG GID=1000

# App location settings, ARG for build time, ENV for runtime parameters
ARG BASE_DIR=/opt
ENV APP_NAME=ddclient
ARG APP_VERSION=3.9.0
ARG APP_REPO=${APP_NAME}-${APP_VERSION}.zip
ENV MAIN_APP_DIR=${BASE_DIR}/${APP_NAME}

# App configuration settings
ENV APP_CONFIG_ARGUMENT_LIST=
ENV APP_STARTUP_ARGUMENTS="-help"
ENV APP_CONFIG_DIR=/etc/ddclient

# Utils for supporting functionality
ENV UTILS_DIR=${BASE_DIR}/utils
ENV APP_LAUNCHER=${UTILS_DIR}/launcher.sh

RUN apk update && apk add --no-cache \
	curl \
  inotify-tools \
  make \
	perl \
	perl-digest-sha1 \
	perl-io-socket-ssl \
	perl-json \
  perl-log-log4perl \
  perl-net-ip \
  perl-netaddr-ip \
  perl-utils \
  perl-yaml \
  unzip \
  wget \
  && apk del --purge

RUN curl -L http://cpanmin.us | perl - App::cpanminus\
  && cpanm \
	Data::Validate::IP

# Create user
RUN addgroup -g ${GID} ${GROUP} \
    && adduser -u ${UID} -G ${GROUP} -D ${USER}
    
# Create application directory and copy application
RUN mkdir -p ${BASE_DIR}
COPY /resources/${APP_REPO} ${BASE_DIR}
RUN unzip ${BASE_DIR}/${APP_REPO} -d ${BASE_DIR} \
  && rm ${BASE_DIR}/${APP_REPO} \
  && mv ${BASE_DIR}/${APP_NAME}-${APP_VERSION} ${MAIN_APP_DIR}

# Prepare directories for the application
RUN mkdir ${APP_CONFIG_DIR} \
  && mkdir /var/cache/ddclient \
  && touch /var/run/ddclient.pid
  
COPY /resources/base-etc_ddclient.conf ${APP_CONFIG_DIR}/ddclient_source.conf

# Prepare utils
RUN mkdir -p ${UTILS_DIR}
COPY /utils/* ${UTILS_DIR}/
  
# User access for the app directories
RUN chown -R ${USER}:${GROUP} ${APP_CONFIG_DIR}
RUN chown -R ${USER}:${GROUP} /var/cache/ddclient
RUN chown -R ${USER}:${GROUP} /var/run/ddclient.pid
RUN chown -R ${USER}:${GROUP} ${BASE_DIR}
RUN chmod -R 755 ${UTILS_DIR}/*.sh
    
USER ${USER}

VOLUME ${APP_CONFIG_DIR}

ENTRYPOINT ["sh", "-c"]
CMD ["sh ${APP_LAUNCHER}"]
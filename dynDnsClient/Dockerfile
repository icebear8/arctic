FROM alpine:3.8

MAINTAINER Cheshire Lynx <cheshire.lynx@protonmail.com>

ARG USER=Ahab
ARG GROUP=Ahab
ARG UID=1000
ARG GID=1000

ARG APP_NAME=ddclient
ARG APP_VERSION=3.9.0

ARG APP_REPO=${APP_NAME}-${APP_VERSION}.zip
ARG BASE_DIR=/opt
ARG MAIN_APP_DIR=${BASE_DIR}/${APP_NAME}

RUN apk update && apk add --no-cache \
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
  && apk del --purge

RUN cpan Data::Validate::IP

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
RUN mkdir /etc/ddclient \
  && mkdir /var/cache/ddclient \
  && touch /var/run/ddclient.pid
  
COPY /resources/base-etc_ddclient.conf /etc/ddclient/ddclient.conf
  
# User access for the app directories
RUN chown -R ${USER}:${GROUP} /etc/ddclient
RUN chown -R ${USER}:${GROUP} /var/cache/ddclient
RUN chown -R ${USER}:${GROUP} /var/run/ddclient.pid
RUN chown -R ${USER}:${GROUP} ${BASE_DIR}
    
USER ${USER}

ENTRYPOINT ["sh", "-c"]
CMD ["sh ${APP_LAUNCHER}"]
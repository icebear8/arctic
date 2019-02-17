FROM alpine:3.8

MAINTAINER Cheshire Lynx <cheshire.lynx@protonmail.com>

# User settings
ARG USER=Ahab
ARG GROUP=Ahab
ARG UID=1000
ARG GID=1000

ENV APP_DIR=/opt/utils
ENV APP_LAUNCHER=${APP_DIR}/launcher.sh
ARG IP_CACHE_DIR="/var/cache/ddnshurricane"
ENV IP_CACHE_PATH="${IP_CACHE_DIR}/ip.cache"

ENV LOC_EXECUTION_PERIOD=1h
ENV LOC_INTERFACE=eth0
ENV LOC_IPV=ipv6
ENV DNS_HOSTNAME=
ENV DNS_TOKEN=

RUN apk update && apk add --no-cache \
	curl \
  && apk del --purge

# Create user
RUN addgroup -g ${GID} ${GROUP} \
    && adduser -u ${UID} -G ${GROUP} -D ${USER}

# Prepare application files and directories
RUN mkdir -p ${APP_DIR}
COPY /utils/* ${APP_DIR}/

RUN mkdir -p ${IP_CACHE_DIR} \
    && touch ${IP_CACHE_PATH}

# Update user access rights
RUN chown -R ${USER}:${GROUP} ${APP_DIR}
RUN chown -R ${USER}:${GROUP} ${IP_CACHE_DIR}
RUN chmod -R 755 ${APP_DIR}/*.sh
    
USER ${USER}

ENTRYPOINT ["sh", "-c"]
CMD ["sh ${APP_LAUNCHER}"]


FROM alpine:3.7

MAINTAINER Dominik Ebert <doe@zuehlke.com>

ARG user=www
ARG group=www
ARG uid=1000
ARG gid=1000
ARG grav_repo=grav-v1.4.6.zip

ENV APP_DIR=/var/www
ENV UTILS_DIR=${APP_DIR}/utils
ENV APP_LAUNCHER=${UTILS_DIR}/launcher.sh

ENV CONTENT_REPO_URL=
ENV CONTENT_DIR=

RUN apk update \
  && apk add --no-cache \
  git \
  logrotate \
  nginx \
  php5 \
  php5-ctype \
  php5-curl \
  php5-dom \
  php5-fpm \
  php5-gd \
  php5-iconv \
  php5-json \
  php5-mcrypt \
  php5-openssl \
  php5-posix \
  php5-sockets \
  php5-xml \
  php5-xmlreader \
  php5-zip \
  wget \
  unzip  

RUN addgroup -g ${gid} ${group} \
    && adduser -u ${uid} -G ${group} -D ${user}

RUN mkdir -p ${APP_DIR}

COPY /resources/nginx/nginx.conf /etc/nginx/nginx.conf
COPY /resources/nginx/config/* /etc/nginx/sites-enabled/

RUN mkdir -p ${UTILS_DIR}
COPY /utils/* ${UTILS_DIR}

COPY /resources/${grav_repo} ${APP_DIR}/
RUN unzip ${APP_DIR}/${grav_repo} -d ${APP_DIR}\
    && rm ${APP_DIR}/${grav_repo}

RUN touch /var/run/nginx.pid
RUN chown -R ${user}:${group} ${APP_DIR}
RUN chown -R ${user}:${group} ${UTILS_DIR}
RUN chown -R ${user}:${group} /var/log
RUN chown -R ${user}:${group} /var/lib/nginx
RUN chown -R ${user}:${group} /var/run/nginx.pid

USER ${user}
    
EXPOSE 8080

ENTRYPOINT ["sh", "-c"]

CMD ["sh ${APP_LAUNCHER}"]
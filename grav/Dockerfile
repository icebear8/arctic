FROM alpine:3.7

MAINTAINER Dominik Ebert <doe@zuehlke.com>

ARG user=www
ARG group=www
ARG uid=1000
ARG gid=1000
ARG app_dir=/var/www/
ARG grav_repo=grav-v1.4.6.zip

RUN apk add --no-cache \
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
    && adduser -h "$JENKINS_HOME" -u ${uid} -G ${group} -s /bin/bash -D ${user}

RUN mkdir -p ${app_dir}

RUN chown -R ${user} /var/log
RUN chown -R ${user} /var/tmp
RUN chown -R ${user} /var/run
RUN chown -R ${user} /var/lib/nginx

COPY /resources/nginx/nginx.conf /etc/nginx/nginx.conf
COPY /resources/nginx/config/* /etc/nginx/sites-enabled/
COPY /resources/run.sh ${app_dir}/

COPY /resources/${grav_repo} ${app_dir}/
RUN unzip ${app_dir}/${grav_repo} -d ${app_dir}\
    && rm ${app_dir}/${grav_repo}

RUN chown -R ${user} ${app_dir}

USER ${user}
    
EXPOSE 8080

CMD ["sh", "/var/www/run.sh"]
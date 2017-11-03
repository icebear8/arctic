FROM alpine:3.4

MAINTAINER Dominik Ebert <doe@zuehlke.com>

ARG user=www
ARG app_dir=/var/www/
ARG grav_repo=grav-admin-v1.2.4.zip

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

RUN adduser -D -u 1000 -g '${user}' ${user}
RUN mkdir -p ${app_dir}

RUN chown -R ${user}:${user} /var/log
RUN chown -R ${user}:${user} /var/lib/nginx
RUN chown -R ${user}:${user} /var/run

COPY /resources/nginx/nginx.conf /etc/nginx/nginx.conf
COPY /resources/nginx/config/* /etc/nginx/sites-enabled/
COPY /resources/run.sh ${app_dir}/

COPY /resources/${grav_repo} ${app_dir}/
RUN unzip ${app_dir}/${grav_repo} -d ${app_dir}&&\
    rm ${app_dir}/${grav_repo}

RUN chown -R ${user}:${user} ${app_dir}

USER ${user}
    
EXPOSE 8080

CMD ["sh", "/var/www/run.sh"]
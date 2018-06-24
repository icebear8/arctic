FROM alpine:3.7

MAINTAINER Dominik Ebert <doe@zuehlke.com>

ARG user=www
ARG app_dir=/var/www

RUN apk update &&\
  apk add --no-cache \
  logrotate \
  nginx


RUN adduser -D -u 1000 -g '${user}' ${user}

COPY ./resources/nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /etc/nginx/sites-enabled/
COPY ./resources/config/* /etc/nginx/sites-enabled/

COPY ./resources/www/* /var/www/

RUN touch /var/run/nginx.pid

RUN mkdir -p ${app_dir}
RUN chown -R ${user}:${user} ${app_dir}
RUN chown -R ${user}:${user} /var/log/nginx
RUN chown -R ${user}:${user} /var/tmp/nginx
RUN chown -R ${user}:${user} /var/lib/nginx
RUN chown -R ${user}:${user} /var/run/nginx.pid
RUN chown -Rh ${user}:${user} /var/lib/nginx

EXPOSE 8080

USER ${user}

CMD ["nginx", "-g", "daemon off;"]

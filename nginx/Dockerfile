FROM alpine:3.4
MAINTAINER Dominik Ebert <doe@zuehlke.com>

ARG user=www
ARG app_dir=/www

RUN apk add --no-cache \
  nginx

COPY nginx.conf /etc/nginx/
  
RUN adduser -D -u 1000 -g '${user}' ${user}

RUN chown -R ${user}:${user} /var/lib/nginx

RUN mkdir -p ${app_dir}
RUN chown -R ${user}:${user} ${app_dir}

VOLUME /etc/nginx/sites-enabled/

EXPOSE 8080
  
CMD ["nginx", "-g", "daemon off;"]

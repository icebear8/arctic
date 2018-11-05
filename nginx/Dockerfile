FROM alpine:3.7

MAINTAINER Cheshire Lynx <cheshire.lynx@protonmail.com>

ARG USER=Ahab
ARG GROUP=Ahab
ARG UID=1000
ARG GID=1000
ARG APP_DIR=/var/www
ARG CONFIG_DIR=/etc/nginx/sites-enabled/

RUN apk update &&\
  apk add --no-cache \
  logrotate \
  nginx


# Create user
RUN addgroup -g ${GID} ${GROUP} \
    && adduser -u ${UID} -G ${GROUP} -D ${USER}

COPY ./resources/nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p ${CONFIG_DIR}
COPY ./resources/config/* ${CONFIG_DIR}

COPY ./resources/www/* ${APP_DIR}

RUN touch /var/run/nginx.pid

RUN mkdir -p ${APP_DIR}
RUN chown -R ${USER}:${GROUP} ${APP_DIR}
RUN chown -R ${USER}:${GROUP} /var/log/nginx
RUN chown -R ${USER}:${GROUP} /var/lib/nginx
RUN chown -R ${USER}:${GROUP} /var/run/nginx.pid
RUN chown -Rh ${USER}:${GROUP} /var/lib/nginx

USER ${USER}
EXPOSE 8080
VOLUME ${APP_DIR}
VOLUME ${CONFIG_DIR}

ENTRYPOINT ["sh", "-c"]
CMD ["nginx -g daemon off;"]

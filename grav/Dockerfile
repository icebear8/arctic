FROM alpine:3.7

MAINTAINER Dominik Ebert <doe@zuehlke.com>

ARG user=www
ARG group=www
ARG uid=1000
ARG gid=1000
ARG grav_repo=grav-v1.4.6.zip
ARG WORK_DIR=/var/www
ARG MAIN_APP_DIR=${WORK_DIR}/grav

ENV UTILS_DIR=${WORK_DIR}/utils
ENV APP_LAUNCHER=${UTILS_DIR}/launcher.sh
ENV CONTENT_DIR=/var/www/content
ENV WEB_CONTENT_DIR=${CONTENT_DIR}/web
ENV CONTENT_REPO_URL=

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

# Create user
RUN addgroup -g ${gid} ${group} \
    && adduser -u ${uid} -G ${group} -D ${user}

# Prepare nginx
COPY /resources/nginx/nginx.conf /etc/nginx/nginx.conf
COPY /resources/nginx/config/* /etc/nginx/sites-enabled/
RUN touch /var/run/nginx.pid

# Prepare utilities
RUN mkdir -p ${UTILS_DIR}
COPY /utils/* ${UTILS_DIR}/

# Create application directory and copy grav
RUN mkdir -p ${WORK_DIR}
COPY /resources/${grav_repo} ${WORK_DIR}/
RUN unzip ${WORK_DIR}/${grav_repo} -d ${WORK_DIR} \
    && rm ${WORK_DIR}/${grav_repo}

# Move the web content into a separate directory and create a symlink
RUN mkdir -p ${CONTENT_DIR} \
    && mkdir -p ${WEB_CONTENT_DIR} \
    && mv ${MAIN_APP_DIR}/user ${WEB_CONTENT_DIR}/user \
    && ln -s ${WEB_CONTENT_DIR}/user ${MAIN_APP_DIR}/user
    
# Setup update script, it can be used if it is located in the nginx base directory
COPY /resources/deploy.php ${MAIN_APP_DIR}/

# Give access to the resources for the specified user
RUN chown -R ${user}:${group} ${WORK_DIR}
RUN chown -R ${user}:${group} ${UTILS_DIR}
RUN chmod -R 755 ${UTILS_DIR}
RUN chown -R ${user}:${group} ${CONTENT_DIR}
RUN chown -R ${user}:${group} ${WEB_CONTENT_DIR}
RUN chown -R ${user}:${group} /var/log
RUN chown -R ${user}:${group} /var/lib/nginx
RUN chown -R ${user}:${group} /var/run/nginx.pid

USER ${user}
    
EXPOSE 8080

VOLUME ${CONTENT_DIR}

ENTRYPOINT ["sh", "-c"]

CMD ["sh ${APP_LAUNCHER}"]
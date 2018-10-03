FROM alpine:3.7

MAINTAINER icebear

ARG USER=www
ARG GROUP=www
ARG UID=1000
ARG GID=1000

ARG GRAV_REPO=grav-v1.4.6.zip
ARG BASE_DIR=/opt
ARG MAIN_APP_DIR=${BASE_DIR}/grav

ENV REPO_DIR=/opt/repo
ENV WEB_CONTENT_DIR=${REPO_DIR}/web

ENV GRAV_UTILS_DIR=${BASE_DIR}/utils/grav
ENV APP_LAUNCHER=${GRAV_UTILS_DIR}/launcher.sh

RUN apk update \
  && apk add --no-cache \
  git \
  logrotate \
  nginx \
  php5 \
  php5-cli \
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
RUN addgroup -g ${GID} ${GROUP} \
    && adduser -u ${UID} -G ${GROUP} -D ${USER}

# Prepare nginx
COPY /resources/nginx/nginx.conf /etc/nginx/nginx.conf
COPY /resources/nginx/config/* /etc/nginx/sites-enabled/
RUN touch /var/run/nginx.pid

# Prepare utilities
RUN mkdir -p ${GRAV_UTILS_DIR}
COPY /utils/* ${GRAV_UTILS_DIR}/

# Create application directory and copy grav
RUN mkdir -p ${BASE_DIR}
COPY /resources/${GRAV_REPO} ${BASE_DIR}/
RUN unzip ${BASE_DIR}/${GRAV_REPO} -d ${BASE_DIR} \
    && rm ${BASE_DIR}/${GRAV_REPO}

# Move the web content into a separate directory and create a symlink
RUN mkdir -p ${REPO_DIR} \
    && mkdir -p ${WEB_CONTENT_DIR} \
    && mv ${MAIN_APP_DIR}/user ${WEB_CONTENT_DIR}/user \
    && ln -s ${WEB_CONTENT_DIR}/user ${MAIN_APP_DIR}/user
    
# Setup update script, it can be used if it is located in the nginx base directory
COPY /resources/deploy.php ${MAIN_APP_DIR}/

# Give access to the resources for the specified user
RUN chown -R ${USER}:${GROUP} /home/${USER}
RUN chown -R ${USER}:${GROUP} ${MAIN_APP_DIR}
RUN chmod -R 755 ${GRAV_UTILS_DIR}/*.sh
RUN chown -R ${USER}:${GROUP} ${REPO_DIR}
RUN chown -R ${USER}:${GROUP} /var/log
RUN chown -R ${USER}:${GROUP} /var/lib/nginx
RUN chown -R ${USER}:${GROUP} /var/run/nginx.pid

USER ${USER}
WORKDIR ${REPO_DIR}    
VOLUME ${REPO_DIR}
EXPOSE 8080

ENTRYPOINT ["sh", "-c"]
CMD ["sh ${APP_LAUNCHER}"]
FROM alpine:3.8

MAINTAINER Cheshire Lynx <cheshire.lynx@protonmail.com>

# Repo settings
ENV REPO_URL=
ENV REPO_DIR=/opt/repo
ENV GIT_UTILS_DIR=/opt/gitUtils
ENV GIT_USER_ACCESS_DIR=/data

RUN apk update \
  && apk add --no-cache \
  git \
  openssh-client \
  openssh-keygen \
  && apk del --purge

# Get git remote access utilities
COPY /utils/ ${GIT_UTILS_DIR}/

# Fix access rights
RUN chmod -R 755 ${GIT_UTILS_DIR}/*.sh

# Prepare ssh directory with known hosts
RUN mkdir -p ${GIT_USER_ACCESS_DIR}/.ssh/ \
  && touch ${GIT_USER_ACCESS_DIR}/.ssh/known_hosts \
  && cat ${GIT_UTILS_DIR}/resources/known_hostsGithub >> ${GIT_USER_ACCESS_DIR}/.ssh/known_hosts

VOLUME ${REPO_DIR}
VOLUME ${GIT_USER_ACCESS_DIR}

WORKDIR ${REPO_DIR}

ENTRYPOINT ["sh", "-c"]

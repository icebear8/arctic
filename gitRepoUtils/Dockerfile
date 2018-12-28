# Git Repo Utils

FROM alpine:3.8
MAINTAINER Cheshire Lynx <cheshire.lynx@protonmail.com>

# Repo settings and paths
ENV REPO_URL=
ENV REPO_DIR=/opt/repo
ENV GIT_HELPERS_DIR=/opt/gitHelperTools
ENV GIT_CONFIG_DIR=/srv/gitConfig

RUN apk update \
  && apk add --no-cache \
  git \
  openssh-client \
  openssh-keygen \
  && apk del --purge

# Copy the git helper tools and make them executable
COPY /utils/ ${GIT_HELPERS_DIR}/
RUN chmod -R 755 ${GIT_HELPERS_DIR}/*.sh

# Prepare git configuration and ssh directory
# Prepare known hosts
RUN mkdir -p ${GIT_CONFIG_DIR}/.ssh/ \
  && touch ${GIT_CONFIG_DIR}/.gitconfig \
  && touch ${GIT_CONFIG_DIR}/.ssh/known_hosts \
  && cat ${GIT_HELPERS_DIR}/resources/known_hostsGithub >> ${GIT_CONFIG_DIR}/.ssh/known_hosts

# Prepare repo directory
RUN mkdir -p ${REPO_DIR}

ENTRYPOINT ["sh", "-c"]

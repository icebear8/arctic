ARG BASE_IMG_VERSION=3.10.3
FROM alpine:${BASE_IMG_VERSION}

MAINTAINER Ponder Bear <ponder.bear@protonmail.com>

# Dummy ARGs for user onbuild workaround
## User is created during the 'FROM' command in the deriving image
ONBUILD ARG USER
ONBUILD ARG GROUP
ONBUILD ARG UID
ONBUILD ARG GID
ONBUILD ARG REPO_DIR

# Repo settings and paths
ONBUILD ENV REPO_DIR=${REPO_DIR}
ENV REPO_URL=
ENV GIT_HELPERS_DIR=/opt/gitHelperTools
ENV GIT_CONFIG_DIR=/srv/gitConfig

RUN apk update && apk add --no-cache \
  git=2.22.0-r0 \
  openssh-client=8.1_p1-r0 \
  openssh-keygen=8.1_p1-r0 \
  && apk del --purge

# Copy the git helper tools and make them executable
COPY /utils/ ${GIT_HELPERS_DIR}/
RUN chmod -R 755 ${GIT_HELPERS_DIR}/*.sh

# Create user in derived image
ONBUILD RUN addgroup -g ${GID} ${GROUP} \
  && adduser -u ${UID} -G ${GROUP} -D ${USER}

# Prepare git configuration and ssh directory
# Prepare known hosts
RUN mkdir -p ${GIT_CONFIG_DIR}/.ssh/ \
  && touch ${GIT_CONFIG_DIR}/.gitconfig \
  && touch ${GIT_CONFIG_DIR}/.ssh/known_hosts \
  && cat ${GIT_HELPERS_DIR}/resources/known_hostsGithub >> ${GIT_CONFIG_DIR}/.ssh/known_hosts

# Sym links to git configuration for the container user and access
ONBUILD RUN ln -s ${GIT_CONFIG_DIR}/.ssh/ /home/${USER}/.ssh \
  && ln -s ${GIT_CONFIG_DIR}/.gitconfig /home/${USER}/.gitconfig \
  && chown -R ${USER}:${GROUP} ${GIT_CONFIG_DIR}

# Prepare repo directory
ONBUILD RUN mkdir -p ${REPO_DIR} \
  && chown -R ${USER}:${GROUP} ${REPO_DIR}

ONBUILD VOLUME ${GIT_CONFIG_DIR}

ENTRYPOINT ["sh", "-c"]

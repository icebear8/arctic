ARG USER=Ahab
ARG GROUP=Ahab
ARG UID=1000
ARG GID=1000
ARG REPO_DIR=/opt/repo
ARG BASE_IMG_VERSION=3.10.1-r2-onbuild

FROM icebear8/gitrepoutils:${BASE_IMG_VERSION}
MAINTAINER Ponder Bear <ponder.bear@protonmail.com>

ENV USER=${USER}

# Repo settings and paths
VOLUME ${REPO_DIR}
WORKDIR ${REPO_DIR}

ENTRYPOINT ["git"]

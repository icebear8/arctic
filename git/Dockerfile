ARG USER=Ahab
ARG GROUP=Ahab
ARG UID=1000
ARG GID=1000
ARG REPO_DIR=/opt/repo

ARG CPU_ARCH=
ARG BASE_IMG_VERSION=3.10.3-r1-onbuild
FROM icebear8/gitrepoutils:${BASE_IMG_VERSION}${CPU_ARCH}
MAINTAINER Ponder Bear <ponder.bear@protonmail.com>

ENV USER=${USER}

# Repo settings and paths
VOLUME ${REPO_DIR}
WORKDIR ${REPO_DIR}

ENTRYPOINT ["git"]

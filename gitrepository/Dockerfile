FROM alpine:3.8
MAINTAINER Dominik Ebert <dominik.ebert@zuehlke.com>

ARG user=Ahab
ARG group=Ahab
ARG uid=1000
ARG gid=1000

ENV UTILS_DIR=/opt/utils
ENV APP_LAUNCHER=${UTILS_DIR}/setupRepoAccess.sh

ENV REPO_DIR=/opt/repo/
ENV REPO_URL=

RUN apk update && apk add --no-cache \
  git \
  openssh-client \
  openssh-keygen
  
RUN addgroup -g ${gid} ${group} && \
    adduser -u ${uid} -G ${group} -D ${user}
    
# Add known hosts
COPY resources/known_hostsGithub /home/${user}/.ssh/known_hosts

# Add utils
RUN mkdir -p ${UTILS_DIR}
COPY utils/* ${UTILS_DIR}/

# Access for the user
RUN mkdir ${REPO_DIR}
RUN chown -R ${user}:${group} ${REPO_DIR}
RUN chown -R ${user}:${group} /home/${user}
RUN chmod -R 755 ${UTILS_DIR}

USER ${user}
WORKDIR ${REPO_DIR}

VOLUME ${REPO_DIR}
  
ENTRYPOINT ["sh", "-c"]

CMD ["sh ${APP_LAUNCHER}"]

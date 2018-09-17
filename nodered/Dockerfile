FROM alpine:3.8
MAINTAINER Dominik Ebert <dominik.ebert@zuehlke.com>

ARG user=pan
ARG group=pan
ARG uid=1000
ARG gid=1000

ENV APP_DIR=/usr/src/node-red
ENV DATA_DIR=/data

# Environment variable holding file path for flows configuration
ENV FLOWS=flows.json
ENV NODE_PATH=${APP_DIR}/node_modules:${DATA_DIR}/node_modules

# Default arguments for service execution
ENV SERVICE_ARGS="--userDir ${DATA_DIR} -v ${FLOWS}"

RUN apk update && apk add --no-cache \
  nodejs \
  nodejs-npm
  
RUN addgroup -g ${gid} ${group} && \
    adduser -u ${uid} -G ${group} -D ${user}
  
# Home directory for Node-RED application source code.
RUN mkdir -p ${APP_DIR}

# User data directory, contains flows, config and nodes.
RUN mkdir ${DATA_DIR}

WORKDIR ${APP_DIR}

# Install node-red
RUN npm install -g --unsafe-perm node-red

# Add node-red user so we aren't running as root.
RUN chown -R ${user}:${group} ${DATA_DIR} && \
    chown -R ${user}:${group} ${APP_DIR}

USER ${user}

# Port and data settings
EXPOSE 1880
VOLUME ${DATA_DIR}

ENTRYPOINT ["sh", "-c"]

CMD ["node-red ${SERVICE_ARGS}"]

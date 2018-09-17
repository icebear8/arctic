FROM alpine:3.8
MAINTAINER Dominik Ebert <dominik.ebert@zuehlke.com>

ARG user=boxer
ARG group=boxer
ARG uid=1000
ARG gid=1000

ENV DATA_DIR=/data

# Default arguments for service execution
ENV SERVICE_ARGS="--userDir ${DATA_DIR}"

RUN apk update && apk add --no-cache \
  nodejs \
  nodejs-npm
  
RUN addgroup -g ${gid} ${group} && \
    adduser -u ${uid} -G ${group} -D ${user}
  
# Install node-red
RUN npm install -g --unsafe-perm node-red
  
# Directory for storing the data
RUN mkdir -p ${DATA_DIR}

# Add node-red user so we aren't running as root.
RUN chown -R ${user}:${group} ${DATA_DIR}

USER ${user}

# Port and data settings
EXPOSE 1880
VOLUME ${DATA_DIR}

ENTRYPOINT ["sh", "-c"]

CMD ["node-red ${SERVICE_ARGS}"]

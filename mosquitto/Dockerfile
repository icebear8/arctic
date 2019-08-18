ARG BASE_IMG_VERSION=3.10.1
FROM alpine:${BASE_IMG_VERSION}
MAINTAINER Ponder Bear <ponder.bear@protonmail.com>

# User definition
ARG USER=Ahab
ARG GROUP=Ahab
ARG UID=1000
ARG GID=1000

# Environment variables for the service
ENV SERVICE_ARGS=

RUN apk update && apk add --no-cache \
  mosquitto=1.6.3-r0 \
  mosquitto-clients=1.6.3-r0 \
  && apk del --purge

# Create user
RUN addgroup -g ${GID} ${GROUP} \
  && adduser -u ${UID} -G ${GROUP} -D ${USER}

USER ${USER}
EXPOSE 1883

ENTRYPOINT ["sh", "-c"]
CMD ["mosquitto ${SERVICE_ARGS}"]

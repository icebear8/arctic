FROM alpine:3.7
MAINTAINER Dominik Ebert <dominik.ebert@zuehlke.com>

ENV SERVICE_ARGS=

RUN apk update && apk add --no-cache \
  mosquitto \
  mosquitto-clients

EXPOSE 1883
  
ENTRYPOINT ["sh", "-c"]

CMD ["mosquitto ${SERVICE_ARGS}"]

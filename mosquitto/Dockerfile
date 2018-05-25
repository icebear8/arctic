FROM alpine:3.7
MAINTAINER Dominik Ebert <dominik.ebert@zuehlke.com>

RUN apk update && apk add --no-cache \
  mosquitto \
  mosquitto-clients

ENV SERVICE_ARGS=-h
  
ENTRYPOINT ["sh", "-c"]

CMD ["mosquitto ${SERVICE_ARGS}"]

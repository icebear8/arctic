FROM alpine:3.9

MAINTAINER Ponder Bear <ponder.bear@protonmail.com>

ARG USER=Ahab
ARG GROUP=Ahab
ARG UID=1000
ARG GID=1000

# Denonservice configuration
ENV DENON_HOST=
ENV CON_TIMEOUT=
ENV LOG_LEVEL=ERROR

ENV APP_DIR=/opt/denonService

RUN apk add --no-cache \
  python3

RUN pip3 install flask

# Create user
RUN addgroup -g ${GID} ${GROUP} \
    && adduser -u ${UID} -G ${GROUP} -D ${USER}


RUN mkdir -p ${APP_DIR}

COPY ./DenonControlService /${APP_DIR}/

RUN chown -R ${USER} ${APP_DIR}

USER ${USER}

EXPOSE 5000

ENTRYPOINT ["sh", "-c"]
CMD ["python3 ${APP_DIR}/DenonControlService.py --host=${DENON_HOST} --log=${LOG_LEVEL} --timeout=${CON_TIMEOUT}"]

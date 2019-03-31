FROM alpine:3.9
MAINTAINER Cheshire Lynx <cheshire.lynx@protonmail.com>

ARG USER=Ahab
ARG GROUP=Ahab
ARG UID=1000
ARG GID=1000

# Denonservice configuration
ENV SERVICE_ARGS=

ENV APP_DIR=/opt/deononService

RUN apk add --no-cache \
  git \
  python3
  
RUN pip3 install flask

# Create user
RUN addgroup -g ${GID} ${GROUP} \
    && adduser -u ${UID} -G ${GROUP} -D ${USER}
    

RUN mkdir -p ${APP_DIR}

COPY ./DenonControlService/DenonControlService /${APP_DIR}/

RUN chown -R ${USER} ${APP_DIR}

USER ${USER}
  
EXPOSE 5000
  
ENTRYPOINT ["sh", "-c"]
CMD ["python3 ${APP_DIR}/DenonControlService.py ${SERVICE_ARGS}"]
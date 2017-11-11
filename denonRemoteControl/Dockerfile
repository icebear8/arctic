FROM alpine:3.4
MAINTAINER Dominik Ebert <doe@zuehlke.com>

ARG user=PeterPan
ARG app_dir=/service

RUN apk add --no-cache \
  git \
  python3
  
RUN pip3 install flask

RUN adduser -S -D ${user}
RUN mkdir -p ${app_dir}

COPY ./DenonControlService/DenonControlService/* /${app_dir}/

RUN chown -R ${user} ${app_dir}

USER ${user}
  
EXPOSE 5000
  
CMD ["python3", "/service/DenonControlService.py", "SERVICE"]
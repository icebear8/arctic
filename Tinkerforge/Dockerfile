FROM alpine:3.7
MAINTAINER Dominik Ebert <dominik.ebert@zuehlke.com>

ARG app_dir=/var/tinkerforge

RUN apk update && apk add --no-cache \
  git \
  libusb-dev \
  make \
  pkgconfig \
  python3 \
  py-pip
  
RUN mkdir -p ${app_dir}
WORKDIR ${app_dir}

RUN git clone https://github.com/Tinkerforge/brickd ${app_dir}/daemon
WORKDIR ${app_dir}/daemon/src
RUN git clone https://github.com/Tinkerforge/daemonlib
WORKDIR ${app_dir}/daemon/src/brickd
RUN make
RUN make install
  
CMD ["/bin/bash"]

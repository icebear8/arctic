FROM alpine:3.8
MAINTAINER Dominik Ebert <dominik.ebert@zuehlke.com>

ENV UTILS_DIR=/opt/utils
ENV REPO_URL=

RUN apk update && apk add --no-cache \
  git \
  openssh-client \
  openssh-keygen
  
# Add utils
RUN mkdir -p ${UTILS_DIR}
COPY utils/* ${UTILS_DIR}/

ENTRYPOINT ["sh", "-c"]

CMD [""]

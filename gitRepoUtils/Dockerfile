FROM alpine:3.8
MAINTAINER Dominik Ebert <dominik.ebert@zuehlke.com>

ENV GIT_UTILS_DIR=/opt/utils/git
ENV REPO_URL=

RUN apk update && apk add --no-cache \
  git \
  openssh-client \
  openssh-keygen
  
# Add utils
RUN mkdir -p ${GIT_UTILS_DIR}
COPY utils/* ${GIT_UTILS_DIR}/

ENTRYPOINT ["sh", "-c"]
CMD [""]

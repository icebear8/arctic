#!/bin/sh

if ! [[ -z "${CONTENT_REPO_URL}" ]]; then
  rm -rf ${CONTENT_DIR}
  git clone --depth 1 ${CONTENT_REPO_URL} ${CONTENT_DIR}
fi

php-fpm5
nginx -g "daemon off;"

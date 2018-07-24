#!/bin/sh

if ! [[ -z "${CONTENT_REPO_URL}" ]]; then
  rm -rf ${APP_DIR}/user/pages/*
  git clone --depth 1 ${CONTENT_REPO_URL} ${APP_DIR}/user/
fi

php-fpm5
nginx -g "daemon off;"

#!/bin/sh

if ! [[ -z "${CONTENT_REPO_URL}" ]]; then
  git clone --depth 1 ${CONTENT_REPO_URL} ${CONTENT_DIR}
  rm -rf ${APP_DIR}/grav/user
  ln -s ${CONTENT_DIR}/public/user ${APP_DIR}/grav/user
fi

php-fpm5
nginx -g "daemon off;"

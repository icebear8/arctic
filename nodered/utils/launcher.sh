#!/bin/sh

if [ ! -f ~/.ssh/id_rsa ]; then
  sh ${GIT_UTILS_DIR}/reinitKey.sh
  sh ${GIT_UTILS_DIR}/printPublicKey.sh
  sh ${GIT_UTILS_DIR}/initGitUser.sh
fi

node-red ${SERVICE_ARGS}

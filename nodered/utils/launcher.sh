#!/bin/sh

if [ ! -f ~/.ssh/id_rsa ]; then
  sh ${GIT_HELPERS_DIR}/reinitKey.sh
  sh ${GIT_HELPERS_DIR}/printPublicKey.sh
  sh ${GIT_HELPERS_DIR}/initGitUser.sh
fi

node-red ${SERVICE_ARGS}

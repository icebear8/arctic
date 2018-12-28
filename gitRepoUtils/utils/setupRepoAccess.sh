#!/bin/sh

# First startup, create new RSA key and setup git user
if [ ! -f ~/.ssh/id_rsa ]; then
  sh ${GIT_HELPERS_DIR}/reinitKey.sh
  sh ${GIT_HELPERS_DIR}/printPublicKey.sh
  sh ${GIT_HELPERS_DIR}/initGitUser.sh
fi

# At every start, remove and clone the repo
sh ${GIT_HELPERS_DIR}/repoClone.sh

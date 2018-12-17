#!/bin/sh

# First startup, create new RSA key and setup git user
if [ ! -f ~/.ssh/id_rsa ]; then
  sh ${GIT_UTILS_DIR}/reinitKey.sh
  sh ${GIT_UTILS_DIR}/printPublicKey.sh
  sh ${GIT_UTILS_DIR}/initGitUser.sh
fi

# At every start, remove and clone the repo
sh ${GIT_UTILS_DIR}/repoClone.sh

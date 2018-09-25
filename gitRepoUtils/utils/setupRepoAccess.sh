#!/bin/sh

# First startup, create new RSA key and setup git user
if [ ! -f ~/.ssh/id_rsa ]; then
  sh ${UTILS_DIR}/initKey.sh
  sh ${UTILS_DIR}/printKey.sh
  sh ${UTILS_DIR}/initGitUser.sh
fi

# At every start, remote and clone the repo
sh ${UTILS_DIR}/repoClone.sh

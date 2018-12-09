#!/bin/sh

if ! [[ -z "${REPO_URL}" ]]; then
  sh ${GIT_UTILS_DIR}/setupRepoAccess.sh
fi

nginx -g "daemon off;"

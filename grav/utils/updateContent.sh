#!/bin/sh

if ! [[ -z "${CONTENT_REPO_URL}" ]]; then
  # Only update if there is a repository available
  echo "Start update"
  date

  cd ${CONTENT_DIR}
  git pull --rebase origin master

  # Wait for all processes to be finished
  wait

  echo "Update done"

fi

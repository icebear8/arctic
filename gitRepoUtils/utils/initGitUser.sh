#!/bin/sh

USER=$(whoami)
CONFIG_FILE=${GIT_CONFIG_DIR}/.gitconfig

touch ${CONFIG_FILE} && \
  echo "[user]" >> ${CONFIG_FILE} && \
  echo "  name = ${USER}" >> ${CONFIG_FILE} && \
  echo "  email = ${USER}@container" >> ${CONFIG_FILE}

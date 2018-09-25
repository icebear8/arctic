#!/bin/sh

USER=$(whoami)

touch /home/${USER}/.gitconfig && \
  echo "[user]" >> /home/${USER}/.gitconfig && \
  echo "  name = ${USER}" >> /home/${USER}/.gitconfig && \
  echo "  email = ${USER}@container" >> /home/${USER}/.gitconfig

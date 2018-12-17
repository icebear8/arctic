#!/bin/sh

# If remote repo exists, clean local repo and clone remote
git ls-remote --exit-code ${REPO_URL}
if test $? = 0; then
  rm -rf ${REPO_DIR}/*
  rm -rf ${REPO_DIR}/.git
  mkdir -p ${REPO_DIR}
  git clone --depth 1 --no-single-branch ${REPO_URL} ${REPO_DIR}
fi

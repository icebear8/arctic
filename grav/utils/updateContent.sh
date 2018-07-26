#!/bin/sh

cd ${CONTENT_DIR}
git pull --rebase origin master

# Wait for all processes to be finished
wait

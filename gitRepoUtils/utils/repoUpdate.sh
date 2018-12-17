#!/bin/sh

git pull --rebase origin master

# Wait for all processes to be finished
wait

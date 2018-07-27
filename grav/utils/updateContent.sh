#!/bin/sh

# Only update if there is a repository available
echo "Start update"
date

cd /var/www/content
git pull --rebase origin master

# Wait for all processes to be finished
wait

echo "Update done"

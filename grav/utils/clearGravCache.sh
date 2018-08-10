#!/bin/sh

cd /var/www/grav
php5 ./bin/grav clearcache

# Wait for all processes to be finished
wait

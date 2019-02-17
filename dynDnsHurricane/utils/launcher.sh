#!/bin/sh

# Execute the script periodically
while [ true ]
do
  ${APP_DIR}/detectUpdateIp.sh
  sleep ${LOC_EXECUTION_PERIOD}
done

#!/bin/sh

IFS=',' read -ra ADDR <<< "$APP_CONFIG_ARGUMENT_LIST"
for i in "${ADDR[@]}"; do
    echo "$i" >> /etc/ddclient/ddclient.conf
done

# Run the application with the startup arguments
${MAIN_APP_DIR}/${APP_NAME} ${APP_STARTUP_ARGUMENTS}
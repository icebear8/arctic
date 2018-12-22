#!/bin/sh

# Add arguments to config file
cp -f /etc/ddclient/ddclient_source.conf ${APP_CONFIG_DIR}/ddclient.conf
for arg in $APP_CONFIG_ARGUMENT_LIST; do
  echo $arg >> /etc/ddclient/ddclient.conf
done

# Run the application with the startup arguments
${MAIN_APP_DIR}/${APP_NAME} ${APP_STARTUP_ARGUMENTS}

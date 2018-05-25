#! /bin/bash

# Service arguments
SERVICE_ARGS='--help'

CONFIG_FILE="${CONFIG_DIR}/launch.cfg"
if [ -f "${CONFIG_FILE}" ]; then
  source ${CONFIG_FILE}
fi

echo "python3 brick-mqtt-proxy.py ${SERVICE_ARGS}"
python3 brick-mqtt-proxy.py ${SERVICE_ARGS}

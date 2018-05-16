#! /bin/bash

# Brick deamon connection settings
BRICKD_HOST=localhost
BRICKD_PORT=4223

# mqtt host connection settings
BROKER_HOST=localhost
BROKER_PORT=1883

CONFIG_FILE="/var/tinkerforge/config/launch.cfg"
if [ -f "${CONFIG_FILE}" ]; then
  source ${CONFIG_FILE}
fi

mosquitto -d
echo "python3 brick-mqtt-proxy.py --brickd-host ${BRICKD_HOST} --brickd-port ${BRICKD_PORT} --broker-host ${BROKER_HOST} --broker-port ${BROKER_PORT}"
python3 brick-mqtt-proxy.py --brickd-host ${BRICKD_HOST} --brickd-port ${BRICKD_PORT} --broker-host ${BROKER_HOST} --broker-port ${BROKER_PORT}

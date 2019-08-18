# Mosquitto
[Mosquitto](https://mosquitto.org/) is an open source implementation of a server for version 5.0, 3.1.1, and 3.1 of the MQTT protocol. It also includes a C and C++ client library, and the mosquitto_pub and mosquitto_sub utilities for publishing and subscribing.

##  Changelog
* mosquitto:1.6.3-r3, Alpine v3.10.1 with mosquitto v1.6.3

# Usage
`docker run -p 1883:1883 icebear8/mosquitto`

##  Environment Variables

| Variable        | Description |
|-                |-            |
| SERVICE_ARGS    | Arguments for the mosquitto service at startup |

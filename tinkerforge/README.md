# Tinkerforge
[Tinkerforge MQTT](https://www.tinkerforge.com/en/doc/Software/API_Bindings_MQTT.html) allows to control Bricks and Bricklets using the MQTT protocol.
This image does only contain the Tinkerforge MQTT translation proxy.
It does **NOT** contain an MQTT broker or Tinkerforge daemon.

##  Changelog
* tinkerforge:2.0.6-r1, Tinkerforge MQTT translation proxy v2.0.6

# Usage
`docker run icebear8/tinkerforge`

##  Environment Variables

| Variable        | Description |
|-                |-            |
| SERVICE_ARGS    | Arguments for the Tinkerforge MQTT proxy service at startup |

##  Connect to Daemon and Broker
The connection to the MQTT broker and the Tinkerforge daemon are provided by the environment variable.
The settings for host accept IPs, host names and URLs.
The Tinkerforge WiFi module can directly be accessed as host.

`docker run -e SERVICE_ARGS='--ipcon-host <tinkerforgeHost> --broker-host <mqttBrokerHost>' icebear8/tinkerforge`

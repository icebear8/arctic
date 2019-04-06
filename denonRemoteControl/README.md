# Supported tags and respective `Dockerfile` links
* 0.6-r1: Proper setup and allow configuration with environment variables
* 0.5-b3: Obsolete

# Denon service
Denon service is a basic Python script to access the TCP interface of Denon receivers.
It provides a REST based interface to interact with the Denon receivers.

# Usage
The service has to share the network interface with the host for proper usage.
Otherwise Bubble UPnP Server will not detect the media libraries and renderers within the network without additional network configuration.
Even if the Rest API is used, the Bubble UPnP Server is started automatically at the container start up.

`docker run -p 5000:5000 icebear8/denonservice:latest`

## Configuration
The Denon service settings are configurable with environment variables.

| Argument    | Default     | Description |
|-            |-            |-            |
| DENON_HOST  | 192.168.0.0 | IP, hostname or URL of the Denon receiver to connect (e.g. 192.168.0.42 or mydenon.local, default: 192.168.0.0)  |
| LOG_LEVEL   | ERROR       | [DEBUG, INFO, WARNING, ERROR, CRITICAL] (default: ERROR)  |
| CON_TIMEOUT | 300         | Idle timeout in seconds to close the Denon TCP connection (default: 300 seconds)  |

`docker run -p 80:5000 -e "DENON_HOST=192.168.0.42" icebear8/denonservice:latest`

## Rest API
The rest service is running on port 5000.
In case REST request occurs, 'Denon service' tries to connect to the receiver (TCP connection).
If the service is idle for a specific time (default 300 Seconds) it disconnects the TCP connection.

Rest API supports:

* `GET <host>/volume`: Gets the current volume level
* `GET <host>/power`: Gets the current power level
* `PUT <host>/power/<cmd>`: Sets the power. Accepted values: `on`, `standby`
* `PUT <host>/start`: Starts the receiver and plays the first favorite item
* `PUT <host>/startVolume/<volume>`: Starts the receiver with volume level `<volume>` and plays the first favorite item
* `PUT <host>/next`: Switches to the next favorite item
* `GET <host>/command?cmd=`: Wildcard, any command supported by the Denon receiver can be sent. Also works as 'PUT' or 'POST'

To control the connection to the receiver:
* `GET <host>/connection`: Gets the TCP connection state of the 'Denon service' to the receiver.
* `PUT <host>/connection/<command>`: Requests to change the connection state of 'Denon service' to the receiver. Accepted values: `connect`, `disconnect`



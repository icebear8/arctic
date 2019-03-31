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
The environment variable `SERVICE_ARGS` is used to configure the Denon service.

| Argument  | Description |
|-          |-            |
| -s        | Denon service is started as service in an endless loop. |
| --host=   | IP, hostname or URL of the Denon receiver to connect    |

`docker run -p 80:5000 -e "SERVICE_ARGS=-s --host=192.168.1.99" icebear8/denonservice/latest`

## Rest API
The rest service is running on port 5000.
In case REST request occures, 'Denon service' tries to connect to the receiver (TCP connection).
If the service is idle for a specific time (default 300 Seconds) it disconnects the TCP connection.

Rest API supports:

* `GET <host>/volume`: Gets the current volume level
* `GET <host>/power`: Gets the current power level
* `PUT <host>/power/<cmd>`: Sets the power. Accepted values: `on`, `standby`
* `PUT <host>/start`: Starts the receiver with volume level 28 and plays the first favorite item
* `PUT <host>/startVolume/<volume>`: Starts the receiver with voluem level `<volume>` and plays the first favorite item
* `PUT <host>/next`: Switches to the next favorite item
* `GET <host>/command?cmd=`: Wildcard, any command supported by the Denon receiver can be sent. Also works as 'PUT' or 'POST'

To control the connection to the receiver:
* `GET <host>/connection`: Gets the TCP connection state of the 'Denon service' to the receiver.
* `PUT <host>/connection/<command>`: Requests to change the connection state of 'Denon service' to the receiver. Accepted values: `connect`, `disconnect`



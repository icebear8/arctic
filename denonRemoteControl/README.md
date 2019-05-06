# Change log
* 0.8-r3: Introduce 'playing' and 'source' requests (changed 'line' request)
* 0.8-r2: Improve connection handling
* 0.8-r1: Throttle NSE messages (2 seconds)
* 0.7-r1: Improved REST API functionality
  - Additional commands (volume, power, display)
  - Improved REST response values
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
| DENON_HOST  | 192.168.0.0 | IP, hostname or URL of the Denon receiver to connect (e.g. 192.168.0.42 or mydenon.local) |
| LOG_LEVEL   | ERROR       | [DEBUG, INFO, WARNING, ERROR, CRITICAL] |
| CON_TIMEOUT | 300         | Idle timeout in seconds to close the Denon TCP connection |

`docker run -p 80:5000 -e "DENON_HOST=192.168.0.42" icebear8/denonservice:latest`

## Rest API
The rest service is running on port 5000.
In case REST request occurs, 'Denon service' tries to connect to the receiver (TCP connection).
If the service is idle for a specific time (default 300 Seconds) it disconnects the TCP connection.

Rest API supports:

* `GET <host>/volume`: Gets the current volume level
* `PUT <host>/volume/<cmd>`: Sets the volume. Accepted values: `up`, `down`, <volume> as decimal
* `GET <host>/power`: Gets the current power level
* `PUT <host>/power/<cmd>`: Sets the power. Accepted values: `on`, `standby`
* `GET <host>/display/lines`: Gets the lines 0..8 from the display
* `GET <host>/display/line/<index>`: Gets a specific display line. Accepted values: <line> as decimal (0..8)
* `GET <host>/playing/<id>`: Gets the information about whats currently playing. Accepted values: `album`, `artist`, `title`
* `GET <host>/source`: Gets the current selected source
* `PUT <host>/source/<id>`: Sets the source. Accepted values:
  - `TUNER`, `DVD`, `BD`, `TV`, `SATCBL`, `MPLAY`, `GAME`, `AUX1`, `NET`, `SPOTIFY`, `FLICKR`, `FAVORITES`, `IRADIO`, `SERVER`, `USBIPOD`
  - North America only: `PANDORA`, `SIRIUSXM`
  - Select and start playback: `USB` (USB), `IPD` (iPod),`IRP` (internet radio), `FVP` (favorites)
* `GET <host>/surround`: Gets the current surround mode
* `PUT <host>/surround/<mode>`: Sets the surround mode, depends on the current listening mode. Accepted values:
  - `MOVIE`, `MUSIC`, `GAME`, `DIRECT`, `STEREO`, `STANDARD`, `DOLBY_DIGITAL`, `DTS SUROUND`
  - `MCH STEREO`, `ROCK ARENA`, `JAZZ CLUB`, `MONO MOVIE`, `MATRIX`, `VIDEO`, `VIRTUAL`
  - North America only: `PURE_DIRECT`
* `PUT <host>/start`: Starts the receiver and plays the first favorite item
* `PUT <host>/startVolume/<volume>`: Starts the receiver with volume level `<volume>` and plays the first favorite item
* `PUT <host>/next`: Switches to the next favorite item
* `GET <host>/command?cmd=`: Wildcard, any command supported by the Denon receiver can be sent. Also works as 'PUT' or 'POST'

To control the connection to the receiver:
* `GET <host>/connection`: Gets the TCP connection state of the 'Denon service' to the receiver.
* `PUT <host>/connection/<command>`: Requests to change the connection state of 'Denon service' to the receiver. Accepted values: `connect`, `disconnect`

## Web Demo
For demonstration purpose there is a simple website which accesses the Denon service REST API.
Call `index.html` to use and test basic commands.
The recommendation is to build a separate website and only use the REST API of the Denon service.

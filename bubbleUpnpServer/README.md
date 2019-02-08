# Supported tags and respective `Dockerfile` links
* 0.9-u31-r1: Update to Bubble UPnP Server 0.9 update 31
* 0.9-u30-r4: Fixed missing startup parameters
* 0.9-u30-r3: Improved tear down of the Bubble UPnP Service
* 0.9-u30-r2: Add a rest api to start/stop the Bubble UPnP Server
* 0.9-u30-r1: Basic Bubble UPnP Server

The image tag identifies the Bubble UPnP Server version plus the revision.

# Bubble UPnP Server
The Bubble UPnP server allows to play media from a media library on a renderer within the network.
The Bubble UPnP App can be used as a control point.
See: [Bubble UPnP Server](http://www.bubblesoftapps.com/bubbleupnpserver/)

The images are setup to run a specific Bubble UPnP Server version.
The auto update feature is disabled by default.

# Usage
The service has to share the network interface with the host for proper usage.
Otherwise Bubble UPnP Server will not detect the media libraries and renderers within the network without additional network configuration.
Even if the Rest API is used, the Bubble UPnP Server is started automatically at the container start up.

`docker run -p 58050:58050 -p 58052:58052 --net=host icebear8/bubbleupnpserver`

## Configuration
By default the server is started without logging and auto update is disabled (server start arguments: `-nologfile -logLevel SEVERE -disableAutoUpdate`). The arguments for the server can be overwritten with the environment variable `SERVICE_ARGS`.

`docker run -p 58050:58050 -p 58052:58052 --net=host -e SERVICE_ARGS='-logLevel INFO' icebear8/bubbleupnpserver`

## Rest API
The rest service is running on port 58052 and allows to start/stop the BubbleUPnP Server.
The rest API was introduced to terminate the Bubble UPnP Service when it is not used because it prevented the NAS from standby mode.
Rest API supports:

* `GET <host>:58052/service`: Gets the state of the service ('running' or 'stopped')
* `PUT <host>:58052/service/start`: Starts the Bubble UPnP Server
* `PUT <host>:58052/service/stop`: Stops the Bubble UPnP Server (kills the process)

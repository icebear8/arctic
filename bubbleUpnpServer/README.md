# Supported tags and respective `Dockerfile` links
* 0.9-u30-r1, latest [(bubbleUpnpServer/Dockerfile)](https://github.com/icebear8/arctic/blob/bubbleupnpserver/0.9-u30-r1/bubbleUpnpServer/Dockerfile)

The image tag identifies the Bubble UPnP Server version.

# Bubble UPnP Server
The Bubble UPnP server allows to play media from a media library on a renderer within the network. The Bubble UPnP App can be used as a control point. See: [Bubble UPnP Server](http://www.bubblesoftapps.com/bubbleupnpserver/)

The images are setup to run a specific Bubble UPnP Server version. The auto update feature is disabled by default.

# Usage
The service has to share the network interface with the host for proper usage. Otherwise Bubble UPnP Server will not detect the media libraries and renderers within the network without additional network configuration.

`docker run -p 58050:58050 --net=host icebear8/bubbleupnpserver`

## Configuration
By default the server is started without logging and auto update is disabled (server start arguments: `-nologfile -logLevel SEVERE -disableAutoUpdate`). The arguments for the server can be overwritten with the environment variable `SERVICE_ARGS`.

`docker run -p 58050:58050 --net=host -e SERVICE_ARGS='-logLevel INFO' icebear8/bubbleupnpserver`
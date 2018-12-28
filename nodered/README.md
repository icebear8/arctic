# Node-RED
[Node-RED](https://nodered.org/) flow-based programming for the Internet of Things

This image contains a basic installation of Node-RED.
The image is prepared to access remote git repositories as well.

##  Changelog
* icebear8/nodered:0.19.5-r2, Node-RED with remote git repository support


# Usage
`docker run -p 1880:1880 icebear8/nodered`

# Configuration and setup
* Use the built-in git support from Node-RED.
* At each container start a git user and ssh key is created if not available

##  Available volumes
| VOLUME            | Description |
|-                  |-            |
${APP_RUNTIME_DIR}  | Contains the Node-RED runtime configuration and data |
${GIT_CONFIG_DIR}   | Contains the git configuration and ssh keys |


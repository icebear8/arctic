# ddclient
[ddclient](https://github.com/ddclient/ddclient) is a Perl client used to update dynamic DNS entries for accounts on many dynamic DNS services.

This image is prepared to run ddclient with a custom configuration through a configuration file or with environment parameter configuration.

##  Changelog
* ddclient:3.9.0-r1, ddclient v3.9.0

# Usage
`docker run -e APP_CONFIG_ARGUMENT_LIST="use=web protocol=namecheap server=dynamicdns.park-your-domain.com login=mysite.com password=<secret> theHost" -e APP_STARTUP_ARGUMENTS="-daemon 3600 -foreground" ddclient`

# Configuration
The predefined configuration file defines to use an ssl connection for updating the IP.
Other configuration values can be added with the environment variables or directly within the configuration file.

## Environment Variables
APP_CONFIG_ARGUMENT_LIST:
The parameters of this environment variable are stored in the ddclient.conf file and used by the ddclient.

APP_STARTUP_ARGUMENTS:
The arguments of this environment variable are used as startup arguments for ddclient.

## Configuration File
As an alternative to the configuration with environment variables, the configuration directory is exposed as volume.
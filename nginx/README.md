# Nginx
[Nginx](https://www.nginx.com/) is a free, open-source, high-performance HTTP server and reverse proxy, as well as an IMAP/POP3 proxy server. Nginx is known for its high performance, stability, rich feature set, simple configuration, and low resource consumption.

This image contains everything to run Nginx with a basic configuration.
Additionally a link to a (private or public) git repository can be used to manage the maintain the nginx configuration files.

##  Changelog
* nginx:1.16.1-r2, Nginx 1.16.1
* nginx:1.16.1-r1, Nginx 1.16.1
* nginx:1.16.0-r4, Use GitRepoUtils base image with on build hooks
* nginx:1.16.0-r1, Update to Alpine 3.10.1, use Nginx 1.16.0
* nginx:0.11-r1, Updated to Alpine 3.9.4, use Nginx 1.14.2-r1
* nginx:0.10-r4, Update to base image icebear8/gitrepoutils:3.8-r2
* nginx:0.10-r3, Use icebear8/gitrepoutils:3.8-r1 as base image to access a git repo
* nginx:0.10-r2, Bugfix and update to alpine 3.8
* nginx:0.10-r1, Nginx with git repo support, config files can be managed on Github
* nginx:0.9, Basic nginx, configuration files with mapped volumes

# Usage
`docker run -p 8080:8080 icebear8/nginx`

# Setup Content on Github
The container supports managing the configuration on a Github repository.
See https://cloud.docker.com/repository/docker/icebear8/gitrepoutils/general for detailed usage instructions.

##  Configuration Structure
* Put the nginx configuration files to the path `nginx/config` in the repository
* Put the nginx website content files to the path `nginx/www` in the repository

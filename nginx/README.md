# Nginx
[Nginx](https://www.nginx.com/) is a free, open-source, high-performance HTTP server and reverse proxy, as well as an IMAP/POP3 proxy server. Nginx is known for its high performance, stability, rich feature set, simple configuration, and low resource consumption.

This image contains everything to run Nginx with a basic configuration.
Additionally a link to a (private or public) git repository can be used to manage the maintain the nginx configuration files.

# Usage
`docker run -p 8080:8080 icebear8/nginx`

# Setup Content on Github
The container supports managing the configuration on a Github repository.
See https://github.com/icebear8/gitRepoUtils for detailed usage instructions.

##  Configuration Structure
* Put the nginx configuration files to the path `nginx/config` in the repository
* Put the nginx website content files to the path `nginx/www` in the repository

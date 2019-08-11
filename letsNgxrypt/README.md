# LetsNgxrypt
[Nginx](https://www.nginx.com/) combined with [Let's Encrypt](https://letsencrypt.org/).

The Nginx part is based on [icebear8/nginx](https://cloud.docker.com/repository/docker/icebear8/nginx).

[Let's Encrypt](https://letsencrypt.org/) is a free, automated, and open Certificate Authority.
To enable HTTPS on a website, you need a certificate from a Certificate Authority such as Let's Encrypt.
This image uses [Lego](https://go-acme.github.io/lego/) to request certificates from Let's Encrypt.

This image contains everything to run Nginx with a basic configuration.
Additionally a link to a (private or public) git repository can be used to manage the maintain the Nginx configuration files.


##  Changelog
* letsngxrypt:0.1-r1, based on icebear8/nginx:1.16.0-r1 with Lego 2.6.0

# Usage
`docker run -p 8080:8080 icebear8/letsngxrypt`

# Setup Content on Github
The container supports managing the content and configuration on a Github repository.
See https://cloud.docker.com/repository/docker/icebear8/gitrepoutils/general for detailed usage instructions.

##  Configuration Structure
* Put the Nginx configuration files to the path `nginx/config` in the repository
* Put the Nginx website content files to the path `nginx/www` in the repository

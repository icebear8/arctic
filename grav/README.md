# Supported tags and respective `Dockerfile` links
* 1.4.6-r5, latest [(grav/Dockerfile)](https://github.com/icebear8/arctic/blob/grav/1.4.6-r5/grav/Dockerfile)

The image tag identifies the Grav version.

# Grav
[Grav](https://getgrav.org/) is a modern open source flat-file CMS and allows to manage website content with markdown files.

This image contains everything to run Grav within a docker container.
Nginx is set up to publish the Grav website.
Additionally a link to a (private or public) git repository can be used to manage the maintain the content.

# Usage
`docker run -p 8080:8080 icebear8/grav`

# Setup Content on Github
Currently only managing the content on Github is supported.

##  Folder Structure for Website Content
* Create the folder `web/user` in the repository with the website content
* The `user` folder corresponds with the `user` folder as documented by [Grav](https://getgrav.org/) and should contain the following subfolders
  * `accounts`, `config`, `data`, `pages`, `plugins`, `themes`
  * The content in markdown format of the website is stored in the `pages` folder

##  Repository URL

The environment variable `REPO_URL` defines the remote git repository which is used.
For this image the SSH should be used as the URL (git@github.com:<someRepository>) .

`docker run -p 80:8080 -d -e REPO_URL=git@github.com:<someRepository> --name grav icebear8/grav`

##  Key Management

* At first startup, the container creates a new private/public key pair
  * The scripts also try to clone the repository at each container start
  * This will fail as long as the public key is not added to the remote repository
* The public key is printed on the shell at the first startup
  * Use `docker logs grav` to print the log after the startup
  * Or use the command `docker exec grav /opt/utils/git/printPublicKey.sh` to print the public key
* Add the public key to your Github repository with the website content
  * Settings/Deploy keys/Add deploy key
  * Read access is enough for the website
* Clone the website content
  * Stop and start the container again
  * Or execute `docker exec grav /opt/utils/git/repoClone.sh`
  
##  Update at Runtime
* A php deploy script (`http://<yourUrl>/deploy.php`) is used to update the website content
* Calling the script will pull the latest changes from the remote repository

# Grav
[Grav](https://getgrav.org/) is a modern open source flat-file CMS and allows to manage website content with markdown files.

This image contains everything to run Grav within a docker container.
Nginx is set up to publish the Grav website.
Additionally a link to a (private or public) git repository can be used to manage the maintain the content.

# Usage
`docker run -p 8080:8080 icebear8/grav`

# Setup Content on Github
The container supports managing the content on a Github repository.
See https://github.com/icebear8/gitRepoUtils for detailed usage instructions.

##  Folder Structure for Website Content
* Create the folder `web/user` in the repository with the website content
* The `user` folder corresponds with the `user` folder as documented by [Grav](https://getgrav.org/) and should contain the following subfolders
  * `accounts`, `config`, `data`, `pages`, `plugins`, `themes`
  * The content in markdown format of the website is stored in the `pages` folder

##  Update at Runtime
* A php deploy script (`http://<yourUrl>/deploy.php`) is used to update the website content
* Calling the script will pull the latest changes from the remote repository

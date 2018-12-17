#   Git Repo Utils

This image contains basic scripts to access a git repository.
This image may be used as base layer to build other services on top of it.

##  Changelog
* gitrepoutils:3.8-r1: Alpine 3.8, initial version

##  Usage
`docker run -e REPO_URL=git@github.com:<someRepository> --name nginx icebear8/gitrepoutils:latest`

##  Environment Variables

| Variable      | Description |
|-              |-            |
| REPO_URL      | The URL of the git repository |
| REPO_DIR      | The target location of the repository (clone) |
| GIT_UTILS_DIR | Location where the git repo utils scripts are located |
| GIT_KEY_DIR   | Location where the .ssh data is stored |

##  Git Repo Utils Scripts

| Script              | Description |
|-                    |-            |
| initGitUser.sh      | Creates the current user as the global git user with a fake mail address  |
| printPublicKey.sh   | Prints the current public key (if existing)
| reinitKey.sh        | Reinitializes the private/public key pair |
| repoClone.sh        | Clones the repository from `REPO_URL` into `REPO_DIR` |
| repoUpdate.sh       | Updates the repository from `REPO_URL`
| setupRepoAccess.sh  | Initializes the git user and the keys if no keys exist and tries to initially clone the repository  |

##  Usage in Docker Containers
Use the environment variable `REPO_URL` to link the container to a specific git repository.

* At first startup, the container creates a new private/public key pair
  * The scripts also try to clone the repository at each container start
  * This will fail as long as the public key is not added to the remote repository
* The variable `GIT_KEY_DIR` points to the location where the gitconfig and .ssh data is stored
  * A symlink from `~/.ssh` and `~/.gitconfig` 
* The public key is printed on the shell at the first startup
  * Use `docker logs grav` to print the log after the startup
  * Or use the command `docker exec grav /opt/gitUtils/printPublicKey.sh` to print the public key
* Add the public key to your Github repository with the website content
  * Settings/Deploy keys/Add deploy key
  * Read access is enough for the website
* Clone the website content
  * Stop and start the container again
  * Or execute `docker exec grav /opt/gitUtils/repoClone.sh`

##  Resources

known_hostsGithub: Public key identification of the Github host
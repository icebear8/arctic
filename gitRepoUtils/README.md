#   Git Repo Utils

This image contains basic scripts to access a git repository.
This image may be used as base layer to build other services on top of it.
The image is prepared to access a remote git repository.
On build hooks are used to setup the base image for a specific user

##  Changelog
* gitrepoutils:3.10.1-r2-onbuild: Alpine 3.10.1, on build hooks for user creation
* gitrepoutils:3.10.1-r1: Alpine 3.10.1
* gitrepoutils:3.10.0-r1: Alpine 3.10.0
* gitrepoutils:3.9.4-r1: Alpine 3.9.4, fix version of installed packages
* gitrepoutils:3.9-r1: Alpine 3.9
* gitrepoutils:3.8-r2: Alpine 3.8, renamed env variables and changed paths
* gitrepoutils:3.8-r1: Alpine 3.8, initial version

##  Usage
`docker run -e REPO_URL=git@github.com:<someRepository> --name nginx icebear8/gitrepoutils:latest`

## ONBUILD Hooks
The arguments for the ONBUILD arguments must be given before the `FROM` statement.
```
ARG USER=me
ARG GROUP=myself
ARG UID=6666
ARG GID=6666
ARG REPO_DIR=/opt/repo
FROM icebear8/gitrepoutils:latest
```

| ONBUILD ARG | Description                 |
|-            |-                            |
| USER        | User to be created and used |
| GROUP       | User group to be used       |
| UID         | The user id to be used      |
| GID         | The group id to be used     |
| REPO_DIR    | Working directory with the repository |

##  Environment Variables

| Variable        | Description |
|-                |-            |
| REPO_URL        | The URL of the remote git repository |
| REPO_DIR        | The local target location of the repository (clone) |
| GIT_HELPERS_DIR | Location where the git repo utils scripts are located |
| GIT_CONFIG_DIR  | Location where the git configuration and .ssh data is stored |

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

* At container startup, call `setupRepoAccess.sh` to
  * Create a new git user and private/public key pair if they do not exist
  * Try to clone the repository at each container start
  * This will fail as long as the public key is not added to the remote repository
* The variable `GIT_CONFIG_DIR` points to the location where the gitconfig and .ssh data is stored
  * A symlink from `~/.ssh` and `~/.gitconfig`
* The public key is printed on the shell at the first startup
  * Use `docker logs <container>` to print the log after the startup
  * Or use the command `docker exec <container> ${GIT_HELPERS_DIR}/printPublicKey.sh` to print the public key
* Add the public key to your Github repository with the website content
  * Settings/Deploy keys/Add deploy key
  * Read access is enough for most of the containers
* Clone the website content
  * Stop and start the container again
  * Or execute `docker exec <container> ${GIT_HELPERS_DIR}/repoClone.sh`

##  Resources
known_hostsGithub: Public key identification of the Github host

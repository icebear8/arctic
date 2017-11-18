// Uses the common library form 'https://github.com/icebear8/pipelineLibrary'

@Library('common-pipeline-library') _
  
def dockerStep = new icebear8.docker.buildSteps()
def tmpExtractor = new icebear8.docker.tempExtraction()

def projectSettings = readJSON text: '''{
  "dockerHub": {
    "user": "icebear8"
  },
  "repository": {
    "url": "https://github.com/icebear8/arctic.git",
    "credentials": "3bc30eda-c17e-4444-a55b-d81ee0d68981"
  },
  "dockerJobs": [
    {"imageName": "nginx",        "dockerfilePath": "./nginx" },
    {"imageName": "denonservice", "dockerfilePath": "./denonRemoteControl" },
    {"imageName": "grav",         "dockerfilePath": "./grav" }
  ]
}'''

node {
  properties([
    pipelineTriggers([cron('H 15 * * 2')]),
    buildDiscarder(logRotator(
      artifactDaysToKeepStr: '5', artifactNumToKeepStr: '5',
      numToKeepStr: '5', daysToKeepStr: '5'))
  ])
  
  def aBranch = "${repositoryUtils.currentBuildBranch()}"
  repositoryUtils.checkoutStage {
    stageName = 'Checkout'
    branchName = aBranch
    repoUrl = "${projectSettings.repository.url}"
    repoCredentials = "${projectSettings.repository.credentials}"
  }
  
  docker.withServer(env.DEFAULT_DOCKER_HOST_CONNECTION, 'default-docker-host-credentials') {
    try {
      stage("Build") {
        parallel tmpExtractor.setupBuildTasks(projectSettings)
      }
      stage("Push") {
        parallel tmpExtractor.setupPushTasks(projectSettings)
      }
    }
    finally {
      stage("Clean up") {
        parallel tmpExtractor.setupPostTasks(projectSettings)
      }
    }
  }
}

def isBuildRequired(isCurrentImageBranch) {
  if (isCurrentImageBranch == true) {
    return true
  }
  else if ((repositoryUtils.isStableBranch() == false) && (repositoryUtils.isReleaseBranch() == false)) {
    return true
  }
  
  return false
}

def isRebuildRequired() {
  if ((repositoryUtils.isLatestBranch() == true) || (repositoryUtils.isStableBranch() == true) || (repositoryUtils.isReleaseBranch() == true)) {
    return true
  }
  
  return false
}

def isPushRequired(isCurrentImageBranch) {
  
  if (((repositoryUtils.isReleaseBranch() == false) && (repositoryUtils.isStableBranch() == false)) || (repositoryUtils.isLatestBranch() == true)) {
    return true
  }
  else if ((isCurrentImageBranch == true) && ((repositoryUtils.isReleaseBranch() == true) || (repositoryUtils.isStableBranch() == true))) {
    return true
  }
  
  return false
}

def evaluateReleaseTag(releaseBranch, imageName) {
  def indexOfImage = releaseBranch.indexOf(imageName)
  
  if (indexOfImage < 0)
  {
    return null // exit if no valid release tag could be found
  }
  
  return releaseBranch.substring(indexOfImage + imageName.length() + 1) // +1 because of additional sign between image id and release tag
}

// Uses the common library form 'https://github.com/icebear8/pipelineLibrary'

@Library('common-pipeline-library') _

def dockerStep = new icebear8.docker.buildSteps()
def tmpExtractor = new icebear8.docker.tempExtraction()

def projectSettings = readJSON text: '''{
  "repository": {
    "url": "https://github.com/icebear8/arctic.git",
    "credentials": "3bc30eda-c17e-4444-a55b-d81ee0d68981"
  },
  "docker": {
    "hostConnection": env.DEFAULT_DOCKER_HOST_CONNECTION,
    "hostCredentials": 'default-docker-host-credentials',
    "user": "icebear8"
  }
  "dockerHub": {
    "user": "icebear8"
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

  repositoryUtils.checkoutCurrentBranch {
    stageName = 'Checkout'
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

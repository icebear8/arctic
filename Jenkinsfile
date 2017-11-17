node {
  @Library('common-pipeline-library') _
  def dockerStep = new icebear8.docker.buildSteps()

  def REPO_URL = 'https://github.com/icebear8/arctic.git'
  def REPO_CREDENTIALS = '3bc30eda-c17e-4444-a55b-d81ee0d68981'  
  def BUILD_PROPERTIES_FILE = "buildProperties.json"
  
  properties([
    pipelineTriggers([cron('H 15 * * 2')]),
    buildDiscarder(logRotator(
      artifactDaysToKeepStr: '5', artifactNumToKeepStr: '5',
      numToKeepStr: '5', daysToKeepStr: '5'))
  ])
  
  def buildProperties
  def buildTasks = [:]
  def pushTasks = [:]
  def postTasks = [:]
  
  stage("Checkout") {
    echo "Current branch: ${repositoryUtils.currentBuildBranch()}"

    checkout([$class: 'GitSCM', branches: [[name: "*/${repositoryUtils.currentBuildBranch()}"]],
      doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'CleanBeforeCheckout'], [$class: 'PruneStaleBranch']], submoduleCfg: [],
      userRemoteConfigs: [[credentialsId: "${REPO_CREDENTIALS}", url: "${REPO_URL}"]]])
  }

  stage("Setup build") {
    echo "Setup build"
    
    buildProperties = readJSON file: "${BUILD_PROPERTIES_FILE}"
    
    echo "Properties: ${buildProperties}"
    
    for(itJob in buildProperties.dockerJobs) {
      
      def isCurrentImageBranch = "${repositoryUtils.currentBuildBranch()}".contains("${itJob.imageName}")
      def imageId = "${buildProperties.dockerHub.user}/${itJob.imageName}"
      def localImageTag = "${env.BRANCH_NAME}_${env.BUILD_NUMBER}".replaceAll('/', '-')
      def localImageId = "${imageId}:${localImageTag}"

      if (isBuildRequired(isCurrentImageBranch, repositoryUtils.isStableBranch(), repositoryUtils.isReleaseBranch()) == true) {
        buildTasks[itJob.imageName] = dockerStep.buildImage(localImageId, itJob.dockerfilePath, isRebuildRequired(repositoryUtils.isLatestBranch(), repositoryUtils.isStableBranch(), repositoryUtils.isReleaseBranch()))
      }
      
      def remoteImageTag = dockerUtils.tagLocalBuild()
      
      if (repositoryUtils.isLatestBranch() == true) {
        remoteImageTag = dockerUtils.tagLatest()
      }
      else if (repositoryUtils.isStableBranch() == true) {
        remoteImageTag = dockerUtils.tagStable()
      }
      else if (repositoryUtils.isReleaseBranch() == true) {
        def releaseTag = evaluateReleaseTag(repositoryUtils.currentBuildBranch(), itJob.imageName)
        remoteImageTag = releaseTag != null ? releaseTag : dockerUtils.tagLatest()
      }
      
      if (isPushRequired(isCurrentImageBranch, repositoryUtils.isStableBranch(), repositoryUtils.isReleaseBranch(), repositoryUtils.isLatestBranch()) == true) {
        pushTasks[itJob.imageName] = dockerStep.pushImage(localImageId, remoteImageTag)
      }
      
      postTasks[itJob.imageName] = dockerStep.removeImage(imageId, localImageTag, remoteImageTag)
    }
  }
    
  docker.withServer(env.DEFAULT_DOCKER_HOST_CONNECTION, 'default-docker-host-credentials') {
    try {
      stage("Build") {
        parallel buildTasks
      }
      stage("Push") {
        parallel pushTasks
      }
    }
    finally {
      stage("Clean up") {
        parallel postTasks
      }
    }
  }
}

def isBuildRequired(isCurrentImageBranch, repositoryUtils.isStableBranch(), repositoryUtils.isReleaseBranch()) {
  if (isCurrentImageBranch == true) {
    return true
  }
  else if ((repositoryUtils.isStableBranch() == false) && (repositoryUtils.isReleaseBranch() == false)) {
    return true
  }
  
  return false
}

def isRebuildRequired(repositoryUtils.isLatestBranch(), repositoryUtils.isStableBranch(), repositoryUtils.isReleaseBranch()) {
  if ((repositoryUtils.isLatestBranch() == true) || (repositoryUtils.isStableBranch() == true) || (repositoryUtils.isReleaseBranch() == true)) {
    return true
  }
  
  return false
}

def isPushRequired(isCurrentImageBranch, repositoryUtils.isStableBranch(), repositoryUtils.isReleaseBranch(), repositoryUtils.isLatestBranch()) {
  
  if (((repositoryUtils.isReleaseBranch() == false) && (repositoryUtils.isStableBranch() == false)) || (repositoryUtils.isLatestBranch() == true)) {
    return true
  }
  else if ((isCurrentImageBranch == true) && ((repositoryUtils.isReleaseBranch() == true) || (repositoryUtils.isStableBranch() == true))) {
    return true
  }
  
  return false
}

def evaluateBuildBranch(defaultValue) {
  if (env.BRANCH_NAME != null) {
    return env.BRANCH_NAME
  }
  
  return defaultValue
}

def evaluateReleaseTag(releaseBranch, imageName) {
  def indexOfImage = releaseBranch.indexOf(imageName)
  
  if (indexOfImage < 0)
  {
    return null // exit if no valid release tag could be found
  }
  
  return releaseBranch.substring(indexOfImage + imageName.length() + 1) // +1 because of additional sign between image id and release tag
}

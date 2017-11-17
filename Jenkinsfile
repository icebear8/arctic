node {
  @Library('common-pipeline-library') _
  def dockerUtils = new docker.utils()

  def REPO_URL = 'https://github.com/icebear8/arctic.git'
  def REPO_CREDENTIALS = '3bc30eda-c17e-4444-a55b-d81ee0d68981'  
  def BUILD_PROPERTIES_FILE = "buildProperties.json"
  
  properties([
    pipelineTriggers([cron('H 15 * * 2')]),
    buildDiscarder(logRotator(
      artifactDaysToKeepStr: '5', artifactNumToKeepStr: '5',
      numToKeepStr: '5', daysToKeepStr: '5'))
  ])
  
  def currentBuildBranch = evaluateBuildBranch(repository.branchLatest())
  
  def buildProperties
  def buildTasks = [:]
  def pushTasks = [:]
  def postTasks = [:]
  
  stage("Checkout") {
    echo "Current branch: ${currentBuildBranch}"
    
    dockerUtils.helloPipelineLibrary()
    echo "Print the var: ${repository.branchLatest()}"

    checkout([$class: 'GitSCM', branches: [[name: "*/${currentBuildBranch}"]],
      doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'CleanBeforeCheckout'], [$class: 'PruneStaleBranch']], submoduleCfg: [],
      userRemoteConfigs: [[credentialsId: "${REPO_CREDENTIALS}", url: "${REPO_URL}"]]])
  }

  stage("Setup build") {
    echo "Setup build"
    
    def isLatestBranch = "${currentBuildBranch}".contains("${repository.branchLatest()}")
    def isReleaseBranch = "${currentBuildBranch}".contains("${repository.branchRelease()}")
    def isStableBranch = "${currentBuildBranch}".contains("${repository.branchStable()}")
    
    buildProperties = readJSON file: "${BUILD_PROPERTIES_FILE}"
    
    echo "Properties: ${buildProperties}"
    
    for(itJob in buildProperties.dockerJobs) {
      
      def isCurrentImageBranch = "${currentBuildBranch}".contains("${itJob.imageName}")
      def imageId = "${buildProperties.dockerHub.user}/${itJob.imageName}"
      def localImageTag = "${env.BRANCH_NAME}_${env.BUILD_NUMBER}".replaceAll('/', '-')
      def localImageId = "${imageId}:${localImageTag}"

      if (isBuildRequired(isCurrentImageBranch, isStableBranch, isReleaseBranch) == true) {
        buildTasks[itJob.imageName] = createDockerBuildStep(localImageId, itJob.dockerfilePath, isRebuildRequired(isLatestBranch, isStableBranch, isReleaseBranch))
      }
      
      def remoteImageTag = docker.tagLocalBuild()
      
      if (isLatestBranch == true) {
        remoteImageTag = docker.tagLatest()
      }
      else if (isStableBranch == true) {
        remoteImageTag = docker.tagStable()
      }
      else if (isReleaseBranch == true) {
        def releaseTag = evaluateReleaseTag(currentBuildBranch, itJob.imageName)
        remoteImageTag = releaseTag != null ? releaseTag : docker.tagLatest()
      }
      
      if (isPushRequired(isCurrentImageBranch, isStableBranch, isReleaseBranch, isLatestBranch) == true) {
        pushTasks[itJob.imageName] = createDockerPushStep(localImageId, remoteImageTag)
      }
      
      postTasks[itJob.imageName] = createRemoveImageStep(imageId, localImageTag, remoteImageTag)
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

def isBuildRequired(isCurrentImageBranch, isStableBranch, isReleaseBranch) {
  if (isCurrentImageBranch == true) {
    return true
  }
  else if ((isStableBranch == false) && (isReleaseBranch == false)) {
    return true
  }
  
  return false
}

def isRebuildRequired(isLatestBranch, isStableBranch, isReleaseBranch) {
  if ((isLatestBranch == true) || (isStableBranch == true) || (isReleaseBranch == true)) {
    return true
  }
  
  return false
}

def isPushRequired(isCurrentImageBranch, isStableBranch, isReleaseBranch, isLatestBranch) {
  
  if (((isReleaseBranch == false) && (isStableBranch == false)) || (isLatestBranch == true)) {
    return true
  }
  else if ((isCurrentImageBranch == true) && ((isReleaseBranch == true) || (isStableBranch == true))) {
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

def createDockerBuildStep(imageId, dockerFilePath, isRebuild) {
  def buildArgs = "${dockerFilePath}"
  
  if (isRebuild == true) {
    buildArgs = "--no-cache --rm ${dockerFilePath}"
  }

  return {
    stage("Build image ${imageId}") {
      echo "Build image: ${imageId} with dockerfile ${dockerFilePath}"
      docker.build("${imageId}", "${buildArgs}")
    }
  }
}

def createDockerPushStep(imageId, remoteTag) {
  return {
    stage("Push image ${imageId} to ${remoteTag}") {
      echo "Push image: ${imageId} to remote with tag ${remoteTag}"
      
      docker.image("${imageId}").push("${remoteTag}")
    }
  }
}

def createRemoveImageStep(imageId, localImageTag, remoteImageTag) {
return {
    stage("Remove image ${imageId}") {
      echo "Remove image: ${imageId}, tags: ${localImageTag}, ${remoteImageTag}"
      sh "docker rmi ${imageId}:${localImageTag}"
      sh "docker rmi ${imageId}:${remoteImageTag}"
    }
  }
}
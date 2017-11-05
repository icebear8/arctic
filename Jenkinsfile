node {
  def REPO_URL = 'https://github.com/icebear8/arctic.git'
  def REPO_CREDENTIALS = '3bc30eda-c17e-4444-a55b-d81ee0d68981'
  
  def BUILD_PROPERTIES_FILE = "buildProperties.json"

  def REPO_LATEST_BRANCH = 'master'
  def REPO_STABLE_BRANCH = 'stable'
  def REPO_RELEASE_BRANCH = 'release'
  
  def DOCKER_TAG_LATEST = 'latest'
  def DOCKER_TAG_STABLE = 'stable'
  
  def currentBuildBranch = evaluateBuildBranch(REPO_LATEST_BRANCH)
  
  def buildProperties
  def buildTasks = [:]
  def pushTasks = [:]
  
  stage("Checkout") {
    echo "Checkout branch: ${currentBuildBranch}"

    checkout([$class: 'GitSCM', branches: [[name: "*/${currentBuildBranch}"]],
      doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [],
      userRemoteConfigs: [[credentialsId: "${REPO_CREDENTIALS}", url: "${REPO_URL}"]]])
  }

  stage("Setup build") {
    echo "Setup build"
    def isLatestBranch = "${currentBuildBranch}".contains("${REPO_LATEST_BRANCH}")
    def remoteImageTag = DOCKER_TAG_LATEST
    
    buildProperties = readJSON file: "${BUILD_PROPERTIES_FILE}"
    
    echo "Properties: ${buildProperties}"
    
    for(itJob in buildProperties.dockerJobs) {
      def isReleaseBranch =
        "${currentBuildBranch}".contains("${itJob.imageName}") &&
        "${currentBuildBranch}".contains("${REPO_RELEASE_BRANCH}")

      def isStableBranch =
        "${currentBuildBranch}".contains("${itJob.imageName}") &&
        "${currentBuildBranch}".contains("${REPO_STABLE_BRANCH}")
      
      def localImageId = "${buildProperties.dockerHub.user}/${itJob.imageName}:${DOCKER_TAG_LATEST}"
      
      if (isStableBranch == true) {
        remoteImageTag = DOCKER_TAG_STABLE
      }
      else if (isReleaseBranch == true) {
        def releaseTag = evaluateReleaseTag(currentBuildBranch, itJob.imageName)
        remoteImageTag = releaseTag != null ? releaseTag : REPO_LATEST_BRANCH
      }
      
      if ((isLatestBranch == true) || (isStableBranch == true) || (isReleaseBranch == true)) {
        buildTasks[itJob.imageName] = createDockerBuildStep(localImageId, itJob.dockerfilePath)
      }

      if ((isLatestBranch == true) || (isStableBranch == true) || (isReleaseBranch == true)) {
        pushTasks[itJob.imageName] = createDockerPushStep(localImageId, remoteImageTag)
      }
    }
  }
    
  docker.withServer(env.DEFAULT_DOCKER_HOST_CONNECTION, 'default-docker-host-credentials') {
    stage("Build") {
      parallel buildTasks
    }
    stage("Push") {
      parallel pushTasks
    }
  }
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

def createDockerBuildStep(imageId, dockerFilePath) {
  return {
    stage("Build image ${imageId}") {
      echo "Build image: ${imageId} with dockerfile ${dockerFilePath}"
      docker.build("${imageId}", "${dockerFilePath}")
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
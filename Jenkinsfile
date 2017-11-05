node {
  def BUILD_PROPERTIES_FILE = "buildProperties.json"

  def REPO_LATEST_BRANCH = 'master'
  def REPO_STABLE_BRANCH = 'stable'
  def REPO_RELEASE_BRANCH_PREFIX = 'release/'
  
  def DOCKER_TAG_LATEST = 'latest'
  def DOCKER_TAG_STABLE = 'stable'
 
  def JOB_BRANCH = evaluateBuildBranch(REPO_LATEST_BRANCH)
  
  def buildProperties
  def buildTasks = [:]
  def pushTasks = [:]

  stage("Setup build") {
    echo "Setup build"
    
    def isLatestBranch = "${JOB_BRANCH}".contains("${REPO_LATEST_BRANCH}")
    def isStableBranch = "${JOB_BRANCH}".contains("${REPO_STABLE_BRANCH}")
    def remoteImageTag = DOCKER_TAG_LATEST
    
    buildProperties = readJSON file: "${BUILD_PROPERTIES_FILE}"
    
    echo "Properties: ${buildProperties}"
    
    for(itJob in buildProperties.dockerJobs) {
      def isReleaseBranch = "${JOB_BRANCH}".contains("${REPO_RELEASE_BRANCH_PREFIX}${itJob.imageName}")
      
      def localImageId = "${buildProperties.dockerHub.user}/${itJob.imageName}:${DOCKER_TAG_LATEST}"
      
      if (isStableBranch == true) {
        remoteImageTag = DOCKER_TAG_STABLE
      }
      else if (isReleaseBranch == true) {
        def releaseTag = evaluateReleaseTag(JOB_BRANCH, itJob.imageName)
        remoteImageTag = releaseTag != null ? releaseTag : REPO_LATEST_BRANCH
      }
      
      buildTasks[itJob.imageName] = createDockerBuildStep(localImageId, itJob.dockerfilePath)

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
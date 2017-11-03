class ImageJob {
  def imageName
  def dockerfilePath
  def image
}

node {
  def imageJobs = [
    new ImageJob(imageName: 'nginx',        dockerfilePath: './nginx'),
    new ImageJob(imageName: 'denonservice', dockerfilePath: './denonRemoteControl/service')
  ]
  
  def REPO_URL = 'https://github.com/icebear8/arctic.git'
  def REPO_CREDENTIALS = '3bc30eda-c17e-4444-a55b-d81ee0d68981'
  def REPO_LATEST_BRANCH = 'latest'
  def REPO_STABLE_BRANCH = 'stable'
  def REPO_RELEASE_BRANCH_PREFIX = 'release/'
  
  def DOCKER_TAG_LATEST = 'latest'
  def DOCKER_TAG_STABLE = 'stable'
  def DOCKER_DEFAULT_USER = "icebear8"
 
  def JOB_BRANCH = evaluateBuildBranch(REPO_LATEST_BRANCH)
  def JOB_IS_STABLE = env.RELEASE_AS_STABLE != null ? env.RELEASE_AS_STABLE : false
  
  def JOB_DOCKER_USER = env.DOCKER_USER != null ? env.DOCKER_USER : DOCKER_DEFAULT_USER
  
  def buildTasks = [:]
  def pushTasks = [:]

  def isLatestBranch = "${JOB_BRANCH}".contains("${REPO_LATEST_BRANCH}")
  def isStableBranch = "${JOB_BRANCH}".contains("${REPO_STABLE_BRANCH}")
    
  for(itJob in imageJobs) {
    def isReleaseBranch = "${JOB_BRANCH}".contains("${REPO_RELEASE_BRANCH_PREFIX}${itJob.imageName}")
    
    def localImageId = "${JOB_DOCKER_USER}/${itJob.imageName}:${DOCKER_TAG_LATEST}"
    def remoteImageTag = DOCKER_TAG_LATEST
    
    if (isStableBranch == true) {
      remoteImageTag = DOCKER_TAG_STABLE
    }
    else if (isReleaseBranch == true) {
      def releaseTag = evaluateReleaseTag(JOB_BRANCH, imageName)
      remoteImageTag = releaseTag != null ? releaseTag : REPO_LATEST_BRANCH
    }
    
    buildTasks[itJob.imageName] = createDockerBuildStep(localImageId, itJob.dockerfilePath)

    if ((isLatestBranch == true) || (isStableBranch == true) || (isReleaseBranch == true)) {
      pushTasks[itJob.imageName] = createDockerPushStep(localImageId, remoteImageTag)
    }
  }
  
  stage("Checkout") {
    echo "Checkout branch: ${JOB_BRANCH}"

    checkout([$class: 'GitSCM', branches: [[name: "*/${JOB_BRANCH}"]],
      doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [],
      userRemoteConfigs: [[credentialsId: "${REPO_CREDENTIALS}", url: "${REPO_URL}"]]])
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
  if (env.REPO_BUILD_BRANCH != null) {
    return env.REPO_BUILD_BRANCH
  }
  else if (env.BRANCH_NAME != null) {
    return env.BRANCH_NAME
  }
  
  return defaultValue
}

def evaluateReleaseTag(releaseBranch, imageName) {
  def indexOfImage = relaseBranch.indexOf(imageName)
  if (indexOfImage < 0)
  {
    return null
  }
  
  return releaseBranch.substring(indexOfImage + imageName.length())
}

def createDockerBuildStep(imageId, dockerFilePath) {
  return {
    stage("Build image ${imageId}:${imageTag}") {
      echo "Build image: ${imageId}"{$imageTag} with dockerfile ${dockerFilePath}"
      docker.build("${imageId}:${imageTag}", "${dockerFilePath}")
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
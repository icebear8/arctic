class ImageJob {
  def imageName
  def dockerfilePath
  def image
}

def createDockerBuildStep(imageId, dockerFilePath) {
  return {
    stage("Build image ${imageId}") {
      echo "Build image: ${imageId} with dockerfile ${dockerFilePath}"
      docker.build("${imageId}", "${dockerFilePath}")
    }
  }
}

def createDockerPushStep(imageId, remoteTag, isStable, latestTag, stableTag) {
  return {
    stage("Push image ${imageId}") {
      echo "Push image: ${imageId} with tag ${remoteTag}"
      def image = docker.image("${imageId}")
      
      image.push("${latestTag}")
      
      if ("${remoteTag}" != "${latestTag}") {
        image.push("${remoteTag}")
      }
        
      if ("${isStable}" == 'true') {
        image.push("${stableTag}")
      }
    }
  }
}

node {
  def imageJobs = [
    new ImageJob(imageName: 'nginx',        dockerfilePath: './nginx'),
    new ImageJob(imageName: 'denonservice', dockerfilePath: './denonRemoteControl/service')
  ]

  def buildTasks = [:]
  def pushTasks = [:]
  
  def REPOSITORY='https://github.com/icebear8/arctic.git'
  
  def TAG_LATEST = 'latest'
  def TAG_STABLE = 'stable'
  def RELEASE_BRANCH_TAG = 'release/'
  
  def MY_BUILD_BRANCH = env.REPO_BUILD_BRANCH != null ? env.REPO_BUILD_BRANCH : "master"
  def MY_IMAGE_USER = env.DOCKER_USER != null ? env.DOCKER_USER : "icebear8"
  def MY_IMAGE_TAG = env.RELEASE_TAG != null ? env.RELEASE_TAG : "${TAG_LATEST}"
  def MY_IS_IMAGE_STABLE = env.RELEASE_AS_STABLE != null ? env.RELEASE_AS_STABLE : false

  for(itJob in imageJobs) {
    def isReleaseBranch = "${MY_BUILD_BRANCH}".contains("${RELEASE_BRANCH_TAG}")
    def isReleaseImage = "${MY_BUILD_BRANCH}".contains("${RELEASE_BRANCH_TAG}${itJob.imageName}")
    def imageId = "${MY_IMAGE_USER}/${itJob.imageName}:${TAG_LATEST}"
    
    if ((isReleaseBranch == false) ||
         (isReleaseImage == true)) {
    
      buildTasks[itJob.imageName] = createDockerBuildStep(imageId, itJob.dockerfilePath)
      pushTasks[itJob.imageName] = createDockerPushStep(imageId, MY_IMAGE_TAG, MY_IS_IMAGE_STABLE, TAG_LATEST, TAG_STABLE)
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
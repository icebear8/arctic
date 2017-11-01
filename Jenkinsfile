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
  def REPO_LATEST_BRANCH = 'master'
  def REPO_RELEASE_BRANCH = 'release/'
  
  def DOCKER_TAG_LATEST = 'latest'
  def DOCKER_TAG_STABLE = 'stable'
  def DOCKER_DEFAULT_USER = "icebear8"
  
 
  def JOB_BRANCH = evaluateBuildBranch(REPO_LATEST_BRANCH)
  def JOB_IS_STABLE = env.RELEASE_AS_STABLE != null ? env.RELEASE_AS_STABLE : false
  
  def JOB_DOCKER_USER = env.DOCKER_USER != null ? env.DOCKER_USER : DOCKER_DEFAULT_USER
  def JOB_DOCKER_TAG = env.RELEASE_TAG != null ? env.RELEASE_TAG : "${DOCKER_TAG_LATEST}"
  
  def buildTasks = [:]
  def pushTasks = [:]

  for(itJob in imageJobs) {
    def isLatestBranch = "${JOB_BRANCH}".contains("${REPO_LATEST_BRANCH}")
    def isReleaseImage = "${JOB_BRANCH}".contains("${REPO_RELEASE_BRANCH}${itJob.imageName}")
    def imageId = "${JOB_DOCKER_USER}/${itJob.imageName}:${DOCKER_TAG_LATEST}"
    
    buildTasks[itJob.imageName] = createDockerBuildStep(imageId, itJob.dockerfilePath)

    if ((isLatestBranch == true) ||
         (isReleaseImage == true)) {
      pushTasks[itJob.imageName] = createDockerPushStep(imageId, JOB_DOCKER_TAG, JOB_IS_STABLE, DOCKER_TAG_LATEST, DOCKER_TAG_STABLE)
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
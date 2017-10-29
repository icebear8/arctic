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
    
    if ((isReleaseBranch == false) ||
         (isReleaseImage == true)) {
    
      buildTasks[itJob.imageName] = {
        stage ('Build image ${itJob.imageName}') {
          echo "Build image: ${MY_IMAGE_USER}/${itJob.imageName}:${TAG_LATEST}"
          itJob.image = docker.build("${MY_IMAGE_USER}/${itJob.imageName}:${TAG_LATEST}", "${itJob.dockerfilePath}")
        }
      }
        
      pushTasks[itJob.imageName] = {
        stage ('Push image ${itJob.imageName}') {
          itJob.image.push("${TAG_LATEST}")
        
          if ("${MY_IMAGE_TAG}" != "${TAG_LATEST}") {
              itJob.image.push("${MY_IMAGE_TAG}")
          }
            
          if ("${MY_IS_IMAGE_STABLE}" == "true") {
              itJob.image.push("${TAG_STABLE}")
          }
        }
      }
    }
  }
  
  stage('Clone Repository') {
    echo "Checkout ${MY_BUILD_BRANCH} from ${REPOSITORY}"
    git branch: "${MY_BUILD_BRANCH}", url: "${REPOSITORY}"
  }
  
  stage('Debug') {
    echo "build branch: ${MY_BUILD_BRANCH}"
    echo "release branch tag: ${RELEASE_BRANCH_TAG}"
    
    for(itJob in imageJobs) {
      def isReleaseBranch = "${MY_BUILD_BRANCH}".contains("${RELEASE_BRANCH_TAG}")
      def isReleaseImage = "${MY_BUILD_BRANCH}".contains("${RELEASE_BRANCH_TAG}${itJob.imageName}")
      
      echo "Release image tag: ${RELEASE_BRANCH_TAG}${itJob.imageName}"
      
      if (isReleaseBranch == false) {
        echo "is relase branch is false"
      } else {
        echo "is relase branch is true"
      }
      
      if (isReleaseImage == true) {
        echo "is release image is true"
      } else {
        echo "is release image is false"
      }
      
      if ((isReleaseBranch == false) ||
         (isReleaseImage == true)) {
         echo "${itJob.imageName} will be built"
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
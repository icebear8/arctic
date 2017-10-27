class ImageJob {
  def imageName
  def dockerfilePath
  def image
}

node {
 
  def imageNames = ["nginx", "denonservice"]
  def imagePaths = ["./nginx", "./denonRemoteControl/service"]
  def images = [:]
  
  def imageJobs = [
    new ImageJob(imageName: 'nginx', dockerfilePath: './nginx'),
    new ImageJob(imageName: 'denonservice', dockerfilePath: './denonRemoteControl/service')
  ]
    
  def buildTasks = [:]
  def pushTasks = [:]
  
  def REPOSITORY='https://github.com/icebear8/arctic.git'
  
  def TAG_LATEST = 'latest'
  def TAG_STABLE = 'stable'
  
  def MY_BUILD_TAG = env.REPO_BUILD_TAG != null ? env.REPO_BUILD_TAG : "${TAG_LATEST}"
  def MY_IMAGE_USER = env.DOCKER_USER != null ? env.DOCKER_USER : "icebear8"
  def MY_IMAGE_TAG = env.RELEASE_TAG != null ? env.RELEASE_TAG : "${TAG_LATEST}"
  def MY_IS_IMAGE_STABLE = env.RELEASE_AS_STABLE != null ? env.RELEASE_AS_STABLE : false

  for(job in imageJobs) {
    def itJob = job
    
      buildTasks[itJob.imageName] = {
   
        stage ('Build image ${itJob.imageName}') {
          images[itJob.imageName] = docker.build("${MY_IMAGE_USER}/${itJob.imageName}:${TAG_LATEST}", "${itJob.dockerfilePath}")
        }
      }
      
      pushTasks[itJob.imageName] = {
        stage ('Push image ${itJob.imageName}') {
          images[itJob.imageName].push("${TAG_LATEST}")
      
          if ("${MY_IMAGE_TAG}" != "${TAG_LATEST}") {
              images[itJob.imageName].push("${MY_IMAGE_TAG}")
          }
          
          if ("${MY_IS_IMAGE_STABLE}" == "true") {
              images[itJob.imageName].push("${TAG_STABLE}")
          }
        }
      }
    }
  
  stage('Clone Repository') {
    if ("${MY_BUILD_TAG}" == "${TAG_LATEST}") {
      git branch: 'master', url: "${REPOSITORY}"
    }
    else {
      checkout scm: [$class: 'GitSCM', 
        userRemoteConfigs: [[url: "${REPOSITORY}"]], 
        branches: [[name: "refs/tags/${MY_BUILD_TAG}"]]], changelog: false, poll: false
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
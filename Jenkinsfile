class TestClass {
  def name
  def path
}

node {
 
  def imageNames = ["nginx", "denonservice"]
  def imagePaths = ["./nginx", "./denonRemoteControl/service"]
  def images = [:]
  
  def theClasses = [
    new TestClass('myName', 'myPath')
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

  for (i = 0; i < imageNames.size(); ++i) {
    def imageName = "${imageNames[i]}"
    def imagePath = "${imagePaths[i]}"
    
      buildTasks[imageName] = {
   
        stage ('Build image ${imageName}') {
          images[imageName] = docker.build("${MY_IMAGE_USER}/${imageName}:${TAG_LATEST}", "${imagePath}")
        }
      }
      
      pushTasks[imageName] = {
        stage ('Push image ${imageName}') {
          images[imageName].push("${TAG_LATEST}")
      
          if ("${MY_IMAGE_TAG}" != "${TAG_LATEST}") {
              images[imageName].push("${MY_IMAGE_TAG}")
          }
          
          if ("${MY_IS_IMAGE_STABLE}" == "true") {
              images[imageName].push("${TAG_STABLE}")
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
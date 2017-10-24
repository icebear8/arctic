node {
    
  def imgJenkins
  
  def REPOSITORY='https://github.com/icebear8/arctic.git'
  def TAG_LATEST='latest'
  def TAG_STABLE='stable'
  
  def MY_IMAGE_NAME = env.IMAGE_NAME != null ? env.IMAGE_NAME : "icebear8/nginx"
  def MY_RELEASE_VERSION = env.RELEASE_VERSION != null ? env.RELEASE_VERSION : "${TAG_LATEST}"
  def MY_RELEASE_AS_STABLE = env.RELEASE_AS_STABLE != null ? env.RELEASE_AS_STABLE : false

  docker.withServer(env.DEFAULT_DOCKER_HOST_CONNECTION, 'default-docker-host-credentials') {
  
    stage('Clone Repository') {
      if ("${MY_RELEASE_VERSION}" == "${TAG_LATEST}") {
        git branch: 'master', url: "${REPOSITORY}"
      }
      else {
        checkout scm: [$class: 'GitSCM', 
          userRemoteConfigs: [[url: "${REPOSITORY}"]], 
          branches: [[name: "refs/tags/${MY_RELEASE_VERSION}"]]], changelog: false, poll: false
      }
    }
    
    stage ('Build Images') {
      imgJenkins = docker.build("${MY_IMAGE_NAME}:${TAG_LATEST}", "./nginx")
    }
    
    stage ('Push Images') {  
      imgJenkins.push()
      
      if ("${MY_RELEASE_VERSION}" != "${TAG_LATEST}") {
          imgJenkins.push("${MY_RELEASE_VERSION}")
      }
      
      if ("${MY_RELEASE_AS_STABLE}" == "true") {
          imgJenkins.push("${TAG_STABLE}")
      }
    }
  }
}
node {
    
  def imgJenkins
  
  def REPOSITORY='https://github.com/icebear8/arctic.git'
  
  def TAG_LATEST = 'latest'
  def TAG_STABLE = 'stable'
  
  def MY_BUILD_TAG=env.REPO_BUILD_TAG != null ? env.REPO_BUILD_TAG : "${TAG_LATEST}"
  def MY_IMAGE_USER=env.DOCKER_USER != null ? env.DOCKER_USER : "icebear8"
  def MY_IMAGE_TAG=env.RELEASE_TAG != null ? env.RELEASE_TAG : "${TAG_LATEST}"
  def MY_IS_IMAGE_STABLE = env.RELEASE_AS_STABLE != null ? env.RELEASE_AS_STABLE : false

  docker.withServer(env.DEFAULT_DOCKER_HOST_CONNECTION, 'default-docker-host-credentials') {
  
    stage('Clone Repository') {
      echo "build tag: ${MY_BUILD_TAG}"
      echo "build user: ${MY_IMAGE_USER}"
      echo "build latest: ${TAG_LATEST}"
      echo "image tag: ${MY_IMAGE_TAG}"
      
      if ("${MY_BUILD_TAG}" == "${TAG_LATEST}") {
        echo 'clone master'
        git branch: 'master', url: "${REPOSITORY}"
      }
      else {
        echo 'checkout tag'
      
        checkout scm: [$class: 'GitSCM', 
          userRemoteConfigs: [[url: "${REPOSITORY}"]], 
          branches: [[name: "refs/tags/${MY_BUILD_TAG}"]]], changelog: false, poll: false
      }
    }
    
    stage ('Build Images') {
      def MY_IMAGE_NAME='nginx'
      
      imgJenkins = docker.build("${MY_IMAGE_USER}/${MY_IMAGE_NAME}:${TAG_LATEST}", "./${MY_IMAGE_NAME}")
    }
    
    stage ('Push Images') {  
      imgJenkins.push("${TAG_LATEST}")
      
      if ("${MY_IMAGE_TAG}" != "${TAG_LATEST}") {
          imgJenkins.push("${MY_IMAGE_TAG}")
      }
      
      if ("${MY_IS_IMAGE_STABLE}" == "true") {
          imgJenkins.push("${TAG_STABLE}")
      }
    }
  }
}
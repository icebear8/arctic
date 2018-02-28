#!/usr/bin/env groovy

// Uses the common library form 'https://github.com/icebear8/pipelineLibrary'
library identifier: 'common-pipeline-library@master',
  retriever: modernSCM(github(
    id: '18306726-fec7-4d80-8226-b78a05add4d0',
    credentialsId: '3bc30eda-c17e-4444-a55b-d81ee0d68981',
    repoOwner: 'icebear8',
    repository: 'pipelineLibrary',
    traits: [
      [$class: 'org.jenkinsci.plugins.github_branch_source.BranchDiscoveryTrait', strategyId: 1],
      [$class: 'org.jenkinsci.plugins.github_branch_source.OriginPullRequestDiscoveryTrait', strategyId: 1],
      [$class: 'org.jenkinsci.plugins.github_branch_source.ForkPullRequestDiscoveryTrait', strategyId: 1, trust: [$class: 'TrustContributors']]]))
      
node {
  def projectSettings = readJSON text: '''{
    "repository": {
      "url": "https://github.com/icebear8/arctic.git",
      "credentials": "3bc30eda-c17e-4444-a55b-d81ee0d68981"
    },
    "dockerHub": {
      "user": "icebear8"
    },
    "dockerJobs": [
      {"imageName": "nginx",        "dockerfilePath": "./nginx" },
      {"imageName": "denonservice", "dockerfilePath": "./denonRemoteControl" },
      {"imageName": "grav",         "dockerfilePath": "./grav" }
    ]
  }'''

  def dockerBuild = new icebear8.projects.arctic.build()
  
  dockerBuild.buildMethod(projectSettings)
}

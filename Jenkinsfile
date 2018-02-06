#!/usr/bin/env groovy
// Uses the common library form 'https://github.com/icebear8/pipelineLibrary'
library identifier: 'common-pipeline-library@stable',
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
  def buildScriptDir = 'buildSubDir'

  stage("Checkout build script") {
    echo "Checkout branch: master"

    checkout([
      $class: 'GitSCM',
      branches: [[name: "*/master"]],
      doGenerateSubmoduleConfigurations: false,
      extensions: [
        [$class: 'CleanBeforeCheckout'],
        [$class: 'PruneStaleBranch'],
        [$class: 'RelativeTargetDirectory', relativeTargetDir: "${buildScriptDir}"]],
      submoduleCfg: [],
      userRemoteConfigs: [[url: 'https://github.com/icebear8/arcticBuild.git', credentialsId: '3bc30eda-c17e-4444-a55b-d81ee0d68981']]])
  
    sh "ls ${buildScriptDir}"
  
  }
  
  sh "ls ${buildScriptDir}"
  load "${buildScriptDir}/buildInstruction.groovy"
}

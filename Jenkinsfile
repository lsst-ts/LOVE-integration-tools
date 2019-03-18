pipeline {
  agent any
  environment {
    registryCredential = "dockerhub-inriachile"
    dockerImageName = "inriachile/love-nginx:${GIT_BRANCH}"
    dockerImage = ""
  }
  stages {
    stage("Build Docker image") {
      when {
        changeset "nginx/*"
        anyOf {
          branch "master"
          branch "develop"
        }
      }
      steps {
        script {
          dockerImage = docker.build(dockerImageName, "./nginx")
        }
      }
    }
    stage("Push Docker image") {
      when {
        changeset "nginx/*"
        anyOf {
          branch "master"
          branch "develop"
        }
      }
      steps {
        script {
          docker.withRegistry("", registryCredential) {
            dockerImage.push()
          }
        }
      }
    }
    stage("Deploy develop version") {
      when {
        branch "develop"
      }
      steps {
        script {
          def remote = [:]
          remote.host = "dev.love.inria.cl"
          remote.user = "love"
          remote.identityFile = "love-ssh-key"
          sshCommand remote: remote, command: "cat /proc/cpuinfo"
        }
      }
    }
  }
}

pipeline {
  agent any
  environment {
    registryCredential = "dockerhub-inriachile"
    dockerImageName = "inriachile/love-nginx:${GIT_BRANCH}"
    dockerImage = ""
    def devServer = [:]
    devServer.host = "dev.love.inria.cl"
    devServer.user = "love"
    devServer.identityFile = "love-ssh-key"
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
        sshCommand remote: devServer, command: "cat /proc/cpuinfo"
      }
    }
  }

}

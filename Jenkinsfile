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
          sshagent(credentials: ['love-ssh-key']) {
            sh 'scp -o StrictHostKeyChecking=no README.md love@dev.love.inria.cl:.'
          }
        }
      }
    }
  }
}

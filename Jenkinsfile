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
            sh 'scp -o StrictHostKeyChecking=no deploy/prod/docker-compose.yml love@dev.love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no deploy/prod/.env love@dev.love.inria.cl:.'
            sh 'ssh love@dev.love.inria.cl docker-compose pull'
            sh 'ssh love@dev.love.inria.cl docker-compose down -v'
            sh 'ssh love@dev.love.inria.cl docker-compose up -d'
          }
        }
      }
    }
  }
}

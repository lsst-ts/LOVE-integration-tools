pipeline {
  agent any
  environment {
    registryCredential = "dockerhub-inriachile"
    dockerImageName = "inriachile/love-nginx:${GIT_BRANCH}"
    dockerImage = ""
  }
  stages {
    stage("Build Nginx Docker image") {
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
    stage("Push Nginx Docker image") {
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
          sshagent(credentials: ['love-ssh-key-2']) {
            sh 'scp -o StrictHostKeyChecking=no deploy/prod/docker-compose-dev.yml love@dev.love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no deploy/prod/.env love@dev.love.inria.cl:.'
            sh 'ssh love@dev.love.inria.cl docker-compose -f docker-compose-dev.yml pull'
            sh 'ssh love@dev.love.inria.cl docker-compose -f docker-compose-dev.yml down -v'
            sh 'ssh love@dev.love.inria.cl docker network ls | grep testnet > /dev/null  || docker network create testnet'
            sh 'ssh love@dev.love.inria.cl docker-compose -f docker-compose-dev.yml up -d'
          }
        }
      }
    }

    stage("Deploy master version") {
      when {
        branch "master"
      }
      steps {
        script {
          sshagent(credentials: ['love-ssh-key-2']) {
            sh 'scp -o StrictHostKeyChecking=no deploy/prod/docker-compose.yml love@love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no deploy/prod/.env love@love.inria.cl:.'
            sh 'ssh love@love.inria.cl docker-compose pull'
            sh 'ssh love@love.inria.cl docker-compose down -v'
            sh 'ssh love@love.inria.cl docker-compose up -d'
          }
        }
      }
    }
  }
}

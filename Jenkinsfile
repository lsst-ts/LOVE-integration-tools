pipeline {
  agent any
  environment {
    registryCredential = "dockerhub-inriachile"
    dockerImageName = "inriachile/love-nginx:${GIT_BRANCH}"
    dockerImageLinode = ""
    dockerImageTucson = ""
  }
  stages {
    stage("Build Linode Nginx Docker image") {
      when {
        changeset "deploy/linode/nginx/*"
        anyOf {
          branch "master"
          branch "develop"
        }
      }
      steps {
        script {
          dockerImageLinode = docker.build(dockerImageName, "./deploy/linode/nginx")
        }
      }
    }
    stage("Push Linode Nginx Docker image") {
      when {
        changeset "deploy/linode/nginx/*"
        anyOf {
          branch "master"
          branch "develop"
        }
      }
      steps {
        script {
          docker.withRegistry("", registryCredential) {
            dockerImageLinode.push()
          }
        }
      }
    }

    stage("Build Tucson Nginx Docker image") {
      when {
        changeset "deploy/tucson/nginx/*"
        anyOf {
          branch "master"
        }
      }
      steps {
        script {
          dockerImageTucson = docker.build("inriachile/love-nginx:eia", "./deploy/tucson/nginx")
        }
      }
    }
    stage("Push Nginx Tucson Docker image") {
      when {
        changeset "deploy/tucson/nginx/*"
        anyOf {
          branch "master"
        }
      }
      steps {
        script {
          docker.withRegistry("", registryCredential) {
            dockerImageTucson.push()
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
            sh 'ssh love@dev.love.inria.cl "docker network ls | grep testnet > /dev/null  || docker network create testnet"'
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

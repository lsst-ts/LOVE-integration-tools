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
          branch "develop"
        }
      }
      steps {
        script {
          dockerImageTucson = docker.build("inriachile/love-nginx:tucson", "./deploy/tucson/nginx")
        }
      }
    }
    stage("Push Nginx Tucson Docker image") {
      when {
        changeset "deploy/tucson/nginx/*"
        anyOf {
          branch "develop"
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

    stage("Build La Serena Nginx Docker image") {
      when {
        changeset "deploy/laserena/prod/nginx/*"
        anyOf {
          branch "develop"
        }
      }
      steps {
        script {
          dockerImageLaSerena = docker.build("inriachile/love-nginx:laserena", "./deploy/laserena/prod/nginx")
        }
      }
    }
    stage("Push Nginx LaSerena Docker image") {
      when {
        changeset "deploy/laserena/prod/nginx/*"
        anyOf {
          branch "develop"
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


    stage("Deploy Linode develop version") {
      when {
        anyOf {
          changeset "deploy/linode/*"
          changeset "Jenkinsfile"
        }
        branch "develop"
      }
      steps {
        script {
          sshagent(credentials: ['love-ssh-key-2']) {
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/docker-compose-dev.yml love@dev.love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/.env love@dev.love.inria.cl:.'
            sh 'ssh love@dev.love.inria.cl docker-compose -f docker-compose-dev.yml pull'
            sh 'ssh love@dev.love.inria.cl docker-compose -f docker-compose-dev.yml down -v'
            sh 'ssh love@dev.love.inria.cl "docker network ls | grep testnet > /dev/null  || docker network create testnet"'
            sh 'ssh love@dev.love.inria.cl docker-compose -f docker-compose-dev.yml up -d'
          }
        }
      }
    }

    stage("Deploy Linode master version") {
      when {
        anyOf {
          changeset "deploy/linode/*"
          changeset "Jenkinsfile"
        }
        branch "master"
      }
      steps {
        script {
          sshagent(credentials: ['love-ssh-key-2']) {
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/docker-compose.yml love@love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/.env love@love.inria.cl:.'
            sh 'ssh love@love.inria.cl docker-compose pull'
            sh 'ssh love@love.inria.cl docker-compose down -v'
            sh 'ssh love@love.inria.cl docker-compose up -d'
          }
        }
      }
    }
  }
}

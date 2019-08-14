pipeline {
  agent any
  environment {
    registryCredential = "dockerhub-inriachile"
    dockerImageName = "inriachile/love-nginx:${GIT_BRANCH}"
    dockerImageLinode = ""
    dockerImageTucson = ""
    dockerImageLaSerena = ""
  }

  stages {
    stage("Build Linode Nginx Docker image") {
      when {
        anyOf {
          changeset "deploy/linode/nginx/*"
          expression {
            return currentBuild.number == 1
          }
        }
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
        anyOf {
          changeset "deploy/linode/nginx/*"
          expression {
            return currentBuild.number == 1
          }
        }
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
        anyOf {
          changeset "deploy/tucson/nginx/*"
          changeset "Jenkinsfile"
          expression {
            return currentBuild.number == 1
          }
        }
        branch "develop"
      }
      steps {
        script {
          dockerImageTucson = docker.build("inriachile/love-nginx:tucson", "./deploy/tucson/nginx")
        }
      }
    }
    stage("Push Tucson Nginx Docker image") {
      when {
        anyOf {
          changeset "deploy/tucson/nginx/*"
          changeset "Jenkinsfile"
          expression {
            return currentBuild.number == 1
          }
        }
        branch "develop"
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
        anyOf {
          changeset "deploy/laserena/nginx/*"
          changeset "Jenkinsfile"
          expression {
            return currentBuild.number == 1
          }
        }
        branch "develop"
      }
      steps {
        script {
          dockerImageLaSerena = docker.build("inriachile/love-nginx:laserena", "./deploy/laserena/nginx")
        }
      }
    }
    stage("Push LaSerena Nginx Docker image") {
      when {
        anyOf {
          changeset "deploy/laserena/nginx/*"
          changeset "Jenkinsfile"
          expression {
            return currentBuild.number == 1
          }
        }
        branch "develop"
      }
      steps {
        script {
          docker.withRegistry("", registryCredential) {
            dockerImageLaSerena.push()
          }
        }
      }
    }


    stage("Deploy Linode develop version") {
      when {
        anyOf {
          changeset "deploy/linode/**/*"
          changeset "Jenkinsfile"
          triggeredBy "UpstreamCause"
        }
        branch "develop"
      }
      steps {
        script {
          sshagent(credentials: ['love-ssh-key-2']) {
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/docker-compose.yml love@dev.love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/.env love@dev.love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/ospl.xml love@dev.love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no -r deploy/linode/config love@dev.love.inria.cl:.'
            sh 'ssh love@dev.love.inria.cl docker-compose  pull'
            sh 'ssh love@dev.love.inria.cl docker-compose  down -v'
            sh 'ssh love@dev.love.inria.cl "source local_env.sh; docker-compose up -d"'
          }
        }
      }
    }

    stage("Deploy Linode master version") {
      when {
        anyOf {
          changeset "deploy/linode/**/*"
          changeset "Jenkinsfile"
          triggeredBy "UpstreamCause"
        }
        branch "master"
      }
      steps {
        script {
          sshagent(credentials: ['love-ssh-key-2']) {
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/docker-compose.yml love@love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/.env love@love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/ospl.xml love@dev.love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no -r deploy/linode/config love@dev.love.inria.cl:.'
            sh 'ssh love@love.inria.cl docker-compose -f docker-compose-master.yml pull'
            sh 'ssh love@love.inria.cl docker-compose -f docker-compose-master.yml down -v'
            sh 'ssh love@love.inria.cl "source local_env.sh; docker-compose -f docker-compose-master.yml up -d"'
          }
        }
      }
    }
  }
}

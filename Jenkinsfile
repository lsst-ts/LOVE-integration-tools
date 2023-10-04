pipeline {
  agent any
  environment {
    registryCredential = "dockerhub-inriachile"
    // SAL setup file
    SAL_SETUP_FILE = "/home/saluser/.setup_dev.sh"
    // LTD credentials
    user_ci = credentials('lsst-io')
    LTD_USERNAME="${user_ci_USR}"
    LTD_PASSWORD="${user_ci_PSW}"
  }

  stages {
    stage("Deploy documentation") {
      agent {
        docker {
          alwaysPull true
          image 'lsstts/develop-env:develop'
          args "--entrypoint=''"
        }
      }
      when {
        branch "main"
        branch "develop"
      }
      steps {
        script {
          sh """
            source ${env.SAL_SETUP_FILE}
            # Create docs
            cd ./docsrc
            pip install -r requirements.txt
            sh ./create_docs.sh
            cd ..
            # Upload docs
            pip install ltd-conveyor
            ltd upload --product love-integration-tools --git-ref ${GIT_BRANCH} --dir ./docs
          """
        }
      }
    }

    stage("Deploy Linode develop version") {
      when {
        anyOf {
          changeset "deploy/linode/config/*"
          changeset "deploy/linode/.env"
          changeset "deploy/linode/ospl.xml"
          changeset "deploy/linode/docker-compose.yml"
          changeset "deploy/linode/nginx-develop.conf"
          changeset "deploy/linode/run.sh"
          changeset "jupyter/*"
          changeset "Jenkinsfile"
          triggeredBy "UpstreamCause"
          triggeredBy "UserIdCause"
        }
        branch "develop"
      }
      steps {
        script {
          sshagent(credentials: ['love-ssh-key-2']) {
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/run.sh love@dev.love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no -r deploy/linode/scripts love@dev.love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/docker-compose.yml love@dev.love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/.env love@dev.love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/ospl.xml love@dev.love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/nginx-develop.conf love@dev.love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no -r deploy/linode/config love@dev.love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no -r deploy/linode/simulatorcamera.py love@dev.love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no -r jupyter love@dev.love.inria.cl:.'
            sh 'ssh love@dev.love.inria.cl "./run.sh"'
          }
        }
      }
    }

    stage("Deploy Linode main version") {
      when {
        anyOf {
          changeset "deploy/linode/config/*"
          changeset "deploy/linode/.env"
          changeset "deploy/linode/ospl.xml"
          changeset "deploy/linode/docker-compose-main.yml"
          changeset "deploy/linode/nginx-main.conf"
          changeset "Jenkinsfile"
          triggeredBy "UpstreamCause"
          triggeredBy "UserIdCause"
        }
        branch "main"
      }
      steps {
        script {
          sshagent(credentials: ['love-ssh-key-2']) {
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/docker-compose-main.yml love@love.inria.cl:./docker-compose.yml'
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/.env love@love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/ospl.xml love@love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/nginx-main.conf love@love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no -r deploy/linode/config love@love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no -r deploy/linode/simulatorcamera.py love@love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no -r jupyter love@love.inria.cl:.'
            sh 'ssh love@love.inria.cl "docker network inspect testnet >/dev/null 2>&1 || docker network create testnet"'
            sh 'ssh love@love.inria.cl docker-compose pull'
            sh 'ssh love@love.inria.cl docker-compose down -v'
            sh 'ssh love@love.inria.cl "source local_env.sh; docker-compose up -d"'
          }
        }
      }
    }
  }
}

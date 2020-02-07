pipeline {
  agent any
  environment {
    registryCredential = "dockerhub-inriachile"
  }

  stages {
    stage("Deploy Linode develop version") {
      when {
        anyOf {
          changeset "deploy/linode/config/*"
          changeset "deploy/linode/.env"
          changeset "deploy/linode/ospl.xml"
          changeset "deploy/linode/docker-compose.yml"
          changeset "deploy/linode/nginx-develop.conf"
          changeset "Jenkinsfile"
          triggeredBy "UpstreamCause"
          triggeredBy "UserIdCause"
        }
        branch "develop"
      }
      steps {
        script {
          sshagent(credentials: ['love-ssh-key-2']) {
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/docker-compose.yml love@dev.love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/.env love@dev.love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/ospl.xml love@dev.love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/nginx-develop.conf love@dev.love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no -r deploy/linode/config love@dev.love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no -r deploy/linode/simulatorcamera.py love@dev.love.inria.cl:.'
            sh 'ssh love@dev.love.inria.cl "docker network inspect testnet >/dev/null 2>&1 || docker network create testnet"'
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
          changeset "deploy/linode/config/*"
          changeset "deploy/linode/.env"
          changeset "deploy/linode/ospl.xml"
          changeset "deploy/linode/docker-compose-master.yml"
          changeset "deploy/linode/nginx-master.conf"
          changeset "Jenkinsfile"
          triggeredBy "UpstreamCause"
          triggeredBy "UserIdCause"
        }
        branch "develop"
      }
      steps {
        script {
          sshagent(credentials: ['love-ssh-key-2']) {
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/docker-compose-master.yml love@love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/.env love@love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/ospl.xml love@love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no deploy/linode/nginx-master.conf love@love.inria.cl:.'
            sh 'scp -o StrictHostKeyChecking=no -r deploy/linode/config love@love.inria.cl:.'
            sh 'ssh love@love.inria.cl "docker network inspect testnet >/dev/null 2>&1 || docker network create testnet"'
            sh 'ssh love@love.inria.cl docker-compose -f docker-compose-master.yml pull'
            sh 'ssh love@love.inria.cl docker-compose -f docker-compose-master.yml down -v'
            sh 'ssh love@love.inria.cl "source local_env.sh; docker-compose -f docker-compose-master.yml up -d"'
          }
        }
      }
    }
  }
}

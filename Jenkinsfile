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
        anyOf {
          branch "main"
          branch "develop"
        }
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
  }
}

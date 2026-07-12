pipeline {
  agent any

  options {
    timestamps()
    timeout(time: 1, unit: 'HOURS')
  }

  parameters {
    string(name: 'DOCKER_IMAGE', defaultValue: 'mario21ic/python-calc', description: 'Docker image')
    string(name: 'DOCKER_CREDENTIALS', defaultValue: 'dockerhub_credentials', description: 'Credentials on Docker Hub organization')
    string(name: 'SLACK_CHANNEL', defaultValue: 'jenkins-blazingsql', description: '')
  }
  
  environment {
    DOCKER_IMAGE_VERSION = "${params.DOCKER_IMAGE}-v${env.BUILD_NUMBER}"
    SLACK_MESSAGE=" - Job '${env.JOB_NAME}' - Build #${env.BUILD_NUMBER}: ${env.BUILD_URL}"
  }

  stages {

    stage("Repository") {
      steps {
        checkout scm
      }
    }

    stage("Docker build") {
      steps {
        sh "docker build -t ${env.DOCKER_IMAGE_VERSION} ./"
      }
    }

    stage("Docker login") {
      steps {
        withCredentials([usernamePassword(credentialsId: "${params.DOCKER_CREDENTIALS}", passwordVariable: 'PASSWORD', usernameVariable: 'USERNAME')]) {
          sh "echo $PASSWORD | docker login -u $USERNAME --password-stdin"
        }
      }
    }

    stage("Publish image") {
      steps {
        sh "docker push ${env.DOCKER_IMAGE_VERSION}"
      }
    }

    stage("Docker logout") {
      steps {
        sh "docker logout"
      }
    }

  }

}


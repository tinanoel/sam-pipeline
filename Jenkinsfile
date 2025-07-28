pipeline {
  agent any

  environment {
    AWS_DEFAULT_REGION = 'ap-south-1'
    SAM_STACK_NAME     = "${params.STACK_NAME}"
    SAM_TEMPLATE       = 'sam-template.yaml'
  }

  parameters {
    string(name: 'BRANCH',     defaultValue: 'main',      description: 'Git branch')
    string(name: 'STACK_NAME', defaultValue: 'orders-svc', description: 'SAM stack name')
  }

  stages {

    stage('Checkout') {
      steps {
        checkout([$class: 'GitSCM',
          branches: [[name: "*/${params.BRANCH}"]],
          userRemoteConfigs: [[url: 'https://github.com/your-org/your-repo.git']]
        ])
      }
    }

    stage('Unit Tests') {
      steps {
        sh 'pip install -r tests/requirements.txt --quiet'
        sh 'pytest -q tests'
      }
    }

    stage('Build') {
      steps {
        sh 'sam build --use-container'
        archiveArtifacts artifacts: '.aws-sam/build/**/*', fingerprint: true
      }
    }

    stage('Deploy to Dev') {
      steps {
        withCredentials([[
          $class: 'AmazonWebServicesCredentialsBinding',
          credentialsId: 'aws-dev'
        ]]) {
          sh """
            sam deploy \
              --stack-name   $SAM_STACK_NAME-dev \
              --template-file .aws-sam/build/template.yaml \
              --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
              --no-fail-on-empty-changeset \
              --parameter-overrides Stage=dev
          """
        }
      }
    }

    stage('Approval for Prod') {
      steps {
        timeout(time: 1, unit: 'HOURS') {
          input message: 'Deploy to PROD?'
        }
      }
    }

    stage('Deploy to Prod') {
      steps {
        withCredentials([[
          $class: 'AmazonWebServicesCredentialsBinding',
          credentialsId: 'aws-prod'
        ]]) {
          sh """
            sam deploy \
              --stack-name   $SAM_STACK_NAME-prod \
              --template-file .aws-sam/build/template.yaml \
              --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
              --no-fail-on-empty-changeset \
              --parameter-overrides Stage=prod
          """
        }
      }
    }
  }

  post {
    failure {
      mail to: 'devops-team@example.com',
           subject: "❌ Build ${env.BUILD_NUMBER} failed",
           body: "Check ${env.BUILD_URL}"
    }
  }
}

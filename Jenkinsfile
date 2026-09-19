pipeline {
    agent any

    environment {
        AWS_REGION       = 'ap-south-1'
        ECR_REPOSITORY   = 'ai-inference'
        EKS_CLUSTER      = 'mlops-cluster'
        AWS_ACCOUNT_ID   = credentials('AWS_ACCOUNT_ID')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Lint & Test') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r app/requirements.txt
                    pip install pytest flake8
                    flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics
                '''
            }
        }

        stage('Build & Push to ECR') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-credentials'
                ]]) {
                    sh '''
                        aws ecr get-login-password --region $AWS_REGION | \
                          docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

                        IMAGE_URI=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY

                        docker build -t \( IMAGE_URI: \){BUILD_NUMBER} -f docker/Dockerfile .
                        docker tag \( IMAGE_URI: \){BUILD_NUMBER} $IMAGE_URI:latest

                        docker push \( IMAGE_URI: \){BUILD_NUMBER}
                        docker push $IMAGE_URI:latest
                    '''
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-credentials'
                ]]) {
                    sh '''
                        aws eks update-kubeconfig --name $EKS_CLUSTER --region $AWS_REGION
                        kubectl apply -f k8s/
                        kubectl set image deployment/ai-inference-service \
                          inference=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:latest
                        kubectl rollout status deployment/ai-inference-service --timeout=300s
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully'
        }
        failure {
            echo 'Pipeline failed'
        }
    }
}

pipeline {
    agent any

    environment {
        DOCKER_ID = credentials('DOCKER_ID')
        DOCKER_PASSWORD = credentials('DOCKER_PASSWORD')
        AWS_DEFAULT_REGION="us-east-1"
        THE_BUTLER_SAYS_SO=credentials('cmb-aws-creds')
    }

    stages {
        stage('Init') {
            steps {
                echo 'Initializing..'
                echo "Running ${env.BUILD_ID} on ${env.JENKINS_URL}"
                echo "Current branch: ${env.BRANCH_NAME}"
                sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_ID --password-stdin'
            }
        }
        stage('AWS') {           
            steps {
                echo 'AWS command..'
                sh '''
                  aws --version
                  aws ec2 describe-instances
                '''
            }
        }        
        stage('Build') {
            steps {
                echo 'Building image..'
                sh 'docker build -t $DOCKER_ID/cotu:latest .'
            }
        }
        stage('Zip') {
            steps {
                echo 'Ziping image..'
                sh 'mkdir myzip1'
                dir('myzip1'){
                    sh 'docker save $DOCKER_ID/cotu:latest > mydocker.tar.gz'
                }
            }
        }        
//        stage('Test') {
//            steps {
//                echo 'Testing..'
//                sh 'docker run --rm -e CI=true $DOCKER_ID/cotu pytest'
//            }
//        }
        stage('Publish') {
            steps {
                echo 'Publishing image to DockerHub..'
                sh 'docker push $DOCKER_ID/cotu:latest'
            }
        }
        stage('Cleanup') {
            steps {
                echo 'Removing unused docker containers and images..'
                sh 'docker ps -aq | xargs --no-run-if-empty docker rm'
                // keep intermediate images as cache, only delete the final image
                sh 'docker images -q | xargs --no-run-if-empty docker rmi'
            }
        }
    }
}

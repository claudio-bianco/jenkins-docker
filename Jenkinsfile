pipeline {
    agent any

    environment {
        DOCKER_ID = credentials('DOCKER_ID')
        DOCKER_PASSWORD = credentials('DOCKER_PASSWORD')
        AWS_DEFAULT_REGION="us-east-1"
        THE_BUTLER_SAYS_SO=credentials('cmb-aws-cred')
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
        stage ('push artifact') {
            steps {
                    sh 'mkdir archive14'
                    sh 'echo test > archive14/test14.txt'
                    sh 'zip -r test14.zip archive14'
                //  zip zipFile: 'test9.zip', archive: false, dir: 'archive9'
                    sh 'ls'
                    sh 'cd $WORKSPACE/archive14 && ls'
                    sh 'aws s3 ls'
                    sh 'aws s3 cp $WORKSPACE/test14.zip s3://create-lambda-from-zip-file/'
                //  sh 'aws s3 cp $WORKSPACE/archive5 s3://create-lambda-from-zip-file/ --recursive --include "*"'                
                    archiveArtifacts artifacts: 'test14.zip', fingerprint: true
            }
        }
        stage('pull artifact') {
            steps {
                step([  $class: 'CopyArtifact',
                        filter: 'test14.zip',
                        fingerprintArtifacts: true,
                        projectName: '${JOB_NAME}',
                        selector: [$class: 'SpecificBuildSelector', buildNumber: '${BUILD_NUMBER}']
                ])
            //  unzip zipFile: 'test.zip', dir: './archive_new'
                sh 'unzip test14.zip -d ./archive_new'
                sh 'cat archive_new/test14.txt'
            }
        }        
        stage('new pull artifact new') {
            steps {                
                    copyArtifacts filter: 'test13.zip', fingerprintArtifacts: true, projectName: env.JOB_NAME, selector: specific(env.BUILD_NUMBER)
                //  unzip zipFile: 'test11.zip', dir: './archive_new'
                    sh 'unzip test13.zip -d ./archive_new'
                    sh 'cat archive_new/test13.txt'                
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

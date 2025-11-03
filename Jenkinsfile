pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                url: 'https://github.com/Amogha04/flask-mysql-ci-cd.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t amogha04/flask-mysql-app .'
                }
            }
        }

        stage('Docker Compose Test Run') {
            steps {
                script {
                    sh 'docker-compose down || true'
                    sh 'docker-compose up -d --build'
                    sh 'sleep 10'
                }
            }
        }

        stage('Login to DockerHub') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub-pass', variable: 'dockerhub_pass')]) {
                    sh "echo $dockerhub_pass | docker login -u amogha04 --password-stdin"
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    sh 'docker push amogha04/flask-mysql-app'
                }
            }
        }
    }

    post {
        always {
            sh 'docker-compose down'
        }
    }
}

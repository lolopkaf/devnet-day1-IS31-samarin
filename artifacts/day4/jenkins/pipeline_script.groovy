pipeline {
    agent any
    stages {
        stage('Preparation') {
            steps {
                echo 'Preparing...'
            }
        }
        stage('Build') {
            steps {
                echo 'Building...'
            }
        }
        stage('Results') {
            steps {
                echo 'Results...'
            }
        }
    }
}

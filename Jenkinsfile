pipeline {
    agent any
    environment {
        DISABLE_AUTH = 'true'
        DB_ENGINE = 'sqlite'
    }
    stages {
        stage('build') {
            steps {
                echo 'Database engine is $(DB_ENGINE}'
                echo 'DISABLE_AUTH is ${DISABLE_AUTH}'
                bat 'python --version'
            }
        }
    }
    post {
            always {
                echo 'This will always run'
            }
            success {
                echo 'This will run only if successful'
            }
            failure {
                echo 'This will run only if failed'
            }
            unstable {
                echo 'This will run only if the run was marked as unstable'
            }
            changed {
                echo 'This will run only if the state of the Pipeline has changed'
            }
    }
}

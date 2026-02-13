pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
        METRICS_FILE = "app/artifacts/metrics.json"
        DOCKER_IMAGE = "2022bcs0125rjhari/wine-infer-jenkins"
    }

    stages {

        // =========================
        // Stage 1: Checkout
        // =========================
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // =========================
        // Stage 2: Setup Python Virtual Environment
        // =========================
        stage('Setup Python Virtual Environment') {
            steps {
                sh '''
                python3 -m venv $VENV_DIR
                . $VENV_DIR/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        // =========================
        // Stage 3: Train Model
        // =========================
        stage('Train Model') {
            steps {
                sh '''
                . $VENV_DIR/bin/activate
                python train.py
                '''
            }
        }

        // =========================
        // Stage 4: Read R2 and MSE
        // =========================
        stage('Read R2 and MSE') {
            steps {
                script {
                    def metrics = readJSON file: "${METRICS_FILE}"
                    env.CUR_R2 = metrics.r2_score.toString()
                    env.CUR_MSE = metrics.mse.toString()

                    echo "--------------------------------"
                    echo "Model Evaluation Metrics"
                    echo "R2 Score : ${env.CUR_R2}"
                    echo "MSE      : ${env.CUR_MSE}"
                    echo "--------------------------------"
                }
            }
        }

        // =========================
        // Stage 5: Compare R2 and MSE
        // =========================
        stage('Compare R2 and MSE') {
            steps {
                script {

                    withCredentials([string(credentialsId: 'best-accuracy', variable: 'BEST_R2')]) {

                        echo "Best Stored R2: ${BEST_R2}"
                        echo "Current R2    : ${env.CUR_R2}"
                        echo "Current MSE   : ${env.CUR_MSE}"

                        if (env.CUR_R2.toFloat() > BEST_R2.toFloat()) {
                            env.BUILD_DOCKER = "true"
                            echo "R2 improved. Docker build will proceed."
                        } else {
                            env.BUILD_DOCKER = "false"
                            echo "R2 did not improve. Skipping Docker build."
                        }
                    }
                }
            }
        }

        // =========================
        // Stage 6: Build Docker Image (Conditional)
        // =========================
        stage('Build Docker Image') {
            when {
                expression { env.BUILD_DOCKER == "true" }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker build -t $DOCKER_USER/wine-infer:${BUILD_NUMBER} .
                    docker tag $DOCKER_USER/wine-infer:${BUILD_NUMBER} $DOCKER_USER/wine-infer:latest
                    '''
                }
            }
        }

        // =========================
        // Stage 7: Push Docker Image (Conditional)
        // =========================
        stage('Push Docker Image') {
            when {
                expression { env.BUILD_DOCKER == "true" }
            }
            steps {
                sh '''
                docker push $DOCKER_USER/wine-infer:${BUILD_NUMBER}
                docker push $DOCKER_USER/wine-infer:latest
                '''
            }
        }
    }

    // =========================
    // Artifact Archiving
    // =========================
    post {
        always {
            archiveArtifacts artifacts: 'app/artifacts/**', fingerprint: true
        }
    }
}

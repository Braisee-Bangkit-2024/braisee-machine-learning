pipeline {
    agent any
    options { timestamps() }
    triggers { githubPush() }

    environment {
        ARTIFACT_REGISTRY_REPO = 'asia-southeast2-docker.pkg.dev/stately-bulwark-464613-j5/jenkins-braisee'
        IMAGE_NAME             = 'braisee-app'
        CLOUD_RUN_SERVICE      = 'braisee-service-ml'
        CLOUD_RUN_REGION       = 'asia-southeast2'
        GCP_PROJECT_ID         = 'stately-bulwark-464613-j5'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                echo "1️⃣ Membangun Docker Image"
                sh "docker build -t ${ARTIFACT_REGISTRY_REPO}/${IMAGE_NAME}:${BUILD_NUMBER} ."
                script {
                    env.DOCKER_IMAGE_TAGGED = "${ARTIFACT_REGISTRY_REPO}/${IMAGE_NAME}:${BUILD_NUMBER}"
                }
            }
        }

        stage('Push Image to Artifact Registry') {
            steps {
                withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GCP_KEYFILE')]) {
                    def REGISTRY_HOSTNAME = 'https://asia-southeast2-docker.pkg.dev'
                    echo "2️⃣ Otentikasi ke Artifact Registry"
                    sh "cat ${GCP_KEYFILE} | docker login -u _json_key --password-stdin ${REGISTRY_HOSTNAME}"
                    echo "🚀 Push Image ke Registry"
                    sh "docker push ${env.DOCKER_IMAGE_TAGGED}"
                }
            }
        }

        stage('Deploy to Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GCP_KEYFILE')]) {
                    echo "3️⃣ Autentikasi ke GCP"
                    sh 'gcloud auth activate-service-account --key-file=${GCP_KEYFILE}'
                    echo "⚙️  Set Project dan Deploy ke Cloud Run"
                    sh """
                        gcloud config set project ${GCP_PROJECT_ID}
                        gcloud run deploy ${CLOUD_RUN_SERVICE} \
                            --image ${env.DOCKER_IMAGE_TAGGED} \
                            --region ${CLOUD_RUN_REGION} \
                            --platform managed \
                            --allow-unauthenticated
                    """
                }
            }
        }
    }
}

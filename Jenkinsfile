pipeline {
    agent any
    triggers {
        githubPush()
    }
 
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
                script {
                    def DOCKER_IMAGE = "${ARTIFACT_REGISTRY_REPO}/${IMAGE_NAME}:${BUILD_NUMBER}"
                    echo "1️⃣ Membangun image: ${DOCKER_IMAGE}"
                    sh "docker build -t ${DOCKER_IMAGE} ."
                    env.DOCKER_IMAGE_TAGGED = DOCKER_IMAGE
                }
            }
        }

        stage('Push Image to Artifact Registry') {
            steps {
                withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GCP_KEYFILE')]) {
                    script {
                        def REGISTRY_HOSTNAME = 'https://asia-southeast2-docker.pkg.dev'
                        echo "2️⃣ Login ke Artifact Registry..."
                        sh "cat ${GCP_KEYFILE} | docker login -u _json_key --password-stdin ${REGISTRY_HOSTNAME}"

                        echo "3️⃣ Push image ke Artifact Registry..."
                        sh "docker push ${env.DOCKER_IMAGE_TAGGED}"
                    }
                }
            }
        }

        stage('Deploy to Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GCP_KEYFILE')]) {
                    script {
                        echo "4️⃣ Aktifkan akun service..."
                        sh "gcloud auth activate-service-account --key-file=${GCP_KEYFILE}"

                        echo "5️⃣ Set project..."
                        sh "gcloud config set project ${GCP_PROJECT_ID}"

                        echo "6️⃣ Deploy ke Cloud Run..."
                        sh """
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
}

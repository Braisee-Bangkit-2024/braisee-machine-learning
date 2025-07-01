pipeline {
    agent any

    // Definisikan environment variables, ambil dari Jenkins Secrets jika ada
environment {
    // Alamat LENGKAP ke repositori Artifact Registry yang baru kamu buat
    ARTIFACT_REGISTRY_REPO = 'asia-southeast2-docker.pkg.dev/stately-bulwark-464613-j5/jenkins-braisee'
    
    // Nama image aplikasimu, bisa tetap sama
    IMAGE_NAME             = 'braisee-app'
    
    // Pastikan nama service Cloud Run dan region-mu juga sudah benar
    CLOUD_RUN_SERVICE      = 'braisee-service-ml' // Pastikan nama ini sesuai dengan di GCP
    CLOUD_RUN_REGION       = 'asia-southeast2'
}

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Buat nama tag yang unik, misal dengan nomor build
                    def DOCKER_IMAGE = "${GCR_HOSTNAME}/${GCP_PROJECT_ID}/${IMAGE_NAME}:${BUILD_NUMBER}"
                    echo "Building image: ${DOCKER_IMAGE}"
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Push Image to GCR') {
            withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GCP_KEYFILE')]) {
                steps {
                    script {
                        def DOCKER_IMAGE = "${GCR_HOSTNAME}/${GCP_PROJECT_ID}/${IMAGE_NAME}:${BUILD_NUMBER}"
                        echo "Authenticating to GCR and pushing image..."
                        sh 'cat ${GCP_KEYFILE} | docker login -u _json_key --password-stdin https://${GCR_HOSTNAME}'
                        sh "docker push ${DOCKER_IMAGE}"
                    }
                }
            }
        }

        stage('Deploy to Cloud Run') {
            withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GCP_KEYFILE')]) {
                steps {
                    script {
                        def DOCKER_IMAGE = "${GCR_HOSTNAME}/${GCP_PROJECT_ID}/${IMAGE_NAME}:${BUILD_NUMBER}"
                        echo "Deploying to Cloud Run service: ${CLOUD_RUN_SERVICE}"
                        sh 'gcloud auth activate-service-account --key-file=${GCP_KEYFILE}'
                        sh "gcloud config set project ${GCP_PROJECT_ID}"
                        sh """
                            gcloud run deploy ${CLOUD_RUN_SERVICE} \\
                                --image ${DOCKER_IMAGE} \\
                                --region ${CLOUD_RUN_REGION} \\
                                --platform managed \\
                                --allow-unauthenticated
                        """
                    }
                }
            }
        }
    }
}
